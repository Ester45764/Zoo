from Eror  import Error,RuntimeEror

class Environnement:
      def __init__(self,enclosing=None):
          self.enclosing=enclosing
          self.values={}
      def define(self,name,value):
           self.values[name]=value
      def get_value(self,name):
        if name.lexeme in self.values:
                return self.values[name.lexeme] # name est un token
        if self.enclosing:
             return self.enclosing.get_value(name)
        raise RuntimeEror(name,"Undefined variable"+name.lexeme+".")
      def assign(self,token,value):
             if token.lexeme in self.values: 
                   self.values[token.lexeme]=value
                   return
             if self.enclosing:
                   self.enclosing.assign(token,value)
                   return
             raise  RuntimeEror(token,"Undefined variable"+token.lexeme+".")
      
