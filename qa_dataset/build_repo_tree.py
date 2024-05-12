import sys
import os

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_path)

from qa_dataset.file_node import File, PythonFile
from qa_dataset.folder_node import Folder


def build_repo_tree(root_path):
    if os.path.isfile(root_path):
        return PythonFile(root_path) if root_path.endswith(".py") else File(root_path)

    assert os.path.isdir(root_path)
    node = Folder(root_path)

    for name in os.listdir(root_path):
        path = os.path.join(root_path, name)
        node.children.append(build_repo_tree(path))
    return node


if __name__ == '__main__':
    from pathlib import Path

    CODE_ROOT = str(Path(__file__).parent.parent.absolute()) + os.sep + "nanoGPT"
    root = build_repo_tree(CODE_ROOT)
    qa = root.prepare_qa()

    print(qa)
