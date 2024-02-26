# 实验二 隐私保护的机器学习

## 1. 相关文件描述

- requirements.txt：python 依赖
- play_active.py, play_passive.py：程序运行代码
- **active.py, passive.py：VFL 模型核心代码，作业相关（关注 TODO）**
- comm.py, dataset.py, paillier.py, transform.py：通信，数据读取，加密协议，特征变换相关文件（可不看）
- cancer-active-train.csv, cancer-passive-train.csv：数据集

## 2. 实验内容

1. 代码相关内容 (50')

   Q1 (20'). 补全 y_hat 计算流程：active.py: line 68-74, passive.py: line 92-96

   Q2 (20'). 补全梯度计算流程：active.py: line 82-90, passive.py: line 98-107

   Q3 (10'). 补全训练过程中模型准确率计算流程：active.py: line 118-124

2. 文字描述内容 (50')

   Q1 (20'). 请说明代码中 scale 函数的原理及作用：play_active.py: line 13, play_passive.py: line 13

   Q2 (20'). 当前代码在每个 epoch 开始时使用 epoch 值作为随机数种子，请说明含义，并实现另一种方式以达到相同的目的

   Q3 (10'). 试分析 VFL-LR 训练流程中潜在的隐私泄露风险，并简要说明可能的保护方式

## 3. 实验结果提交

- **三份文件：补全后的 active.py, passive.py 以及实验报告，以压缩包的形式提交**
- 实验报告中说明代码实现方法，简要给出实验结果说明

