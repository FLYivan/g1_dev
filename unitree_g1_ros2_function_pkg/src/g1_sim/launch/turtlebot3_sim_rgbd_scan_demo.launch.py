# Requirements: 要求：
#   Install Turtlebot3 packages  # 安装Turtlebot3软件包
#   Modify turtlebot3_waffle SDF:  # 修改turtlebot3_waffle SDF文件：
#     1) Edit /opt/ros/$ROS_DISTRO/share/turtlebot3_gazebo/models/turtlebot3_waffle/model.sdf  # 编辑SDF模型文件
#     2) Add  # 添加以下内容
#          <joint name="camera_rgb_optical_joint" type="fixed">  # 添加固定关节
#            <parent>camera_rgb_frame</parent>  # 父链接
#            <child>camera_rgb_optical_frame</child>  # 子链接
#            <pose>0 0 0 -1.57079632679 0 -1.57079632679</pose>  # 位姿设置
#            <axis>  # 轴向设置
#              <xyz>0 0 1</xyz>  # 沿Z轴
#            </axis>
#          </joint> 
#     3) Rename <link name="camera_rgb_frame"> to <link name="camera_rgb_optical_frame">  # 重命名链接
#     4) Add <link name="camera_rgb_frame"/>  # 添加新的相机RGB帧链接
#     5) Change <sensor name="camera" type="camera"> to <sensor name="camera" type="depth">  # 将相机类型改为深度相机
#     6) Change image width/height from 1920x1080 to 640x480  # 修改图像分辨率
#     7) Note that we can increase min scan range from 0.12 to 0.2 to avoid having scans   # 增加最小扫描范围以避免扫描到机器人本身
#        hitting the robot itself
# Example:  # 示例：
#   $ ros2 launch rtabmap_demos turtlebot3_sim_rgbd_scan_demo.launch.py  # 启动仿真demo
#
#   Teleop:  # 遥控：
#     $ ros2 run turtlebot3_teleop teleop_keyboard  # 运行键盘遥控节点

from ament_index_python.packages import get_package_share_directory  # 导入包共享目录获取函数

from launch import LaunchDescription  # 导入启动描述
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction  # 导入启动动作
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution  # 导入路径替换功能
from launch.launch_description_sources import PythonLaunchDescriptionSource  # 导入Python启动描述源
from launch_ros.substitutions import FindPackageShare  # 导入包查找功能

import os  # 导入操作系统模块

def launch_setup(context, *args, **kwargs):  # 启动设置函数
    if not 'TURTLEBOT3_MODEL' in os.environ:  # 检查环境变量中是否设置机器人型号
        os.environ['TURTLEBOT3_MODEL'] = 'waffle'  # 设置默认机器人型号为waffle

    # Directories  # 目录设置
    pkg_turtlebot3_gazebo = get_package_share_directory(  # 获取turtlebot3_gazebo包路径
        'turtlebot3_gazebo')
    pkg_nav2_bringup = get_package_share_directory(  # 获取nav2_bringup包路径
        'nav2_bringup')
    pkg_rtabmap_demos = get_package_share_directory(  # 获取rtabmap_demos包路径
        'rtabmap_demos')

    world = LaunchConfiguration('world').perform(context)  # 获取世界配置
    
    nav2_params_file = PathJoinSubstitution(  # 设置导航参数文件路径
        [FindPackageShare('rtabmap_demos'), 'params', 'turtlebot3_rgbd_scan_nav2_params.yaml']
    )

    # Paths  # 路径设置
    gazebo_launch = PathJoinSubstitution(  # 设置Gazebo启动文件路径
        [pkg_turtlebot3_gazebo, 'launch', f'turtlebot3_{world}.launch.py'])
    nav2_launch = PathJoinSubstitution(  # 设置导航启动文件路径
        [pkg_nav2_bringup, 'launch', 'navigation_launch.py'])
    rviz_launch = PathJoinSubstitution(  # 设置RViz启动文件路径
        [pkg_nav2_bringup, 'launch', 'rviz_launch.py'])
    rtabmap_launch = PathJoinSubstitution(  # 设置RTAB-Map启动文件路径
        [pkg_rtabmap_demos, 'launch', 'turtlebot3', 'turtlebot3_rgbd_scan.launch.py'])

    # Includes  # 包含其他启动文件
    gazebo = IncludeLaunchDescription(  # 包含Gazebo启动描述
        PythonLaunchDescriptionSource([gazebo_launch]),
        launch_arguments=[  # 设置启动参数
            ('x_pose', LaunchConfiguration('x_pose')),  # 机器人初始X位置
            ('y_pose', LaunchConfiguration('y_pose'))   # 机器人初始Y位置
        ]
    )
    nav2 = IncludeLaunchDescription(  # 包含导航启动描述
        PythonLaunchDescriptionSource([nav2_launch]),
        launch_arguments=[  # 设置启动参数
            ('use_sim_time', 'true'),  # 使用仿真时间
            ('params_file', nav2_params_file)  # 导航参数文件
        ]
    )
    rviz = IncludeLaunchDescription(  # 包含RViz启动描述
        PythonLaunchDescriptionSource([rviz_launch])
    )
    rtabmap = IncludeLaunchDescription(  # 包含RTAB-Map启动描述
        PythonLaunchDescriptionSource([rtabmap_launch]),
        launch_arguments=[  # 设置启动参数
            ('localization', LaunchConfiguration('localization')),  # 定位模式
            ('use_sim_time', 'true')  # 使用仿真时间
        ]
    )
    return [  # 返回要启动的节点列表
        # Nodes to launch  # 要启动的节点
        nav2,  # 导航节点
        rviz,  # 可视化节点
        rtabmap,  # RTAB-Map节点
        gazebo  # Gazebo仿真节点
    ]

def generate_launch_description():  # 生成启动描述
    return LaunchDescription([  # 返回启动描述
        
        # Launch arguments  # 启动参数
        DeclareLaunchArgument(  # 声明定位模式参数
            'localization', default_value='false',
            description='Launch in localization mode.'),
        
        DeclareLaunchArgument(  # 声明世界选择参数
            'world', default_value='house',
            choices=['world', 'house', 'dqn_stage1', 'dqn_stage2', 'dqn_stage3', 'dqn_stage4'],
            description='Turtlebot3 gazebo world.'),
        
        DeclareLaunchArgument(  # 声明机器人初始X位置参数
            'x_pose', default_value='-2.0',
            description='Initial position of the robot in the simulator.'),
        
        DeclareLaunchArgument(  # 声明机器人初始Y位置参数
            'y_pose', default_value='0.5',
            description='Initial position of the robot in the simulator.'),

        OpaqueFunction(function=launch_setup)  # 使用不透明函数设置启动配置
    ])
