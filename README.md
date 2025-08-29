> **Language**: 中文 / English  
> **Task**: 典型病历诊断一致性评测（Typical EMR Diagnosis-Consistency Evaluation）  
> **Rank**: 🥈 2nd Place (Public LB & Private LB)  
> **Method**: Dataset Optimization + LoRA + SWIFT + CoT + ICL + LoRA+  

---

## 技术邀稿
该**Rank 2**方案论文
**Utilizing Large Language Models Enhanced by Chain-of-Thought for the Diagnosis of Typical Medical Cases**
已发表至[10th China Health Information Processing Conference, CHIP 2024](https://link.springer.com/chapter/10.1007/978-981-96-4298-4_16)

由于主办方没有在天池平台公布隐藏B榜测试集分数及最终排名，在此进行澄清：
![Final Rank](https://github.com/liuliAI/Tianchi-CHIP2024-Silver-Medal-Solution-for-the-Typical-Case-Diagnostic-Consistency-Task-Competition/blob/main/rank.jpg)
![Final Rank](https://github.com/liuliAI/Tianchi-CHIP2024-Silver-Medal-Solution-for-the-Typical-Case-Diagnostic-Consistency-Task-Competition/blob/main/Evidence_1.jpg)
![Final Rank](https://github.com/liuliAI/Tianchi-CHIP2024-Silver-Medal-Solution-for-the-Typical-Case-Diagnostic-Consistency-Task-Competition/blob/main/Evidence_2.jpg)

## 1. 赛题回顾
- **目标**：根据病历文本（text），在选项（options）中选出与医生诊断一致的单项或多项答案（answer_idx）。
- **数据规模**：
  - 训练集 2 591 条  
  - 测试集 648 条
- **评价指标**：Micro Precision / Recall / F1

---

## 2. 方案框架
![Framework](https://github.com/liuliAI/Tianchi-CHIP2024-Silver-Medal-Solution-for-the-Typical-Case-Diagnostic-Consistency-Task-Competition/blob/main/Framework.jpg)

---

## 3. 方案亮点
| 模块 | 关键技术 | 亮点简述 |
|------|----------|----------|
| **规则** | 选项个数 → 题型判断 | 选项 ≤ 6 → 单选；≥ 7 → 多选 |
| **微调** | LoRA + LoRA+ | 仅训练 0.12 % 参数，显存 < 14 GB |
| **框架** | SWIFT (ModelScope) | 300+ LLM 支持，一键训练/推理/量化 |
| **Prompt** | Zero-Shot-CoT + ICL | 逐步推理 + 1-shot 示例，提升可解释性 |
---

## 4. 依赖环境

```bash
# 建议使用 conda
conda create -n cma python=3.10
conda activate cma
pip install -r requirements.txt
```
运行一次数据观察脚本，自动生成统计图表：
```bash
python src/train_observe.py --input data/cma_yidu_disease_diagnosis_train_v2.jsonl
```
输出：

stats.csv 选项长度分布

plot_*.png 可视化图表


## 5. 训练

```bash
CUDA_VISIBLE_DEVICES=0 swift sft \
    --model_type  glm4-9b
    --model_id_or_path glm/glm4-9b \
    --dataset CHIPoutput/test1.jsonl \
    --output_dir CHIPoutput \
    --merge_lora true
```

## 6. 推理
```bash
CUDA_VISIBLE_DEVICES=0 python glm4_infer.py
```