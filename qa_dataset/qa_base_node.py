from abc import ABC

import ollama


def llm_inference(messages, model='llama3:8b'):
    messages_dict = {'role': 'user', 'content': messages}
    output = ollama.chat(model=model, messages=[messages_dict])
    return output["message"]["content"]


class Node(ABC):
    def __init__(self):
        super().__init__()
        self.qa_functions = []
        self.class_name = "Node"
        self.children = []

    def prepare_qa(self):
        qa_data = []
        for question_fn in self.qa_functions:
            question, prompt, answer = question_fn(self)
            if answer is None:
                assert prompt is not None
                answer = llm_inference(prompt)
            qa_data.append({"question": question, "answer": answer})

        return qa_data
    def __repr__(self, level=0):
        ret = "\t" * level + f"{self.class_name}({self.name})\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret
