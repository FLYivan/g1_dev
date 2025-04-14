# 一、WIFI连接调试
## 首次需先确保wifi已连接
    ### 安装nomachine
    1、下载安装包
    https://downloads.nomachine.com/download/?id=1

    2、先有线连接G1,确保G1的wifi连接上手机热点
        更改有线连接的IP和子网掩码
        ip:192.168.123.123 (这个地址不能设为pc2的ip地址，否则无法ssh登陆)
        子网掩码：255.255.255.0

    3、远程登陆
        ssh unitree@192.168.123.164
        密码为123

    4、然后ssh进入pc2并./nomachine.sh运行脚本文件

    5、然后打开自己pc的nomachine就可以看到pc2里面的图形化界面了

    6、把wifi打开，将pc2和自己的pc连到同一个wifi

## 在wifi连接下远程登陆
    1、用自己的pc ssh进入wifi给pc2分配的ip就可以无线开发了

        笔记本的ip：172.20.10.4
        pc2的ip：172.20.10.5

    2、可使用nomachine远程登陆图形化页面


# 二、g1 控制接口

## 确认是否可以下肢服务控制，上肢电机控制，在什么模式下
    上肢控制可以在运行机器人内置移动控制器的同时，单独控制上肢电机完成操作任务，提供 DDS 接口
    DDS 接口支持上肢控制，仅能在锁定站立、运控 1 与运控 2 中使用
    运控 1 与运控 2 是G1的两种运动步态，你可以遥控R1+X（主运控），R2+X（跑步运控）进行切换这两个运控体验一下


## 使用服务功能驱动下肢

    1、进入高层控制模式
        1、进入阻尼模式：长按 L1 + 单击 A
        2、进入锁定站立模式：长按 L1 + 单击 UP
        3、将机器人脚着地
        4、进入运控1: R1+X（主运控）
        5、或进入运控2：R2+X（跑步运控）

    2、构建ros2节点
        cd ~/unitree_ros2/unitree_ros2_ws/ # 进入unitree_ros2工作空间
        colcon build #编译工作空间下的所有功能包

    3、测试连接性
        在上位机输入：ros2 topic list

    4、测试loco服务例程
        ./install/unitree_ros2_example/bin/g1_loco_client_example --move="0 0 0.1"


    5、如果可行，python改造（保存到github）
        
        这是一个服务通信模式，还要该写base_client.hpp文件
        

    6、调试问题，先试下狗吧
        服务模式
            ./install/unitree_ros2_example/bin/go2_sport_client_example
            机器人会先坐下然后等待3秒后恢复站立

        话题通讯模式
            ./install/unitree_ros2_example/bin/sport_mode_ctrl
            程序启动1秒后，机器人将在x方向来回行走。

        关注下网口对不对
    
