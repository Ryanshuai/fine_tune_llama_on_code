from qa_dataset.llama_inference import llm_inference


def augment_question(question):
    merged_q = (f"Give me other ways of saying questions: {question}, \
                directly output other ways, don't answer, don't explain, don't provide anything else.\
                list them one question per line. \
                Do not split under_score-linked strings.\
                Key information cannot be ignored!\n")

    # merged_q = (f"Translate the question: {question} into Chinese. And then translate the Chinese back into English.\
    #             Do not split under_score-linked variables, do not split camelCase.\
    #             put two Enter at beginning of the result.")

    new_qs = llm_inference(merged_q)

    try:
        new_qs = new_qs.split("\n\n")[1]
        new_qs = new_qs.split("\n")
    except:
        new_qs = [question]

    return new_qs


if __name__ == '__main__':
    from funciton_level_infer import ask_questions_about_function

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
        question = qa["question"]
        print("original question:", question)
        print("augmented question:")
        new_qs = augment_question(question)
        for new_q in new_qs:
            print(new_q)
