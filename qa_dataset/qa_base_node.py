from abc import ABC

import ollama


def llm_inference(messages, model='llama3:8b'):
    messages_dict = {'role': 'user', 'content': messages}
    output = ollama.chat(model=model, messages=[messages_dict])
    return output["message"]["content"]


class Node(ABC):
    def __init__(self):
        super().__init__()
        self.name = ""

        self.qa_functions = []
        self.children = []
        self.qa = []

    def prepare_qa(self):
        for question_fn in self.qa_functions:
            question, prompt, answer = question_fn(self)
            if answer is None:
                assert prompt is not None
                answer = llm_inference(prompt)

            print("=" * 80)
            print(f"Question: {question}")
            print(f"Answer: {answer}")

            self.qa.append({"question": question, "answer": answer})

        for child in self.children:
            self.qa.extend(child.prepare_qa())

        return self.qa

    def __repr__(self, level=0):
        ret = "\t" * level + f"{self.__class__.__name__}({self.name})\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret
