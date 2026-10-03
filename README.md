# Zoo Programming Language
<img width="200" height="200" alt="zoo (4)" src="https://github.com/user-attachments/assets/a48b77af-5dc8-459c-b3a5-c3c13364d9f1">

* Zoo is an experimental programming language I am building for educational purposes
## Language Structure
``` mermaid
flowchart LR
   A[Source Code] -->Lexer
   Lexer --> Parser
   Parser --> Evaluate
```

## Grammatical rules
```text
  programm-> declaration* EOF
  declaration -> statement|var_declaration
  var_declaration -> "var" IDENTIFIER ("=" expression)? ";" ;
  -------------------------------------------------------------------------->
  statement      → exprStmt 
               | ifStmt
               | printStmt
               | whileStmt
               | blockStmt ;
  --------------------------------------------------------------------------->
  exprStmt -> expression ";" ;
  ifStmt  ->  "if" "(" expression ")" statement ("else" statement)?;
  printStmt -> "print" expression  ;
  whileStmt -> "while" "(" expression ")"  statement ; 
  blockStmt-> "{"declaration*"}"
  ----------------------------------------------------------------------------->
  expression    -> asign;
  asign -> IDENTIFIER  "=" asign | Or_LG;
  Or_LG  -> AND_LG ("or" AND_LG);
  AND_LG -> equality ("and" equality)*;
  equality       → comparison ( ( "!=" | "==" ) comparison )* ;
  comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
  term           → factor ( ( "-" | "+" ) factor )* ;
  factor         → unary ( ( "/" | "*" ) unary )* ; 
  unary          → ( "!" | "-" ) unary | primary ;
  primary        → NUMBER | STRING | "true" | "false" | "nil";
               | "(" expression ")" ;

```
