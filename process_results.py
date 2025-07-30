"""
Unified script to process evaluation results from evaluate.py
This script handles the post-evaluation workflow:
1. Combining results from multiple evaluators (deepseek-r1-ls-z2 and gpt-4o)
2. Calculating final accuracy metrics

Note: Manual annotation should be completed before running this script.
See AccuracyCalculation.md for manual annotation instructions.
"""

import json
import os
import argparse
from pathlib import Path

def combine_results(deepseek_path, gpt_path, language, output_file):
    """
    Combine results from multiple evaluators (deepseek-r1-ls-z2 and gpt-4o)
    """
    print(f"Combining {language} results...")
    
    # Define evaluator paths
    evaluators = {
        "dpsk": deepseek_path,
        "gpt": gpt_path
    }
    
    combined_results = []
    
    # Process each evaluator's results
    for evaluator, folder in evaluators.items():
        if not os.path.exists(folder):
            print(f"Warning: {folder} not found, skipping...")
            continue
            
        for root, dirs, files in os.walk(folder):
            for file_name in files:
                if file_name.endswith(".json"):
                    file_path = os.path.join(root, file_name)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
                        continue
                    
                    # Extract data ID
                    data_id_base = file_path.replace(folder, "").replace(".json", "")
                    
                    # Process each item
                    for idx, item in enumerate(data):
                        data_id = f"{data_id_base}/{idx}"
                        
                        # Extract evaluation result
                        check_answer = item.get("check_answer", "")
                        if language == "chinese":
                            check_result = "right" if len(check_answer.split("最终答案为：")) > 1 and \
                                 check_answer.split("最终答案为：")[-1].startswith("是") else "wrong"
                        else:  # english
                            if (
                                (
                                    len(check_answer.split("the answer is: ")) > 1 and \
                                    check_answer.split("the answer is: ")[-1].startswith(("Yes", "yes"))
                                )
                                or
                                (
                                    len(check_answer.split("The answer is: ")) > 1 and \
                                    check_answer.split("The answer is: ")[-1].startswith(("Yes", "yes"))
                                )
                            ):
                                check_result = "right"
                            else:
                                check_result = "wrong"
                        
                        # Find or create existing item
                        existing_item = next((x for x in combined_results if x["data_id"] == data_id), None)
                        if existing_item:
                            existing_item[evaluator] = check_result
                        else:
                            combined_results.append({
                                "data_id": data_id,
                                evaluator: check_result
                            })
    
    # Save combined results
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(combined_results, f, indent=4, ensure_ascii=False)
    
    print(f"Combined results saved to: {output_file}")
    return output_file

def calculate_metrics(combined_file, output_file):
    """
    Calculate final accuracy metrics from combined results
    """
    print(f"Calculating metrics from {combined_file}...")
    
    try:
        with open(combined_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {combined_file}: {e}")
        return
    
    # Initialize metrics
    metrics = []
    overall_metrics = {
        "category": "overall",
        "dpsk_correct": 0,
        "gpt_correct": 0,
        "total": 0
    }
    metrics.append(overall_metrics)
    
    # Process each item
    for item in data:
        
        # Extract category
        category = item["data_id"].rsplit('/', 1)[0]
        
        # Count correct answers
        dpsk_correct = 1 if item.get('dpsk') == 'right' else 0
        gpt_correct = 1 if item.get('gpt') == 'right' else 0
        
        # Update overall metrics
        metrics[0]["dpsk_correct"] += dpsk_correct
        metrics[0]["gpt_correct"] += gpt_correct
        metrics[0]["total"] += 1
        
        # Find or create category metrics
        existing_category = next((x for x in metrics if x["category"] == category), None)
        if existing_category:
            existing_category["dpsk_correct"] += dpsk_correct
            existing_category["gpt_correct"] += gpt_correct
            existing_category["total"] += 1
        else:
            metrics.append({
                "category": category,
                "dpsk_correct": dpsk_correct,
                "gpt_correct": gpt_correct,
                "total": 1
            })
    
    # Calculate accuracy for each category
    for item in metrics:
        if item["total"] > 0:
            item["dpsk_accuracy"] = round(item["dpsk_correct"] / item["total"], 4)
            item["gpt_accuracy"] = round(item["gpt_correct"] / item["total"], 4)
        else:
            item["dpsk_accuracy"] = 0.0
            item["gpt_accuracy"] = 0.0
    
    # Save metrics
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4, ensure_ascii=False)
    
    print(f"Metrics saved to: {output_file}")
    
    # Print summary
    print(f"\n{'='*40}")
    print("SUMMARY")
    print(f"{'='*40}")
    for item in metrics:
        if item["category"] == "overall":
            print(f"Overall Accuracy:")
            print(f"  DeepSeek: {item['dpsk_accuracy']:.2%} ({item['dpsk_correct']}/{item['total']})")
            print(f"  GPT-4o:   {item['gpt_accuracy']:.2%} ({item['gpt_correct']}/{item['total']})")
            break

def main():
    parser = argparse.ArgumentParser(description="Process evaluation results from evaluate.py")
    parser.add_argument("--language", type=str, choices=["english", "chinese"], required=True,
                       help="Language of the evaluation results")
    parser.add_argument("--sdm_name", type=str, required=True,
                       help="Name of the SDM model")
    parser.add_argument("--output_path", type=str, default="baseline",
                       help="Base path for output files (default: baseline)")
    parser.add_argument("--deepseek_path", type=str, required=True,
                       help="Path to DeepSeek evaluation results (e.g., /path/to/deepseek-r1-ls-z2/english)")
    parser.add_argument("--gpt_path", type=str, required=True,
                       help="Path to GPT evaluation results (e.g., /path/to/gpt-4o/english)")
    
    args = parser.parse_args()
    
    # Set output paths
    base_path = f"{args.output_path}"
    combined_file = f"{base_path}/combined_{args.language}_statistic.json"
    metrics_file = f"{base_path}/{args.language}_result_data.json"
    
    print(f"Processing {args.language} results for {args.sdm_name}...")
    print(f"DeepSeek path: {args.deepseek_path}")
    print(f"GPT path: {args.gpt_path}")
    print(f"Output base path: {base_path}")
    
    # Combine results
    combined_file = combine_results(args.deepseek_path, args.gpt_path, args.language, combined_file)
    
    # Calculate metrics
    calculate_metrics(combined_file, metrics_file)
    
    print(f"\n✅ Processing completed successfully!")
    print(f"📊 Final metrics: {metrics_file}")

if __name__ == "__main__":
    main() 