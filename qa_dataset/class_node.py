import re

from qa_dataset.qa_base_node import Node


class PyClass(Node):
    def __init__(self, class_name, class_instance):
        super().__init__()
        self.name = class_name
        self.instance = class_instance
        self.methods = []
        self.attributes = []

        self.qa_questions = [purpose_question, summary_question, list_methods_question, list_attributes_question]

    def __repr__(self, ):
        return f"PyClass({self.name})\n"


def purpose_question(class_name, class_code):
    question = f"what is the purpose of the class {class_name}?"
    prompt = f"what is the purpose of the class: \n{class_code}"
    answer = None
    return question, prompt, answer


def summary_question(class_name, class_code):
    question = f"summarize the class {class_name}"
    prompt = f"summarize the class: \n{class_code}"
    answer = None
    return question, prompt, answer


def list_methods_question(class_name, class_code):
    question = f"list the methods in the class {class_name}"
    prompt = None

    pattern = r'\bdef\b\s+(\w+)\('
    answer = re.findall(pattern, class_code)
    answer = " ".join(answer)
    return question, prompt, answer


def list_attributes_question(class_name, class_code):
    question = f"list the attributes in the class {class_name}"
    prompt = f"list the attributes in the class: \n{class_code}, do not explain, just list them."
    answer = None
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
    class_name = "data.Annotation"
    qa_data = ask_questions_about_class(class_name, example_class)

    for qa in qa_data:
        print("-" * 50)
        print("question:", qa["question"])
        print("answer:", qa["answer"])
