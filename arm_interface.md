# /arm_sdk话题，LowCmd接口的MotorCmd[35] motor_cmd字段结构


12	WAIST_YAW	WAIST_YAW                        # 腰部偏航关节,控制腰部左右转动
13	WAIST_ROLL	WAIST_A                          # 腰部横滚关节,控制腰部左右倾斜
14	WAIST_PITCH	WAIST_B                          # 腰部俯仰关节,控制腰部前后倾斜
15	L_SHOULDER_PITCH	L_SHOULDER_PITCH         # 左肩俯仰关节,控制左臂上下摆动
16	L_SHOULDER_ROLL	L_SHOULDER_ROLL              # 左肩横滚关节,控制左臂内外展开
17	L_SHOULDER_YAW	L_SHOULDER_YAW               # 左肩偏航关节,控制左臂前后旋转
18	L_ELBOW	L_ELBOW                              # 左肘关节,控制左前臂弯曲
19	L_WRIST_ROLL	L_WRIST_ROLL                 # 左腕横滚关节,控制左手腕内外旋转
20	L_WRIST_PITCH	L_WRIST_PITCH                # 左腕俯仰关节,控制左手腕上下弯曲
21	L_WRIST_YAW	L_WRIST_YAW                      # 左腕偏航关节,控制左手腕左右转动
22	R_SHOULDER_PITCH	R_SHOULDER_PITCH         # 右肩俯仰关节,控制右臂上下摆动
23	R_SHOULDER_ROLL	R_SHOULDER_ROLL              # 右肩横滚关节,控制右臂内外展开
24	R_SHOULDER_YAW	R_SHOULDER_YAW               # 右肩偏航关节,控制右臂前后旋转
25	R_ELBOW	R_ELBOW                              # 右肘关节,控制右前臂弯曲
26	R_WRIST_ROLL	R_WRIST_ROLL                 # 右腕横滚关节,控制右手腕内外旋转
27	R_WRIST_PITCH	R_WRIST_PITCH                # 右腕俯仰关节,控制右手腕上下弯曲
28	R_WRIST_YAW	R_WRIST_YAW                      # 右腕偏航关节,控制右手腕左右转动
29  MotorCmd_.q                                  # 关节目标位置，表示权重，取值范围为 [0.0, 1.0]。