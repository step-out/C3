# Evaluation Script Usage Guide

This document explains how to use the unified `evaluate.py` script that combines both Chinese and English evaluation functionalities.

## Overview

The `evaluate.py` script is a unified evaluation tool that can evaluate speech dialogue models on both Chinese and English datasets. It uses prompts from `prompts.json` for consistent evaluation across languages.

## Prerequisites

1. Install required dependencies:
```bash
pip install openai
```

2. Set up environment variables:
```bash
export OPENAI_BASE_URL="your_base_url"
export OPENAI_API_KEY="your_api_key"
```

3. Ensure `prompts.json` is in the same directory as `evaluate.py`

## Command Line Usage

### Basic Syntax
```bash
python evaluate.py \
    --sdm MODEL_NAME \
    --language LANGUAGE \
    --reference_path REF_PATH \
    --answer_path ANSWER_PATH \
    --result_path RESULT_PATH \
    --model_name EVAL_MODEL
```

### Parameters

- `--sdm`: Name of the SDM model being evaluated
- `--language`: Language to evaluate - either `english` or `chinese`
- `--reference_path`: Path to text of reference answers and questions from the [C3 dataset](https://huggingface.co/datasets/ChengqianMa/C3)
- `--answer_path`: Path to model text responses
- `--result_path`: Path to save evaluation results
- `--model_name`: LLM model name for evaluation

### Examples

#### English Evaluation (using gpt-4o)
```bash
python evaluate.py \
    --sdm "Mooer-Omni" \
    --language english \
    --reference_path "/C3/english/text" \
    --answer_path "/Mooer-Omni/english/txt" \
    --result_path "/Mooer-Omni/gpt-4o/english" \
    --model_name "gpt-4o"
```

#### Chinese Evaluation (using deepseek-r1-ls-z2)
```bash
python evaluate.py \
    --sdm "Mooer-Omni" \
    --language chinese \
    --reference_path "/C3/chinese/text" \
    --answer_path "/Mooer-Omni/chinese/txt" \
    --result_path "/Mooer-Omni/deepseek-r1-ls-z2/chinese" \
    --model_name "deepseek-r1-ls-z2"
```

## Output

The script will create evaluation results in the specified `result_path` with the same directory structure as the `reference_path`, but with JSON files containing evaluation results.

The result JSON file may contain:
- `content/problem`: The question
- `annotation/notation/correct_answer`: The reference answer
- `answer`: The model's answer
- `check_answer`: The evaluation result from the LLM

### Multiple Evaluators

To evaluate with multiple LLM models, run `evaluate.py` multiple times with different `model_name` values and `result_path`. This will create separate directories for each evaluator:

```
result_path/
├── result_deepseek_r1_ls_z2/
│   ├── english/
│   └── chinese/
└── result_gpt-4o/
    ├── english/
    └── chinese/
```

These separate evaluator directories are then combined by `process_results.py` using the `--deepseek_path` and `--gpt_path` parameters to calculate final metrics.

## Notes

- The script automatically creates output directories if they don't exist