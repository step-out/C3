# Response Structure

SDM responses should include both speech (`.wav`) and text (`.txt`) files, following the same structure as the [C3 dataset](https://huggingface.co/datasets/ChengqianMa/C3).

## English Structure

```
answer_path/
├── ambiguity/
│   ├── phonological/
│   │   ├── generation/
│   │   ├── heterograph/
│   │   ├── pause/
│   │   ├── stress/
│   │   └── intonation/
│   └── semantic/
│       ├── lexical/
│       └── syntactic/
└── context-dependency/
    ├── omission-detection/
    ├── omission-completion/
    ├── coreference-detection/
    ├── coreference-resolution/
    └── multi-turn/
```

## Chinese Structure

```
answer_path/
├── ambiguity/
│   ├── phonological/
│   │   ├── generation/
│   │   │   ├── pause/
│   │   │   ├── heteronym/
│   │   │   └── tone/
│   │   ├── pause/
│   │   ├── heteronym/
│   │   ├── heterograph/
│   │   └── tone/
│   └── semantic/
└── context-dependency/
    ├── omission-detection/
    ├── omission-completion/
    ├── coreference-detection/
    ├── coreference-resolution/
    └── multi-turn/
```

## File Format

Each folder contains:
- `.txt` files with corresponding text
- `.wav` files with model responses