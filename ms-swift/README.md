swift微调方法
1.    数据集格式更改
2.   /data/liujiqiang/ms-swift/swift/llm/utils/model.py     修改要微调的模型路径
3.  CUDA_VISIBLE_DEVICES=0 swift sft \
    --model_type  模型
    --model_id_or_path qwen/Qwen-7B-Chat 模型路径\
    --dataset chatml.jsonl \
    --output_dir output \

如果出现缺少config 使用swift export --ckpt_dir /data/liujiqiang/ms-swift/CHIPoutput/glm4-9b/v1-20241102-151644/checkpoint-200 --merge_lora true
