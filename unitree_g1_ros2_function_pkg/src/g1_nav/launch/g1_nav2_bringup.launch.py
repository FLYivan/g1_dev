import os
import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # 获取与拼接默认路径
    g1_navigation2_dir = get_package_share_directory(
        'g1_nav')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    rviz_config_dir = os.path.join(
        g1_navigation2_dir, 'rviz', 'nav2_go2_view.rviz')
    
    # 创建 Launch 配置
    use_sim_time = launch.substitutions.LaunchConfiguration(
        'use_sim_time', default='false')
    map_yaml_path = launch.substitutions.LaunchConfiguration(
        'map', default=os.path.join(g1_navigation2_dir, 'map', 'room.yaml'))
    nav2_param_path = launch.substitutions.LaunchConfiguration(
        'params_file', default=os.path.join(g1_navigation2_dir, 'config', 'nav2_params.yaml'))
    
    declare_use_sim_time_cmd = launch.actions.DeclareLaunchArgument('use_sim_time', default_value=use_sim_time,
                                            description='Use simulation (Gazebo) clock if true')
    
    declare_map_yaml_path_cmd = launch.actions.DeclareLaunchArgument('map', default_value=map_yaml_path,
                                             description='Full path to map file to load')
    
    declare_nav2_param_path_cmd = launch.actions.DeclareLaunchArgument('params_file', default_value=nav2_param_path,
                                             description='Full path to param file to load')
    # nav2启动文件
    nav2_bringup = launch.actions.IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [nav2_bringup_dir, '/launch', '/navigation_launch.py']),
            # 使用 Launch 参数替换原有参数
            launch_arguments={
                # 'map': map_yaml_path,
                'use_sim_time': use_sim_time,
                'params_file': nav2_param_path}.items(),
        )


    # slam启动launch文件
    launch_slam = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory(
            'g1_slam_algorithm'), '/launch', '/g1_slam_toolbox_for_nav.launch.py']),
    )	

    # g1的URDF发布launch文件
    launch_urdf = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory(
            'g1_sim'), '/launch', '/g1_urdf2tf.launch.py']),
    )	

    
    # 运动控制节点
    node_g1Move =  Node(
            package='g1_cmd',                      
            executable='g1_move',             
            name='g1_move',
            output='screen',
        )
    
    # RViz2节点
    node_rviz =Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'
        )
    
    # 初始化位置节点
    node_initialpose =  Node(
            package='g1_nav',                      
            executable='initialpose_publisher',             
            name='initialpose_publisher',
            output='screen',
        )

    return launch.LaunchDescription([


        declare_use_sim_time_cmd,
        declare_map_yaml_path_cmd,
        declare_nav2_param_path_cmd,


        launch_slam,
        # launch_urdf,
        node_g1Move,
        nav2_bringup,
        node_rviz,
        # node_initialpose,

    ])