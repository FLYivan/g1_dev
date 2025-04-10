import launch
import os

from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.descriptions import ParameterFile
from nav2_common.launch import HasNodeParams, RewrittenYaml

def generate_launch_description():
    # 输入参数声明
    namespace = LaunchConfiguration('namespace')
    nav2_params_file = LaunchConfiguration('nav2_params_file')
    slam_params_file = LaunchConfiguration('slam_params_file')
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    use_respawn = LaunchConfiguration('use_respawn')
    log_level = LaunchConfiguration('log_level')

    # 变量定义
    lifecycle_nodes = ['map_saver']

    # 获取launch文件和定义地址
    slam_bringup_dir = get_package_share_directory("g1_slam_algorithm")
    nav_bringup_dir = get_package_share_directory("g1_nav")

    # Create our own temporary YAML files that include substitutions
    param_substitutions = {
        'use_sim_time': use_sim_time}

    configured_params = ParameterFile(
        RewrittenYaml(
            source_file=nav2_params_file ,
            root_key=namespace,
            param_rewrites=param_substitutions,
            convert_types=True),
        allow_substs=True)


    # 声明slam-toolbox启动时，参数文件的默认地址
    declare_slam_params_file_cmd = DeclareLaunchArgument(
        'slam_params_file',
        default_value=os.path.join(slam_bringup_dir,'config', 'mapper_params_online_async.yaml'),                
        description='Full path to the slam parameters file to use for the slam_toolbox node')
    
    # Declare the launch arguments
    declare_namespace_cmd = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Top-level namespace')

    # 声明nav2相关功能包启动时的参数文件地址
    declare_nav2_params_file_cmd = DeclareLaunchArgument(
        'nav2_params_file',
        default_value=os.path.join(nav_bringup_dir, 'config', 'nav2_params.yaml'),
        description='Full path to the nav2 parameters file to use for all launched nodes')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='False',
        description='Use simulation (Gazebo) clock if true')

    declare_autostart_cmd = DeclareLaunchArgument(
        'autostart', default_value='True',
        description='Automatically startup the nav2 stack')

    # 是否在节点崩溃时重新启动节点。当组合被禁用时适用
    declare_use_respawn_cmd = DeclareLaunchArgument(
        'use_respawn', default_value='False',
        description='Whether to respawn if a node crashes. Applied when composition is disabled.')

    declare_log_level_cmd = DeclareLaunchArgument(
        'log_level', default_value='info',
        description='log level')


    # 两个衔接nav2的节点
    start_map_saver_server_cmd = Node(
            package='nav2_map_server',
            executable='map_saver_server',
            output='screen',
            respawn=use_respawn,
            respawn_delay=2.0,
            arguments=['--ros-args', '--log-level', log_level],
            parameters=[configured_params])

    start_lifecycle_manager_cmd = Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_slam',
            output='screen',
            arguments=['--ros-args', '--log-level', log_level],
            parameters=[{'use_sim_time': use_sim_time},
                        {'autostart': autostart},
                        {'node_names': lifecycle_nodes}])


    # 自定义odom的tf关系发布节点
    start_cus_tftree_node =  Node(
            package='g1_slam_algorithm',                      
            executable='motion_to_tf',             
            name='motion_to_tf',
            output='screen',
        )
    
    # slam-toolbox节点
    start_async_slam_toolbox_node = Node(
            parameters=[
                slam_params_file,
                {'use_sim_time': use_sim_time}
            ],
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            # remappings=[
            #         ('/map', '/map_slamtoolbox_g1')  # 将 /map 重映射为 /map_slamtoolbox_g1
            #          ]
        )
 
    # 激光frame_id修改launch文件
    start_lidar_launch_file = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory(
            'g1_lidar_processing'), '/launch', '/cloud_to_scan.launch.py']),
    )	

    # L1点云转2d激光
    start_L1_lidar_launch_file = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory(
            'g1_lidar_processing'), '/launch', '/cloud_to_scan_L1.launch.py']),
    )	


    # 自动保存地图
    start_map_saver_node =  Node(
            package='g1_slam_algorithm',                      
            executable='auto_map_saver',             
            name='auto_map_saver',
            output='screen',
        )
    


    return launch.LaunchDescription([

        
        declare_slam_params_file_cmd,
        declare_namespace_cmd,
        declare_nav2_params_file_cmd,
        declare_use_sim_time_cmd,
        declare_autostart_cmd,
        declare_use_respawn_cmd,
        declare_log_level_cmd,


        # start_L1_lidar_launch_file,     # 启动L1点云转2d激光文件
        start_lidar_launch_file,        # 启动激光frame_id修改launch文件
        start_cus_tftree_node,
        start_async_slam_toolbox_node,  # slam-toolbox算法节点

        # start_map_saver_node,           # 自动保存地图

    ])
