# TikZ Generator (LoRA 版)

本项目基于 Qwen2.5-VL（Qwen2_5_VLForConditionalGeneration）与自定义的修复/编译流水线，实现从图片自动生成并递归修复 LaTeX（TikZ）代码，可选启用 LoRA 权重进行推理。支持 YAML 变量替换 与 双输出目录（LoRA / Base），并在运行时自动落盘详细的配置与环境日志，便于复现实验。

--- 

## 功能概览
- 从图像与提示描述生成 TikZ 代码，失败时进行递归修复（util/repar_strategy.generate_and_repair）。
- 将生成的 LaTeX 编译为 PDF / PNG，并保存日志（util/save_and_complie.compile_and_save）。
- 可选启用 LoRA（需安装 peft），支持按需 merge and unload。
- 支持在 YAML 中用 ${var} 进行变量替换（如 ${checkpoint}）。
- 根据是否启用 LoRA，自动切换输出目录组（outputs_lora 或 outputs_base）。
- 运行前/后自动打印与保存 运行配置总览（log/run_config.json、log/run_summary.txt）。

--- 

## 环境准备

### 1.	创建并激活虚拟环境

```
conda create -n svgenv python=3.10 -y
conda activate svgenv
```
### 2.	安装依赖
```
pip install torch transformers pillow tqdm pyyaml
# 需要编译/渲染 TikZ（建议）
pip install automatikz
# 启用 LoRA 时需要
pip install peft
```

**说明**
- automatikz 提供 TikzDocument / 编译能力（你本地也可换其他编译方案）。
- 启用 LoRA 时务必安装 peft，否则程序会报错并退出。

--- 

## 项目结构（示例）

.
├── yaml/
│   └── lora_model.yaml          # 推荐的配置文件路径（示例）
├── generate_lora.py             # 主运行脚本（包含 LoRA / 变量替换 / 日志等）
├── util/
│   ├── repair_strategy.py       # generate_and_repair
│   └── save_and_complie.py      # compile_and_save（注意文件名是 complie）
├── eval_dataset/                # 示例数据根目录（见 YAML 中 data.base_dir）
│   ├── test_metadata.json
│   └── ...                      # 实际图片等
└── output/                      # 运行输出（按配置自动创建）

如果你把配置或脚本放在不同路径，注意同步更新 README 与命令。

--- 

## 配置文件说明（支持变量替换）

示例：yaml/lora_model.yaml

```
# 顶层定义变量（可被 ${var} 引用）
checkpoint: 40
model_name: Qwen2.5-VL-7B-Instruct
lora_task_id: lora_exp2_checkpoint

# 模型与设备
model:
  model_path: /mnt/data/model/Qwen2.5-VL-7B-Instruct
  device: cuda                  # cuda / cpu / auto
  dtype: auto                   # auto / bf16 / fp16 / fp32
  enable_lora: True             # 启用 LoRA
  lora_path: /home/yuwenhan/LLaMA-Factory/saves/Qwen2.5-VL-7B-Instruct/lora/train_2025-09-06-16-37-47/checkpoint-${checkpoint}
  lora_merge: False             # True 将 LoRA 合并进基座权重（仅推理更便捷，后续不可再训练 LoRA）

# 数据集位置
data:
  metadata_path: ../eval_dataset/test_metadata.json
  base_dir: ../eval_dataset

# 生成参数
gen:
  do_sample: true
  temperature: 0.8
  max_new_tokens: 2048
  top_p: 0.9

# 运行控制
run:
  max_attempts: 5
  limit: null                   # null 处理全部；或设为整数（仅处理前 N 条）

# 启用 LoRA 时的输出目录（会自动用到 ${lora_task_id} 与 ${checkpoint}）
outputs_lora:
  json_dir: output/lora/${lora_task_id}${checkpoint}/original-output
  tex_dir:  output/lora/${lora_task_id}${checkpoint}/output-tex
  pdf_dir:  output/lora/${lora_task_id}${checkpoint}/pdf
  png_dir:  output/lora/${lora_task_id}${checkpoint}/png
  log_dir:  output/lora/${lora_task_id}${checkpoint}/log

# 不启用 LoRA 时的输出目录
outputs_base:
  json_dir: output/base/${model_name}/original-output
  tex_dir:  output/base/${model_name}/output-tex
  pdf_dir:  output/base/${model_name}/pdf
  png_dir:  output/base/${model_name}/png
  log_dir:  output/base/${model_name}/log

# 运行日志总目录（保存 run_config.json / run_summary.txt）
output_log:
  log_dir : log/

变量替换规则
- 顶层所有标量（str/int/float/bool）都会被加入变量表，可在任意字符串中使用 ${var}。
- 预置同义变量：checkpoint 与 ckpt 等价。
- 解析顺序：载入 YAML 后会先做一轮替换；随后在默认值与路径补全后，再做一次全局替换。未知变量会原样保留（不报错）。

dtype 取值
- auto / bf16(bfloat16) / fp16(float16, half) / fp32(float32)；也兼容直接给 torch.dtype。
```

--- 

## 运行方法

推荐方式（项目根目录执行）：

```
python -m test.generate_lora
``` 

保存log
```
nohup python -m test.generate_lora > log/output.log 2>&1 &
```

脚本默认读取：
```
main("yaml/lora_model.yaml")
```
如需指定其他配置文件，修改最后一行或把它改成：
```
# main("path/to/your_config.yaml")
```

也可以用模块方式运行（按你的包结构自行调整）。关键是确保 util 能被正常导入。

--- 

## 输出与日志
- 若 model.enable_lora=True，使用 outputs_lora 目录组；否则使用 outputs_base。
- 每个样本会输出：
- *.json：生成结果与关键信息（如 attempts、dtype、device、lora_path、lora_merged 等）
- *.tex：最终 LaTeX（TikZ）代码
- *.pdf / *.png：编译后的可视化结果
- *.log：编译日志
- 运行配置与环境摘要会保存到：
- log/run_config.json
- log/run_summary.txt

**控制台也会打印运行配置总览与样本处理进度，例如：**
- 载入模型/LoRA 成功与否、设备信息、实际 torch_dtype
- 每个样本的尝试次数、是否编译成功、各类输出路径
- 最后给出跳过的样本索引列表

--- 

## 数据集要求

data.metadata_path 指向形如：

```
[
  { "image_path": "rel/path/to/img1.png",
    "caption": "（可选）文字描述",
    "code": "（可选）参考 TikZ 代码"
  },
  ...
]
```

- 程序会从 data.base_dir 与 image_path 拼出图片绝对路径并读取。
- 不存在或读失败的图片会被跳过并在控制台给出告警。

--- 

## 常见用法与小贴士
- 只用基座模型（不启用 LoRA）：把 enable_lora 设为 False 即可，输出将写入 outputs_base 路径组。
- LoRA 合并：将 lora_merge 设为 True，脚本会在加载适配器后执行 merge_and_unload()，适合仅推理部署。
- 性能建议：run.max_attempts 过大可能显著拉长生成时长；gen.max_new_tokens 与 temperature/top_p 可按任务难度与质量需求调整。
- GPU 信息：脚本会在日志中记录 CUDA 可用性、设备名与算力；若无 GPU，会自动标注 cuda_available=False。
- 异常处理：模型/LoRA 加载失败、元数据读取失败、图片缺失等都会给出明确报错/告警并尽量不中断其他样本处理。

--- 
