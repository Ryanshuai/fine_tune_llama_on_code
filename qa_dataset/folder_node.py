import os.path
from collections import defaultdict

from qa_dataset.qa_base_node import Node


class Folder(Node):
    name_path_dict = defaultdict(set)

    def __init__(self, path):
        super().__init__()
        self.name = os.path.basename(path)
        self.path = path
        self.children = []

        Folder.name_path_dict[self.name].add(path)
        self.qa_functions = [where_folder_question]

    def __repr__(self, level=0):
        ret = "\t" * level + f"Folder({self.name})\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret


def where_folder_question(folder):
    question = f"where is the folder {folder.name} located?"
    prompt = None
    answer = "\n" + "\n".join(Folder.name_path_dict[folder.name])
    return question, prompt, answer
