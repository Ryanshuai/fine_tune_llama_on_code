import os.path
from collections import defaultdict

from qa_dataset.qa_base_node import Node


class File(Node):
    name_path_dict = defaultdict(set)

    def __init__(self, path):
        super().__init__()
        self.name = os.path.basename(path)
        self.path = path
        self.content = None
        self.import_from_file = []

        File.name_path_dict[self.name].add(path)
        self.qa_functions = [where_file_question]

    def __repr__(self, level=0):
        return "\t" * level + f"File({self.name})\n"


def where_file_question(file):
    question = f"where is the file {file.name} located?"
    prompt = None
    answer = "\n" + "\n".join(File.name_path_dict[file.name])
    return question, prompt, answer
