import os.path
from collections import defaultdict

from qa_dataset.qa_base_node import Node

from constant import PROJECT_ROOT

class Folder(Node):
    name_path_dict = defaultdict(set)

    def __init__(self, path):
        super().__init__()
        self.name = os.path.basename(path)
        self.path = path

        path_to_project = os.path.relpath(path, PROJECT_ROOT)
        path_to_project = path_to_project.replace("\\", "/")
        Folder.name_path_dict[self.name].add(path_to_project)
        self.qa_functions = [where_folder_question]


def where_folder_question(folder):
    question = f"where is the folder {folder.name} located?"
    prompt = None
    answer = "\n".join(Folder.name_path_dict[folder.name])
    return question, prompt, answer


def where_inside_folder_question(folder):
    question = f"where are the files inside the folder {folder.name}?"
    # TODO
    prompt = None
    answer = "\n".join(Folder.name_path_dict[folder.name])
    return None
