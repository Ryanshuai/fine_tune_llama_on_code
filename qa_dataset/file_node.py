import os.path

from collections import defaultdict
import libcst as cst
from qa_dataset.qa_base_node import Node
from qa_dataset.function_node import PyFunction
from qa_dataset.class_node import PyClass

def cst_parse_python_file(file_path):
    with open(file_path, 'r') as file:
        source_code = file.read()
    
    # Parse the source code into a CST
    parsed_cst = cst.parse_module(source_code)
    
    return parsed_cst



class PythonFile(Node):
    name_path_dict = defaultdict(set)

    def __init__(self, path):
        super().__init__()
        self.class_name = "PythonFile"
        self.name = os.path.basename(path)
        self.path = path
        self.content = None
        self.import_from_file = []
        self.cst_node = cst_parse_python_file(path)

        PythonFile.name_path_dict[self.name].add(path)
        self.qa_functions = [where_file_question]

        self.top_level_code = self.get_top_level_code()
        self.build_children_nodes()


    def build_children_nodes(self):
        for node in self.cst_node.body:
            if isinstance(node, cst.FunctionDef):
                self.children.append(PyFunction(node))
            elif isinstance(node, cst.ClassDef):
                self.children.append(PyClass(node))
        return
    
    def get_top_level_code(self):
        top_level_code = []
        for node in self.cst_node.body:
            # Checking for non-function and non-class top-level elements
            if not isinstance(node, cst.FunctionDef) and not isinstance(node, cst.ClassDef):
                # Using cst.Module to convert node back to source code string
                top_level_code.append(cst.Module(body=[node]).code)

        # Joining all the elements into a single string with newline characters
        return "\n".join(top_level_code)



class File(Node):
    name_path_dict = defaultdict(set)

    def __init__(self, path):
        super().__init__()
        self.name = os.path.basename(path)
        self.path = path
        self.content = None
        self.import_from_file = []
        self.ast_node = None

        File.name_path_dict[self.name].add(path)
        self.qa_functions = [where_file_question]

    def __repr__(self, level=0):
        return "\t" * level + f"File({self.name})\n"


def where_file_question(file):
    question = f"where is the file {file.name} located?"
    prompt = None
    answer = "\n" + "\n".join(File.name_path_dict[file.name])
    return question, prompt, answer


