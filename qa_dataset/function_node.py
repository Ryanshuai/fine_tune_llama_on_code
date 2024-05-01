from qa_dataset.llama_inference import llm_inference
import libcst as cst

from qa_dataset.qa_base_node import Node

class PyFunction(Node,cst.CSTVisitor):
    
    def __init__(self, node):
        assert isinstance(node, cst.FunctionDef)
        super().__init__()
        self.class_name = "PyFunction"
        self.name = node.name.value
        self.cst_node = node
        self.code = cst.Module(body=[node]).code
        self.attributes = []
        self.qa_questions = [purpose_question, purpose_question2, summary_question, list_parameter_question, list_return_value_question]


    def get_function_parameters(self):
        func_node = self.cst_node
        params = []
        # Accessing parameters from the function definition
        for param in func_node.params.params:
            params.append(param.name.value)
        # Handling variable arguments (*args)
        if func_node.params.star_arg:
            params.append('*' + func_node.params.star_arg.name.value)
        # Handling keyword-only arguments
        for kwonly in func_node.params.kwonly_params:
            params.append(kwonly.name.value)
        # Handling keyword arguments (**kwargs)
        if func_node.params.star_kwarg:
            params.append('**' + func_node.params.star_kwarg.name.value)
        return params
        #Output a list of return value


    
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

def ask_questions_about_function(pyfunction: PyFunction):
    qa_data = []
    for question_func in pyfunction.question_funcs:
        question, prompt, answer = question_func(pyfunction)
        if answer is None:
            assert prompt is not None
            answer = llm_inference(prompt)
        qa_data.append({"question": question, "answer": answer})

    return qa_data
if __name__ == '__main__':
    example_function = r'''
    def add_metadata_to_image(tensor: torch.Tensor, metadata: Dict[Any, Any]) -> Figure:
    """
    Displays an image and adds metadata as a title to the plot.

    Args:
        tensor (torch.Tensor): A tensor of shape (C, H, W) representing an image.
        metadata (Dict[Any, Any]): A dictionary containing metadata to be displayed in the plot title.

    Returns:
        figure (matplotlib.figure.Figure): A Matplotlib figure object containing the plotted image and metadata title.
    """
    figure = plt.figure()
    img = tensor.cpu().numpy().transpose((1, 2, 0))
    plt.imshow(img)
    d = max(map(len, metadata.keys()))
    texts = "\n".join([str(key) + "  " * (d - len(key)) + ":  " + str(value) for key, value in metadata.items()])
    plt.suptitle(texts, fontsize=25, ha='left', va='top', x=0.01, y=0.99)
    plt.tight_layout()
    return figure
    '''
    class_name = "add_metadata_to_image"
    qa_data = ask_questions_about_function(class_name, example_function)

    for qa in qa_data:
        print("-" * 50)
        print("question:", qa["question"])
        print("answer:", qa["answer"])
