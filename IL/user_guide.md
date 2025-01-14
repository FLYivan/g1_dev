# 环境配置

1、安装Hugging Face CLI
    pip install --upgrade pip
    pip install huggingface-cli
    pip install -U huggingface_hub

2、配置环境变量
    # Hugging Face CLI数据源调整为镜像站
    export HF_ENDPOINT=https://hf-mirror.com


# 脚本配置

1、复制download_dataset.sh脚本
2、给脚本赋权限
sudo chmod +x download_dataset.sh