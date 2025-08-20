import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import json
from swift.llm import (
    get_model_tokenizer, get_template, inference, ModelType, get_default_template_type
)
from swift.tuners import Swift
ckpt_dir = '/data/liujiqiang/ms-swift/CHIPoutput/glm4-9b/v1-20241102-151644/checkpoint-150-merged'
model_type = ModelType.glm4_9b
template_type = get_default_template_type(model_type)

model, tokenizer = get_model_tokenizer(model_type, model_kwargs={'device_map': 'auto'},model_id_or_path=ckpt_dir)
model = Swift.from_pretrained(model, ckpt_dir, inference_mode=True)
template = get_template(template_type, tokenizer)


i_file = '/data/liujiqiang/CHIP/cma_yidu_disease_diagnosis_test_v2_wo_answer.jsonl'
options_dict = {}
with open(i_file, 'r', encoding='utf-8') as i_file:
    for line in i_file:
        content2 = json.loads(line)
        i_d = content2['id']
        options_dict[i_d] = content2['options']


def load_options(path: str) -> Dict[str, List[str]]:
    options_map: Dict[str, List[str]] = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            js = json.loads(line)
            options_map[js["id"]] = js.get("options", [])
    return options_map

TEST_WO_ANS = "/data/liujiqiang/CHIP/cma_yidu_disease_diagnosis_test_v2_wo_answer.jsonl"
INPUT_FILE = "/data/liujiqiang/CHIP/webcrawl_f2.jsonl"
OUTPUT_FILE = "/data/liujiqiang/CHIP/submit_glm_sft2.jsonl"
options_dict = load_options(TEST_WO_ANS)

PROMPT_TPL = (
    "你是一名专业实习医生，请根据以下诊断结果完成{task}。\n"
    "诊断结果：{diagnosis}\n"
    "候选项：{options}\n"
    "注意：答案必须从给定候选项中选择，请逐步思考并给出最终答案。\n"
)


def build_prompt(diagnosis: str, options: List[str]) -> str:
    task = "单项选择题" if len(options) <= 6 else "多项选择题"
    return PROMPT_TPL.format(task=task, diagnosis=diagnosis, options=options)


with open(INPUT_FILE, "r", encoding="utf-8") as fin, \
        open(OUTPUT_FILE, "w", encoding="utf-8") as fout:

    for idx, line in enumerate(fin, 1):
        line = line.strip()
        if not line:
            continue

        try:
            js = json.loads(line)
            i_id = js["id"]
            diagnosis = js["Diagnostic_results"]
            options = options_dict.get(i_id, [])
            if not options:
                print(f"第 {idx} 行未找到选项，跳过")
                continue

            prompt = build_prompt(diagnosis, options)
            answer, _ = inference(model, template, prompt)

            fout.write(json.dumps(
                {"id": i_id, "answer_idx": answer},
                ensure_ascii=False
            ) + "\n")
            print(f"{i_id} -> {answer}")

        except Exception as e:
            print(f"第 {idx} 行处理失败：{e}")
            continue