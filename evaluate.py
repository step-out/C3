import os
import json
import argparse
import time
from openai import OpenAI

# Configuration
MODEL_NAME = "your-LLM-name"
MAX_TRY_N = 5
TIME_SLEEP = 5
base_url = os.environ.get('OPENAI_BASE_URL', 'your_base_url')
api_key = os.environ.get('OPENAI_API_KEY', 'your_api_key') 
client = OpenAI(base_url=base_url, api_key=api_key)

# Load prompts from JSON file
def load_prompts():
    with open('prompts.json', 'r', encoding='utf-8') as f:
        return json.load(f)

prompts = load_prompts()

def chat_with_llm(system_prompt, user_prompt, model_name=MODEL_NAME, max_try_n=MAX_TRY_N, time_sleep=TIME_SLEEP):
    cnt = 0
    while cnt < max_try_n:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"content": system_prompt, "role": "system"},
                    {"content": user_prompt, "role": "user"}
                ],
                stream=False,
                temperature=0,
                max_tokens=2048
            )
            return response
        except Exception as e:
            print(f"Attempt {cnt + 1} failed: {e}")
            cnt += 1
            if cnt < max_try_n:
                time.sleep(time_sleep)
    print(f"Failed after {max_try_n} attempts")
    return None

def get_output(input, language='english'):
    system_prompt = prompts['system_prompts'][language]
    user_prompt = input
    response = chat_with_llm(system_prompt, user_prompt)
    if response:
        return response.choices[0].message.content
    return ""

def print_progress(current, total, task_name):
    """Print progress bar for long-running tasks"""
    percentage = (current / total) * 100
    bar_length = 50
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\r{task_name}: |{bar}| {percentage:.1f}% ({current}/{total})', end='')
    if current == total:
        print()

