# 流配置参数
<stream_name>_format
用于选择数据流格式的字符串参数
<stream_name> 可以是: infra(红外), infra1(红外1), infra2(红外2), color(彩色), depth(深度)
例如: depth_module.depth_format:=Z16

注意:
支持大小写字母
如果指定的格式不可用，将使用默认值或之前的设置
更改后需要重新启用数据流才能生效

enable_<stream_name>
用于启用或禁用指定的数据流
图像流默认为true，方向数据流默认为false
<stream_name> 可以是: infra, infra1, infra2, color, depth, gyro(陀螺仪), accel(加速度计)
示例: enable_infra1:=true enable_color:=false

# 同步和QoS参数
enable_sync
同步不同传感器(红外、彩色和深度)的最近帧，使它们具有相同的时间戳
当启用点云等滤波器时会自动启用
<stream_type>_qos
设置话题的QoS(服务质量)级别
可用值: SYSTEM_DEFAULT, DEFAULT, PARAMETER_EVENTS, SERVICES_DEFAULT, PARAMETERS, SENSOR_DATA
示例: depth_qos:=SENSOR_DATA

# TF变换相关参数
tf_publish_rate
这是一个双精度浮点数参数
用于设置动态转换(dynamic transforms)的发布频率，单位是赫兹(Hz)
默认值是 0.0 Hz，表示不发布动态转换
这个参数的实际效果依赖于 publish_tf 参数的设置

publish_tf
这是一个布尔值参数
控制是否发布转换（包括静态和动态转换）

两个参数的组合效果：
如果 publish_tf = false：
无论 tf_publish_rate 设置为多少，都不会发布任何转换

如果 publish_tf = true： （主要用于将光学坐标转化为机器人坐标）
静态转换会被发布
如果 tf_publish_rate > 0.0，动态转换会以设定的频率发布
如果 tf_publish_rate = 0.0，则只发布静态转换

# IMU相关参数
unite_imu_method
用于D400系列相机的IMU数据合并方法
值含义:
0: 不合并IMU数据
1: 复制模式 - 每个陀螺仪消息都附带最新的加速度计消息
2: 线性插值 - 加速度计数据根据陀螺仪时间戳进行插值

# GPU处理点云
accelerate_gpu_with_glsl 是一个布尔类型的参数，用于控制是否使用 GPU（通过 GLSL）来加速处理点云（PointCloud）和颜色器（Colorizer）过滤器。
主要内容包括：
功能：
使用 GPU 加速点云和颜色器的处理
通过 GLSL（OpenGL Shading Language）实现加速

动态更新处理：
当这个参数被动态更新时，系统会按以下步骤执行：
停止视频传感器
进行必要的 GLSL 配置
重新启动视频传感器

启用方法：
要启用 GPU 加速，需要在编译时打开相关选项：
colcon build --cmake-args '-DBUILD_ACCELERATE_GPU_WITH_GLSL=ON'

# 其他不可实时调整的参数

1、serial_no
用于连接指定序列号的RealSense设备
默认连接列表中的第一个设备
注意：序列号前必须加上""前缀（这是ROS2的一个临时解决方案）
示例：serial_no:=_831612073525

2、usb_port_id
用于连接指定USB端口的设备
示例：usb_port_id:=4-1 或 usb_port_id:=4-2
默认不考虑USB端口号

3、device_type
用于连接特定型号的设备，支持正则表达式匹配
默认不考虑设备类型
示例：
device_type:=d435 会匹配d435和d435i
device_type=d435(?!i) 只匹配d435，不匹配d435i

4、reconnect_timeout
当设备连接失败时，重新尝试连接的等待时间（秒）
示例：reconnect_timeout:=10

5、wait_for_device_timeout
等待设备连接的超时时间（秒）
默认值小于0，表示无限等待
示例：wait_for_device_timeout:=60

6、rosbag_filename
用于从rosbag文件发布话题
两种设置方式：
命令行：ros2 run realsense2_camera realsense2_camera_node -p rosbag_filename:="/path/to/rosbag.bag"
启动文件：在launch文件中设置参数

7、initial_reset
设备初始化时是否重置
当设备之前未正常关闭时可能需要重置
示例：initial_reset:=true

8、base_frame_id
定义所有静态转换所参考的框架ID

9、clip_distance
设置深度图像的最大距离值（米）
负值表示禁用此功能
示例：clip_distance:=1.5

10、linear_accel_cov, angular_velocity_cov
设置IMU读数的方差值

11、hold_back_imu_for_frames
控制IMU消息的发布时序
设为true时，会在图像处理期间保持IMU消息，然后一起发布
用于确保消息发布顺序与到达顺序一致

12、publish_tf
控制是否发布静态和动态TF转换
默认为true
动态TF需要设置tf_publish_rate>0.0

13、diagnostics_period
设置诊断信息发布的周期（在/diagnostics话题上）
0或负值表示不发布诊断信息
包含设备温度和启用流的实际频率信息