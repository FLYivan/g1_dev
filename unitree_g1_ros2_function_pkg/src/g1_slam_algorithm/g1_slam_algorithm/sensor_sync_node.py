#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo, LaserScan, PointCloud2, Imu, CompressedImage
from message_filters import TimeSynchronizer, ApproximateTimeSynchronizer, Subscriber
from cv_bridge import CvBridge
import cv2

class SensorSyncNode(Node):
    def __init__(self):
        super().__init__('sensor_sync_node')
        
        # 创建CV桥接器用于图像转换
        self.bridge = CvBridge()
        
        # 创建时间同步的订阅器
        self.rgb_sub = Subscriber(self, Image, '/camera/color/image_raw')
        self.rgb_compressed_sub = Subscriber(self, CompressedImage, 'rgb/image/compressed')
        self.depth_sub = Subscriber(self, Image, '/camera/depth/image_rect_raw')
        self.depth_compressed_sub = Subscriber(self, CompressedImage, 'depth/image/compressed')
        self.camera_info_sub = Subscriber(self, CameraInfo, '/camera/color/camera_info')
        self.scan_sub = Subscriber(self, LaserScan, '/scan_old')
        self.pointcloud_sub = Subscriber(self, PointCloud2, '/livox/lidar')
        self.imu_sub = Subscriber(self, Imu, '/livox/imu')
        
        # 设置时间同步器，严格时间同步
        self.ts = TimeSynchronizer(
            [self.rgb_sub, 
             self.depth_sub, 
             self.rgb_compressed_sub,
             self.depth_compressed_sub,
             self.camera_info_sub, 
             self.scan_sub, 
             self.pointcloud_sub, 
             self.imu_sub,
             
             ],
            queue_size=10
        )


        # # 设置近似时间同步器，允许0.1秒的时间误差
        # self.ts = ApproximateTimeSynchronizer(
        #     [self.rgb_sub, 
        #      self.depth_sub, 
        #      self.rgb_compressed_sub,
        #      self.depth_compressed_sub,
        #      self.camera_info_sub, 
        #      self.scan_sub, 
        #      self.pointcloud_sub, 
        #      self.imu_sub
             
        #      ],
        #     queue_size=10,
        #     slop=0.1    # 这个参数设置允许的时间误差（单位：秒）
        # )



        self.ts.registerCallback(self.sync_callback)
        
        # 创建同步后的发布器
        self.rgb_pub = self.create_publisher(Image, 'sync/rgb/image', 10)
        self.rgb_compressed_pub = self.create_publisher(CompressedImage, 'sync/rgb/image/compressed', 10)
        self.depth_pub = self.create_publisher(Image, 'sync/depth/image', 10)
        self.depth_compressed_pub = self.create_publisher(CompressedImage, 'sync/depth/image/compressed', 10)
        self.camera_info_pub = self.create_publisher(CameraInfo, 'sync/rgb/camera_info', 10)
        self.scan_pub = self.create_publisher(LaserScan, 'sync/scan', 10)
        self.pointcloud_pub = self.create_publisher(PointCloud2, 'sync/points', 10)
        self.imu_pub = self.create_publisher(Imu, 'sync/imu', 10)
        
        self.get_logger().info('传感器同步节点已启动')

    def sync_callback(self, rgb_msg, rgb_compressed_msg, depth_msg, depth_compressed_msg,
                     camera_info_msg, scan_msg, pointcloud_msg, imu_msg):
        """
        处理同步后的传感器数据
        """
        try:
            # 获取当前ROS时间
            current_time = self.get_clock().now().to_msg()
            
            # 更新时间戳
            rgb_msg.header.stamp = current_time
            rgb_compressed_msg.header.stamp = current_time
            depth_msg.header.stamp = current_time
            depth_compressed_msg.header.stamp = current_time
            camera_info_msg.header.stamp = current_time
            scan_msg.header.stamp = current_time
            pointcloud_msg.header.stamp = current_time
            imu_msg.header.stamp = current_time
            
            # 发布同步后的消息
            self.rgb_pub.publish(rgb_msg)
            self.rgb_compressed_pub.publish(rgb_compressed_msg)
            self.depth_pub.publish(depth_msg)
            self.depth_compressed_pub.publish(depth_compressed_msg)
            self.camera_info_pub.publish(camera_info_msg)
            self.scan_pub.publish(scan_msg)
            self.pointcloud_pub.publish(pointcloud_msg)
            self.imu_pub.publish(imu_msg)
            
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
