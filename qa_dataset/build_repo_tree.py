import os.path
from pathlib import Path

PROJECT_ROOT = str(Path(__file__).parent.parent.absolute())


class PyClass:
    def __init__(self, class_name, class_instance):
        self.class_name = class_name
        self.class_instance = class_instance
        self.methods = []
        self.attributes = []

    def ask_questions(self):
        pass


class File:
    def __init__(self, path):
        self.name = os.path.basename(path)
        self.path = path
        self.content = None
        self.import_from_file = []

    def __repr__(self, level=0):
        return "\t" * level + f"File({self.name})\n"

    def ask_questions(self):
        pass


class Folder:
    def __init__(self, path):
        self.name = os.path.basename(path)
        self.path = path
        self.children = []

    def __repr__(self, level=0):
        ret = "\t" * level + f"Folder({self.name})\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

    def ask_questions(self):
        pass


def build_repo_tree(root_path):
    if os.path.isfile(root_path):
        return File(root_path)

    assert os.path.isdir(root_path)
    node = Folder(root_path)

    for name in os.listdir(root_path):
        path = os.path.join(root_path, name)
        node.children.append(build_repo_tree(path))
    return node


if __name__ == '__main__':
    res = build_repo_tree(PROJECT_ROOT + os.sep + "nanoGPT")
    print(res)
