from llama_inference import llm_inference


def purpose_question(function_name, function_code):
    question = f"what is the purpose of the function: {function_name}?"
    prompt = f"what is the purpose of the function: \n{function_code}"
    answer = None
    return question, prompt, answer


def summary_question(function_name, function_code):
    question = f"summarize the class {function_name}"
    prompt = f"summarize the class: \n{function_code}"
    answer = None
    return question, prompt, answer


def input_question(function_name, function_code):
    question = f"what are the inputs to the function {function_name}?"
    prompt = f"what are the inputs to the function: \n{function_code}"
    answer = None
    return question, prompt, answer


def output_question(function_name, function_code):
    question = f"what are the outputs of the function {function_name}?"
    prompt = f"what are the outputs of the function: \n{function_code}"
    answer = None
    return question, prompt, answer


question_funcs = [purpose_question, summary_question, input_question, output_question]


def ask_questions_about_class(class_name, class_code):
    qa_data = []
    for question_func in question_funcs:
        question, prompt, answer = question_func(class_name, class_code)
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
    qa_data = ask_questions_about_class(class_name, example_function)

    for qa in qa_data:
        print("-" * 50)
        print("question:", qa["question"])
        print("answer:", qa["answer"])
