import ollama
### Utility class that wraps the ollama API with some niceties for my use case.
class OllamaConnection:
  def __init__(self, server="127.0.0.1"):
    self.server = server

  def AskOllama(self, question):
      response = ollama.chat(model='wopr', messages=[
        {
          'role': 'user',
          'content': question,
        },
      ])
      responseContent = response['message']['content']
      cleaned = self.handleCodeBlocks(responseContent)
      return cleaned
    
  # Later I can clean up the unknown characters in a better way, maybe color or other things
  def handleCodeBlocks(self, text):
    remove="`"    
    table=str.maketrans("","",remove)    
    return text.translate(table)    
