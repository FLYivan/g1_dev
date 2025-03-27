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


# 三、fork源仓库
    1、git remote add upstream https://github.com/NVIDIA/Isaac-GR00T.git
    2、git remote -v
    3、git fetch upstream
    4、git merge upstream/main

# 四、安装

    conda activate unitree_g1
    pip install --upgrade setuptools
    pip install -e .
    pip install --no-build-isolation flash-attn==2.7.1.post4


# 二、已有数据集格式转换

    1、注册huggingface

    2、数据集上传
        参考如下地址：
        https://hugging-face.cn/docs/hub/datasets-adding

    --repo-id unitree/UnitreeG1_DualArmGrasping
    --repo-id 可根据自己需求填写，这里时unitree/UnitreeG1_DualArmGrasping

    这里自定义了一个 FLYivan/G1_Arm_Test


# 五、已有数据集离线测试

    # 放入g1的modality.json文件

    # 服务器模式
    python scripts/inference_service.py --model_path nvidia/GR00T-N1-2B --server

    python scripts/inference_service.py --model_path /home/flyivan/human_robot/VLA/model/GR00T_N1 --server
   

    # 在不同的终端中，运行客户端模式向服务器发送请求
    python scripts/inference_service.py --client



    # 运行新训练的模型
    python scripts/inference_service.py --server \
    --model_path <MODEL_PATH> \
    --embodiment_tag new_embodiment

    # 运行离线评估脚本
    python scripts/eval_policy.py --plot \
    --dataset_path /home/flyivan/human_robot/VLA/dataset/unitreerobotics/G1_DualArmGrasping_Dataset \
    --embodiment_tag new_embodiment



# 三、已有数据集微调测试




# 四、已有数据集与机器人控制衔接





# 五、遥操作采集数据


    安装OpenDrop：
        pip3 install opendrop

    发送文件： 
        首先，使用find命令发现附近的设备： opendrop find 
        然后，使用send命令发送文件： opendrop send -r 0 -f /path/to/some/file

    通过 AirDrop 将 rootCA.pem 复制到 Apple Vision Pro 并安装它。



# 问宇树问题

    1、连接G1的时候，host和port 分别是什么