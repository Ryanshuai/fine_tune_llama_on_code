from torch.utils.data import Dataset

# TODO
prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""


class CodeRepoDataset(Dataset):
    def __init__(self, code_root, eos_token):
        self.code_root = code_root
        self.eos_token = eos_token

    def __len__(self):
        return 0  # TODO

    def __getitem__(self, idx):
        # TODO
        return {"text": ""}
