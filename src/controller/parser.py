from src.model.error_token import ErrorToken
from src.model.code import Code
from src.definitions.firsts import *

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
        if self.token is None:
            line = 0

            if len(self.lexical_tokens) > 0:
                line = self.syntactic_tokens[self.tokens_index - 1].line_begin_index
            
            error_token = ErrorToken(line, f'Expected `{expected}` and found `EOF`.')
            self.syntactic_tokens.append(error_token)
        else:
            error_token = ErrorToken(self.token.line_begin_index, f'Expected `{expected}` and found `{self.token.lexeme}`.')
            self.syntactic_tokens.append(error_token)

    def add_custom_error(self, message):
        if self.token is None:
            line = 0

            if len(self.lexical_tokens) > 0:
                line = self.syntactic_tokens[self.tokens_index - 1].line_begin_index
            
            error_token = ErrorToken(line, message)
            self.syntactic_tokens.append(error_token)
        else:
            error_token = ErrorToken(self.token.line_begin_index, message)
            self.syntactic_tokens.append(error_token)

    def advance(self):
        self.syntactic_tokens.append(self.token)
        self.tokens_index += 1
        
        if len(self.lexical_tokens) > 0 and self.tokens_index < len(self.lexical_tokens):
            self.token = self.lexical_tokens[self.tokens_index]
        else:
            self.token = None

    def eat_lexeme(self, lexeme):
        if self.token is not None and self.token and lexeme == self.token.lexeme:
            self.advance()
            return True

        return False

    def eat_code(self, code):
        if self.token is not None and self.token and code == self.token.code:
            self.advance()
            return True

        return False
        
    def eat_type(self):
        if (self.eat_lexeme('int') or self.eat_lexeme('real') or
            self.eat_lexeme('boolean') or self.eat_lexeme('string')):
            return True
        if self.eat_lexeme('struct'):
            if self.eat_code(Code.IDENTIFIER):
                return True
            self.add_error('Id')

        return False

    def verify(self, first):
        if self.token is None:
            return None
            
        for terminal in first:
            if terminal == 'id':
                if self.token.code == Code.IDENTIFIER:
                    return True
            elif terminal == 'num':
                if self.token.code == Code.NUMBER:
                    return True
            elif terminal == 'str':
                if self.token.code == Code.STRING:
                    return True
            elif self.token and terminal == self.token.lexeme:
                return True

        return False

    def stm_cmd(self):
        if self.eat_lexeme('print'):
            if self.eat_lexeme('('):
                self.args()

                if self.eat_lexeme(')'):
                    if not self.eat_lexeme(';'):
                        self.add_error(';')
        elif self.eat_lexeme('read'):
            if self.eat_lexeme('('):
                self.args()

                if self.eat_lexeme(')'):
                    if not self.eat_lexeme(';'):
                        self.add_error(';')
        else:
            self.add_error('read` or `print')

    def stm_id(self):
        if self.verify(first_assign()):
            self.assign()
        elif self.verify(first_array()):
            self.array()
            self.arrays()
            self.accesses()
            self.assign()
        elif self.verify(first_access()):
            self.access()
            self.accesses()
            self.assign()
        elif self.eat_lexeme('('):
            self.args()

            if self.eat_lexeme(')'):
                if not self.eat_lexeme(';'):
                    self.add_error(';')
            else:
                self.add_error(')')
        else:
            self.add_error('=`, `+`, `-`, `[`, `.` or `(')

    def stm_scope(self):
        if self.eat_lexeme('local'): 
            self.access()
            self.accesses()
            self.assign()
        elif self.eat_lexeme('global'):
            self.access()
            self.accesses()
            self.assign()
        else:
            self.add_error('local` or `global')

    def var_stm(self):
        if self.verify(first_stm_scope()):
            self.stm_scope()
        elif self.eat_code(Code.IDENTIFIER):
            self.stm_id()
        elif self.verify(first_stm_cmd()):
            self.stm_cmd()
        else:
            self.add_error('local`, `global`, `id`, `print` or `read')

    def assign(self):
        if self.eat_lexeme('='):
            self.expr()
                
            if not self.eat_lexeme(';'):
                self.add_error(';')  
        elif self.eat_lexeme('++') or self.eat_lexeme('--'):
            if not self.eat_lexeme(';'):
                self.add_error(';')  
        else:
            self.add_error('=`, `++` or `--`')

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
        if self.verify(first_expr()):
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

    def log_unary(self):
        if self.eat_lexeme('!'): 
            self.log_unary()
        elif self.eat_lexeme('local'):
            self.access()
        elif self.eat_lexeme('global'):
            self.access()
        elif self.eat_code(Code.IDENTIFIER):
            self.id_value()
        elif self.eat_lexeme('('):
            self.log_expr()

            if not self.eat_lexeme(')'):
                self.add_error(')')
        elif not (self.eat_code(Code.NUMBER) or self.eat_code(Code.STRING) or
            self.eat_lexeme('true') or self.eat_lexeme('false')):
            self.add_error('Num`, `Str` or `Boolean')

    def log_compare_2(self):
        if self.eat_lexeme('<'):
            self.log_unary()
            self.log_compare_2()
        elif self.eat_lexeme('>'):
            self.log_unary()
            self.log_compare_2()
        elif self.eat_lexeme('<='):
            self.log_unary()
            self.log_compare_2()
        elif self.eat_lexeme('>='):
            self.log_unary()
            self.log_compare_2()

    def log_compare_(self):
        self.log_unary()
        self.log_compare_2()

    def log_equate_2(self):
        if self.eat_lexeme('=='):
            self.log_compare_()
            self.log_equate_2()
        elif self.eat_lexeme('!='):
            self.log_compare_()
            self.log_equate_2()

    def log_equate_(self):
        self.log_compare_()
        self.log_equate_2()

    def log_and_2(self):
        if self.eat_lexeme('&&'):
            self.log_equate_()
            self.log_and_2()

    def log_and_(self):
        self.log_equate_()
        self.log_and_2()

    def log_or_2(self):
        if self.eat_lexeme('||'):
            self.log_and_()
            self.log_or_2()

    def log_or_(self):
        self.log_and_()
        self.log_or_2()

    def log_expr(self):
        self.log_or_()

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
        if self.verify(first_array()):
            self.array()
            self.arrays()
            
    def array(self):
        if self.eat_lexeme('['):
            if self.verify(first_expr()):
                self.expr()

            if not self.eat_lexeme(']'):
                self.add_error(']')
        else:
            self.add_error('[')

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

    def var_id(self):
        if self.verify(first_var()):
            self.var()
            self.var_list()
        elif self.verify(first_stm_id()):
            self.stm_id()
        else:
            self.add_error('--`, `Id`, `[`, `(`, `++`, `.` or `=')

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
        elif self.verify(first_stm_scope()):
            self.stm_scope()
        elif self.eat_code(Code.IDENTIFIER):
            self.var_id()

    def var_block(self):
        if self.eat_lexeme('var'):
            if self.eat_lexeme('{'):
                self.var_decls()

                if not self.eat_lexeme('}'):
                    self.add_error('}')
            else:
                self.add_error('{')

    def func_normal_stm(self):
        if self.eat_lexeme('{'):
            self.var_stm()
            
            if not self.eat_lexeme('}'):
                self.add_error('}')
        elif self.verify(first_var_stm()):
            self.var_stm()
        elif self.eat_lexeme('return'):
            self.expr()
            
            if not self.eat_lexeme(';'):
                self.add_error(';')
        elif not self.eat_lexeme(';'):
            self.add_error('{`, `id`, `local`, `global`, `print`, `read`, `;` or `return')

    def else_stm(self):
        self.eat_lexeme('else')

    def func_stm(self):
        if self.eat_lexeme('if'):
            if self.eat_lexeme('('):
                self.log_expr()

                if self.eat_lexeme(')'):
                    if self.eat_lexeme('then'):
                        self.func_stm()
                        self.else_stm()
                        self.func_stm()
                        
                    else:
                        self.add_error('then')
                    
                else:
                    self.add_error(')')
            else:
                self.add_error('(')
        elif self.eat_lexeme('while'):
            if self.eat_lexeme('('):
                self.log_expr()

                if self.eat_lexeme(')'):
                    self.func_stm()
                else:
                    self.add_error(')')
            else:
                self.add_error('(')
        elif self.verify(first_func_normal_stm()):
            self.func_normal_stm()

    def func_stms(self):
        if self.verify(first_func_stm()):
            self.func_stm()
            self.func_stms()

    def func_block(self):
        if self.eat_lexeme('{'):
            self.var_block()
            self.func_stms()
            
            if not self.eat_lexeme('}'):
                self.add_error('}')
            
        else:
            self.add_error('{')

    def start_block(self): 
        if self.eat_lexeme('procedure'):
            if self.eat_lexeme('start'):
                if self.eat_lexeme('('):
                    if self.eat_lexeme(')'):
                        self.func_block()
                    else:
                        self.add_error(')')
                else:
                    self.add_error('(')

            else:
                self.add_error('start')
        else:
            self.add_error('procedure')

    def program(self):
        if self.eat_lexeme('structs'):
            print()
        if self.eat_lexeme('const'):
            print()
        self.var_block()

        if self.verify(first_start_block()):
            self.start_block()
        else:   
            self.add_custom_error('The procedure `start` has not found.')

    def execute(self):
        self.program()
        