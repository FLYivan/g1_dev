# 例程调试


# 底层运控
    ## C++
        ### 下肢
        sudo ./g1_ankle_swing_example enp0s31f6

        ### 手臂
        sudo ./g1_dual_arm_example enp0s31f6

    ## Python
        ### 下肢
        python3 ./example/g1/low_level/g1_low_level_example.py enp0s31f6



# 高层运控及状态获取
    ## C++
        ### 下肢
            #### 运控
            1、行走
            sudo ./g1_loco_client --network_interface=enp0s31f6 --set_velocity="0.5 0 0 1"

            2、下蹲
            sudo ./g1_loco_client --network_interface=enp0s31f6 --squat 

            #### 状态获取
            1、站立高度获取
            sudo ./g1_loco_client --network_interface=enp0s31f6 --get_stand_height

        ### 手臂    
            #### 运控
            1、手臂按既定逻辑摆动
            sudo ./g1_arm7_sdk_dds_example enp0s31f6

    ## Python
        ### 下肢
            #### 运控
            python3 ./example/g1/high_level/g1_loco_client_example.py enp0s31f6

                TestOption(name="damp", id=0),              阻尼态
                TestOption(name="stand_up", id=1),          站起
                TestOption(name="sit", id=2),               坐下
                TestOption(name="move forward", id=3),      向前移动   
                TestOption(name="move lateral", id=4),      横向移动
                TestOption(name="move rotate", id=5),       旋转移动
                TestOption(name="low stand", id=6),         站低
                TestOption(name="high stand", id=7),        站高
                TestOption(name="zero torque", id=8)   

        


# 雷达驱动

# 深度相机驱动

ros2 launch realsense2_camera rs_launch.py
ros2 launch realsense2_camera rs_launch.py depth_module.depth_profile:=1280x720x30 pointcloud.enable:=true

通过添加以下参数来启用加速度和陀螺仪
ros2 launch realsense2_camera rs_launch.py pointcloud.enable:=true enable_gyro:=true enable_accel:=true

默认值
camera_namespace:=camera
camera_name:=camera

结果
> ros2 node list
/camera/camera

> ros2 topic list
/camera/camera/color/camera_info
/camera/camera/color/image_raw
/camera/camera/color/metadata
/camera/camera/depth/camera_info
/camera/camera/depth/image_rect_raw
/camera/camera/depth/metadata
/camera/camera/extrinsics/depth_to_color
/camera/camera/imu

> ros2 service list
/camera/camera/device_info


有多个相机，多个机器人情况
ros2 launch realsense2_camera rs_launch.py camera_namespace:=robot1 camera_name:=D455_1
或
ros2 run realsense2_camera realsense2_camera_node --ros-args -r __node:=D455_1 -r __ns:=robot1

结果
> ros2 node list
/robot1/D455_1

> ros2 topic list
/robot1/D455_1/color/camera_info
/robot1/D455_1/color/image_raw
/robot1/D455_1/color/metadata
/robot1/D455_1/depth/camera_info
/robot1/D455_1/depth/image_rect_raw
/robot1/D455_1/depth/metadata
/robot1/D455_1/extrinsics/depth_to_color            # 外参信息
/robot1/D455_1/imu

> ros2 service list
/robot1/D455_1/device_info

在RealSense相机中，原点（0,0,0）取自左侧IR（infra1）位置，并命名为“camera_link”帧
深度、左IR和“camera_link”坐标会聚在一起。
