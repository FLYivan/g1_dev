import launch
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction

def generate_launch_description():

    # 点云转2d激光节点
    node_p2l = Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            name='pointcloud_to_laserscan',
            parameters=[{
                # 'target_frame': 'cloud_test',
                'transform_tolerance': 0.01,
                'min_height': 0.0,
                'max_height': 1.8,                       # 障碍物最大高度 （长直走廊如果设的过大，会把过道的屋顶作为障碍物，投射到2d平面）
                'angle_min': -3.14,                      # -M_PI/2
                'angle_max': 3.14,                       # M_PI/2
                'angle_increment': 0.0087,               # M_PI/360.0
                'scan_time': 0.1,                        # 10Hz，点云生成的激光雷达频率(不可动参数)
                'range_min': 0.0,                        # 激光扫描中测量的最小距离，单位为米(为了避开路由器，最小距离必须大于0.25米)
                'range_max': 100.0,                      # 激光扫描中测量的最大距离，单位为米
                'use_inf': False,                        # 是否使用无穷大值来表示超出测量范围的点。
                'inf_epsilon': 0.001,                    # 是一个小的正数，用于替代激光扫描数据中超出测量范围的无穷大值
            }],
            remappings=[
                ('cloud_in', '/livox/lidar'),           # 禾赛sdk独立驱动xt16雷达     
                ('scan', '/scan'),
            ]
        )

    # 激光frame_id修改节点
    node_frame =  Node(
            package='g1_slam_algorithm',                      
            executable='frame_id_modifier',             
            name='frame_id_modifier',
            output='screen',
            parameters=[{'new_frame_id': 'mid360_link'}]        # 修改后frameid
        )

    # 延迟启动 node_frame
    delayed_node = TimerAction(period=3.0,  actions=[node_frame]) # 延迟 3 秒启动


    return LaunchDescription([
        node_p2l,
        # delayed_node,
    ])



