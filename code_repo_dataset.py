import os
from glob import glob
import itertools

from torch.utils.data import Dataset


class MixDataset(Dataset):
    def __init__(self, datasets):
        self.datasets = datasets

        self.lengths = [len(dataset) for dataset in datasets]
        self.cumulative_lengths = [0] + list(itertools.accumulate(self.lengths))

    def __len__(self):
        return self.cumulative_lengths[-1]

    def __getitem__(self, idx):
        dataset_idx = next(i for i, cl in enumerate(self.cumulative_lengths) if cl > idx) - 1
        return self.datasets[dataset_idx][idx - self.cumulative_lengths[dataset_idx]]


qa_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""


class QADataset(Dataset):
    def __init__(self, qa_question_file, eos_token):
        self.qa_question_file = qa_question_file
        self.eos_token = eos_token

        self.qa_questions = list(self.prepare_qa_questions(qa_question_file))

    def prepare_qa_questions(self, code_root):
        # TODO
        yield ""

    def __len__(self):
        return len(self.qa_questions)

    def __getitem__(self, idx):
        return self.qa_questions[idx]


code_prompt = """Below is a code snippet.

### File:
{}

### Line:
{}

### Code:
{}"""


class CodeRepoDataset(Dataset):
    def __init__(self, code_root, eos_token):
        self.code_root = code_root
        self.eos_token = eos_token

        self.plain_code = list(self.prepare_plain_code(code_root))

    def prepare_plain_code(self, code_root, num_lines_per_snippet=10):
        files_list = glob(f"{code_root}/**/*", recursive=True)
        files_list = [file for file in files_list if os.path.isfile(file)]

        for file in files_list:
            with open(file, "r") as f:
                code = f.readlines()
            num_lines = len(code)
            num_snippets = num_lines - num_lines_per_snippet + 1
            for i in range(num_snippets):
                snippet = code[i:i + num_lines_per_snippet]
                snippet = "".join(snippet)
                yield code_prompt.format(file, f"{i}-{i + num_lines_per_snippet}", snippet) + self.eos_token

    def __len__(self):
        return len(self.plain_code)

    def __getitem__(self, idx):
        return self.plain_code[idx]
