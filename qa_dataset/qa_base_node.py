from abc import ABC

import ollama


def llm_inference(messages, model='llama3:8b'):
    messages_dict = {'role': 'user', 'content': messages}
    output = ollama.chat(model=model, messages=[messages_dict])
    return output["message"]["content"]


class Node(ABC):
    def __init__(self):
        super().__init__()
        self.qa_questions = []

    def prepare_qa(self):
        qa_data = []
        for question_func in self.qa_questions:
            question, prompt, answer = question_func(self)
            if answer is None:
                assert prompt is not None
                answer = llm_inference(prompt)
            qa_data.append({"question": question, "answer": answer})

        return qa_data