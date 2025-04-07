# Requirements: 需求：
#   Download rosbag: 下载rosbag文件：
#    * demo_mapping.db3: https://drive.google.com/file/d/1v9qJ2U7GlYhqBJr7OQHWbDSCfgiVaLWb/view?usp=drive_link
#
# Example: 示例：
#
#   SLAM: SLAM建图：
#     $ ros2 launch rtabmap_demos robot_mapping_demo.launch.py rviz:=true rtabmap_viz:=true
#
#   Rosbag: 运行rosbag：
#     $ ros2 bag play demo_mapping.db3 --clock
#

# 导入必要的launch相关模块
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch_ros.actions import SetParameter
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    # 定义定位模式配置变量
    localization = LaunchConfiguration('localization')

    # RTAB-Map的参数配置
    parameters={
          'frame_id':'base_footprint',          # 基础坐标系
          'odom_frame_id':'odom',               # 里程计坐标系
          'odom_tf_linear_variance':0.001,      # 里程计线性方差
          'odom_tf_angular_variance':0.001,     # 里程计角度方差
          'subscribe_rgbd':True,                # 订阅RGBD数据
          'subscribe_scan':True,                # 订阅激光扫描数据
          'approx_sync':True,                   # 启用近似同步
          'sync_queue_size': 10,                # 同步队列大小
          # RTAB-Map的内部参数需要使用字符串格式
          'RGBD/NeighborLinkRefining': 'true',    # 使用连续激光扫描进行里程计校正
          'RGBD/ProximityBySpace':     'true',    # 使用WM中的位置进行局部回环检测
          'RGBD/ProximityByTime':      'false',   # 使用STM中的位置进行局部回环检测
          'RGBD/ProximityPathMaxNeighbors': '10', # 通过合并近距离扫描进行空间近邻检测
          'Reg/Strategy':              '1',       # 配准策略：0=视觉，1=ICP，2=视觉+ICP
          'Vis/MinInliers':            '12',      # 接受回环检测的最小内点数
          'RGBD/OptimizeFromGraphEnd': 'false',   # 从初始节点优化图以生成/map到/odom的转换
          'RGBD/OptimizeMaxError':     '4',       # 拒绝导致地图中大误差的回环
          'Reg/Force3DoF':             'true',    # 2D SLAM模式
          'Grid/FromDepth':            'false',   # 从激光扫描创建2D占据栅格
          'Mem/STMSize':               '30',      # 增加到30以避免在刚看到的位置添加太多回环
          'RGBD/LocalRadius':          '5',       # 限制近邻检测的范围
          'Icp/CorrespondenceRatio':   '0.2',     # 接受回环的最小扫描重叠率
          'Icp/PM':                    'false',    # 点匹配ICP
          'Icp/PointToPlane':          'false',    # 点到平面ICP
          'Icp/MaxCorrespondenceDistance': '0.15', # ICP最大对应距离
          'Icp/VoxelSize':             '0.05'      # 体素大小
    }
    
    # 话题重映射配置
    remappings=[
         ('rgb/image',       '/data_throttled_image'),
         ('depth/image',     '/data_throttled_image_depth'),
         ('rgb/camera_info', '/data_throttled_camera_info'),
         ('scan',            '/jn0/base_scan')]
    
    # 获取rviz配置文件路径
    config_rviz = os.path.join(
        get_package_share_directory('rtabmap_demos'), 'config', 'demo_robot_mapping.rviz'
    )

    return LaunchDescription([

        # Launch参数声明
        DeclareLaunchArgument('rtabmap_viz',  default_value='true',  description='Launch RTAB-Map UI (optional).'),
        DeclareLaunchArgument('rviz',         default_value='false', description='Launch RVIZ (optional).'),
        DeclareLaunchArgument('localization', default_value='false', description='Launch in localization mode.'),
        DeclareLaunchArgument('rviz_cfg', default_value=config_rviz,  description='Configuration path of rviz2.'),

        # 设置使用仿真时间
        SetParameter(name='use_sim_time', value=True),

        # 启动RGBD同步节点
        Node(
            package='rtabmap_sync', executable='rgbd_sync', output='screen',
            parameters=[parameters,
              {'rgb_image_transport':'compressed',
               'depth_image_transport':'compressedDepth',
               'approx_sync_max_interval': 0.02}],
            remappings=remappings),
        
        # SLAM模式节点
        Node(
            condition=UnlessCondition(localization),
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=[parameters],
            remappings=remappings,
            arguments=['-d']), # 这将删除之前的数据库 (~/.ros/rtabmap.db)
            
        # 定位模式节点
        Node(
            condition=IfCondition(localization),
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=[parameters,
              {'Mem/IncrementalMemory':'False',
               'Mem/InitWMWithAllNodes':'True'}],
            remappings=remappings),

        # 可视化节点配置
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
