# 订阅话题

话题名	                类型	                        解析
odom	            nav_msgs/Odometry	        里程计流。如果参数subscribe_depth或subscribe_stereo为true；且未设置odom_frame_id，则为必需参数。
rgb/image	        sensor_msgs/Image	        RGB/单目图像。
rgb/camera_info	    sensor_msgs/CameraInfo	    RGB相机参参数。
depth/image	        sensor_msgs/Image	        深度图像。
scan	            sensor_msgs/LaserScan	    单线激光。
scan_cloud	        sensor_msgs/PointCloud2	    激光扫描点云流。
left/image_rect	    sensor_msgs/Image	        左目校正图像。
left/camera_info	sensor_msgs/CameraInfo	    左目相机参数。
right/image_rect	sensor_msgs/Image	        右目校正图像。
right/camera_info	sensor_msgs/CameraInfo	    右目相机参数。
goal	            geometry_msgs/PoseStamped	规划使用当前在线地图规划实现此目标的路径。
rgbd_image	        rtabmap_ros/RGBDImage	    RGB-D同步映像，仅当subscribe_rgbd为true时。

# 发布话题

话题名	                        类型	                        解析
info	                rtabmap_ros/Info	            rtabmap信息。
mapData	                rtabmap_ros/MapData	            rtabmap的图形和最新节点数据。
mapGraph	            rtabmap_ros/MapGraph	        rtabmap的图形
grid_map	            nav_msgs/OccupancyGrid	        通过激光扫描生成的地图占用网格。
proj_map	            nav_msgs/OccupancyGrid	        不推荐使用，使用/grid_map替换为Grid/FromDepth=true
cloud_map	            sensor_msgs/PointCloud2	        从局部栅格生成的三维点云。
cloud_obstacles	        sensor_msgs/PointCloud2	        从局部网格生成障碍物的三维点云。
cloud_ground	        sensor_msgs/PointCloud2	        从局部栅格生成的三维地面点云。
scan_map	            sensor_msgs/PointCloud2	        2D扫描或3D扫描生成的3D点云。
labels	                visualization_msgs/MarkerArray	在RVIZ中显示图形标签的方便方法。
global_path	            nav_msgs/Path	                规划全局路径的规划位姿。仅为每个规划路径发布一次。
local_path	            nav_msgs/Path	                规划与全局路径对应的未来局部位姿。在每次地图更新时发布。
goal_reached	        std_msgs/Bool	                是否成功实现目标的计划状态消息。
goal_out	            geometry_msgs/PoseStamped	    规划从rtabmap的拓扑规划器发送的当前度量目标。例如，可以通过move_base_simple/goal连接到move_base。
octomap_full	        octomap_msgs/Octomap	        获取octomap。仅当rtabmap_ros使用octomap构建时可用。
octomap_binary	        octomap_msgs/Octomap	        获取octomap。仅当rtabmap_ros使用octomap构建时可用。
octomap_occupied_space	sensor_msgs/PointCloud2	        octomap占用空间（障碍物和地面）的点云。仅当rtabmap_ros使用octomap构建时可用。
octomap_obstacles	    sensor_msgs/PointCloud2	        octomap上障碍物的点云。仅当rtabmap_ros使用octomap构建时可用。
octomap_ground	        sensor_msgs/PointCloud2	        octomap的点云。仅当rtabmap_ros使用octomap构建时可用。
octomap_empty_space	    sensor_msgs/PointCloud2	        octomap的空白点云。仅当rtabmap_ros使用octomap构建时可用。
octomap_grid	        nav_msgs/OccupancyGrid	        将octomap投影到二维占用栅格地图中。仅当rtabmap_ros使用octomap构建时可用。