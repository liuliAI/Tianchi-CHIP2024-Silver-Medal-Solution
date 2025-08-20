import json
import matplotlib.pyplot as plt

# 设置matplotlib的字体为支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用的字体
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

input_file_path = 'cma_yidu_disease_diagnosis_train_v2.jsonl'  # 确保这是正确的文件路径

single_choice_counts = {}
multi_choice_counts = {}

with open(input_file_path, 'r', encoding='utf-8') as input_file:
    for line in input_file:
        content = json.loads(line)
        options = content['options']
        type = content['question_type']

        # 记录选项长度及其数量
        if type == '单选题':
            option_length = len(options)
            single_choice_counts[option_length] = single_choice_counts.get(option_length, 0) + 1
        elif type == '多选题':
            option_length = len(options)
            multi_choice_counts[option_length] = multi_choice_counts.get(option_length, 0) + 1

# 打印单选题的表格
print("题目类型")
print("单选题")
print("选项个数\t数量")
for length, count in sorted(single_choice_counts.items()):
    print(f"{length}\t{count}")

# 打印多选题的表格
print("\n题目类型")
print("多选题")
print("选项个数\t数量")
for length, count in sorted(multi_choice_counts.items()):
    print(f"{length}\t{count}")


options_lengths = []
types = []

with open(input_file_path, 'r', encoding='utf-8') as input_file:
    for line in input_file:
        content = json.loads(line)
        options = content['options']
        type = content['question_type']

        options_lengths.append(len(options))
        types.append(type)

plt.figure(figsize=(10, 6))
plt.scatter(options_lengths, types, alpha=0.5)
plt.title('关系图：选项个数与题目类型')
plt.xlabel('选项个数')
plt.ylabel('题目类型')
plt.grid(True)
plt.show()

