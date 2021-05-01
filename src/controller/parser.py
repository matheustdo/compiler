from src.model.error_token import ErrorToken
from src.model.code import Code

'''
This class does the iteration on tokens array and the syntactic analysis.
'''
class Parser:
    def __init__(self, lexical_tokens):
        self.lexical_tokens = lexical_tokens
        self.tokens_index = 0
        self.token = None
        self.syntactic_tokens = []

        if len(lexical_tokens) > 0:
            self.token = lexical_tokens[0]

    def add_error(self, expected):
        error_token = ErrorToken(self.token.line_begin_index, f'Expected `{expected}` and found `{self.token.lexeme}`.')
        self.syntactic_tokens.append(error_token)

    def add_custom_error(self, message):
        error_token = ErrorToken(self.token.line_begin_index, message)
        self.syntactic_tokens.append(error_token)

    def advance(self):
        self.syntactic_tokens.append(self.token)
        self.tokens_index += 1
        
        if len(self.lexical_tokens) > 0:
            self.token = self.lexical_tokens[self.tokens_index]
        else:
            self.token = None

    def eat_lexeme(self, lexeme):
        if self.token and lexeme == self.token.lexeme:
            self.advance()
            return True

        return False

    def eat_code(self, code):
        if self.token and code == self.token.code:
            self.advance()
            return True

        return False

    def eat_type(self):
        if (self.eat_lexeme('int') or self.eat_lexeme('real') or
            self.eat_lexeme('boolean') or self.eat_lexeme('string')):
            return True
        if self.eat_lexeme('struct') and self.eat_code(Code.IDENTIFIER):
            return True

        return False

    def eat_first_expr(self):
        if (self.eat_lexeme('!') or self.eat_code(Code.NUMBER) or 
            self.eat_code(Code.STRING) or self.eat_lexeme('true') or
            self.eat_lexeme('false')):
            return True
        if self.eat_code(Code.IDENTIFIER) and self.eat_lexeme('('):
            return True

        return False

    def unary(self):
        if self.eat_lexeme('!'): 
            self.unary()
        elif not self.eat_first_expr():
            self.add_error('Value')            

    def mult_(self):
        if self.eat_lexeme('*'):
            self.unary()
            self.mult_()
        elif self.eat_lexeme('/'):
            self.unary()
            self.mult_()

    def add_(self):
        if self.eat_lexeme('+'):
            if self.eat_first_expr():
                self.mult_()
                self.add_()
            else:
                self.add_error('Expression')
        elif self.eat_lexeme('-'):
            if self.eat_first_expr():
                self.mult_()
                self.add_()
            else:
                self.add_error('Expression')
        else:
            self.mult_()

    def compare_(self):
        if self.eat_lexeme('<'):
            if self.eat_first_expr():
                self.add_()
                self.compare_()
            else:
                self.add_error('Expression')
        elif self.eat_lexeme('>'):
            if self.eat_first_expr():
                self.add_()
                self.compare_()
            else:
                self.add_error('Expression')
        elif self.eat_lexeme('<='):
            if self.eat_first_expr():
                self.add_()
                self.compare_()
            else:
                self.add_error('Expression')
        elif self.eat_lexeme('>='):
            if self.eat_first_expr():
                self.add_()
                self.compare_()
            else:
                self.add_error('Expression')
        else:
            self.add_()

    def equate_(self):
        if self.eat_lexeme('=='):
            if self.eat_first_expr():
                self.compare_()
                self.equate_()
            else:
                self.add_error('Expression')
        elif self.eat_lexeme('!='):
            if self.eat_first_expr():
                self.compare_()
                self.equate_()
            else:
                self.add_error('Expression')
        else:
            self.compare_()

    def and_(self):
        if self.eat_lexeme('&&'):
            if self.eat_first_expr():
                self.equate_()
                self.and_()
            else:
                self.add_error('Expression')
        else:
            self.equate_()

    def or_(self):
        if self.eat_lexeme('||'):
            if self.eat_first_expr():
                self.and_()
                self.or_()
            else:
                self.add_error('Expression')
        else:
            self.and_()


    def expr(self):
        if self.eat_first_expr():
            self.or_()

    def type_def(self):
        if self.eat_type():
            if self.eat_code(Code.IDENTIFIER):
                if not self.eat_lexeme(';'):
                    self.add_error(';')
            else:
                self.add_error('Id')
        else:
            self.add_error('Type.')

    def arrays(self):
        if self.eat_lexeme('['):
            self.expr()
            
            if self.eat_lexeme(']'):
                self.arrays()
            else:
                self.add_error(']')

    def var_list(self):
        if self.eat_lexeme(','):
            if self.eat_code(Code.IDENTIFIER):
                self.arrays()
                self.var_list()
            else:
                self.add_error('Id')

    def var_decls(self):
        if self.eat_type():
            if self.eat_code(Code.IDENTIFIER):
                self.arrays()
                self.var_list()

                if not self.eat_lexeme(';'):
                    self.add_error(';')
            else:
                self.add_error('Id')
            self.var_decls()
        elif self.eat_lexeme('typedef'):
            self.type_def()

    def var_block(self):
        if self.eat_lexeme('{'):
            self.var_decls()

            if not self.eat_lexeme('}'):
                self.add_error('}')
        else:
            self.add_error('{')

    def program(self):
        if self.eat_lexeme('structs'):
            print()
        if self.eat_lexeme('const'):
            print()
        if self.eat_lexeme('var'):
            self.var_block()
        if self.eat_lexeme(''):
            print()
        else:   
            self.add_custom_error('The procedure `start` has not found.')

    def execute(self):
        self.program()
        