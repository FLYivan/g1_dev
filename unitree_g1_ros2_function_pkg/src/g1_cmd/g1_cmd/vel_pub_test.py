#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class VelocityPublisher(Node):
    def __init__(self, name):
        super().__init__(name)
        
        # 创建一个发布者，发布到cmd_vel话题
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        
        # 设置发布频率
        self.timer = self.create_timer(2.0, self.publish_velocity)  # 每0.1秒发布一次

    def publish_velocity(self):
        # 创建Twist消息
        twist = Twist()
        
        # 设置线速度和角速度
        twist.linear.x = 0.3  # 前进速度
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0  # 旋转速度
        
        # 发布消息
        self.publisher_.publish(twist)
        # self.get_logger().info(f'Publishing: linear={twist.linear}, angular={twist.angular}')

def main(args=None):
    rclpy.init(args=args)
    node = VelocityPublisher("vel_pub_test")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()