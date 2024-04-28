import ast

from qa_dataset.qa_base_node import Node


class PyClass(Node, ast.NodeVisitor):
    def __init__(self, node):
        super().__init__()
        self.name = node.body[0].name
        self.node = node
        self.methods = dict()
        self.attributes = []
        self.visit(node)

        self.qa_questions = [purpose_question, summary_question, list_methods_question, list_attributes_question]

    def visit_FunctionDef(self, node):
        self.methods[node.name] = ast.unparse(node)
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.attributes.append(target.id)
        self.generic_visit(node)

    def __repr__(self, ):
        return f"PyClass({self.name})\n"


def purpose_question(py_class: PyClass):
    question = f"what is the purpose of the class {py_class.name}?"
    prompt = f"what is the purpose of the class: \n{ast.unparse(py_class.node)}"
    answer = None
    return question, prompt, answer


def summary_question(py_class: PyClass):
    question = f"summarize the class {py_class.name}?"
    prompt = f"summarize the class: \n{ast.unparse(py_class.node)}"
    answer = None
    return question, prompt, answer


def list_methods_question(py_class: PyClass):
    question = f"list the methods in the class {py_class.name}"
    prompt = None
    answer = " ".join(py_class.methods.keys())
    return question, prompt, answer


def list_attributes_question(py_class: PyClass):
    question = f"list the attributes in the class {py_class.name}"
    prompt = None
    answer = " ".join(py_class.attributes)
    return question, prompt, answer


if __name__ == '__main__':
    import ast

    example_class = """class Annotation(ABC):
        def __init__(self, **kwargs):
            self.annotations = None
            if "im_root" in kwargs and "annotation_path" in kwargs:
                im_root = kwargs["im_root"]
                annotation_path = kwargs["annotation_path"]
                self.load_anno(annotation_path)
                self.inject_im_root(im_root)

            elif "annotations" in kwargs:
                self.annotations = kwargs["annotations"]

        @abstractmethod
        def load_anno(self, annotation_path):
            pass

        @abstractmethod
        def inject_im_root(self, im_root):
            pass

        @abstractmethod
        def __len__(self):
            pass

        @abstractmethod
        def __add__(self, other):
            pass

        @abstractmethod
        def split(self, ratios):
            pass

        @staticmethod
        def ratios_check(ratios):
            if abs(sum(ratios) - 1.0) >= 1e-9:
                raise ValueError("The sum of the ratios must equal 1.")
            for ratio in ratios:
                if ratio < 0 or ratio > 1:
                    raise ValueError("The ratio must be between 0 and 1.")
    """
    cls = ast.parse(example_class)
    py_class = PyClass(cls)
    py_class.prepare_qa()

    print(py_class.methods)
    print(py_class.attributes)
