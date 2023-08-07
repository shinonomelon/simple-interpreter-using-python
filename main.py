class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

# Token types
INTEGER, FLOAT, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = (
    "INTEGER", "FLOAT", "PLUS", "MINUS", "MUL", "DIV", "LPAREN", "RPAREN", "EOF"
)

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self, msg):
        raise Exception(msg)

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def number(self):
        result = ""
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()

        if '.' in result:
            return float(result)
        else:
            return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
                continue
            if self.current_char == '-' and (self.text[self.pos + 1].isdigit() or self.text[self.pos + 1] == '.'):
                self.advance()  # Move to the number part
                return Token(INTEGER if '.' not in self.text[self.pos:] else FLOAT, -self.number())
            if self.current_char.isdigit() or self.current_char == '.':
                return Token(INTEGER if '.' not in self.text[self.pos:] else FLOAT, self.number())
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error(f"Invalid character: {self.current_char}")

        return Token(EOF, None)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type in (INTEGER, FLOAT):
            self.eat(token.type)
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result

    def term(self):
        result = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result *= self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                result /= self.factor()
        return result

    def expr(self):
        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result -= self.term()
        return result

def interpret(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    return parser.expr()

# Test
test_input = input("計算式を入力して：")
result = interpret(test_input)
print(f"結果: {result}")
