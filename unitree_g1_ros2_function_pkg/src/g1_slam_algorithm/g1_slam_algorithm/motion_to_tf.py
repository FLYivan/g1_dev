import rclpy
import subprocess
import numpy as np

from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import StaticTransformBroadcaster, TransformBroadcaster, Buffer
from nav_msgs.msg import Odometry
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from scipy.spatial.transform import Rotation as R

from unitree_go.msg import SportModeState


topic_name = "odommodestate"


# ANSI 转义序列，定义打印颜色
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'  # 重置颜色



class DynamicTFPublisher(Node):
    def __init__(self):
        super().__init__('motion_to_tf')
                         
        self.x = 0.0                                    # 初始化x位置
        self.y = 0.0                                    # 初始化y位置
        self.z = 0.0                                    # 初始化z位置
        self.vx = 0.0                                   # 初始化x方向速度
        self.vy = 0.0                                   # 初始化y方向速度
        self.vz = 0.0                                   # 初始化z方向速度
        self.vthx = 0.0                                 # 初始化角速度
        self.vthy = 0.0 
        self.vthz = 0.0                                 
        self.quat_w = 0.0                               # 初始化四元数
        self.quat_x = 0.0
        self.quat_y = 0.0
        self.quat_z = 0.0

        # 自定义QoS配置
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,     # 可靠性策略： 确保消息被传递，如果失败会尝试重传
            history=QoSHistoryPolicy.KEEP_LAST,            # 历史策略： 只保留最新的N条消息
            depth=10                                       # N=10
        )

        # 创建一个订阅器，用于订阅消息
        self.motion_sub = self.create_subscription(SportModeState, topic_name, self.motion_callback, qos_profile)   


        # 创建一个发布器，用于发布Odometry消息
        self.odom_pub = self.create_publisher(Odometry, 'odom', qos_profile)    
        self.odom = Odometry()                               # 创建一个Odometry消息对象


        # 创建动态 TF 缓存和广播器
        self.tf_buffer = Buffer(cache_time=rclpy.duration.Duration(seconds=10))  # 设置缓存时间
        self.tf_broadcaster = TransformBroadcaster(self)
        self.transform = TransformStamped()  # 初始化 transform


        # 将定时器间隔设置为0.05秒（即20Hz）
        self.publish_frequency = 20                  # 设置发布频率为20Hz
        self.publish_period = 1.0 / self.publish_frequency                                  # 计算发布周期
        self.timer = self.create_timer(self.publish_period , self.publish_all)        # 动态tf发布的频率为20hz(不可动参数)
        

    def motion_callback(self, msg):                     # 定义运动状态回调函数
        """
        获取基本状态
        """
        # 获取基于坐标系A的位置信息
            # 获取当前位置信息
        position_A = np.array([
            float(msg.position[0]),
            float(msg.position[1]),
            float(msg.position[2])
        ])

             # 获取当前四元数
        orientation_A = np.array([
            float(msg.imu_state.quaternion[1]),
            float(msg.imu_state.quaternion[2]),
            float(msg.imu_state.quaternion[3]),
            float(msg.imu_state.quaternion[0])
        ])

        if self.initial_position_A is None and self.initial_orientation_A is None:
            # 设置初始位置和姿态偏移
            self.initial_position_A = position_A
            self.initial_orientation_A = R.from_quat(orientation_A)

            # self.get_logger().info(f'Set initial position: {self.initial_position_A}')
            # self.get_logger().info(f'Set initial orientation: {self.initial_orientation_A.as_quat()}')
            return  # 记录初始位置和姿态后，返回以等待下一个回调
        
        # 计算从A到B的变换
        self.position_offset = self.initial_position_B - self.initial_position_A
        self.rotation_offset = self.initial_orientation_B * self.initial_orientation_A.inv()    # 将坐标系A的方向调整到坐标系B的方向

        # 计算相对于坐标系B的位置信息
        relative_position = self.rotation_offset.apply(position_A - self.initial_position_A)

        # 计算相对于坐标系B的旋转
        rotation_A = R.from_quat(orientation_A)
        relative_rotation = self.rotation_offset * rotation_A


        # 更新角速度
        self.vthx = float(msg.imu_state.gyroscope[0])                           # 从消息中获取x轴角速度
        self.vthy = float(msg.imu_state.gyroscope[1])                           # 从消息中获取y轴角速度
        self.vthz = float(msg.imu_state.gyroscope[2])                           # 从消息中获取z轴角速度


        # 获取并更新线速度
        self.vx = float(msg.velocity[0])   # 获取x轴线速度
        self.vy = float(msg.velocity[1])   # 获取y轴线速度
        self.vz = float(msg.velocity[2])   # 获取z轴线速度


        """
        里程计话题信息生成
        """
        
        self.odom.header.stamp = self.get_clock().now().to_msg()    # 以上位机时间戳为准

        self.odom.header.frame_id = 'odom_slamtoolbox'                   # 设置消息的坐标系ID
        self.odom.child_frame_id = 'base'               # 设置子坐标系ID

        # 设置位置
        self.odom.pose.pose.position.x = relative_position[0]
        self.odom.pose.pose.position.y = relative_position[1]
        self.odom.pose.pose.position.z = relative_position[2]
        # self.odom.pose.pose.position.z = float(msg.position[2])           # 狗上电时，z轴是按站立姿态的位置定义的，如果slam里程也按站立姿态启动，则无需加0.05


        # 设置姿态
        self.odom.pose.pose.orientation.x = relative_rotation.as_quat()[0]
        self.odom.pose.pose.orientation.y = relative_rotation.as_quat()[1]
        self.odom.pose.pose.orientation.z = relative_rotation.as_quat()[2]
        self.odom.pose.pose.orientation.w = relative_rotation.as_quat()[3]


        self.odom.twist.twist.linear.x = self.vx                     # 设置线速度x
        self.odom.twist.twist.linear.y = self.vy                     # 设置线速度y
        self.odom.twist.twist.linear.z = self.vz                     # 设置线速度z
        self.odom.twist.twist.angular.x = self.vthx                  # 设置角速度x
        self.odom.twist.twist.angular.y = self.vthy                  # 设置角速度y
        self.odom.twist.twist.angular.z = self.vthz                  # 设置角速度z


        """
        静态tf生成
        """
        # 使用雷达的时间戳
        # self.static_transform_stamped.header.stamp.sec = sec
        # self.static_transform_stamped.header.stamp.nanosec = nanosec

        self.static_transform_stamped.header.stamp = self.get_clock().now().to_msg()    # 以上位机时间戳为准

        self.static_transform_stamped.header.frame_id = 'base'  # 目标frame_id
        self.static_transform_stamped.child_frame_id = 'mid360_link'  # 原始frame_id rslidar


        self.static_transform_stamped.transform.translation.x = 0.171
        self.static_transform_stamped.transform.translation.y = 0.0
        self.static_transform_stamped.transform.translation.z = 0.0908

        q = R.from_euler('z', np.radians(90)).as_quat()                 # 雷达坐标系默认方向和本体实际坐标系默认方向相差90度,故需修正
        self.static_transform_stamped.transform.rotation.x = q[0]
        self.static_transform_stamped.transform.rotation.y = q[1]
        self.static_transform_stamped.transform.rotation.z = q[2]
        self.static_transform_stamped.transform.rotation.w = q[3]


        """
        动态tf关系生成
        """


        self.transform.header.stamp = self.get_clock().now().to_msg()    # 以上位机时间戳为准

        # 设置坐标系
        self.transform.header.frame_id = 'odom_slamtoolbox'                          # 设置一个坐标变换的源坐标系
        self.transform.child_frame_id = 'base'                                       # 设置一个坐标变换的目标坐标系

        # 设置转化参数
        self.transform.transform.translation.x = relative_position[0]
        self.transform.transform.translation.y = relative_position[1]
        self.transform.transform.translation.z = relative_position[2]
        # self.transform.transform.translation.z = float(msg.position[2])

        self.transform.transform.rotation.x = relative_rotation.as_quat()[0]
        self.transform.transform.rotation.y = relative_rotation.as_quat()[1]
        self.transform.transform.rotation.z = relative_rotation.as_quat()[2]
        self.transform.transform.rotation.w = relative_rotation.as_quat()[3]

        


    # 回调函数，处理接收到的odom消息，并发布tf
    def publish_all(self):
        
        # 发布里程计消息
        self.odom_pub.publish(self.odom) 
        # self.get_logger().info(f'{BLUE}里程计时间戳: {self.transform.header.stamp}{RESET}')    
        
        # 发布静态变换
        # self.static_broadcaster.sendTransform(self.static_transform_stamped)
        # self.get_logger().info(f'{RED}静态TF时间戳: {self.transform.header.stamp}{RESET}')                       


        # 广播坐标变换信息
        self.tf_broadcaster.sendTransform(self.transform)
        # self.get_logger().info(f'{YELLOW}动态TF时间戳: {self.transform.header.stamp}{RESET}')

        

def main(args=None):
    rclpy.init(args=args)
    dynamic_tf_publisher = DynamicTFPublisher()
    rclpy.spin(dynamic_tf_publisher)
    dynamic_tf_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()