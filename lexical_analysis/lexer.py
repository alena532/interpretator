from .token_type import *
from .token import Token

RESERVED_KEYWORDS = {
    'char': Token(CHAR, 'char'),
    'int': Token(INT, 'int'),
    'float': Token(FLOAT, 'float'),
    'double': Token(DOUBLE, 'double'),
    'if': Token(IF, 'if'),
    'else': Token(ELSE, 'else'),
    'for': Token(FOR, 'for'),
    'while': Token(WHILE, 'while'),
    'do': Token(DO, 'do'),
    'return': Token(RETURN, 'return'),
    'break': Token(BREAK, 'break'),
    'continue': Token(CONTINUE, 'continue'),
    'void': Token(VOID, 'void'), 
    'cin': Token(CIN,'cin'),
    'cout': Token(COUT,'cout'),
    'using': Token(NAMESPACE,'using'),
    'include': Token(INCLUDE,'include')
}

class Lexer(object):
    def __init__(self, text):
        self.text = text.replace('\\n', '\n')
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.line = 1
        self.line_position = 0
        self.current_token = 0

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.line_position +=1
            self.current_char = self.text[self.pos]

    def peek(self, n):
        peek_pos = self.pos + n
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == '\n':
                self.line += 1
                self.line_position = 0
            self.advance()

    def skip_comment(self):
        while self.current_char is not None:
            if self.current_char == '\n':
                self.line += 1
                self.line_position = 0
                self.advance()
                return
            self.advance()

    def skip_multiline_comment(self):
        while self.current_char is not None:
            if self.current_char == '*' and self.peek(1) == '/':
                self.advance()
                self.advance()
                return
            if self.current_char == '\n':
                self.line += 1
                self.line_position = 0
            self.advance()


    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += self.current_char
            self.advance()

            while (self.current_char is not None and self.current_char.isdigit()):
                result += self.current_char
                self.advance()

            self.current_token = Token(REAL_CONST, float(result))
        else:
            self.current_token = Token(INTEGER_CONST, int(result))

        return self.current_token

    def char(self):
        self.advance()
        char = self.current_char
        self.advance()
        self.advance()
        self.current_token = Token(CHAR_CONST, ord(char))
        return self.current_token

    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        self.current_token = RESERVED_KEYWORDS.get(result,Token(ID, result))
        return self.current_token

    @property
    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '/' and self.peek(1) == '/':
                self.skip_comment()
                continue

            if self.current_char == '/' and self.peek(1) == '*':
                self.skip_multiline_comment()
                continue

            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == '\'':
                return self.char()

            if self.current_char == '+' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.current_token = Token(ADD_ASSIGN, '+=')
                return self.current_token

            if self.current_char == '-' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.current_token = Token(SUB_ASSIGN, '-=')
                return self.current_token

            if self.current_char == '*' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.current_token = Token(MUL_ASSIGN, '*=')
                return self.current_token

            if self.current_char == '/' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.current_token = Token(DIV_ASSIGN, '/=')
                return self.current_token

            if self.current_char == '%' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.current_token = Token(MOD_ASSIGN, '%=')
                return self.current_token


            if self.current_char == '>' and self.peek(1) == '>':
                self.advance()
                self.advance()
                self.current_token = Token(STREAM, '>>')
                return self.current_token

            if self.current_char == '<' and self.peek(1) == '<':
                self.advance()
                self.advance()
                self.current_token = Token(STREAM, '<<')
                return self.current_token

            if self.current_char == '+' and self.peek(1) == '+':
                self.advance()
                self.advance()
                self.current_token = Token(INC_OP, '++')
                return self.current_token

            if self.current_char == '-' and self.peek(1) == '-':
                self.advance()
                self.advance()
                self.current_token = Token(DEC_OP, '--')
                return self.current_token

            if self.current_char == '&' and self.peek(1) == '&':
                self.advance()
                self.advance()
                self.current_token = Token(LOG_AND_OP, '&&')
                return self.current_token

            if self.current_char == '|' and self.peek(1) == '|':
                self.advance()
                self.advance()
                self.current_token = Token(LOG_OR_OP, '||')
                return self.current_token

            if self.current_char == '<' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.current_token = Token(LE_OP, '<=')
                return self.current_token

            if self.current_char == '>' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.current_token = Token(GE_OP, '>=')
                return self.current_token

            if self.current_char == '=' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.current_token = Token(EQ_OP, '==')
                return self.current_token

            if self.current_char == '!' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.current_token = Token(NE_OP, '!=')
                return self.current_token

            if self.current_char == '<':
                self.advance()
                self.current_token = Token(LT_OP, '<')
                return self.current_token

            if self.current_char == '>':
                self.advance()
                self.current_token = Token(GT_OP, '>')
                return self.current_token

            if self.current_char == '=':
                self.advance()
                self.current_token = Token(ASSIGN, '=')
                return self.current_token

            if self.current_char == '!':
                self.advance()
                return Token(LOG_NEG, '!')

            if self.current_char == '+':
                self.advance()
                return Token(ADD_OP, '+')

            if self.current_char == '-':
                self.advance()
                self.current_token = Token(SUB_OP, '-')
                return self.current_token

            if self.current_char == '*':
                self.advance()
                self.current_token = Token(MUL_OP, '*')
                return self.current_token

            if self.current_char == '/':
                self.advance()
                self.current_token = Token(DIV_OP, '/')
                return self.current_token

            if self.current_char == '%':
                self.advance()
                self.current_token = Token(MOD_OP, '%')
                return self.current_token

            if self.current_char == '(':
                self.advance()
                self.current_token = Token(LPAREN, '(')
                return self.current_token

            if self.current_char == ')':
                self.advance()
                self.current_token = Token(RPAREN, ')')
                return self.current_token

            if self.current_char == '{':
                self.advance()
                self.current_token = Token(LBRACKET, '{')
                return self.current_token

            if self.current_char == '}':
                self.advance()
                self.current_token = Token(RBRACKET, '}')
                return self.current_token

            if self.current_char == ';':
                self.advance()
                self.current_token = Token(SEMICOLON, ';')
                return self.current_token

            if self.current_char == ':':
                self.advance()
                self.current_token = Token(COLON, ':')
                return self.current_token

            if self.current_char == ',':
                self.advance()
                self.current_token = Token(COMMA, ',')
                return self.current_token

            if self.current_char == '.':
                self.advance()
                self.current_token = Token(DOT, '.')
                return self.current_token

            if self.current_char == '#':
                self.advance()
                self.current_token = Token(HASH, '#')
                return self.current_token

            if self.current_char == '?':
                self.advance()
                self.current_token = Token(QUESTION_MARK, '?')
                return self.current_token


        return Token(EOF, None)
