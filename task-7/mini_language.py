class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})" if self.value is not None else self.type

KEYWORDS = {"fn", "let", "if", "return", "print"}

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def peek(self):
        return self.text[self.pos] if self.pos < len(self.text) else None

    def advance(self):
        self.pos += 1

    def tokenize(self):
        tokens = []
        while self.pos < len(self.text):
            ch = self.peek()

            if ch.isspace():
                self.advance()

            elif ch.isdigit():
                tokens.append(self.number())

            elif ch.isalpha():
                tokens.append(self.identifier())

            elif ch == '"':
                tokens.append(self.string())

            elif ch == '+':
                tokens.append(Token("PLUS")); self.advance()
            elif ch == '-':
                tokens.append(Token("MINUS")); self.advance()
            elif ch == '*':
                tokens.append(Token("STAR")); self.advance()
            elif ch == '/':
                tokens.append(Token("SLASH")); self.advance()
            elif ch == '(':
                tokens.append(Token("LPAREN")); self.advance()
            elif ch == ')':
                tokens.append(Token("RPAREN")); self.advance()
            elif ch == '{':
                tokens.append(Token("LBRACE")); self.advance()
            elif ch == '}':
                tokens.append(Token("RBRACE")); self.advance()
            elif ch == ',':
                tokens.append(Token("COMMA")); self.advance()
            elif ch == '=':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    tokens.append(Token("EQ"))
                else:
                    tokens.append(Token("ASSIGN"))
            elif ch == '<':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    tokens.append(Token("LTE"))
            else:
                raise Exception(f"Unknown character: {ch}")

        tokens.append(Token("EOF"))
        return tokens

    def number(self):
        num = ""
        while self.peek() and self.peek().isdigit():
            num += self.peek()
            self.advance()
        return Token("INT", int(num))

    def identifier(self):
        ident = ""
        while self.peek() and self.peek().isalnum():
            ident += self.peek()
            self.advance()

        if ident in KEYWORDS:
            return Token(ident.upper())
        return Token("IDENT", ident)

    def string(self):
        self.advance()
        s = ""
        while self.peek() != '"':
            s += self.peek()
            self.advance()
        self.advance()
        return Token("STRING", s)

class Program:
    def __init__(self, statements):
        self.statements = statements

class FunctionDecl:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class LetDecl:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class IfStmt:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ReturnStmt:
    def __init__(self, value):
        self.value = value

class PrintStmt:
    def __init__(self, expr):
        self.expr = expr

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Literal:
    def __init__(self, value):
        self.value = value

class Identifier:
    def __init__(self, name):
        self.name = name

