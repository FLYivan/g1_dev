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
            /camera/camera/color/camera_info
            /camera/camera/color/image_raw
            /camera/camera/color/image_raw/compressed
            /camera/camera/color/image_raw/compressedDepth
            /camera/camera/color/image_raw/theora
            /camera/camera/color/metadata
            /camera/camera/depth/camera_info
            /camera/camera/depth/image_rect_raw
            /camera/camera/depth/image_rect_raw/compressed
            /camera/camera/depth/image_rect_raw/compressedDepth
            /camera/camera/depth/image_rect_raw/theora
            /camera/camera/depth/metadata
            /camera/camera/extrinsics/depth_to_color

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

## 下载安装
### PC2上
    sudo apt install ros-$ROS_DISTRO-rtabmap-ros

    sudo chmod u+w 

    更新源：
        # 写入新的配置（移除 fuerte 相关配置）
sudo bash -c 'cat > /etc/ros/rosdep/sources.list.d/20-default.list << EOF
# os-specific listings first
yaml https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/osx-homebrew.yaml osx

# generic
yaml https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/base.yaml
yaml https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/python.yaml
yaml https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/ruby.yaml
gbpdistro https://raw.githubusercontent.com/ros/rosdistro/master/releases/fuerte.yaml fuerte

# newer distributions (Groovy, Hydro, ...) must not be listed anymore, they are being fetched from the rosdistro index.yaml instead
EOF'
        
        # 添加 GitHub 相关域名的解析
            sudo bash -c 'cat >> /etc/hosts << EOF
            185.199.108.133 raw.githubusercontent.com
            185.199.109.133 raw.githubusercontent.com
            185.199.110.133 raw.githubusercontent.com
            185.199.111.133 raw.githubusercontent.com
            EOF'

        # 清理缓存
            sudo rm -rf /etc/ros/rosdep/sources.cache/
            rm -rf ~/.ros/rosdep/sources.cache/

        # 初始化 rosdep
        sudo rosdep init

        # 更新 rosdep
        rosdep update

## 测试可用性
    colcon build --packages-select rtabmap_examples
    colcon build --packages-select rtabmap_util

    1、视觉slam
        1）在pc2上

            ros2 launch realsense2_camera rs_launch.py enable_gyro:=true enable_accel:=true unite_imu_method:=2 enable_sync:=true align_depth.enable:=true

            ros2 launch rtabmap_examples realsense_d435i_color.launch.py

        
        2）在上位机上

            ros2 launch realsense2_camera rs_launch.py \
                camera_namespace:="" \
                enable_gyro:=true \
                enable_accel:=true \
                unite_imu_method:=1 \
                align_depth.enable:=true \
                enable_sync:=true \
                rgb_camera.profile:=640x360x30

            ros2 launch rtabmap_examples realsense_d435i_color.launch.py


    2、激光slam

        ros2 launch livox_ros_driver2 rviz_MID360_launch.py

        ros2 launch rtabmap_examples lidar3d.launch.py lidar_topic:=/livox/lidar frame_id:=mid360_link imu_topic:=/livox/imu 


    3、室内2d激光和RGB-D融合slam

        激光驱动：
            ros2 launch livox_ros_driver2 rviz_MID360_launch.py

        双目驱动：
            ros2 launch realsense2_camera rs_launch.py \
                align_depth.enable:=true \
                enable_sync:=true \
                rgb_camera.profile:=640x360x30

        tf和单线激光驱动：
            ros2 launch g1_slam_algorithm g1_rtabmap_pre_pc.launch.py


            
        ros2 launch g1_slam_algorithm robot_mapping_demo_g1.launch.py
        

## 构建
    colcon build --packages-select rtabmap_demos

## 测试节点
### 1、2d lidar+RGB-D slam + nav2
        RGB-D: 
            ros2 launch rtabmap_demos turtlebot3_sim_rgbd_demo.launch.py
            ros2 launch rtabmap_demos turtlebot3_sim_rgbd_demo.launch.py world:=dqn_stage2
        RGB-D+scan:
            ros2 launch rtabmap_demos turtlebot3_sim_rgbd_scan_demo.launch.py
        
        操作：
            ros2 run turtlebot3_teleop teleop_keyboard

### 2、室内2d激光和RGB-D融合slam

    SLAM:
        ros2 launch rtabmap_demos robot_mapping_demo.launch.py rviz:=true rtabmap_viz:=true

    Rosbag:
        ros2 bag play demo_mapping.db3 --clock
### 3、find-object

    SLAM:
        ros2 launch rtabmap_demos find_object_demo.launch.py

    Rosbag:
        ros2 bag play demo_find_object.db3 --clock

### 4、3d激光点云+RGB-D slam融合+nav2

    ros2 launch rtabmap_demos husky_sim_scan3d_assemble_demo.launch.py robot_ns:=a200_0000

    启动后，先按gazebo左下角暂停

    ros2 launch clearpath_nav2_demos nav2.launch.py setup_path:=/home/flyivan/dog_robot/lib/rtabmap_ros_ws/src/rtabmap_ros/rtabmap_demos/data/clearpath/ use_sim_time:=true
        
### 5、3d激光点云+RGB-D slam+nav2

    ros2 launch rtabmap_demos husky_sim_scan3d_demo.launch.py robot_ns:=a200_0000

    ros2 launch clearpath_nav2_demos nav2.launch.py setup_path:=/home/flyivan/dog_robot/lib/rtabmap_ros_ws/src/rtabmap_ros/rtabmap_demos/data/clearpath/ use_sim_time:=true

### 6、isaac sim中，nav2+RGB-D slam
    先要安装issac sim。笔记本内存不够

    ros2 launch rtabmap_demos isaac_vslam.launch.py stereo:=false vo:=rtabmap


## 地图保存

    地图默认保存路径【~/.ros/rtabmap.db】
    打开方式
        1、rtabmap
        2、载入文件
    
    rtabmap.launch.py文件有很多参数可以自定义

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

    pc2:
        ros2 launch livox_ros_driver2 rviz_MID360_launch.py


    上位机：
        ros2 launch realsense2_camera rs_launch.py 
        frame_id: camera_color_optical_frame

# 构建节点

    colcon build --packages-select g1_sim
    colcon build --packages-select g1_lidar_processing
    colcon build --packages-select g1_slam_algorithm


# 建图
    slam-toolbox:
        ros2 launch g1_slam_algorithm g1_slam_toolbox.launch.py 
        ros2 launch g1_lidar_processing cloud_to_scan.launch.py
        ros2 run g1_slam_algorithm motion_to_tf 

    rtabmap:
        ros2 launch g1_slam_algorithm g1_rtabmap_pre_pc.launch.py
        ros2 launch g1_slam_algorithm robot_mapping_demo_g1.launch.py


    报错：
        [rgbd_sync-1] [ERROR] [1744708214.025348285] [rgbd_sync]: SubscriberPlugin::subscribeImpl with five arguments has not been overridden



# nav2导航
ros2 launch g1_lidar_processing cloud_to_scan.launch.py
ros2 launch g1_nav g1_nav2_bringup.launch.py


# 启动仿真
     
    ros2 launch g1_sim g1_urdf2tf.launch.py