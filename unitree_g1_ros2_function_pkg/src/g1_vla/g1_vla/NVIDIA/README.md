# 一、安装miniconda
    参考：
        https://blog.csdn.net/KRISNAT/article/details/124041869

    2、默认启动时不使用conda
        conda config --set auto_activate_base false


# 二、安装cuda 12.4/安装cudnn/安装TensorRT
    1、cuda
    参考 https://blog.csdn.net/xuehu96/article/details/133577211


    2、

    3、TensorRT
    参考 https://blog.csdn.net/qq_58158950/article/details/143061098
    https://blog.csdn.net/weixin_60864335/article/details/126671341


    pip install nvidia-pyindex
    pip install nvidia-tensorrt

    1）查看python版本
        python --version

    2）所以对应的版本安装
        pip install --force-reinstall tensorrt-10.0.0b6-cp310-none-linux_x86_64.whl 


# 三、安装必要依赖库
    sudo apt update
    sudo apt install ffmpeg libsm6 libxext6


# 四、fork源仓库
    1、git remote add upstream https://github.com/NVIDIA/Isaac-GR00T.git
    2、git remote -v
    3、git fetch upstream
    4、git merge upstream/main

# 五、安装

    conda activate unitree_g1
    pip install --upgrade setuptools
    pip install -e .
    pip install --no-build-isolation flash-attn==2.7.1.post4


# 六、自采数据集格式转换

    ## 在线数据集
        1、注册huggingface

        2、数据集上传
            参考如下地址：
            https://hugging-face.cn/docs/hub/datasets-adding

        --repo-id unitree/UnitreeG1_DualArmGrasping
        --repo-id 可根据自己需求填写，这里时unitree/UnitreeG1_DualArmGrasping

        这里自定义了一个 FLYivan/G1_Arm_Test

# 七、数据集加载

    1、下载到本地
        利用download_dataset.sh 脚本

    2、加载数据集
        python scripts/load_dataset.py --data_path /home/flyivan/human_robot/VLA/dataset/unitreerobotics/G1_DualArmGrasping_Dataset/ --embodiment_tag g1

# 八、在给定测试数据集的情况下，使用GR00T推理模型从观察值中预测操作。（服务端-客户端模式）

    1、模型离线下载（无法访问huggingface)
        使用download_model.py脚本

    2、放入g1的modality.json文件

    3、更改服务器模式下模型获取地址

        python scripts/inference_service.py --model_path /home/flyivan/human_robot/VLA/model/GR00T_N1 --embodiment_tag g1 --server 


    4、在不同的终端中，运行客户端模式向服务器发送请求
        python scripts/inference_service.py --embodiment_tag g1 --client 


    g1的video_backend参数要特别设置
        video_backend="torchvision_av"

# 九、已训模型离线评估

    ## 运行新训练的模型
    python scripts/inference_service.py --server \
    --model_path /home/flyivan/human_robot/VLA/dataset/unitreerobotics/G1_DualArmGrasping_Dataset/ \
    --embodiment_tag g1

    ## 运行离线评估脚本（用现有数据集）
    python scripts/eval_policy.py --plot \
    --dataset_path /home/flyivan/human_robot/VLA/dataset/unitreerobotics/G1_DualArmGrasping_Dataset/ \
    --embodiment_tag g1


# 三、已有数据集微调测试




# 十一、已有策略在机器人上部署

    1、通过Gr00tPolicy类实现

        类中根据不同机器人平台要指定embodiment_tag，在embodiment_tags.py文件中设置


    2、启动策略服务
        python scripts/inference_service.py --server \
        --model_path /home/flyivan/human_robot/VLA/model/GR00T_N1 \
        --embodiment_tag g1 \
        --data_config g1_arms_only \
        --denoising_steps 4

    3、启动客户端节点

        python examples/eval_gr00t_so100.py \
        --use_policy --host <YOUR_POLICY_SERVER_HOST> \
        --port <YOUR_POLICY_SERVER_PORT> \
        --camera_index <YOUR_CAMERA_INDEX>

        客户端节点可以使用from gr00t.eval.service import ExternalRobotInferenceClient类实现
        policy.get_action()端点是唯一的接口

        1）实例为适配So100 Lerobot的
        2）和宇树确认host和port,以及camera_index
            查询https://support.unitree.com/home/zh/G1_developer/depth_camera_instruction页面
        3) 确认模仿学习时是否需要手腕摄像头

# 十二、遥操作采集数据


    安装OpenDrop：
        pip3 install opendrop

    发送文件： 
        首先，使用find命令发现附近的设备： opendrop find 
        然后，使用send命令发送文件： opendrop send -r 0 -f /path/to/some/file

    通过 AirDrop 将 rootCA.pem 复制到 Apple Vision Pro 并安装它。



# 问宇树问题

    1、连接G1的时候，host和port 分别是什么
    2）和宇树确认host和port,以及camera_index
    3) 确认模仿学习时是否需要手腕摄像头