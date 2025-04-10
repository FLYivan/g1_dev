"""
将宇数的python api 作为模块导入到ros2节点中
"""

import rclpy
from rclpy.node import Node
# 使用 ReentrantCallbackGroup 允许定时器回调的重入
# 使用 MutuallyExclusiveCallbackGroup 确保同类回调的互斥执行
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup   
from rclpy.executors import MultiThreadedExecutor   # 替换默认的单线程执行器为 MultiThreadedExecutor
from geometry_msgs.msg import Twist
from std_msgs.msg import String

from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.g1.loco.g1_loco_client import LocoClient

# ANSI 转义序列，定义打印颜色
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'  # 重置颜色

class Python2RosCmd(Node):
    def __init__(self,name):
        super().__init__(name)
        

        # 定义网口名称参数
        self.declare_parameter('channel_name', "enp0s31f6")  # 参数名为'channel_name'，需根据自身网口名调整
        # 获取参数值
        channel_name_value = self.get_parameter('channel_name').get_parameter_value().string_value

        # 初始化网络通道
        ChannelFactoryInitialize(0, channel_name_value)

        self.get_logger().info(f'{YELLOW}通道初始化成功{RESET}')

        # 初始化客户端
        self.sport_client = LocoClient()  
        self.sport_client.SetTimeout(10.0)
        self.sport_client.Init()
        self.get_logger().info(f'{RED}客户端初始化成功{RESET}')



        # 创建不同的回调组
        self.command_callback_group = MutuallyExclusiveCallbackGroup()
        self.velocity_callback_group = MutuallyExclusiveCallbackGroup()
        self.timer_callback_group = ReentrantCallbackGroup()

            
        # 创建速度指令订阅者（使用独立的回调组）
        self.velocity_subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.velocity_callback,
            10,
            callback_group=self.velocity_callback_group)
        
        # 创建模式控制指令订阅者（使用独立的回调组）
        self.command_subscription = self.create_subscription(
            String,
            'cmd_control_command',
            self.command_callback,
            10,
            callback_group=self.command_callback_group)
        
        # 创建定时器（使用独立的回调组）
        self.timer = self.create_timer(
            0.1,  # 10Hz
            self.control_loop,
            callback_group=self.timer_callback_group
        )              

        # 初始化当前控制模式
        # self.current_mode = 'idle'
        self.current_mode = 'velocity_control'  # 调试时，默认值设为速度控制
        
        # 初始化存储最新的速度指令
        self.latest_twist = Twist()
        
        self.get_logger().info('g1机器人控制模式已经完成初始化')

    def command_callback(self, msg):
        """处理模式控制指令"""
        command = msg.data
        if command in ['velocity_control', 
                       'stand', 
                       'squat']:
            
            self.current_mode = command
            self.get_logger().info(f'Switching to mode: {command}')
        else:
            self.get_logger().warn(f'Unknown command: {command}')

    def velocity_callback(self, msg):
        """处理速度控制指令"""
        self.latest_twist = msg
        # 如果当前模式是速度控制，直接执行速度控制
        if self.current_mode == 'velocity_control':
            self.velocity_control(self.latest_twist.linear.x, self.latest_twist.linear.y, self.latest_twist.angular.z)

    """
    运动控制技能库
    """ 

    def velocity_control(self, vx, vy, vyaw):
        """速度控制方法"""
        # 使用最新的 Twist 消息作为 Move 方法的参数
        self.sport_client.Move(vx, vy, vyaw)

        # 打印速度日志
        self.get_logger().info(f'{YELLOW}Sending to g1: vx ={vx}, vy={vy}, vyaw={vyaw}{RESET}')

    def stand_control(self):
        """站立控制方法"""
        self.sport_client.Squat2StandUp()

    def squat_down_control(self):
        """蹲下控制方法"""
        self.sport_client.StandUp2Squat()

    def control_loop(self):
        """主控制循环"""
        if self.current_mode == 'stand':
            self.stand_control()
        elif self.current_mode == 'squat':
            self.lie_down_control()
        else:
            # 空闲状态或未知状态处理
            pass




def main():
    rclpy.init()
    node = Python2RosCmd('g1_move')


    # 使用多线程执行器
    executor = MultiThreadedExecutor(num_threads=3)
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()