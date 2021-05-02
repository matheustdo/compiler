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

    def assign(self):
        if self.eat_lexeme('='):
            if self.eat_lexeme(';'):
                self.add_error('Expected `Expression` and found `;`.')  
            else:
                self.expr()
                
                if self.eat_lexeme(';'):
                    self.add_error(';')  
        elif self.eat_lexeme('++') or self.eat_lexeme('--'):
            if not self.eat_lexeme(';'):
                self.add_error(';')  
        else:
            self.add_error('=, ++, --')


    def access(self):
        if self.eat_lexeme('.'):
            if self.eat_code(Code.IDENTIFIER):
                self.arrays()
            else:
                self.add_error('Id')
        else:
            self.add_error('.')
            
    def accesses(self):
        if self.eat_lexeme('.'):
            if self.eat_code(Code.IDENTIFIER):
                self.arrays()
                self.accesses()
            else:
                self.add_error('Id')

    def args_list(self):
        if self.eat_lexeme(','):
            self.expr()
            self.args_list()
            
    def args(self):
        if self.token.lexeme != ')':
            self.expr()
            self.args_list()

    def id_value(self):
        if self.eat_lexeme('('):
            self.args()

            if not self.eat_lexeme(')'):
                self.add_error(')')
        else:
            self.arrays()
            self.accesses()

    def unary(self):
        if self.eat_lexeme('!'): 
            self.unary()
        elif self.eat_lexeme('local'):
            self.access()
        elif self.eat_lexeme('global'):
            self.access()
        elif self.eat_code(Code.IDENTIFIER):
            self.id_value()
        elif self.eat_lexeme('('):
            self.expr()

            if not self.eat_lexeme(')'):
                self.add_error(')')
        elif not (self.eat_code(Code.NUMBER) or self.eat_code(Code.STRING) or
            self.eat_lexeme('true') or self.eat_lexeme('false')):
            self.add_error('Num`, `Str` or `Boolean')

    def mult_2(self):
        if self.eat_lexeme('*'):
            self.unary()
            self.mult_2()
        elif self.eat_lexeme('/'):
            self.unary()
            self.mult_2()

    def mult_(self):
        self.unary()
        self.mult_2()

    def add_2(self):
        if self.eat_lexeme('+'):
            self.mult_()
            self.add_2()
        elif self.eat_lexeme('-'):
            self.mult_()
            self.add_2()

    def add_(self):
        self.mult_()
        self.add_2()

    def compare_2(self):
        if self.eat_lexeme('<'):
            self.add_()
            self.compare_2()
        elif self.eat_lexeme('>'):
            self.add_()
            self.compare_2()
        elif self.eat_lexeme('<='):
            self.add_()
            self.compare_2()
        elif self.eat_lexeme('>='):
            self.add_()
            self.compare_2()

    def compare_(self):
        self.add_()
        self.compare_2()

    def equate_2(self):
        if self.eat_lexeme('=='):
            self.compare_()
            self.equate_2()
        elif self.eat_lexeme('!='):
            self.compare_()
            self.equate_2()

    def equate_(self):
        self.compare_()
        self.equate_2()

    def and_2(self):
        if self.eat_lexeme('&&'):
            self.equate_()
            self.and_2()

    def and_(self):
        self.equate_()
        self.and_2()
            
    def or_2(self):
        if self.eat_lexeme('||'):
            self.and_()
            self.or_2()

    def or_(self):
        self.and_()
        self.or_2()

    def expr(self):
        self.or_()

    def arrays(self):
        if self.eat_lexeme('['):
            if not self.eat_lexeme(']'):
                self.expr()
            
                if self.eat_lexeme(']'):
                    self.arrays()
                else:
                    self.add_error(']')

    def var(self):
        if self.eat_code(Code.IDENTIFIER):
            self.arrays()
        else:
            self.add_error('Id')
            
    def var_list(self):
        if self.eat_lexeme(','):
            if self.eat_code(Code.IDENTIFIER):
                self.arrays()
                self.var_list()
            else:
                self.add_error('Id')

    def var_decls(self):
        if self.eat_type():
            self.var()
            self.var_list() 

            if self.eat_lexeme(';'):
                self.var_decls()
            else:
                self.add_error(';')
        elif self.eat_lexeme('typedef'): 
            if self.eat_type():
                if self.eat_code(Code.IDENTIFIER):
                    if self.eat_lexeme(';'):
                        self.var_decls()
                    else:
                        self.add_error(';')
                else:
                    self.add_error('Id')
            else:
                self.add_error('Type')

    def var_block(self):
        if self.eat_lexeme('var'):
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
        self.var_block()
        if self.eat_lexeme(''):
            print()
        else:   
            self.add_custom_error('The procedure `start` has not found.')

    def execute(self):
        self.program()
        