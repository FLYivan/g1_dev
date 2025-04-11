#!/usr/bin/env python3

"""
根据里程计信息，实现行进轨迹可视化的节点

"""

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker
from std_msgs.msg import ColorRGBA
import numpy as np

class TrajectoryVisualizer(Node):
    def __init__(self):
        super().__init__('trajectory_visualizer')
        
        # Subscribe to odometry topic
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',  # Change this to match your odometry topic
            self.odom_callback,
            10)
            
        # Publisher for trajectory marker
        self.marker_pub = self.create_publisher(
            Marker,
            'robot_trajectory',
            10)
            
        # Initialize trajectory marker
        self.trajectory = Marker()
        self.trajectory.header.frame_id = "odom_slamtoolbox"
        self.trajectory.type = Marker.LINE_STRIP
        self.trajectory.action = Marker.ADD
        self.trajectory.scale.x = 0.05  # Line width
        
        # Set color (blue)
        self.trajectory.color = ColorRGBA()
        self.trajectory.color.r = 0.0
        self.trajectory.color.g = 0.0
        self.trajectory.color.b = 1.0
        self.trajectory.color.a = 1.0
        
        self.trajectory.pose.orientation.w = 1.0
        
    def odom_callback(self, msg):
        # Add new point to trajectory
        point = Point()
        point.x = msg.pose.pose.position.x
        point.y = msg.pose.pose.position.y
        point.z = msg.pose.pose.position.z
        
        self.trajectory.points.append(point)
        
        # Update timestamp
        self.trajectory.header.stamp = self.get_clock().now().to_msg()
        
        # Publish updated trajectory
        self.marker_pub.publish(self.trajectory)

def main(args=None):
    rclpy.init(args=args)
    
    visualizer = TrajectoryVisualizer()
    
    try:
        rclpy.spin(visualizer)
    except KeyboardInterrupt:
        pass
        
    visualizer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

