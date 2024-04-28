import os
from collections import defaultdict

ignore_dirs = {'.git', '.idea', '__pycache__', '.gitattributes', '.gitignore'}


def filter_out_ignore(root, dirs, files):
    if any(ignored in root for ignored in ignore_dirs):
        return "", [], []

    dirs = [d for d in dirs if d not in ignore_dirs]
    files = [f for f in files if f not in ignore_dirs]
    return root, dirs, files


def get_project_paths(project_root, code_rela_path):
    code_root = os.path.join(project_root, code_rela_path)
    paths = []
    folder_content = defaultdict(set)
    for root, dirs, files in os.walk(code_root, topdown=True):
        root, dirs, files = filter_out_ignore(root, dirs, files)
        if not root:
            continue

        code_root = root.replace(project_root, "")
        folder_content[code_root] = dirs + files

        for name in files:
            paths.append(os.path.join(code_root, name))
        for name in dirs:
            paths.append(os.path.join(code_root, name))

    return paths, folder_content


def reverse_path_to_dict(paths, project_root):
    file_path_dict = defaultdict(set)
    folder_path_dict = defaultdict(set)
    for path in paths:
        path = path.replace(os.sep, '/')
        while os.path.dirname(path):
            name = os.path.basename(path)
            if os.path.isdir(project_root + "/" + path):
                folder_path_dict[name].add(path)
            else:
                file_path_dict[name].add(path)
            path = os.path.dirname(path)
    return file_path_dict, folder_path_dict


def project_tree_questions(project_root, code_rela_path):
    paths, folder_content = get_project_paths(project_root, code_rela_path)
    file_path_dict, folder_path_dict = reverse_path_to_dict(paths, project_root)
    questions = []

    for name, paths in file_path_dict.items():
        question = f"where is the file {name} located?"
        prompt = None
        answer = "\n" + "\n".join(paths)
        questions.append({"question": question, "prompt": prompt, "answer": answer})

        question = f"where is {name}?"
        questions.append({"question": question, "prompt": prompt, "answer": answer})

    for name, paths in folder_path_dict.items():
        question = f"where is the folder {name} located?"
        prompt = None
        answer = "\n" + "\n".join(paths)
        questions.append({"question": question, "prompt": prompt, "answer": answer})

        question = f"where is {name}?"
        questions.append({"question": question, "prompt": prompt, "answer": answer})

    for folder, content in folder_content.items():
        question = f"what is in the folder {folder}?"
        prompt = None
        answer = "\n" + "\n".join(content)
        questions.append({"question": question, "prompt": prompt, "answer": answer})

    return questions


if __name__ == '__main__':
    project_root = "../"
    paths = get_project_paths(project_root="../", code_rela_path="nanoGPT")

    qa_data = project_tree_questions(project_root="../", code_rela_path="nanoGPT")

    for qa in qa_data:
        print("-" * 50)
        print("question:", qa["question"])
        print("answer:", qa["answer"])
