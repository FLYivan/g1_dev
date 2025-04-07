#!/bin/bash
  
# 把TigerResearch/pretrain_zh换成需要的路径
export HF_ENDPOINT=https://hf-mirror.com
COMMAND="huggingface-cli download --repo-type dataset --resume-download unitreerobotics/G1_DualArmGrasping_Dataset --local-dir unitreerobotics/G1_DualArmGrasping_Dataset"

# 循环执行命令，直到成功
while true; do
    $COMMAND
    if [ $? -eq 0 ]; then
        echo "Command executed successfully."
        break
    else
        echo "Command failed, retrying..."
        sleep 5  # 可选：等待5秒后重试，避免过于频繁的重试
    fi
done
