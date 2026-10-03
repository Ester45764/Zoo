from TokenType import TokenType
from Eror import Error
class Token:
    def __init__(self,Type,lexeme,litteral,line):
      self.Type=Type
      self.lexeme=lexeme
      self.litteral=litteral 
      self.line=line
class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start=0
        self.current=0
        self.len_source=len(self.source)
        self.line=1
        self.keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE
        }
    def end(self): 
        return self.current>=self.len_source
    def nxt_cr_w(self):
       if self.end(): return "\0"
       return self.source[self.current]
    def addTokens(self,type,litteral):
        text=self.source[self.start:self.current]
        self.tokens.append(Token(type,text,litteral,self.line))
    def addToken_1(self,Type):  
        self.addTokens(Type,None)
    def next_caractere(self):
       cur_char=self.source[self.current]
       self.current+=1
       return cur_char
    def match(self,ch):
        if self.end():return False 
        verif=(self.source[self.current]==ch)
        if  verif:
            self.current+=1
        return verif  
    def String(self,c):
        while not self.end() and self.nxt_cr_w()!='"':
            c=self.next_caractere()
            if c=="\n":
             self.line+=1
        if self.end():
            Error.error(self.line,"Unterminated string")
            return
        self.next_caractere()
        self.addTokens(TokenType.STRING,self.source[self.start+1:self.current-1])
    def Number(self):
        while not self.end() and self.nxt_cr_w().isdigit():
            self.next_caractere()
        if not self.end() and self.nxt_cr_w() == ".":
            self.next_caractere() 
            while not self.end() and self.nxt_cr_w().isdigit():
               self.next_caractere()
        self.addTokens(TokenType.NUMBER,float(self.source[self.start:self.current]))
    def identifier_or_keywords(self):
        while self.nxt_cr_w().isalnum() or self.nxt_cr_w()=="_":
            self.current+=1
        word=self.source[self.start:self.current]
        if word in self.keywords:
           self.addToken_1(self.keywords[word])
        else:
           self.addToken_1(TokenType.IDENTIFIER)        
    def scantoken(self):
        c=self.next_caractere()
        if c.isdigit():
             self.Number()
             return
        if c.isalpha() or c=="_": 
            self.identifier_or_keywords()
            return
        match c: 
            case "!":  return self.addToken_1(TokenType.BANG_EQUAL) if self.match("=") else self.addToken_1(TokenType.BANG)
            case "(":return self.addToken_1(TokenType.LEFT_PAREN)
            case ")":return self.addToken_1(TokenType.RIGHT_PAREN)
            case "{":return self.addToken_1(TokenType.LEFT_BRACE) 
            case "}":return self.addToken_1(TokenType.RIGHT_BRACE)
            case "+":return self.addToken_1(TokenType.PLUS)
            case "-":return self.addToken_1(TokenType.MINUS)
            case ".":return self.addToken_1(TokenType.DOT)
            case ",":return self.addToken_1(TokenType.COMMA)
            case ";":return self.addToken_1(TokenType.SEMICOLON)
            case "*":return self.addToken_1(TokenType.STAR)
            case "=":return self.addToken_1(TokenType.EQUAL_EQUAL) if self.match("=") else self.addToken_1(TokenType.EQUAL)
            case "<":return self.addToken_1(TokenType.LESS_EQUAL) if self.match("=") else self.addToken_1(TokenType.LESS)
            case ">":return self.addToken_1(TokenType.GREATER_EQUAL) if self.match("=") else self.addToken_1(TokenType.GREATER)
            case "/": 
                if not self.match("/"): return self.addToken_1(TokenType.SLASH)
                while not self.end():
                    chr=self.next_caractere()
                    if chr=="\n":
                      self.line+=1
                      break
            case " ":
                 pass
            case "\t": 
                 pass
            case "\n":
                 self.line+=1 
                 pass
            case '"':
               self.String(c)
               pass
            case _:
                Error.error(self.line,"Unexpected character")
   
    def scanTokens(self):
        while not self.end():
          self.start=self.current
          self.scantoken()
        self.tokens.append(Token(TokenType.EOF,"",None,self.line))
        return  self.tokens

