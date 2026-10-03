from TokenType import TokenType
from Eror import Error
class ParseError(Exception):
    pass
class Assign:
       def __init__(self,token,expr):
              self.token=token
              self.expr=expr
       def accept(self,vis):
            return vis.visAssign(self)
class Var_expression:
       def __init__(self,name):
             self.name=name
       def accept(self,vis):
            return vis.visitorvar(self)
class Groupping:
     def __init__(self,expression):
        self.expression=expression 
     def accept(self,vis):
          return vis.vst_grouppinExpre(self)     
class Binary:
     def __init__(self,left,operator,right):
         self.left=left
         self.operator=operator
         self.right=right
     def accept(self,vis):
          return vis.visit_binary_oper(self)
class Litteral:
      def __init__(self,value):
        self.value=value
      def accept(self,vis):
            return vis.vst_litteralExpre(self)
class Unary:
    def __init__(self,operator,right):
       self.operator=operator
       self.right=right
    def accept(self,vis):
         return vis.vst_unaryexpre(self)
class Logical:
      def __init__(self,expr_left,operator,expr_right):
           self.left=expr_left
           self.operator=operator
           self.right=expr_right
      def accept(self,vis):
         return vis.vst_logical(self)
class Stmt:
      class Bloc:
            def __init__(self,instructions):
                self.instructions=instructions
            def accept(self,vis): 
                return vis.visBlocsStmt(self)
      class Expression:
           def __init__(self,expression):
               self.expression=expression
           def accept(self,vis):
                 return vis.visitorExpressionStmt(self)
      class Print:
            def __init__(self,expression):
                 self.expression=expression
            def accept(self,vis): 
                 return vis.visitorPrintStmt(self)
      class Var:
            def __init__(self,name,initializer):
                   self.name=name
                   self.initializer=initializer
            def  accept(self,vis):
                 return vis.visitorVarStmt(self)
      class ifsmt: 
            def __init__(self,expr,if_statement,else_statement):
                   self.expr=expr
                   self.if_statement=if_statement
                   self.else_statement=else_statement
            def accept(self,vis):
                  return vis.visitor_ifstatement(self)
      class whileStmt:
            def __init__(self,expr,stmt):
                 self.expr=expr
                 self.stmt=stmt
            def accept(self,vis):
                  return vis.visitor_whilestatement(self)            