# 三、传感器驱动安装
## 雷达驱动安装到PC2

    1、下载ros2驱动
        git clone https://github.com/Livox-SDK/livox_ros_driver2.git ws_livox/src/livox_ros_driver2

    2、安装Cmake，g++
        sudo apt update
        sudo apt install cmake
        cmake --version


    3、下载SDK
        git clone https://github.com/Livox-SDK/Livox-SDK2.git
        cd ./Livox-SDK2/
        mkdir build
        cd build
        cmake .. && make -j
        sudo make install

    4、ip地址修改
        需要修改.../livox_ros_driver2/config/MID360_config.json 文件内的 "lidar_configs" "ip" 为 "192.168.123.120"
        "host_net_info" 下的 所有ip 为主机 ip——（G1的pc2：192.168.123.164，笔记本电脑：192.168.123.145）

    5、构建ros2驱动
        source /opt/ros/foxy/setup.sh
        ./build.sh ROS2

    6、source环境变量  
        1）source ~/Lidar/ws_livox/install/setup.bash

        2）在bashrc文件中添加如下内容
            # lidar环境变量
            source ~/Lidar/ws_livox/install/setup.bash;;

    7、运行驱动
        5.1、通过rviz显示雷达点云
        ros2 launch livox_ros_driver2 rviz_MID360_launch.py

        5.2、通过/livox/lidar(点云话题）、/livox/imu话题，订阅数据
        ros2 launch livox_ros_driver2 msg_MID360_launch.py
            /livox/imu
            /livox/lidar



## 相机驱动（已安装）

    *右上角type-c口为支持USB3.2 host，支持DP1.4，其余均为支持USB3.0 host，5V/1.5A电源输出

    1、启动节点
        
        ros2 launch realsense2_camera rs_launch.py

        > ros2 topic list
            /camera/color/camera_info
            /camera/color/image_raw
            /camera/color/metadata
            /camera/depth/camera_info
            /camera/depth/image_rect_raw
            /camera/depth/metadata
            /camera/extrinsics/depth_to_color
            /camera/extrinsics/depth_to_depth
            /camera/imu

        > ros2 service list
            /camera/camera/describe_parameters
            /camera/camera/get_parameter_types
            /camera/camera/get_parameters
            /camera/camera/list_parameters
            /camera/camera/set_parameters
            /camera/camera/set_parameters_atomically
            /camera/device_info


        ros2 launch realsense2_camera rs_launch.py depth_module.depth_profile:=1280x720x30 pointcloud.enable:=true
        > ros2 topic list
            /camera/color/camera_info
            /camera/color/image_raw
            /camera/color/metadata
            /camera/depth/camera_info
            /camera/depth/color/points
            /camera/depth/image_rect_raw
            /camera/depth/metadata
            /camera/extrinsics/depth_to_color
            /camera/extrinsics/depth_to_depth
            /camera/imu

        > ros2 service list
            /camera/camera/describe_parameters
            /camera/camera/get_parameter_types
            /camera/camera/get_parameters
            /camera/camera/list_parameters
            /camera/camera/set_parameters
            /camera/camera/set_parameters_atomically
            /camera/device_info


        
        默认值：
        camera_namespace:=camera
        camera_name:=camera   

    2、通过添加以下参数来启用加速度和陀螺仪
        ros2 launch realsense2_camera rs_launch.py pointcloud.enable:=true enable_gyro:=true enable_accel:=true
        > ros2 topic list
            /camera/accel/imu_info
            /camera/accel/metadata
            /camera/accel/sample
            /camera/color/camera_info
            /camera/color/image_raw
            /camera/color/metadata
            /camera/depth/camera_info
            /camera/depth/color/points
            /camera/depth/image_rect_raw
            /camera/depth/metadata
            /camera/extrinsics/depth_to_accel
            /camera/extrinsics/depth_to_color
            /camera/extrinsics/depth_to_depth
            /camera/extrinsics/depth_to_gyro
            /camera/gyro/imu_info
            /camera/gyro/metadata
            /camera/gyro/sample
            /camera/imu

        > ros2 service list
            /camera/camera/describe_parameters
            /camera/camera/get_parameter_types
            /camera/camera/get_parameters
            /camera/camera/list_parameters
            /camera/camera/set_parameters
            /camera/camera/set_parameters_atomically
            /camera/device_info



        frame_id改为：camera_depth_frame

    3、通过上位软件查看
        realsense-viewer


# 四、导航建图方案
    1、先在原仓库测试
            ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

            ros2 launch g1_sim turtlebot3_sim_rgbd_scan_demo.launch.py
            

            ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py

            ros2 launch turtlebot3_gazebo spawn_turtlebot3.launch.py

            ros2 run turtlebot3_teleop teleop_keyboard

            [ERROR] [gzserver-1]: process has died [pid 193163, exit code 255, cmd 'gzserver /opt/ros/humble/share/turtlebot3_gazebo/worlds/turtlebot3_house.world -slibgazebo_ros_init.so -slibgazebo_ros_factory.so -slibgazebo_ros_force_system.so'].
            [ERROR] [spawn_entity.py-4]: Service /spawn_entity unavailable. Was Gazebo started with GazeboRosFactory?

# 五、在go2上测试

    1、go2接双目相机
        怎么驱动
            在上位机已经可以驱动，换到nx上

    2、桥接接口
        # 先试下官方Python接口

        python3 ./go2_sport_client.py wlp0s20f3

        # 桥街准备

        1）安装unitree_sdk2py库
            
            sudo pip3 install -e .
            
        2）卸载sudo安装的opencv
            sudo pip uninstall opencv-python

        3）确认unitree_sdk2py库安装成功
            pip show unitree_sdk2py

        # 测试桥接效果节点

            colcon build --packages-select go2_cmd
            ros2 launch go2_cmd go2_cmd_test.launch.py
            ros2 run go2_cmd cmd_pub_test
            ros2 run go2_cmd go2_p2r_cmd



# 硬件驱动
    ros2 launch livox_ros_driver2 msg_MID360_launch.py
    ros2 launch livox_ros_driver2 rviz_MID360_launch.py
    更改frame_id ——mid360_link

    # 问题
    1、ros2 launch livox_ros_driver2 msg_MID360_launch.py发布出有效话题
    2、点云数据是180度倒置的

    ros2 launch realsense2_camera rs_launch.py pointcloud.enable:=true enable_gyro:=true enable_accel:=true

# 构建节点

colcon build --packages-select g1_sim
colcon build --packages-select g1_lidar_processing
colcon build --packages-select g1_slam_algorithm


# 建图
ros2 launch g1_slam_algorithm g1_slam_toolbox.launch.py 
ros2 launch g1_lidar_processing cloud_to_scan.launch.py
ros2 run g1_slam_algorithm motion_to_tf 


# nav2导航
ros2 launch g1_lidar_processing cloud_to_scan.launch.py
ros2 launch g1_nav g1_nav2_bringup.launch.py


# 启动仿真
     
    ros2 launch g1_sim g1_urdf2tf.launch.py