import ollama

messages = []


def llm_inference(messages, model='llama3:8b'):
    messages_dict = {'role': 'user', 'content': messages}
    output = ollama.chat(model=model, messages=[messages_dict])
    return output["message"]["content"]


def send(chat):
    messages.append(
        {
            'role': 'user',
            'content': chat,
        }
    )
    stream = ollama.chat(model='llama3:8b',
                         messages=messages,
                         stream=True,
                         )

    response = ""
    for chunk in stream:
        part = chunk['message']['content']
        print(part, end='', flush=True)
        response = response + part

    messages.append(
        {
            'role': 'assistant',
            'content': response,
        }
    )

    print("")


if __name__ == '__main__':
    while True:
        chat = input(">>> ")

        if chat == "/exit":
            break
        elif len(chat) > 0:
            send(chat)
