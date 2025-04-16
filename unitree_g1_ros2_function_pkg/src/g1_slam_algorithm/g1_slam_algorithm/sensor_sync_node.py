#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo, LaserScan
from message_filters import TimeSynchronizer, Subscriber
from cv_bridge import CvBridge
import cv2

class SensorSyncNode(Node):
    def __init__(self):
        super().__init__('sensor_sync_node')
        
        # 创建CV桥接器用于图像转换
        self.bridge = CvBridge()
        
        # 创建时间同步的订阅器
        self.rgb_sub = Subscriber(self, Image, 'rgb/image')             # Subscriber: 便于多个话题的同步处理
        self.depth_sub = Subscriber(self, Image, 'depth/image')
        self.camera_info_sub = Subscriber(self, CameraInfo, 'rgb/camera_info')
        self.scan_sub = Subscriber(self, LaserScan, 'scan')
        
        # 设置时间同步器，允许0.1秒的时间误差
        self.ts = TimeSynchronizer(
            [self.rgb_sub, self.depth_sub, self.camera_info_sub, self.scan_sub],
            queue_size=10
        )
        self.ts.registerCallback(self.sync_callback)
        
        # 创建同步后的发布器
        self.rgb_pub = self.create_publisher(Image, 'sync/rgb/image', 10)
        self.depth_pub = self.create_publisher(Image, 'sync/depth/image', 10)
        self.camera_info_pub = self.create_publisher(CameraInfo, 'sync/rgb/camera_info', 10)
        self.scan_pub = self.create_publisher(LaserScan, 'sync/scan', 10)
        
        self.get_logger().info('传感器同步节点已启动')

    def sync_callback(self, rgb_msg, depth_msg, camera_info_msg, scan_msg):
        """
        处理同步后的传感器数据
        """
        try:
            # 获取当前ROS时间
            current_time = self.get_clock().now().to_msg()
            
            # 更新时间戳
            rgb_msg.header.stamp = current_time
            depth_msg.header.stamp = current_time
            camera_info_msg.header.stamp = current_time
            scan_msg.header.stamp = current_time
            
            # 发布同步后的消息
            self.rgb_pub.publish(rgb_msg)
            self.depth_pub.publish(depth_msg)
            self.camera_info_pub.publish(camera_info_msg)
            self.scan_pub.publish(scan_msg)
            
        except Exception as e:
            self.get_logger().error(f'处理同步数据时出错: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    node = SensorSyncNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
