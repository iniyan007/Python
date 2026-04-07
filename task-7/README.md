# 🧠 Mini Language Interpreter (Python)

## 📌 Overview

This project implements a **custom interpreter for a mini programming language** using Python. It includes all major components of a compiler pipeline:

* Lexer (Tokenizer)
* Parser (Recursive Descent)
* AST (Abstract Syntax Tree)
* Interpreter (Tree-walking execution)

The language supports:

* Variables (`let`)
* Functions (`fn`)
* Conditionals (`if`)
* Arithmetic operations
* Recursion
* Built-in functions (`print`, `str`)

---

## 🏗️ Architecture

```text
Source Code
   ↓
Lexer → Tokens
   ↓
Parser → AST
   ↓
Interpreter → Output
```

---

## 🔤 1. Lexer (Lexical Analysis)

### 📌 Purpose

Converts raw source code into a list of tokens.

### ✅ Supported Tokens

* Keywords: `fn`, `let`, `if`, `return`, `print`
* Identifiers: variable/function names
* Literals: integers, strings
* Operators: `+`, `-`, `*`, `/`, `<=`
* Symbols: `(` `)` `{` `}` `,` `=`

### 🧪 Example

#### Input:

```txt
let x = 5 + 3
```

#### Output:

```txt
[LET, IDENT(x), ASSIGN, INT(5), PLUS, INT(3)]
```

---

## 🌳 2. AST (Abstract Syntax Tree)

### 📌 Purpose

Represents the structure of the program in a tree format.

### ✅ Node Types

* `Program`
* `FunctionDecl`
* `LetDecl`
* `IfStmt`
* `ReturnStmt`
* `PrintStmt`
* `BinOp`
* `Literal`
* `Identifier`
* `CallExpr`

### 🧪 Example

Expression:

```txt
5 + 3
```

AST:

```text
BinOp(5, +, 3)
```

---

## 🧱 3. Parser (Recursive Descent)

### 📌 Purpose

Converts tokens into an AST.

### 🔑 Key Features

* Recursive descent parsing
* Handles function definitions
* Supports nested expressions
* Builds structured AST nodes

### 🧪 Example

#### Input Tokens:

```txt
[IDENT(fibonacci), LPAREN, INT(10), RPAREN]
```

#### Output AST:

```text
CallExpr("fibonacci", [10])
```

---

## 🏠 4. Environment (Scope Management)

### 📌 Purpose

Stores variables and function definitions.

### 🔑 Features

* Nested scope using parent environments
* Supports recursion
* Variable lookup with fallback to parent

### 🧪 Example

```python
env = {
    "x": 10,
    "fibonacci": <function>
}
```

---

## 🔄 5. Interpreter (Execution Engine)

### 📌 Purpose

Executes the AST by traversing it.

### 🔑 Features

* Visitor pattern (`visit_*` methods)
* Supports:

  * Arithmetic operations
  * Function calls
  * Conditionals
  * Recursion
* Built-in functions:

  * `print()`
  * `str()`

---

## 🔥 Function Execution Flow

1. Function is stored in environment
2. On call:

   * New environment is created
   * Arguments are assigned to parameters
3. Function body is executed
4. `ReturnException` is used to return values

---

## 🔁 Recursion Support

Recursion works using:

```python
new_env = Environment(parent=env)
```

This allows functions to call themselves by accessing the parent scope.

---

## 🧪 Example Program

```txt
fn fibonacci(n) {
    if n <= 1 {
        return n
    }
    return fibonacci(n - 1) + fibonacci(n - 2)
}

let result = fibonacci(10)
print("Fibonacci(10) = " + str(result))
```

---

## ▶️ Execution

Run the program:

```bash
python mini_language.py
```

---

## 📤 Output

```txt
=== TOKENS ===
[FN, IDENT(fibonacci), LPAREN, IDENT(n), RPAREN, LBRACE, IF, IDENT(n), LTE, INT(1), LBRACE, RETURN, IDENT(n), RBRACE, RETURN, IDENT(fibonacci), LPAREN, IDENT(n), MINUS, INT(1), RPAREN, PLUS, IDENT(fibonacci), LPAREN, IDENT(n), MINUS, INT(2), RPAREN, RBRACE, LET, IDENT(result), ASSIGN, IDENT(fibonacci), LPAREN, INT(10), RPAREN, PRINT, LPAREN, STRING(Fibonacci(10) = ), PLUS, IDENT(str), LPAREN, IDENT(result), RPAREN, RPAREN, EOF]
=== OUTPUT ===
Fibonacci(10) = 55
```

---

## 🧠 Key Concepts Used

* Lexical Analysis
* Recursive Descent Parsing
* Abstract Syntax Trees (AST)
* Visitor Pattern
* Scope & Environment Chains
* Recursion
* Tree Traversal
