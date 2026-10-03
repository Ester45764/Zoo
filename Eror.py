
from TokenType import TokenType
class RuntimeEror(Exception):
    def __init__(self, token,messge):
      super().__init__(messge)
      self.token=token
      
class Error:
    had_error=False
    had_runtime_error=False
    @staticmethod
    def runtimeError(error):
         print(f"{error} \n [{error.token.line} line]")
         Error.had_runtime_error=True
    @staticmethod
    def error(line,message):# scanner
        Error.report(line,"",message)
    @staticmethod
    def report(line,where,message):
        print(f"[line {line}] Error {where} :{message}")
        Error.had_error=True
    @staticmethod 
    def error_token(token,message): #parsing
          if token.Type==TokenType.EOF:
             Error.report(token.line,"at end",message)
          else:
              Error.report(token.line,"at '"+token.lexeme+"'",message) 
