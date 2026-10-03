from TokenType import TokenType
from Eror import Error,RuntimeEror
from Environement import *
class Interpreter:
  def __init__(self):
      self.environement=Environnement()
  def checkNumberOperand(self,operator,operand):
     if isinstance(operand,float): return
     raise RuntimeEror(operator,"Operand must be a Number")
  def checkNumberOperands(self,operator,left,right):
        if isinstance(left,float) and isinstance(right,float):return
        raise RuntimeEror(operator,"Operands must be numbers!")
  def visBlocsStmt(self,stmt_bloc):
         self.excuteblock(stmt_bloc.instructions,Environnement(self.environement))
         return None
  def vst_logical(self):
      left=self.excute(self.left)
      if self.operator==TokenType.OR:
        if self.isTruthy(left):return left
      if self.operator==TokenType.AND:
          if self.isTruthy(left):return left
      return self.evaluate(self.right)

  def excuteblock(self,stmts,env):
     previous=self.environement
     try :
         self.environement=env
         for statement in stmts:
            self.excute(statement)
     finally:
         self.environement=previous
  def vst_litteralExpre(self,expr):
   return expr.value
  def evaluate(self,expr):
     return expr.accept(self)
  def vst_grouppinExpre(self,expr): 
    return self.evaluate(expr.expression)
  def isTruthy(self,var):
     if var is None:
       return False
     if isinstance(var,bool):
        return var
     return True
  def vst_unaryexpre(self,exp):
    right=self.evaluate(exp.right)
    operator_type=exp.operator.Type
    match operator_type: 
      case TokenType.MINUS:
          self.checkNumberOperand(operator_type,right)
          return -right
      case TokenType.BANG: 
         return not self.isTruthy(right)
    return None
  def isequal(self,a,b):
       return a==b
  def visit_binary_oper(self,exp):
      left=self.evaluate(exp.left)
      right=self.evaluate(exp.right)
      operator_type=exp.operator.Type
      match operator_type:
          case TokenType.PLUS:
              if (isinstance(left,str) and isinstance(right,str)) or (isinstance(left,float) and isinstance(right,float)):
                  return left+right
              raise RuntimeEror(operator_type,"Operands must be two numbers or two strings")
          case TokenType.MINUS:
            self.checkNumberOperands(operator_type,left,right)
            return left-right
          case TokenType.STAR:
             self.checkNumberOperands(operator_type,left,right)
             return left*right
          case TokenType.SLASH:
             self.checkNumberOperands(operator_type,left,right)
             return left/right
          case TokenType.GREATER:
             self.checkNumberOperands(operator_type,left,right)
             return left>right
          case TokenType.GREATER_EQUAL:
            self.checkNumberOperands(operator_type,left,right)
            return left>=right
          case TokenType.LESS:
            self.checkNumberOperands(operator_type,left,right)
            return left<right
          case TokenType.LESS_EQUAL:
            self.checkNumberOperands(operator_type,left,right)
            return left<=right
          case TokenType.BANG_EQUAL:
            return not self.isequal(left,right)
          case TokenType.EQUAL:
             return self.isequal(left,right)
      return None   
  def visitor_ifstatement(self,stmt):
      if self.isTruthy(self.evaluate(stmt.expr)):
          return self.excute(stmt.if_statement)
      if stmt.else_statement:
           return self.excute(stmt.else_statement)
      return None
  def visitorExpressionStmt(self,stmt):
        self.evaluate(stmt.expression)
        return None
  def visitor_whilestatement(self,Stmt):
      while self.evaluate(Stmt.expr):
          self.excute(Stmt.stmt) 
      return None
  def visAssign(self,exp):
      value=self.evaluate(exp.expr)
      self.environement.assign(exp.token,value)
      return value
  def stringfy(self,obj):
      if obj==None:
          return "nil"
      if isinstance(obj,float): 
         text=str(obj)
         if text.endswith(".0"):
            text=text[:-2]
         return text
      return str(obj)
  def visitorPrintStmt(self,stmt):
       value=self.evaluate(stmt.expression)
       print(self.stringfy(value))
       return None
  def visitorvar(self,expr_var):
      return  self.environement.get_value(expr_var.name) 
  def visitorVarStmt(self,stmt_var):
         value=None
         if stmt_var.initializer!=None:
            value=self.evaluate(stmt_var.initializer)
         self.environement.define(stmt_var.name.lexeme,value)
         return None
  def excute(self,stmt):
        stmt.accept(self)
  def interpret(self,statements):
    try:
      for statement in statements:
         self.excute(statement)
    except  RuntimeEror as eror:
        Error.runtimeError(eror)
