from Scanner import Scanner
from Parser import Parser
from Evaluate import Interpreter 
from Eror import Error
class Zoo:
     def __init__(self,file):
        self.file=file
     def run(self):
            with open(self.file) as f:
                  content=f.read()
                  Tokens=Scanner(content).scanTokens()
                  root_Ast=Parser(Tokens).parse()
                  if not Error.had_error:
                         Interpreter().interpret(root_Ast)

