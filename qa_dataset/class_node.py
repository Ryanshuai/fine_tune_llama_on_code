import libcst as cst

from qa_dataset.qa_base_node import Node
from qa_dataset.function_node import PyFunction


class PyClass(Node, cst.CSTVisitor):
    def __init__(self, node):
        assert isinstance(node, cst.ClassDef)
        super().__init__()
        self.name = node.name.value
        self.cst_node = node
        self.class_name = "PyClass"
        self.code = cst.Module(body=[node]).code
        self.build_children_nodes()
        self.qa_functions = [purpose_question, summary_question, list_methods_question]
        self.qa = []

    def build_children_nodes(self):
        body = self.cst_node.body
        if isinstance(body, cst.IndentedBlock):
            body = body.body

        for node in body:
            if isinstance(node, cst.FunctionDef):
                self.children.append(PyFunction(node))
            elif isinstance(node, cst.ClassDef):
                self.children.append(PyClass(node))


def purpose_question(py_class: PyClass):
    question = f"what is the purpose of the class {py_class.name}?"
    prompt = f"what is the purpose of the class: \n{py_class.code}"
    answer = None
    return question, prompt, answer


def inheritence_question(py_class: PyClass):
    question = f"Does this class {py_class.name} inheritant from any class?"
    prompt = f"Does this class inheritant from any class: \n{py_class.code}"
    answer = None
    return question, prompt, answer


def summary_question(py_class: PyClass):
    question = f"summarize the class {py_class.name}?"
    prompt = f"summarize the class: \n{py_class.code}"
    answer = None
    return question, prompt, answer


def list_methods_question(py_class: PyClass):
    question = f"list the methods in the class {py_class.name}"
    prompt = None
    answer = " ".join([node.name.value for node in py_class.cst_node.body.body if isinstance(node, cst.FunctionDef)])
    return question, prompt, answer


# TODO
def list_attributes_question(py_class: PyClass):
    question = f"list the attributes in the class {py_class.name}"
    prompt = None
    answer = " ".join(py_class.attributes)
    return question, prompt, answer


if __name__ == '__main__':
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
    cst_tree = cst.parse_module(example_class)
    # Need to traverse and find the ClassDef node
    class_node = next(node for node in cst_tree.children if isinstance(node, cst.ClassDef))
    py_class = PyClass(class_node)
    qa = py_class.prepare_qa()

    for qa_pair in qa:
        print("=" * 80)
        print(qa_pair["question"])
        print(qa_pair["answer"])