# English evaluation functions
def ambiguity_phonological_generation_english(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "ambiguity", "phonological", "generation.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    answer_list = []
    files_to_answer_list = []
    folder_path_to_answer = os.path.join(path_to_answer_base, "ambiguity", "phonological", "generation")
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    for file_to_answer_list in files_to_answer_list:
        answer = open(file_to_answer_list).read()
        answer_list.append(answer)
    path_to_result = os.path.join(path_to_result_base, "ambiguity", "phonological", "generation.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    for data_pair, answer in zip(data_pairs, answer_list):
        content = data_pair["content"]
        notation = data_pair["notation"]
        result.append({"content": content, "notation": notation, "answer": answer, "check_answer": ""})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def ambiguity_phonological_heterograph_english(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "ambiguity", "phonological", "heterograph.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    folder_path_to_answer = os.path.join(path_to_answer_base, "ambiguity", "phonological", "heterograph")
    files_to_answer_list = []
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    path_to_result = os.path.join(path_to_result_base, "ambiguity", "phonological", "heterograph.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    for data_pair, file_to_answer_list in zip(data_pairs, files_to_answer_list):
        content = data_pair["content"]
        notation = data_pair["notation"]
        problem = data_pair["problem"]
        answer = open(file_to_answer_list).read()
        prompt = prompts['evaluation_prompts']['english']['ambiguity_phonological_heterograph'].format(
            content=content, problem=problem, notation=notation, answer=answer
        )
        check_answer = get_output(prompt, 'english')
        result.append({"content": content, "notation": notation, "problem": problem, "answer": answer, "check_answer": check_answer})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def ambiguity_phonological_pause_english(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "ambiguity", "phonological", "pause.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    folder_path_to_answer = os.path.join(path_to_answer_base, "ambiguity", "phonological", "pause")
    files_to_answer_list = []
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    path_to_result = os.path.join(path_to_result_base, "ambiguity", "phonological", "pause.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    for data_pair, file_to_answer_list in zip(data_pairs, files_to_answer_list):
        content = data_pair["content"]
        notation = data_pair["notation"]
        answer = open(file_to_answer_list).read()
        prompt = prompts['evaluation_prompts']['english']['ambiguity_phonological_pause'].format(
            content=content, notation=notation, answer=answer
        )
        check_answer = get_output(prompt, 'english')
        result.append({"content": content, "notation": notation, "answer": answer, "check_answer": check_answer})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def ambiguity_phonological_stress_english(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "ambiguity", "phonological", "stress.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    folder_path_to_answer = os.path.join(path_to_answer_base, "ambiguity", "phonological", "stress")
    files_to_answer_list = []
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    path_to_result = os.path.join(path_to_result_base, "ambiguity", "phonological", "stress.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    for data_pair, file_to_answer_list in zip(data_pairs, files_to_answer_list):
        content = data_pair["content"]
        notation = data_pair["notation"]
        answer = open(file_to_answer_list).read()
        prompt = prompts['evaluation_prompts']['english']['ambiguity_phonological_stress'].format(
            content=content, notation=notation, answer=answer
        )
        check_answer = get_output(prompt, 'english')
        result.append({"content": content, "notation": notation, "answer": answer, "check_answer": check_answer})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def ambiguity_phonological_intonation_english(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "ambiguity", "phonological", "intonation.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    folder_path_to_answer = os.path.join(path_to_answer_base, "ambiguity", "phonological", "intonation")
    files_to_answer_list = []
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    path_to_result = os.path.join(path_to_result_base, "ambiguity", "phonological", "intonation.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    for data_pair, file_to_answer_list in zip(data_pairs, files_to_answer_list):
        content = data_pair["content"]
        notation = data_pair["notation"]
        answer = open(file_to_answer_list).read()
        prompt = prompts['evaluation_prompts']['english']['ambiguity_phonological_intonation'].format(
            content=content, notation=notation, answer=answer
        )
        check_answer = get_output(prompt, 'english')
        result.append({"content": content, "notation": notation, "answer": answer, "check_answer": check_answer})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def ambiguity_semantic_lexical_english(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "ambiguity", "semantic", "lexical.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    folder_path_to_answer = os.path.join(path_to_answer_base, "ambiguity", "semantic", "lexical")
    files_to_answer_list = []
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    path_to_result = os.path.join(path_to_result_base, "ambiguity", "semantic", "lexical.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    for data_pair, file_to_answer_list in zip(data_pairs, files_to_answer_list):
        content = data_pair["content"]
        notation = data_pair["notation"]
        answer = open(file_to_answer_list).read()
        prompt = prompts['evaluation_prompts']['english']['ambiguity_semantic_lexical'].format(
            content=content, notation=notation, answer=answer
        )
        check_answer = get_output(prompt, 'english')
        result.append({"content": content, "notation": notation, "answer": answer, "check_answer": check_answer})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def ambiguity_semantic_syntactic_english(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "ambiguity", "semantic", "syntactic.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    folder_path_to_answer = os.path.join(path_to_answer_base, "ambiguity", "semantic", "syntactic")
    files_to_answer_list = []
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    path_to_result = os.path.join(path_to_result_base, "ambiguity", "semantic", "syntactic.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    for data_pair, file_to_answer_list in zip(data_pairs, files_to_answer_list):
        content = data_pair["content"]
        notation = data_pair["notation"]
        answer = open(file_to_answer_list).read()
        
        # Format interpretations for the prompt
        interpretations = ""
        for i in range(len(notation["interpretations"])):
            interpretations += f"\nThe {str(i + 1)} meaning of this sentence is:\n```\n{notation['interpretations'][i]}\n```"
        
        prompt = prompts['evaluation_prompts']['english']['ambiguity_semantic_syntactic'].format(
            content=content, ambiguity=notation['ambiguity'], interpretations=interpretations, answer=answer
        )
        check_answer = get_output(prompt, 'english')
        result.append({"content": content, "notation": notation, "answer": answer, "check_answer": check_answer})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

# Chinese evaluation functions
def ambiguity_phonological_generation_pause_chinese(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "ambiguity", "phonological", "generation", "pause.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    path_to_result = os.path.join(path_to_result_base, "ambiguity", "phonological", "generation", "pause.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    for data_pair in data_pairs:
        content = data_pair["content"]
        annotation = data_pair["annotation"]
        answer = data_pair["answer"]
        result.append({"content": content, "annotation": annotation, "answer": answer, "check_answer": ""})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def ambiguity_phonological_generation_heteronym_chinese(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "ambiguity", "phonological", "generation", "heteronym.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    path_to_result = os.path.join(path_to_result_base, "ambiguity", "phonological", "generation", "heteronym.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    for data_pair in data_pairs:
        content = data_pair["content"]
        annotation = data_pair["annotation"]
        answer = data_pair["answer"]
        result.append({"content": content, "annotation": annotation, "answer": answer, "check_answer": ""})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def ambiguity_phonological_generation_tone_chinese(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "ambiguity", "phonological", "generation", "tone.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    path_to_result = os.path.join(path_to_result_base, "ambiguity", "phonological", "generation", "tone.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    for data_pair in data_pairs:
        content = data_pair["content"]
        annotation = data_pair["annotation"]
        result.append({"content": content, "annotation": annotation, "check_answer": ""})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def ambiguity_phonological_pause_chinese(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "ambiguity", "phonological", "pause.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    folder_path_to_answer = os.path.join(path_to_answer_base, "ambiguity", "phonological", "pause")
    path_to_result = os.path.join(path_to_result_base, "ambiguity", "phonological", "pause.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    files_to_answer_list = []
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    for data_pair, file_to_answer_list in zip(data_pairs, files_to_answer_list):
        content = data_pair["content"]
        annotation = data_pair["annotation"]
        answer = open(file_to_answer_list).read()
        prompt = prompts['evaluation_prompts']['chinese']['ambiguity_phonological'].format(
            content=content, annotation=annotation, answer=answer
        )
        check_answer = get_output(prompt, 'chinese')
        result.append({"content": content, "annotation": annotation, "answer": answer, "check_answer": check_answer})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def ambiguity_phonological_heteronym_chinese(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "ambiguity", "phonological", "heteronym.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    folder_path_to_answer = os.path.join(path_to_answer_base, "ambiguity", "phonological", "heteronym")
    path_to_result = os.path.join(path_to_result_base, "ambiguity", "phonological", "heteronym.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    files_to_answer_list = []
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    for data_pair, file_to_answer_list in zip(data_pairs, files_to_answer_list):
        content = data_pair["content"]
        annotation = data_pair["annotation"]
        answer = open(file_to_answer_list).read()
        prompt = prompts['evaluation_prompts']['chinese']['ambiguity_phonological'].format(
            content=content, annotation=annotation, answer=answer
        )
        check_answer = get_output(prompt, 'chinese')
        result.append({"content": content, "annotation": annotation, "answer": answer, "check_answer": check_answer})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def ambiguity_phonological_heterograph_chinese(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "ambiguity", "phonological", "heterograph.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    folder_path_to_answer = os.path.join(path_to_answer_base, "ambiguity", "phonological", "heterograph")
    path_to_result = os.path.join(path_to_result_base, "ambiguity", "phonological", "heterograph.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    files_to_answer_list = []
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    for data_pair, file_to_answer_list in zip(data_pairs, files_to_answer_list):
        content = data_pair["content"]
        annotation = data_pair["annotation"]
        answer = open(file_to_answer_list).read()
        prompt = prompts['evaluation_prompts']['chinese']['ambiguity_phonological'].format(
            content=content, annotation=annotation, answer=answer
        )
        check_answer = get_output(prompt, 'chinese')
        result.append({"content": content, "annotation": annotation, "answer": answer, "check_answer": check_answer})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def ambiguity_phonological_tone_chinese(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "ambiguity", "phonological", "tone.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    folder_path_to_answer = os.path.join(path_to_answer_base, "ambiguity", "phonological", "tone")
    path_to_result = os.path.join(path_to_result_base, "ambiguity", "phonological", "tone.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    files_to_answer_list = []
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    for data_pair, file_to_answer_list in zip(data_pairs, files_to_answer_list):
        content = data_pair["content"]
        annotation = data_pair["annotation"]
        answer = open(file_to_answer_list).read()
        prompt = prompts['evaluation_prompts']['chinese']['ambiguity_phonological'].format(
            content=content, annotation=annotation, answer=answer
        )
        check_answer = get_output(prompt, 'chinese')
        result.append({"content": content, "annotation": annotation, "answer": answer, "check_answer": check_answer})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def ambiguity_semantic_chinese(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "ambiguity", "semantic.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    folder_path_to_answer = os.path.join(path_to_answer_base, "ambiguity", "semantic")
    path_to_result = os.path.join(path_to_result_base, "ambiguity", "semantic.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    files_to_answer_list = []
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    for data_pair, file_to_answer_list in zip(data_pairs, files_to_answer_list):
        content = data_pair["content"]
        annotation = data_pair["annotation"]
        answer = open(file_to_answer_list).read()
        prompt = prompts['evaluation_prompts']['chinese']['ambiguity_semantic'].format(
            content=content, annotation=annotation, answer=answer
        )
        check_answer = get_output(prompt, 'chinese')
        result.append({"content": content, "annotation": annotation, "answer": answer, "check_answer": check_answer})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

# Context dependency functions (both languages)
# English context dependency functions
def context_dependency_omission_detection_english(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "context-dependency", "omission.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    folder_path_to_answer = os.path.join(path_to_answer_base, "context-dependency", "omission-detection")
    files_to_answer_list = []
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    path_to_result = os.path.join(path_to_result_base, "context-dependency", "omission-detection.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    if os.path.exists(path_to_result):
        result = json.load(open(path_to_result))
    for data_pair, file_to_answer_list in zip(data_pairs, files_to_answer_list):
        content = data_pair["content"]
        notation = data_pair["notation"]
        answer = open(file_to_answer_list).read()
        if notation in [data["notation"] for data in result]:
            continue
        prompt = prompts['evaluation_prompts']['english']['context_dependency_omission_detection'].format(
            content=content, answer=answer
        )
        check_answer = get_output(prompt, 'english')
        result.append({"content": content, "notation": notation, "answer": answer, "check_answer": check_answer})
        json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def context_dependency_omission_completion_english(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "context-dependency", "omission.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    folder_path_to_answer = os.path.join(path_to_answer_base, "context-dependency", "omission-completion")
    files_to_answer_list = []
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    path_to_result = os.path.join(path_to_result_base, "context-dependency", "omission-completion.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    if os.path.exists(path_to_result):
        result = json.load(open(path_to_result))
    for data_pair, file_to_answer_list in zip(data_pairs, files_to_answer_list):
        content = data_pair["content"]
        notation = data_pair["notation"]
        answer = open(file_to_answer_list).read()
        if notation in [data["notation"] for data in result]:
            continue
        prompt = prompts['evaluation_prompts']['english']['context_dependency_omission_completion'].format(
            content=content, notation=notation, answer=answer
        )
        check_answer = get_output(prompt, 'english')
        result.append({"content": content, "notation": notation, "answer": answer, "check_answer": check_answer})
        json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def context_dependency_coreference_resolution_english(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "context-dependency", "coreference.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    folder_path_to_answer = os.path.join(path_to_answer_base, "context-dependency", "coreference-resolution")
    files_to_answer_list = []
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    path_to_result = os.path.join(path_to_result_base, "context-dependency", "coreference-resolution.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    for data_pair, file_to_answer_list in zip(data_pairs, files_to_answer_list):
        content = data_pair["content"]
        problem = data_pair["problem"]
        correct_answer = data_pair["answer"]
        answer = open(file_to_answer_list).read()
        prompt = prompts['evaluation_prompts']['english']['context_dependency_coreference_resolution'].format(
            content=content, problem=problem, correct_answer=correct_answer, answer=answer
        )
        check_answer = get_output(prompt, 'english')
        result.append({"content": content, "problem": problem, "correct_answer": correct_answer, "answer": answer, "check_answer": check_answer})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def context_dependency_coreference_detection_english(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "context-dependency", "coreference.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    folder_path_to_answer = os.path.join(path_to_answer_base, "context-dependency", "coreference-detection")
    files_to_answer_list = []
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    path_to_result = os.path.join(path_to_result_base, "context-dependency", "coreference-detection.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    for data_pair, file_to_answer_list in zip(data_pairs, files_to_answer_list):
        content = data_pair["content"]
        answer = open(file_to_answer_list).read()
        prompt = prompts['evaluation_prompts']['english']['context_dependency_coreference_detection'].format(
            content=content, answer=answer
        )
        check_answer = get_output(prompt, 'english')
        result.append({"content": content, "answer": answer, "check_answer": check_answer})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def context_dependency_multi_turn_english(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "context-dependency", "multi-turn.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    path_to_result = os.path.join(path_to_result_base, "context-dependency", "multi-turn.json")
    if not os.path.exists(path_to_result):
        open(path_to_result, "w").close()
    result = []
    if os.path.getsize(path_to_result) > 0:
        result = json.load(open(path_to_result))
    for i in range(len(data_pairs)):
        data_pair = data_pairs[i]
        if data_pair[0] in [data["annotation"] for data in result]:
            continue
        dialogue = []
        for j in range(len(data_pair)):
            dialogue.append(data_pair[j])
            dialogue.append(open(os.path.join(path_to_answer_base, "context-dependency", "multi-turn", str(i), str(j) + ".txt")).read())
        
        # Format dialogues for the prompt
        dialogues = ""
        for j in range(len(dialogue)):
            if j % 2 == 0:
                dialogues += f"\nA:\n```\n{dialogue[j]}\n```"
            else:
                dialogues += f"\nB:\n```\n{dialogue[j]}\n```"
        
        prompt = prompts['evaluation_prompts']['english']['context_dependency_multi_turn'].format(dialogues=dialogues)
        check_answer = get_output(prompt, 'english')
        result.append({"content": prompt, "annotation": data_pair[0], "check_answer": check_answer})
        json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

# Chinese context dependency functions
def context_dependency_omission_detection_chinese(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "context-dependency", "omission.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    folder_path_to_answer = os.path.join(path_to_answer_base, "context-dependency", "omission-detection")
    path_to_result = os.path.join(path_to_result_base, "context-dependency", "omission-detection.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    files_to_answer_list = []
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    for data_pair, file_to_answer_list in zip(data_pairs, files_to_answer_list):
        dialogue = data_pair["history"]
        answer = open(file_to_answer_list).read()
        dialogue_content = ""
        for i in range(len(dialogue)):
            dialogue_content += dialogue[i] + "\n"
        prompt = prompts['evaluation_prompts']['chinese']['context_dependency_omission_detection'].format(
            dialogue_content=dialogue_content, answer=answer
        )
        check_answer = get_output(prompt, 'chinese')
        result.append({"content": dialogue_content, "answer": answer, "check_answer": check_answer})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def context_dependency_omission_completion_chinese(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "context-dependency", "omission.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    folder_path_to_answer = os.path.join(path_to_answer_base, "context-dependency", "omission-completion")
    path_to_result = os.path.join(path_to_result_base, "context-dependency", "omission-completion.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    files_to_answer_list = []
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    for data_pair, file_to_answer_list in zip(data_pairs, files_to_answer_list):
        dialogue = data_pair["history"]
        omission_complete = data_pair["omission_complete"]
        answer = open(file_to_answer_list).read()
        dialogue_content = ""
        for i in range(len(dialogue)):
            dialogue_content += dialogue[i] + "\n"
        prompt = prompts['evaluation_prompts']['chinese']['context_dependency_omission_completion'].format(
            dialogue_content=dialogue_content, omission_complete=omission_complete, answer=answer
        )
        check_answer = get_output(prompt, 'chinese')
        result.append({"content": dialogue_content, "annotation": omission_complete, "answer": answer, "check_answer": check_answer})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def context_dependency_coreference_detection_chinese(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "context-dependency", "coreference.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    folder_path_to_answer = os.path.join(path_to_answer_base, "context-dependency", "coreference-detection")
    path_to_result = os.path.join(path_to_result_base, "context-dependency", "coreference-detection.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    files_to_answer_list = []
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    for data_pair, file_to_answer_list in zip(data_pairs, files_to_answer_list):
        dialogue = data_pair["history"]
        answer = open(file_to_answer_list).read()
        dialogue_content = ""
        for i in range(len(dialogue)):
            dialogue_content += dialogue[i] + "\n"
        prompt = prompts['evaluation_prompts']['chinese']['context_dependency_coreference_detection'].format(
            dialogue_content=dialogue_content, answer=answer
        )
        check_answer = get_output(prompt, 'chinese')
        result.append({"content": dialogue_content, "answer": answer, "check_answer": check_answer})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def context_dependency_coreference_resolution_chinese(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "context-dependency", "coreference.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    folder_path_to_answer = os.path.join(path_to_answer_base, "context-dependency", "coreference-resolution")
    path_to_result = os.path.join(path_to_result_base, "context-dependency", "coreference-resolution.json")
    os.makedirs(os.path.dirname(path_to_result), exist_ok=True)
    result = []
    files_to_answer_list = []
    for i in range(len(os.listdir(folder_path_to_answer))):
        files_to_answer_list.append(os.path.join(folder_path_to_answer, str(i) + ".txt"))
    for data_pair, file_to_answer_list in zip(data_pairs, files_to_answer_list):
        dialogue = data_pair["history"]
        coreference_complete = data_pair["coreference_complete"]
        answer = open(file_to_answer_list).read()
        dialogue_content = ""
        for i in range(len(dialogue)):
            dialogue_content += dialogue[i] + "\n"
        prompt = prompts['evaluation_prompts']['chinese']['context_dependency_coreference_resolution'].format(
            dialogue_content=dialogue_content, coreference_complete=coreference_complete, answer=answer
        )
        check_answer = get_output(prompt, 'chinese')
        result.append({"content": dialogue_content, "annotation": coreference_complete, "answer": answer, "check_answer": check_answer})
    json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def context_dependency_multi_turn_chinese(path_to_reference_answer_and_question_base, path_to_answer_base, path_to_result_base):
    path_to_reference_answer_and_question = os.path.join(path_to_reference_answer_and_question_base, "context-dependency", "multi-turn.json")
    data_pairs = json.load(open(path_to_reference_answer_and_question))
    path_to_result = os.path.join(path_to_result_base, "context-dependency", "multi-turn.json")
    if not os.path.exists(path_to_result):
        open(path_to_result, "w").close()
    result = []
    if os.path.getsize(path_to_result) > 0:
        result = json.load(open(path_to_result))
    for i in range(len(data_pairs)):
        data_pair = data_pairs[i]
        history = data_pair["history"]
        if history[0] in [data["annotation"] for data in result]:
            continue
        dialogues = []
        for j in range(len(history)):
            dialogues.append(history[j])
            dialogues.append(open(os.path.join(path_to_answer_base, "context-dependency", "multi-turn", str(i), str(j) + ".txt")).read())
        dialogues.append(data_pair['question'])
        dialogues.append(open(os.path.join(path_to_answer_base, "context-dependency", "multi-turn", str(i), str(len(history)) + ".txt")).read())
        
        # Format dialogues for the prompt
        dialogues_formatted = ""
        for j in range(len(dialogues)):
            if j % 2 == 0:
                dialogues_formatted += "\n甲说：\n"
            else:
                dialogues_formatted += "\n乙说：\n"
            dialogues_formatted += f"```\n{dialogues[j]}\n```"
        
        prompt = prompts['evaluation_prompts']['chinese']['context_dependency_multi_turn'].format(dialogues=dialogues_formatted)
        check_answer = get_output(prompt, 'chinese')
        result.append({"content": prompt, "annotation": history[0], "check_answer": check_answer})
        json.dump(result, open(path_to_result, "w"), ensure_ascii=False, indent=4)

def main():
    global MODEL_NAME
    parser = argparse.ArgumentParser(description='Evaluate speech dialogue models')
    parser.add_argument("--sdm", type=str, required=True, help="Name of the SDM model")
    parser.add_argument("--language", type=str, choices=['english', 'chinese'], required=True, help="Language to evaluate")
    parser.add_argument("--reference_path", type=str, required=True, help="Path to reference answers and questions")
    parser.add_argument("--answer_path", type=str, required=True, help="Path to model answers")
    parser.add_argument("--result_path", type=str, required=True, help="Path to save evaluation results")
    parser.add_argument("--model_name", type=str, default=MODEL_NAME, help="LLM model name for evaluation")
    
    args = parser.parse_args()
    
    # Update global model name if provided
    MODEL_NAME = args.model_name
    
    print(f"Starting evaluation for {args.language} language using {args.sdm} model")
    print(f"Reference path: {args.reference_path}")
    print(f"Answer path: {args.answer_path}")
    print(f"Result path: {args.result_path}")
    print(f"Evaluation model: {MODEL_NAME}")
    print("-" * 80)
    
    try:
        if args.language == 'english':
            print("Running English evaluation tasks...")
            # English evaluation
            print("1. Ambiguity - Phonological Generation")
            ambiguity_phonological_generation_english(args.reference_path, args.answer_path, args.result_path)
            
            print("2. Ambiguity - Phonological Heterograph")
            ambiguity_phonological_heterograph_english(args.reference_path, args.answer_path, args.result_path)
            
            print("3. Ambiguity - Phonological Pause")
            ambiguity_phonological_pause_english(args.reference_path, args.answer_path, args.result_path)
            
            print("4. Ambiguity - Phonological Stress")
            ambiguity_phonological_stress_english(args.reference_path, args.answer_path, args.result_path)
            
            print("5. Ambiguity - Phonological Intonation")
            ambiguity_phonological_intonation_english(args.reference_path, args.answer_path, args.result_path)
            
            print("6. Ambiguity - Semantic Lexical")
            ambiguity_semantic_lexical_english(args.reference_path, args.answer_path, args.result_path)
            
            print("7. Ambiguity - Semantic Syntactic")
            ambiguity_semantic_syntactic_english(args.reference_path, args.answer_path, args.result_path)
            
            print("8. Context Dependency - Omission Detection")
            context_dependency_omission_detection_english(args.reference_path, args.answer_path, args.result_path)
            
            print("9. Context Dependency - Omission Completion")
            context_dependency_omission_completion_english(args.reference_path, args.answer_path, args.result_path)
            
            print("10. Context Dependency - Coreference Resolution")
            context_dependency_coreference_resolution_english(args.reference_path, args.answer_path, args.result_path)
            
            print("11. Context Dependency - Coreference Detection")
            context_dependency_coreference_detection_english(args.reference_path, args.answer_path, args.result_path)
            
            print("12. Context Dependency - Multi-turn")
            context_dependency_multi_turn_english(args.reference_path, args.answer_path, args.result_path)
        
        elif args.language == 'chinese':
            print("Running Chinese evaluation tasks...")
            # Chinese evaluation
            print("1. Ambiguity - Phonological Generation Pause")
            ambiguity_phonological_generation_pause_chinese(args.reference_path, args.answer_path, args.result_path)
            
            print("2. Ambiguity - Phonological Generation Heteronym")
            ambiguity_phonological_generation_heteronym_chinese(args.reference_path, args.answer_path, args.result_path)
            
            print("3. Ambiguity - Phonological Generation Tone")
            ambiguity_phonological_generation_tone_chinese(args.reference_path, args.answer_path, args.result_path)
            
            print("4. Ambiguity - Phonological Pause")
            ambiguity_phonological_pause_chinese(args.reference_path, args.answer_path, args.result_path)
            
            print("5. Ambiguity - Phonological Heteronym")
            ambiguity_phonological_heteronym_chinese(args.reference_path, args.answer_path, args.result_path)
            
            print("6. Ambiguity - Phonological Heterograph")
            ambiguity_phonological_heterograph_chinese(args.reference_path, args.answer_path, args.result_path)
            
            print("7. Ambiguity - Phonological Tone")
            ambiguity_phonological_tone_chinese(args.reference_path, args.answer_path, args.result_path)
            
            print("8. Ambiguity - Semantic")
            ambiguity_semantic_chinese(args.reference_path, args.answer_path, args.result_path)
            
            print("9. Context Dependency - Omission Detection")
            context_dependency_omission_detection_chinese(args.reference_path, args.answer_path, args.result_path)
            
            print("10. Context Dependency - Omission Completion")
            context_dependency_omission_completion_chinese(args.reference_path, args.answer_path, args.result_path)
            
            print("11. Context Dependency - Coreference Detection")
            context_dependency_coreference_detection_chinese(args.reference_path, args.answer_path, args.result_path)
            
            print("12. Context Dependency - Coreference Resolution")
            context_dependency_coreference_resolution_chinese(args.reference_path, args.answer_path, args.result_path)
            
            print("13. Context Dependency - Multi-turn")
            context_dependency_multi_turn_chinese(args.reference_path, args.answer_path, args.result_path)
        
        print("-" * 80)
        print(f"Evaluation completed successfully for {args.language} language!")
        print(f"Results saved to: {args.result_path}")
        
    except Exception as e:
        print(f"Error during evaluation: {e}")
        raise

if __name__ == "__main__":
    main()