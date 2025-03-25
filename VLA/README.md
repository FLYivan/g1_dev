# 一、安装miniconda
    参考：
        https://blog.csdn.net/KRISNAT/article/details/124041869

    2、默认启动时不使用conda
        conda config --set auto_activate_base false


# 二、安装cuda 12.4




# 二、已有数据集格式转换

    1、注册huggingface

    2、数据集上传
        参考如下地址：
        https://hugging-face.cn/docs/hub/datasets-adding

    --repo-id unitree/UnitreeG1_DualArmGrasping
    --repo-id 可根据自己需求填写，这里时unitree/UnitreeG1_DualArmGrasping

    这里自定义了一个 FLYivan/G1_Arm_Test

    


# 三、已有数据集微调测试




# 四、已有数据集与机器人控制衔接





# 五、遥操作采集数据


    安装OpenDrop：
        pip3 install opendrop

    发送文件： 
        首先，使用find命令发现附近的设备： opendrop find 
        然后，使用send命令发送文件： opendrop send -r 0 -f /path/to/some/file

    通过 AirDrop 将 rootCA.pem 复制到 Apple Vision Pro 并安装它。