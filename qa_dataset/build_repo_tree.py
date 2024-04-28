import os.path

from qa_dataset.file_node import File
from qa_dataset.folder_node import Folder


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
    from pathlib import Path

    CODE_ROOT = str(Path(__file__).parent.parent.absolute()) + os.sep + "nanoGPT"
    res = build_repo_tree(CODE_ROOT)
    print(res)
