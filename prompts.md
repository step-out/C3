# The Content 

- [Prompt Template for English Dataset Evaluation](#prompt-template-for-english-dataset-evaluation)  
  - [1. System Prompt](#1-system-prompt)  
  - [2. Phonological Ambiguity](#2-phonological-ambiguity)  
    - [2.1 Heterograph](#21-heterograph)  
    - [2.2 Pause, Stress, Intonation](#22-pause-stress-intonation)  
  - [3. Semantic Ambiguity](#3-semantic-ambiguity)  
    - [3.1 Lexical Semantic Ambiguity](#31-lexical-semantic-ambiguity)  
    - [3.2 Syntactic Semantic Ambiguity](#32-syntactic-semantic-ambiguity)  
  - [4. Omission](#4-omission)  
    - [4.1 Omission Detection](#41-omission-detection)  
    - [4.2 Omission Completion](#42-omission-completion)  
  - [5. Coreference](#5-coreference)  
    - [5.1 Coreference Detection](#51-coreference-detection)  
    - [5.2 Coreference Resolution](#52-coreference-resolution)  
  - [6. Multi-turn Interaction](#6-multi-turn-interaction)  

- [Prompt Template for Chinese Dataset Evaluation](#prompt-template-for-chinese-dataset-evaluation)  
  - [1. System Prompt](#1-system-prompt-1)
  - [2. Phonological Ambiguity](#2-phonological-ambiguity-1)
  - [3. Semantic Ambiguity](#3-semantic-ambiguity-1)
  - [4. Omission](#4-omission-1)
    - [4.1 Omission Detection](#41-omission-detection-1)
    - [4.2 Omission Completion](#42-omission-completion-1)
  - [5. Coreference](#5-coreference-1)
    - [5.1 Coreference Detection](#51-coreference-detection-1)
    - [5.2 Coreference Resolution](#52-coreference-resolution-1)
  - [6. Multi-turn Interaction](#6-multi-turn-interaction-1)

# The Prompt

## Prompt Template for English Dataset Evaluation

### 1. System Prompt

```text
You are an expert proficient in analyzing linguistic and phonetic phenomena, with extensive research experience in various aspects of language and speech, including semantic comprehension, homophone differentiation, polysemy disambiguation, analysis of special sentence structures, ambiguity identification, and grammatical structure analysis in English spoken conversations.
```

### 2. Phonological Ambiguity

#### 2.1 Heterograph
```text
This is a sentence that contains ambiguity caused by homophony when read:
<origin instance>

Regarding this sentence, there is a question:
<qusestion>

The standard answer to this question is:
<reference answer>

A student provided their own answer to the question:
<response from SDM>

Please analyze whether the student's answer is correct. First, understand the question and the standard answer, and then analyze the student's answer. If the student's answer is correct, output 'The answer is: yes.' at the end; otherwise, output 'The answer is: no.' at the end.
```

#### 2.2 Pause, Stress, Intonation
```text
This is a sentence that contains ambiguity caused by <pauses/stress/intonation> when read:
<origin instance>

The correct understanding of this sentence is:
<reference answer>

A student has provided their own interpretation of this sentence:
<response from SDM>

Please analyze whether the student's interpretation is correct. First, understand the ambiguous sentence and its corresponding correct interpretation, and then analyze the student's interpretation.
If the student's interpretation is correct, output 'The answer is: yes.' at the end; otherwise, output 'The answer is: no.' at the end.
```

### 3. Semantic Ambiguity

#### 3.1 Lexical Semantic Ambiguity
```text
This is a sentence that contains ambiguity caused by polysemy:
<origin instance>

The correct understanding of this sentence is:
<reference answer>

A student has provided their own interpretation of this sentence:
<response from SDM>

Please analyze whether the student's interpretation is correct. First, understand the ambiguous sentence and its corresponding correct interpretation, and then analyze the student's interpretation.
If the student's interpretation is correct, output 'The answer is: yes.' at the end; otherwise, output 'The answer is: no.' at the end.
```

#### 3.2 Syntactic Semantic Ambiguity
```text
This is a sentence that contains ambiguity caused by syntactic structure:
<origin instance>

The correct understanding of this sentence is:
<ambiguity>

The 1 meaning of this sentence is:
<interpretations 1>
The 2 meaning of this sentence is:
<interpretations 2>

...

A student has provided their own interpretation of this sentence:
<response from SDM>

Please analyze whether the student's interpretation is correct. First, understand the ambiguous sentence and its corresponding correct interpretation, and then analyze the student's interpretation.
If the student's interpretation is correct, output 'The answer is: yes.' at the end; otherwise, output 'The answer is: no.' at the end.
```

### 4. Omission

#### 4.1 Omission Detection

```text
This is a sentence that contains ambiguity caused by omission:
<origin instance>

When asked whether there was any omission in the sentence, one student gave his/her answer:
<response from SDM>

Check if the student correctly identified the omission in the sentence.
If the student's answer is correct, output 'The answer is: yes.' at the end; otherwise, output 'The answer is: no.' at the end.
```

#### 4.2 Omission Completion

```text
This is a sentence that contains ambiguity caused by omission:
<origin instance>

How should we resolve the ambiguity of this sentence and complete the missing content? This is the standard answer:
<reference answer>

A student has provided their own answer regarding this problem:
<response from SDM>

Compared to the standard answer, did the student restore all the omitted content? First, understand the ambiguous sentence, the question, and the correct answer, and then analyze the student's answer. If the student's answer includes all the restored content that is present in the standard answer, then the student's answer is considered correct.
If the student's answer is correct, output 'The answer is: yes.' at the end; otherwise, output 'The answer is: no.' at the end.
```

### 5. Coreference

#### 5.1 Coreference Detection

```text
This is a sentence that contains ambiguity caused by coreference:
<origin instance>

When asked whether there was any coreference in the sentence, one student gave his/her answer:
<response from SDM>

Assess whether the student has successfully detected the presence of a coreference phenomenon in the sentence.
If the student has identified the coreference phenomenon, their response is deemed correct, irrespective of the accuracy of the content they identified as being referred to.
Conversely, if the student fails to identify the referential phenomenon, their response is considered incorrect, regardless of the reasons provided.
If the student's answer is correct, output 'The answer is: yes.' at the end; otherwise, output 'The answer is: no.' at the end.
```

#### 5.2 Coreference Resolution

```text
This is a sentence that contains ambiguity caused by coreference:
<origin instance>

Regarding this sentence, there is a question:
<question>

The standard answer to this question is:
<reference answer>

A student provided their own answer to the question:
<response from SDM>

Please analyze whether the student's answer is correct. First, understand the question and the standard answer, and then analyze the student's answer.
If the student's answer is correct, output 'The answer is: yes.' at the end; otherwise, output 'The answer is: no.' at the end.
```

### 6. Multi-turn Interaction

```text
This is a conversation between A and B. Please understand this dialogue, and I will pose a question after the dialogue:

A: <first input from C3Benchmark>  
B: <first response from SDM>  
...  
A: <last input from C3Benchmark>  
B: <last response from SDM>  

Please analyze whether B's response in the last round of the dialogue is correct. It is known that the question posed by A in the last round of the dialogue is the same as the question posed by A in the first round. If B's response in the last round is consistent with B's response in the first round and does not conflict with the content of the dialogue in between, then B's response in the last round is considered correct. Please first understand B's responses in both the first and last rounds of the dialogue, compare whether the two responses are consistent, and finally analyze whether B's response in the last round does not conflict with the content of the dialogue in between.
If B's response in the last round is correct, answer 'The answer is: yes.' at the end; otherwise, answer 'The answer is: no.' at the end.
```


## Prompt Template for Chinese Dataset Evaluation

This is the core prompt template for each complex phenomena. The variable part is marked with `<...>`.

### 1. System Prompt

```
你是一个擅长分析语言学、语音学现象的专家，在中文语音对话中的语义理解、同音词辨别、一词多义辨析、特殊句式分析、歧义辨别、语法结构分析等语言和语音中的各个领域都拥有丰富的研究经验。
```

### 2. Phonological Ambiguity

```text
这里有一段考察语义理解的材料，材料内容如下：
<origin instance>
请问这段材料应该如何理解？

正确的答案为：
<reference answer>

有一名学生针对如何理解该材料这一问题，给出了如下答案：
<response from SDM>

请问该学生的理解是否正确？在分析过程中，请先理解题目和正确答案，随后分析学生的答案是否正确。
请在最后一行回答是或否。回答时请遵循格式：

最终答案为：是。
或者
最终答案为：否。
```

### 3. Semantic Ambiguity

```text
这里有一段考察语义理解的材料，材料内容如下：
<origin instance>
请问这段材料应该如何理解？

正确的答案为：
<reference answer>

有一名学生针对如何理解该材料这一问题，给出了如下答案：
<response from SDM>

请问该学生的理解是否正确？在分析过程中，请先理解题目和正确答案，随后分析学生的答案是否正确。
请在最后一行回答是或否。回答时请遵循格式：

最终答案为：是。
或者
最终答案为：否。
```

### 4. Omission

#### 4.1 Omission Detection

```text
这里有一段对话，对话中最后一句存在省略现象，对话内容如下：
<origin instance>

对于这句话中是否包含省略现象，一名学生给出了自己的回答如下：：
<response from SDM>

请分析，该学生是否正确识别出了对话中的省略现象？当该学生识别出最后一句话中存在的省略现象时，我们认为是；当该学生没能识别出最后一句话中存在的省略现象时，我们认为否。请在最后一行回答是或否。回答时请遵循格式：

最终答案为：是。
或者
最终答案为：否。
```

#### 4.2 Omission Completion

```text
这里有一段对话，对话中最后一句存在省略现象，对话内容如下：
<origin instance>

请补全被省略的内容，给出省略内容被补全后的完整语句。
将其中省略内容全部补全后的正确答案为：
<reference answer>

有一名学生给出这样的回答：
<response from SDM>

请分析：该学生的回答是否正确？正确的标准是：学生的回答将正确答案中被补全的所有省略内容，都进行了补全。
请在最后一行回答是或否。回答时请遵循格式：

最终答案为：是。
或者
最终答案为：否。
```

### 5. Coreference

#### 5.1 Coreference Detection

```text
这里有一段对话，对话中最后一句存在使用代词指代具体内容的现象，对话内容如下：
<origin instance>

对于这句话中是否包含指代现象，一名学生给出了自己的回答如下：
<response from SDM>

请分析，该学生是否正确识别出了对话中的指代现象？当该学生识别出最后一句话中存在的指代现象时，我们认为是；当该学生没能识别出最后一句话中存在的指代现象时，我们认为否。
请在最后一行回答是或否。回答时请遵循格式：

最终答案为：是。
或者
最终答案为：否。
```

#### 5.2 Coreference Resolution

```text
这里有一段对话，对话中最后一句存在使用代词指代具体内容的现象，对话内容如下：
<origin instance>

请把代词替换成代词指代的内容，给出所有代词被替换后的完整语句。
将其中代词全部替换后的正确答案为：
<reference answer>

有一名学生给出这样的回答：
<response from SDM>

请分析：该学生的回答是否正确？正确的标准是：学生的回答将正确答案中被替换的所有代词，都进行了替换。
请在最后一行回答是或否。回答时请遵循格式：

最终答案为：是。
或者
最终答案为：否。
```

### 6. Multi-turn Interaction

```text
这里有甲和乙的一段对话，请听完这段对话，并回答我在对话之后提出的问题：

甲说：<The first input from C3Benchmark>
乙说：<The first response from SDM>
...
甲说：<The last input from C3Benchmark>
乙说：<The last response from SDM>

对话结束，请分析乙在最后一轮对话中的回答是否正确。已知最后一轮对话中甲提出的问题，和第一轮对话中甲提出的问题是一样的。如果乙最后一轮对话中给出的回答，和乙第一轮对话中给出的回答一致，且和两人中间对话的内容不冲突，则说明乙在最后一轮对话中的回答是正确的。请先理解乙在第一轮和最后一轮对话中的回答，再对比两次回答是否一致，接着分析乙最后一轮的回答是否不与中间对话的内容冲突。最后分析乙最后一轮对话中的回答是否正确。请在最后一行回答是或否。回答时请遵循格式：

最终答案为：是。
或者
最终答案为：否。
```
