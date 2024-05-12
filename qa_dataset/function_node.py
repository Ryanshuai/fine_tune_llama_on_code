import libcst as cst

from qa_dataset.qa_base_node import Node


class PyFunction(Node, cst.CSTVisitor):

    def __init__(self, node):
        assert isinstance(node, cst.FunctionDef)
        super().__init__()
        self.class_name = "PyFunction"
        self.name = node.name.value
        self.cst_node = node
        self.code = cst.Module(body=[node]).code
        self.attributes = []
        self.qa_functions = [purpose_question, purpose_question2, summary_question, list_parameter_question,
                             list_return_value_question]

    def get_function_parameters(self):
        func_node = self.cst_node
        params = []
        # Accessing parameters from the function definition
        for param in func_node.params.params:
            params.append(param.name.value)
        # Handling variable arguments (*args)
        if isinstance(func_node.params.star_arg, cst.Param):
            params.append('*' + func_node.params.star_arg.name.value)
        # Handling keyword-only arguments
        for kwonly in func_node.params.kwonly_params:
            params.append(kwonly.name.value)
        # Handling keyword arguments (**kwargs)
        if isinstance(func_node.params.star_kwarg, cst.Param):
            params.append('**' + func_node.params.star_kwarg.name.value)
        return params
        # Output a list of return value

    def get_return_statements(self):
        func_body = self.cst_node.body
        return_statements = []
        for item in func_body.body:
            if isinstance(item, cst.Return):
                return_statements.append(item)
            elif isinstance(item, (cst.If, cst.For, cst.While, cst.Try)):
                return_statements.extend(self._extract_returns_from_compound(item))
        return return_statements

    def _extract_returns_from_compound(self, compound_stmt):
        returns = []
        for body_part in compound_stmt.body.body:
            if isinstance(body_part, cst.Return):
                returns.append(body_part)
            elif isinstance(body_part, (cst.If, cst.For, cst.While, cst.Try)):
                returns.extend(self._extract_returns_from_compound(body_part))
        return returns


def purpose_question(pyfunction: PyFunction):
    question = f"what is the purpose of the function: {pyfunction.name}?"
    prompt = f"what is the purpose of the function:  \n{pyfunction.code}"
    answer = None
    return question, prompt, answer


def purpose_question2(pyfunction: PyFunction):
    question = f"Generate a one-sentence description for the purpose of the function: {pyfunction.name}?"
    prompt = f"Generate a one-sentence description for the purpose of the function:  \n{pyfunction.code}"
    answer = None
    return question, prompt, answer


def list_parameter_question(pyfunction: PyFunction):
    question = f"what are the return values of the function: {pyfunction.name}?"
    prompt = None
    return_values = pyfunction.get_return_statements
    answer = f"Function '{pyfunction.name}' has return values: {return_values}"
    return question, prompt, answer


def list_return_value_question(pyfunction: PyFunction):
    question = f"what are the return  of the function: {pyfunction.name}?"
    prompt = None
    parameters = pyfunction.get_function_parameters()
    answer = f"Function '{pyfunction.name}' has parameters: {parameters}"
    return question, prompt, answer


def summary_question(pyfunction: PyFunction):
    question = f"summarize the function {pyfunction.name}"
    prompt = f"summarize the function: \n{pyfunction.code}"
    answer = None
    return question, prompt, answer


def output_meaning_question(pyfunction: PyFunction):
    question = f"what is the meaning of the output of the function {pyfunction.name}?"
    prompt = f"what is the meaning of the output of the function : \n{pyfunction.code}"
    answer = None
    return question, prompt, answer


if __name__ == '__main__':
    example_function = example_class = """class Annotation(ABC):
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

    cst_tree = cst.parse_module(example_function)
    cst_clas_node = next(node for node in cst_tree.children if isinstance(node, cst.ClassDef))
    function_node = cst_clas_node.body.body[0]
    pyfunction = PyFunction(function_node)
    qa = pyfunction.prepare_qa()

    for qa_pair in qa:
        print("=" * 80)
        print(qa_pair["question"])
        print(qa_pair["answer"])
