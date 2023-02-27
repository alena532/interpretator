from lexical_analysis.lexer import Lexer
from lexical_analysis.token_type import *

class Compute:
    def __init__(self,code):
        self.tokens = []
        self.variable_table = {}
        self.constants_table = {}
        self.key_words_table={}
        self.operator_table={}
        self.code=code

    def const_table(self,token):
        if(self.constants_table.get(token.value) != None):
            self.constants_table[token.value][1] +=1
        elif token.type == INTEGER_CONST:
            self.constants_table[token.value]=['int constant',1]
        elif token.type == REAL_CONST:
            self.constants_table[token.value] = ['real constant',1]
        elif token.type == CHAR_CONST:
            self.constants_table[token.value] = ['char constant', 1]

    def initializing_key_words(self):
        self.key_words_table = {
            'char': ['variables type',0],
            'int': ['variables type',0],
            'float': ['variables type',0],
            'double': ['variables type',0],
            'if': ['condition statement',0],
            'else': ['condition statement',0],
            'for': ['loop statement',0],
            'while': ['loop statement',0],
            'do': ['loop statement',0],
            'return': ['statement',0],
            'break': ['condition statement',0],
            'continue': ['condition statement',0],
            'void': ['function type',0],
            'cin': ['input statement',0],
            'cout': ['output statement',0],
            'using': ['namespace',0],
            'include': ['library statement',0]
        }

    def initializing_operators(self):
        self.operator_table = {
            '-': ['arithmetic operator',0],
            '+': ['arithmetic operator',0],
            '/': ['arithmetic operator',0],
            '%': ['arithmetic operator',0],
            '*': ['arithmetic operator',0],
            '!': ['condition statement',0],
            '=': ['arithmetic operator',0],
            '>': ['arithmetic operator',0],
            '<': ['arithmetic operator',0],
            '!=': ['comparison operator',0],
            '==': ['comparison operator',0],
            '<=': ['comparison operator',0],
            '>=': ['comparison operator',0],
            '||': ['comparison operator',0],
            '&&': ['comparison operator',0],
            '--': ['arithmetic operator',0],
            '++': ['arithmetic operator', 0],
            '+=': ['arithmetic operator',0],
            '-=': ['arithmetic operator', 0],
            '*=': ['arithmetic operator', 0],
            '/=': ['arithmetic operator', 0],
            '%=': ['arithmetic operator', 0]
        }


    def tokenize(self):
        lexer = Lexer(self.code)
        self.initializing_key_words()
        self.initializing_operators()
        lexer.get_next_token
        self.tokens.append(lexer.current_token)
        while lexer.peek(1)!= None:
            if lexer.current_token.type == HASH:
                if lexer.get_next_token.type == INCLUDE:
                    self.tokens.append(lexer.current_token)
                    if lexer.get_next_token.type == LT_OP:
                        self.tokens.append(lexer.current_token)
                        if lexer.get_next_token.type == ID:
                            self.tokens.append(lexer.current_token)
                            library_name = lexer.current_token.value
                            if lexer.get_next_token.type == GT_OP:
                                self.tokens.append(lexer.current_token)
                                lexer.get_next_token
            if lexer.current_token.value == 'using':
                lexer.get_next_token
                lexer.get_next_token

            elif lexer.get_next_token.type == ID:
                if self.tokens[-1].type not in (CHAR,INT, FLOAT, DOUBLE, VOID):
                    if self.variable_table.get(lexer.current_token.value) == None:
                        print("Invalid char {} at line {} at position {}".format(lexer.current_token.value, lexer.line,lexer.line_position-len(lexer.current_token.value)))
                self.tokens.append(lexer.current_token)
                if lexer.get_next_token.type == ASSIGN:
                    if self.variable_table.get(self.tokens[-1].value) == None:
                        self.variable_table[self.tokens[-1].value]=self.tokens[-2].type
            self.tokens.append(lexer.current_token)

            if lexer.current_token.type == INTEGER_CONST or lexer.current_token.type == CHAR_CONST or lexer.current_token.type == REAL_CONST:
                self.const_table(lexer.current_token)
            elif self.key_words_table.get(lexer.current_token.value) != None:
                self.key_words_table[lexer.current_token.value][1] =self.key_words_table[lexer.current_token.value][1]+1
            elif self.operator_table.get(lexer.current_token.value) != None:
                if self.operator_table.get(self.tokens[-2].value)!=None:
                    self.operator_table.__delitem__(self.tokens[-2].value)
                    print("Invalid char {} at line {} at position {}".format(self.tokens[-2].value+self.tokens[-1].value, lexer.line,
                                                                             lexer.line_position - len(
                                                                                 lexer.current_token.value)- len(
                                                                                 self.tokens[-2].value)))
                else:
                    self.operator_table[lexer.current_token.value][1] = self.operator_table[lexer.current_token.value][1] + 1

        print("-------")
        print('variable table')
        print("-------")
        print("{:<8} {:<15}".format('Name', 'Type'))
        for key,value in self.variable_table.items():
            print("{:<8} {:<15}".format(key, value))

        print("-------")
        print('constants table')
        print("-------")
        print("{:<8} {:<15} {:<18}".format('Name', 'Type','Amount'))
        for key, value in self.constants_table.items():
            print("{:<8} {:<15} {:<18}".format(key,value[0], value[1]))

        print("-------")
        print('key words table')
        print("-------")
        print("{:<8} {:<15}  {:<18}".format('Name', 'Type', 'Amount'))
        for key, value in self.key_words_table.items():
            if (value[1] != 0):
                print("{:<8} {:<15}    {:<2}".format(key, value[0],value[1]))

        print("-------")
        print('operators table')
        print("-------")
        print("{:<8} {:<15}   {:<18}".format('Name', 'Type', 'Amount'))
        for key, value in self.operator_table.items():
            if(value[1]!=0):
                print("{:<8} {:<15}   {:<18}".format(key, value[0], value[1]))

if __name__ == '__main__':
    f = open("example.cpp", "r")
    code = f.read()
    compute=Compute(code)
    compute.tokenize()


