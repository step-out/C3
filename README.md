# 👉🏻 C<sup>3</sup> Benchmark 👈🏻

🌐 <a href="https://step-out.github.io/C3-web" target="_blank">Website</a>  •  🤗 <a href="https://huggingface.co/datasets/ChengqianMa/C3" target="_blank">Hugging Face</a>  •  📃 <a href="http://arxiv.org/abs/" target="_blank">arXiv Paper</a> 

## ✨ Key Features

* 🌍 **Bilingual Coverage**: Comprehensive evaluation in both English and Chinese.

* 🎯 **Real-world Complexity**: Based on empirical analysis of actual spoken dialogues, covering 1,079 instances with 1,586 audio-text paired samples.

* 💪 **LLM-based Automatic Evaluation**: Reliable evaluation with >0.87 correlation to human judgments using GPT-4o and DeepSeek-R1. See [prompts.md](prompts.md) for evaluation prompts.
* 🎵 **End-to-End Focus**: Specifically designed for end-to-end spoken dialogue models, considering crucial phonological features.

* 📊 **Challenging Benchmark**(as of 29 July 2025): Comprehensive evaluation of 10 leading SDMs reveals the benchmark’s difficulty. Top scores reach only 40.08 % (Chinese) and 55.68 % (English).

## 🚀 Usage

> [!Important]
> 🔥 **Limited Time Offer!** Free SDM evaluation on our benchmark until September 1, 2025. Email chengqianma@yeah.net with subject: `[C3Bench Evaluation] - [Model_Name]`

1. **Prepare Data**: 
   - Download the [C3 dataset](https://huggingface.co/datasets/ChengqianMa/C3) to `reference_path`
   - Organize your SDM responses in `answer_path` with the structure as the [ResponseStructure](ResponseStructure.md)

2. **Run Evaluation**:
   - Use `evaluate.py` for automatic evaluation (see [EvaluationUsage.md](EvaluationUsage.md))

3. **Calculate Accuracy**:
   - **Annotate**: Manually annotate generation tasks in JSON files
   - **Calculate**: Use `process_results.py` to generate final accuracy metrics automatically, see [CalculationUsage.md](CalculationUsage.md) for detailed workflow

4. **Submit Results**:
   - Send JSON files from step 3 to chengqianma@yeah.net for [Leaderboard](https://step-out.github.io/C3-web) inclusion with subject `[C3Bench Submission] - [Model_Name]`

## 📖 Citation

If you find [C3Bench](https://github.com/step-out/C3Bench) useful for your research and applications, feel free to give us a star ⭐ or cite us using:

```bibtex
@inproceedings{c3bench,
  title={C3: A Bilingual Benchmark for Spoken Dialogue Models Exploring Challenges in Complex Conversations},
  author={Ma, Chengqian and Tao, Wei and Guo, Yiwen},
  booktitle={arXiv Preprint},
  year={2025},
}
```
