import ollama
def AskOllama(question):
    response = ollama.chat(model='wopr', messages=[
      {
        'role': 'user',
        'content': question,
      },
    ])
    responseText = response['message']['content'].replace('\r\n', '\n')
    responseText = '\r\n'.join(responseText.splitlines())
    return responseText