class Parser :
    def __init__(self,tokens):
       self.tokens=tokens
       self.current=0
    def peek(self):
        return self.tokens[self.current]
    def end(self):
        return self.peek().Type==TokenType.EOF
    def previous(self): 
        return self.tokens[self.current-1]
    def advance(self): 
        if not self.end(): 
           self.current+=1
        return self.previous()
    def checker(self,Type):
        if self.end():return False
        return self.peek().Type==Type
    def match(self,*types):
         for type in types:
            if self.checker(type): 
                 self.advance()
                 return True
         return False
    def unary(self):
        if self.match(TokenType.BANG,TokenType.MINUS):
               operator=self.previous() 
               right=self.unary()
               return Unary(operator,right)
        return self.primary()
    def factor(self):  
           expression=self.unary()
           while  self.match(TokenType.STAR,TokenType.SLASH):
                operator=self.previous()
                right_expression=self.unary() 
                expression=Binary(expression,operator,right_expression)
           return expression
    def term(self):
        expression=self.factor()
        while self.match(TokenType.PLUS,TokenType.MINUS):
              operator=self.previous()
              right_expresion=self.factor()
              expression=Binary(expression,operator,right_expresion)
        return expression
    def comparison(self):
          expression=self.term()
          while self.match(TokenType.GREATER_EQUAL,TokenType.BANG_EQUAL,TokenType.GREATER,TokenType.LESS,TokenType.LESS_EQUAL):
              operator=self.previous()
              right_expression=self.term()
              expression=Binary(expression,operator,right_expression)   
          return expression
    def equality(self):
        expression=self.comparison()
        while self.match(TokenType.BANG_EQUAL,TokenType.EQUAL_EQUAL):
              operator=self.previous()
              right_expression=self.comparison()
              expression=Binary(expression,operator,right_expression)
        return expression
    def AND(self):
         expression=self.equality()
         while  self.match(TokenType.AND):
                operator=self.previous()
                right_expresion=self.equality()
                expression=Logical(expression,operator,right_expresion)
         return expression
    def Or(self):
        expression=self.AND()
        while self.match(TokenType.OR):
              operator=self.previous()
              right_expresion=self.AND
              expression=Logical(expression,operator,right_expresion)
        return expression 
    def assign(self):
           expr=self.Or()
           if self.match(TokenType.EQUAL):
                equals=self.previous()
                value=self.assign()
                if isinstance(expr,Var_expression):
                     return Assign(expr.name,value)
                self.error(equals,"Invalid assignement")
           return expr
    def expression(self):
       return  self.assign()
    def error(self,token,message):
         Error.error_token(token,message)
         return ParseError()
    def consume(self,token_type,message):
        if self.checker(token_type):return self.advance()
        raise self.error(self.peek(),message)
    def synchronize(self):
         self.advance()
         while not self.end():
               if self.previous().type==TokenType.SEMICOLON: return
               nxt_token=self.peek().type
               match nxt_token:
                      case TokenType.CLASS |TokenType.FUN |TokenType.VAR|TokenType.FOR|TokenType.IF |TokenType.WHILE|TokenType.PRINT|TokenType.RETURN: return;
               self.advance()
    def primary(self):
         if self.match(TokenType.IDENTIFIER):
              return Var_expression(self.previous())
         if self.match(TokenType.TRUE):return Litteral(True)
         if self.match(TokenType.FALSE): return Litteral(False)
         if self.match(TokenType.NIL):return Litteral(None)
         if self.match(TokenType.NUMBER,TokenType.STRING):return Litteral(self.previous().litteral)
         if self.match(TokenType.LEFT_PAREN):
             expr=self.expression()
             self.consume(TokenType.RIGHT_PAREN,"Expect ')' after expression.")
             return Groupping(expr)  
         raise self.error(self.peek(),"Except expression")
    def printStmt(self):
         value=self.expression()
         self.consume(TokenType.SEMICOLON,"Except ';' after value")
         return Stmt.Print(value)
    def expressionStmt(self):
          expr=self.expression()
          self.consume(TokenType.SEMICOLON,"Except ';' after value")
          return Stmt.Expression(expr)
    def whileStatement(self):
          self.consume(TokenType.LEFT_PAREN,"Except '(' after while loop")
          expr=self.expression()
          self.consume(TokenType.RIGHT_PAREN,"Except ')' after conditon")
          statement_while=self.statement()
          return  Stmt.whileStmt(expr,statement_while)
    def blocStmt(self):
          instructions=[]
          while not self.checker(TokenType.RIGHT_BRACE) and not self.end():
                instructions.append(self.declaration())
          self.consume(TokenType.RIGHT_BRACE,"Except '}' after bloc")
          return instructions
    def ifstmt(self): 
         self.consume(TokenType.LEFT_PAREN,"Except '(' after if condition ")
         expr=self.expression()
         self.consume(TokenType.RIGHT_PAREN,"Except ')' after if condition")
         statement_if=self.statement()
         statement_else=None
         if self.match(TokenType.ELSE):
            statement_else=self.statement()
         return Stmt.ifsmt(expr,statement_if,statement_else)
    def statement(self):
          if self.match(TokenType.PRINT):return self.printStmt()
          if self.match(TokenType.LEFT_BRACE): return Stmt.Bloc(self.blocStmt())
          if self.match(TokenType.IF) :return self.ifstmt()
          if self.match(TokenType.WHILE):return self.whileStatement()
          if self.match(TokenType.FOR): return self.forstatament()
          return self.expressionStmt()
    def var_declaration(self):
        name=self.consume(TokenType.IDENTIFIER,"Except variable name ")
        initalizer=None
        if self.match(TokenType.EQUAL):
              initalizer=self.expression()
        self.consume(TokenType.SEMICOLON,"Except ';' after value")
        return Stmt.Var(name,initalizer)
    def forstatament(self):
           self.consume(TokenType.LEFT_PAREN,"Except '(' after 'for' . ")
           if self.match(TokenType.SEMICOLON):
                 initializer=None
           elif self.match(TokenType.VAR):
                 initializer=self.var_declaration()
           else:
               initializer=self.expressionStmt()
           condition=None
           if not self.checker(TokenType.SEMICOLON):
                 condition=self.expression()
           self.consume(TokenType.SEMICOLON,"Except ';' after loop condition") 
           increment=None
           if not self.checker(TokenType.RIGHT_PAREN):
                  increment=self.expression()
           self.consume(TokenType.RIGHT_PAREN,"')' after for clauses")
           body=self.statement()
           if  increment :
                body=Stmt.Bloc([body,Stmt.Expression(increment)])
           if not condition:
                 condition=Litteral(True) 
           body=Stmt.whileStmt(condition,body)
           if initializer:
                 body=Stmt.Bloc([initializer,body])
           return body                 
    def declaration(self):
           if self.match(TokenType.VAR):
                 return self.var_declaration()
           return self.statement()
    def parse(self): # program->declatation *EOF 
      try :
        declarations=[]
        while not self.end():
          declarations.append(self.declaration())
        return declarations
      except ParseError :
             pass  

        