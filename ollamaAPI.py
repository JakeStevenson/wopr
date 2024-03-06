import ollama
def AskOllama(question):
    response = ollama.chat(model='wopr', messages=[
      {
        'role': 'user',
        'content': question,
      },
    ])
    responseText = response['message']['content'].replace('\r\n', '\n')
    responseText = handleCodeBlocks(responseText)
    responseText = '\r\n'.join(responseText.splitlines())
    return responseText
  
# Later I can clean up the unknown characters in a better way
def handleCodeBlocks(text):
  remove="`"    
  table=str.maketrans("","",remove)    
  return text.translate(table)    