class CallExpr:
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def eat(self, type_):
        token = self.current()
        if token.type == type_:
            self.pos += 1
            return token
        raise Exception(f"Expected {type_}, got {token.type}")

    def parse(self):
        statements = []
        while self.current().type != "EOF":
            statements.append(self.statement())
        return Program(statements)

    def statement(self):
        tok = self.current()

        if tok.type == "FN":
            return self.function_decl()
        elif tok.type == "LET":
            return self.let_decl()
        elif tok.type == "IF":
            return self.if_stmt()
        elif tok.type == "RETURN":
            self.eat("RETURN")
            return ReturnStmt(self.expression())
        elif tok.type == "PRINT":
            self.eat("PRINT")
            return PrintStmt(self.expression())
        else:
            return self.expression()

    def function_decl(self):
        self.eat("FN")
        name = self.eat("IDENT").value
        self.eat("LPAREN")

        params = []
        if self.current().type != "RPAREN":
            params.append(self.eat("IDENT").value)
            while self.current().type == "COMMA":
                self.eat("COMMA")
                params.append(self.eat("IDENT").value)

        self.eat("RPAREN")
        self.eat("LBRACE")

        body = []
        while self.current().type != "RBRACE":
            body.append(self.statement())

        self.eat("RBRACE")
        return FunctionDecl(name, params, body)

    def let_decl(self):
        self.eat("LET")
        name = self.eat("IDENT").value
        self.eat("ASSIGN")
        value = self.expression()
        return LetDecl(name, value)

    def if_stmt(self):
        self.eat("IF")
        condition = self.expression()
        self.eat("LBRACE")

        body = []
        while self.current().type != "RBRACE":
            body.append(self.statement())

        self.eat("RBRACE")
        return IfStmt(condition, body)

    def expression(self):
        return self.equality()

    def equality(self):
        node = self.term()
        while self.current().type in ("PLUS", "MINUS", "LTE"):
            op = self.eat(self.current().type).type
            right = self.term()
            node = BinOp(node, op, right)
        return node

    def term(self):
        tok = self.current()

        if tok.type == "INT":
            self.eat("INT")
            return Literal(tok.value)

        elif tok.type == "STRING":
            self.eat("STRING")
            return Literal(tok.value)

        elif tok.type == "IDENT":
            name = self.eat("IDENT").value
            if self.current().type == "LPAREN":
                self.eat("LPAREN")
                args = []
                if self.current().type != "RPAREN":
                    args.append(self.expression())
                    while self.current().type == "COMMA":
                        self.eat("COMMA")
                        args.append(self.expression())
                self.eat("RPAREN")
                return CallExpr(name, args)
            return Identifier(name)

        elif tok.type == "LPAREN":
            self.eat("LPAREN")
            expr = self.expression()
            self.eat("RPAREN")
            return expr

        raise Exception("Invalid syntax")

class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def get(self, name):
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name)
        raise Exception(f"Undefined variable {name}")

    def set(self, name, value):
        self.values[name] = value

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.global_env.set("str", lambda x: str(x))

    def visit(self, node, env):
        method = getattr(self, f"visit_{type(node).__name__}")
        return method(node, env)

    def interpret(self, program):
        for stmt in program.statements:
            self.visit(stmt, self.global_env)

    def visit_Program(self, node, env):
        self.interpret(node)

    def visit_FunctionDecl(self, node, env):
        env.set(node.name, node)

    def visit_LetDecl(self, node, env):
        value = self.visit(node.value, env)
        env.set(node.name, value)

    def visit_IfStmt(self, node, env):
        if self.visit(node.condition, env):
            for stmt in node.body:
                self.visit(stmt, env)

    def visit_ReturnStmt(self, node, env):
        raise ReturnException(self.visit(node.value, env))

    def visit_PrintStmt(self, node, env):
        print(self.visit(node.expr, env))

    def visit_BinOp(self, node, env):
        left = self.visit(node.left, env)
        right = self.visit(node.right, env)

        if node.op == "PLUS":
            return left + right
        elif node.op == "MINUS":
            return left - right
        elif node.op == "LTE":
            return left <= right

    def visit_Literal(self, node, env):
        return node.value

    def visit_Identifier(self, node, env):
        return env.get(node.name)

    def visit_CallExpr(self, node, env):
        func = env.get(node.name)

        if callable(func):
            args = [self.visit(arg, env) for arg in node.args]
            return func(*args)

        new_env = Environment(parent=env)

        for param, arg in zip(func.params, node.args):
            new_env.set(param, self.visit(arg, env))

        try:
            for stmt in func.body:
                self.visit(stmt, new_env)
        except ReturnException as r:
            return r.value


code = '''
fn fibonacci(n) {
    if n <= 1 {
        return n
    }
    return fibonacci(n - 1) + fibonacci(n - 2)
}

let result = fibonacci(10)
print("Fibonacci(10) = " + str(result))
'''

lexer = Lexer(code)
tokens = lexer.tokenize()

print("=== TOKENS ===")
print(tokens)

parser = Parser(tokens)
ast = parser.parse()

print("=== OUTPUT ===")
interpreter = Interpreter()
interpreter.interpret(ast)