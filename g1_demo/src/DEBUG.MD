ctrl+shirt+v 预览
# 调试问题
1、如果只有底层能支持ros2框架，在使用时，是否要先确保R2+L2，进入调试模式，关闭掉主运控？
2、realsense安装
3、看下pc2中是否已安装雷达驱动 find . -name livox_sdk2
4、怎么连wifi



# 底层运控
## C++
    ### 下肢
    sudo ./g1_ankle_swing_example enp0s31f6

    ### 手臂
    sudo ./g1_dual_arm_example enp0s31f6        # 按预设轨迹移动手臂

## Python
    ### 下肢
        #### 运控
        1、 将机器人所有关节缓慢归零（0-3秒）
        2、使用PR(Pitch/Roll)模式控制脚踝关节， 脚踝进行正弦摆动，最大角度：- 俯仰(Pitch): ±30度，- 横滚(Roll): ±10度 (3-6秒)
        3、切换到AB模式控制脚踝和手腕（AB模式主要用于具有并联机构的关节（如脚踝）），脚踝和手腕进行正弦摆动
        
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
## 雷达点云显示
    ### 通过上位机软件
        https://www.livoxtech.com/cn/downloads

    ### 通过ros框架
        1、下载ros2驱动
        git clone https://github.com/Livox-SDK/livox_ros_driver2.git ws_livox/src/livox_ros_driver2

        2、下载SDK
            git clone https://github.com/Livox-SDK/Livox-SDK2.git
            cd ./Livox-SDK2/
            mkdir build
            cd build
            cmake .. && make -j
            sudo make install

        3、ip地址修改
        需要修改.../livox_ros_driver2/config/MID360_config.json 文件内的 "lidar_configs" "ip" 为 "192.168.123.120"
        "host_net_info" 下的 ip 为主机 ip——（G1的pc2：192.168.123.164，笔记本电脑：192.168.123.145）

        4、构建
        source /opt/ros/humble/setup.sh
        ./build.sh humble

        5、运行驱动
            5.1、通过rviz显示雷达点云
            ros2 launch livox_ros_driver2 rviz_MID360_launch.py

            5.2、通过/livox/lidar(点云话题）、/livox/imu话题，订阅数据
            ros2 launch livox_ros_driver2 msg_MID360_launch.py

# 深度相机驱动
## 驱动安装
    1、安装SDK
    sudo apt install ros-$ROS_DISTRO-librealsense2*

    2、安装ros功能包
    #### 命令行安装
        在PC2中，输入如下命令
        sudo apt install ros-$ROS_DISTRO-realsense2-*

    #### 源码安装
        1、创建工作空间
        mkdir -p ~/ros2_ws/src
        cd ~/ros2_ws/src/

        2、下载源码
        git clone https://github.com/IntelRealSense/realsense-ros.git -b ros2-master
        cd ~/ros2_ws

        3、安装依赖
        sudo apt-get install python3-rosdep -y

        （sudo rosdep init # "sudo rosdep init --include-eol-distros" for Foxy and earlier
            rosdep update # "sudo rosdep update --include-eol-distros" for Foxy and earlier）

        rosdep install -i --from-path src --rosdistro $ROS_DISTRO --skip-keys=librealsense2 -y

        4、构建
        colcon build

        5、配置环境变量
        source /opt/ros/$ROS_DISTRO/setup.bash
        cd ~/ros2_ws
        . install/local_setup.bash


## 图像显示
    ### 通过上位机
        #### 安装nomachine
        1、下载安装包
        https://downloads.nomachine.com/download/?id=1

        2、然后ssh进入pc2并./nomachine.sh运行脚本文件，
        3、然后打开自己pc的nomachine就可以看到pc2里面的图形化界面了

    ### 在上位机安装驱动
        #### 参考如下网址步骤安装
        https://github.com/IntelRealSense/librealsense/releases

    ### 在PC2中安装驱动
        
        1、查看linux内核： uname -mrs
        2、查看jepack版本：
            cat /etc/nv_tegra_release
            sudo apt-cache show nvidia-jetpack
            dpkg-query --show nvidia-jetpack

        #### 参考如下网址步骤安装
        https://github.com/IntelRealSense/librealsense/releases



        #### 单个机器人
        1、启动节点
            
            ros2 launch realsense2_camera rs_launch.py
            ros2 launch realsense2_camera rs_launch.py depth_module.depth_profile:=1280x720x30 pointcloud.enable:=true

            
            默认值：
            camera_namespace:=camera
            camera_name:=camera   

        2、通过添加以下参数来启用加速度和陀螺仪
            ros2 launch realsense2_camera rs_launch.py pointcloud.enable:=true enable_gyro:=true enable_accel:=true

        3、获取话题和服务
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

        #### 有多个相机，多个机器人情况
            1、启动节点
                ros2 launch realsense2_camera rs_launch.py camera_namespace:=robot1 camera_name:=D455_1
                或
                ros2 run realsense2_camera realsense2_camera_node --ros-args -r __node:=D455_1 -r __ns:=robot1

                结果：
                > ros2 node list
                    /robot1/D455_1

            2、获取话题和服务
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

# WIFI连接开发
pc2内置了wifi模块，默认是关闭的，如果想使用的话
1.用屏幕连接G1的pd输出的usb-c口，进入pc2关闭掉飞行模式（注意此步不能ssh进入pc2操作，只能连屏幕操作）
2.打开pc2的wifi，将pc2和自己的pc连到同一个wifi，然后用自己的pc ssh进入wifi给pc2分配的ip就可以无线开发了











