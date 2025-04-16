# Requirements:
#   Download rosbag:
#    * demo_mapping.db3: https://drive.google.com/file/d/1v9qJ2U7GlYhqBJr7OQHWbDSCfgiVaLWb/view?usp=drive_link
#
# Example:
#
#   SLAM:
#     $ ros2 launch rtabmap_demos robot_mapping_demo.launch.py rviz:=true rtabmap_viz:=true
#
#   Rosbag:
#     $ ros2 bag play demo_mapping.db3 --clock
#

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch_ros.actions import SetParameter
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    localization = LaunchConfiguration('localization')

    parameters={
          'frame_id':'base',                              # 基础坐标系ID
          'odom_frame_id':'odom',                         # 里程计坐标系ID
          'odom_tf_linear_variance':0.001,                # 里程计线性运动的方差
          'odom_tf_angular_variance':0.001,               # 里程计角度运动的方差
          'subscribe_rgbd':True,                          # 订阅RGB-D相机数据
          'subscribe_scan':True,                          # 订阅激光扫描数据
          'approx_sync':True,                             # 启用近似时间同步
          'sync_queue_size': 10,                          # 同步队列大小
          # RTAB-Map's internal parameters should be strings
          'RGBD/NeighborLinkRefining': 'true',           # 使用连续激光扫描进行里程计校正
          'RGBD/ProximityBySpace':     'true',           # 使用工作内存中的位置进行局部回环检测
          'RGBD/ProximityByTime':      'false',          # 使用短期内存中的位置进行局部回环检测
          'RGBD/ProximityPathMaxNeighbors': '10',        # 通过合并近距离扫描来进行空间邻近检测
          'Reg/Strategy':              '1',               # 配准策略：0=视觉，1=ICP，2=视觉+ICP
          'Vis/MinInliers':            '12',              # 接受回环检测所需的最小3D视觉特征点数量
          'RGBD/OptimizeFromGraphEnd': 'false',          # 从初始节点优化图以生成/map到/odom的转换
          'RGBD/OptimizeMaxError':     '4',              # 拒绝导致地图中大误差的回环检测
          'Reg/Force3DoF':             'true',           # 启用2D SLAM
          'Grid/FromDepth':            'false',          # 从激光扫描创建2D占用栅格地图
          'Mem/STMSize':               '30',             # 增加到30以避免在刚看到的位置添加过多回环
          'RGBD/LocalRadius':          '5',              # 限制邻近检测的范围
          'Icp/CorrespondenceRatio':   '0.2',           # 接受回环检测的最小扫描重叠率
          'Icp/PM':                    'false',          # 禁用点匹配ICP
          'Icp/PointToPlane':          'false',          # 禁用点到平面ICP
          'Icp/MaxCorrespondenceDistance': '0.15',       # ICP最大对应点距离
          'Icp/VoxelSize':             '0.05'           # ICP体素大小
    }
    
    remappings=[
         ('rgb/image',       '/camera/camera/color/image_raw/compressed'),
         ('depth/image',     '/camera/camera/depth/image_rect_raw/compressedDepth'),
         ('rgb/camera_info', '/camera/camera/color/camera_info'),
         ('scan',            '/scan')]
    
            # /camera/color/camera_info
            # /camera/color/image_raw
            # /camera/depth/image_rect_raw

    config_rviz = os.path.join(
        get_package_share_directory('rtabmap_demos'), 'config', 'demo_robot_mapping.rviz'
    )

    return LaunchDescription([

        # Launch arguments
        DeclareLaunchArgument('rtabmap_viz',  default_value='true',  description='Launch RTAB-Map UI (optional).'),
        DeclareLaunchArgument('rviz',         default_value='false', description='Launch RVIZ (optional).'),
        DeclareLaunchArgument('localization', default_value='false', description='Launch in localization mode.'),
        DeclareLaunchArgument('rviz_cfg', default_value=config_rviz,  description='Configuration path of rviz2.'),

        SetParameter(name='use_sim_time', value=True),

        # Nodes to launch
        # 创建一个ROS2节点用于RGB-D相机数据同步
        Node(
            package='rtabmap_sync',          # 使用rtabmap_sync包
            executable='rgbd_sync',           # 运行rgbd_sync可执行文件
            output='screen',                  # 输出信息到屏幕
            parameters=[parameters,           # 使用上面定义的参数
              {'rgb_image_transport':'compressed',        # RGB图像使用压缩传输
               'depth_image_transport':'compressedDepth', # 深度图像使用压缩传输
               'approx_sync_max_interval': 0.02}],       # 最大同步时间间隔为0.02秒
            remappings=remappings),          # 使用上面定义的话题重映射
        # SLAM mode:
        Node(
            condition=UnlessCondition(localization),
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=[parameters],
            remappings=remappings,
            arguments=['-d']), # This will delete the previous database (~/.ros/rtabmap.db)
            
        # Localization mode:
        Node(
            condition=IfCondition(localization),
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=[parameters,
              {'Mem/IncrementalMemory':'False',
               'Mem/InitWMWithAllNodes':'True'}],
            remappings=remappings),

        # Visualization:
        Node(
            package='rtabmap_viz', executable='rtabmap_viz', output='screen',
            condition=IfCondition(LaunchConfiguration("rtabmap_viz")),
            parameters=[parameters],
            remappings=remappings),
        Node(
            package='rviz2', executable='rviz2', name="rviz2", output='screen',
            condition=IfCondition(LaunchConfiguration("rviz")),
            arguments=[["-d"], [LaunchConfiguration("rviz_cfg")]]),
    ])
