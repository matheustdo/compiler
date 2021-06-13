from os import read
from src.model.error_token import ErrorToken
from src.model.code import Code
from src.definitions.firsts import *
from src.definitions.follows import *

'''
This class does the iteration on tokens array and the syntactic analysis.
'''
class Parser:
    def __init__(self, lexical_tokens, semantic):
        self.lexical_tokens = lexical_tokens
        self.tokens_index = 0
        self.token = None
        self.syntactic_tokens = []
        self.semantic = semantic

        if len(lexical_tokens) > 0:
            self.token = lexical_tokens[0]

    def last_token(self): 
        if len(self.syntactic_tokens) > 1:
            return self.syntactic_tokens[self.tokens_index - 1]

    def sync(self, follow):
        synced = False

        while not synced and self.token is not None:
            for terminal in follow:
                if terminal == 'id':
                    if self.token.code == Code.IDENTIFIER:
                        synced = True
                elif terminal == 'num':
                    if self.token.code == Code.NUMBER:
                        synced = True
                elif terminal == 'str':
                    if self.token.code == Code.STRING:
                        synced = True
                elif self.token and terminal == self.token.lexeme:
                    synced = True

            if not synced:
                self.advance()

    def add_error(self, expected, follow):
        if self.token is None:
            line = 0

            if len(self.lexical_tokens) > 0:
                line = self.syntactic_tokens[self.tokens_index - 1].line_begin_index
            
            error_token = ErrorToken(line, f'Expected `{expected}` and found `EOF`.', Code.MF_SYNTAX)
            self.syntactic_tokens.append(error_token)
            self.semantic.semantic_tokens.append(error_token)
        else:
            error_token = ErrorToken(self.token.line_begin_index, f'Expected `{expected}` and found `{self.token.lexeme}`.', Code.MF_SYNTAX)
            self.syntactic_tokens.append(error_token)
            self.semantic.semantic_tokens.append(error_token)
            self.sync(follow)

    def add_custom_error(self, message, follow):
        if self.token is None:
            line = 0

            if len(self.lexical_tokens) > 0:
                line = self.syntactic_tokens[self.tokens_index - 1].line_begin_index
            
            error_token = ErrorToken(line, message, Code.MF_SYNTAX)
            self.syntactic_tokens.append(error_token)
            self.semantic.semantic_tokens.append(error_token)
        else:
            error_token = ErrorToken(self.token.line_begin_index, message, Code.MF_SYNTAX)
            self.syntactic_tokens.append(error_token)
            self.semantic.semantic_tokens.append(error_token)
            self.sync(follow)

    def add_error_without_sync(self, expected):
        if self.token is None:
            line = 0

            if len(self.lexical_tokens) > 0:
                line = self.syntactic_tokens[self.tokens_index - 1].line_begin_index
            
            error_token = ErrorToken(line, f'Expected `{expected}` and found `EOF`.', Code.MF_SYNTAX)
            self.syntactic_tokens.append(error_token)
        else:
            error_token = ErrorToken(self.token.line_begin_index, f'Expected `{expected}` and found `{self.token.lexeme}`.', Code.MF_SYNTAX)
            self.syntactic_tokens.append(error_token)

    def advance(self):
        self.syntactic_tokens.append(self.token)
        self.semantic.semantic_tokens.append(self.token)
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

    def eat_opening(self, lexeme):
        if self.token is not None and self.token and lexeme == self.token.lexeme:
            self.advance()
        elif lexeme == "{" or lexeme == "(":
            self.add_error_without_sync(lexeme)

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
            self.eat_opening('(')
            self.args()

            if self.eat_lexeme(')'):
                if not self.eat_lexeme(';'):
                    self.add_error(';', follow_stm_cmd()) 
        elif self.eat_lexeme('read'):
            self.eat_opening('(')
            self.args()

            if self.eat_lexeme(')'):
                if not self.eat_lexeme(';'):
                    self.add_error(';', follow_stm_cmd())  
        else:
            self.add_error('read` or `print', follow_stm_cmd())

    def stm_id(self):
        read_token = self.last_token()

        if self.verify(first_assign()):
            self.assign(read_token, '')
        elif self.verify(first_array()):
            self.array()
            self.arrays()
            self.accesses('')
            self.assign(read_token, '')
        elif self.verify(first_access()):
            self.access('')
            self.accesses('')
            self.assign(read_token, '')
        elif self.eat_lexeme('('):
            self.args()

            if self.eat_lexeme(')'):
                if not self.eat_lexeme(';'):
                    self.add_error(';', follow_stm_id()) 
            else:
                self.add_error(')', follow_stm_id()) 
        else:
            self.add_error('=`, `+`, `-`, `[`, `.` or `(', follow_stm_id())

    def stm_scope(self):
        if self.eat_lexeme('local'): 
            self.access('local')
            self.accesses('local')
            self.assign(self.last_token(), 'local')
        elif self.eat_lexeme('global'):
            self.access('global')
            self.accesses('global')
            self.assign(self.last_token(), 'global')
        else:
            self.add_error('local` or `global', follow_stm_scope())

    def var_stm(self):
        if self.verify(first_stm_scope()):
            self.stm_scope()
        elif self.eat_code(Code.IDENTIFIER):
            self.semantic.verify_id_not_declared(self.last_token(), '')
            self.stm_id()
        elif self.verify(first_stm_cmd()):
            self.stm_cmd()
        else:
            self.add_error('local`, `global`, `Id`, `print` or `read', follow_var_stm())

    def assign(self, identifier, scope):
        self.semantic.verify_attribution(identifier, scope)

        if self.eat_lexeme('='):
            self.semantic.init_expr()
            self.expr()
            self.semantic.verify_assign_type(identifier)
                
            if not self.eat_lexeme(';'):
                self.add_error(';', follow_assign())   
        elif self.eat_lexeme('++') or self.eat_lexeme('--'):
            if not self.eat_lexeme(';'):
                self.add_error(';', follow_assign())   
        else:
            self.add_error('=`, `++` or `--', follow_assign())

    def access(self, scope):
        if self.eat_lexeme('.'):
            if self.semantic.reading_expr:
                self.semantic.add_expr('.', self.last_token())
            if self.eat_code(Code.IDENTIFIER):
                if self.semantic.reading_expr:
                    self.semantic.add_expr(self.last_token().lexeme, self.last_token())
                self.semantic.verify_id_not_declared(self.last_token(), scope)
                self.arrays()
            else:
                self.add_error('Id', follow_access()) 
        else:
            self.add_error('.', follow_access())
            
    def accesses(self, scope):
        if self.eat_lexeme('.'):
            if self.semantic.reading_expr:
                self.semantic.add_expr('.', self.last_token())
            if self.eat_code(Code.IDENTIFIER):
                if self.semantic.reading_expr:
                    self.semantic.add_expr(self.last_token().lexeme, self.last_token())
                self.semantic.verify_id_not_declared(self.last_token(), scope)
                self.arrays()
                self.accesses(scope)
            else:
                self.add_error('Id', follow_accesses())

    def args_list(self):
        if self.eat_lexeme(','):
            if self.semantic.reading_expr:
                self.semantic.add_expr(',', self.last_token())
            self.expr()
            self.args_list()
            
    def args(self):
        if self.verify(first_expr()):
            self.expr()
            self.args_list()

    def id_value(self):
        if self.eat_lexeme('('):
            if self.semantic.reading_expr:
                self.semantic.add_expr('(', self.last_token())
            self.args()

            if self.eat_lexeme(')'):
                if self.semantic.reading_expr:
                    self.semantic.add_expr(')', self.last_token())
            else:
                self.add_error(')', follow_id_value()) 
        else:
            self.arrays()
            self.accesses('')

    def log_unary(self):
        if self.eat_lexeme('!'): 
            self.log_unary()
        elif self.eat_lexeme('local'):
            self.access('local')
            self.accesses('local')
        elif self.eat_lexeme('global'):
            self.access('global')
            self.accesses('global')
        elif self.eat_code(Code.IDENTIFIER):
            self.id_value()
        elif self.eat_lexeme('('):
            self.log_expr()

            if not self.eat_lexeme(')'):
                self.add_error(')', follow_log_unary())  
        elif not (self.eat_code(Code.NUMBER) or self.eat_code(Code.STRING) or
            self.eat_lexeme('true') or self.eat_lexeme('false')):
            self.add_error('Num`, `Str` or `Boolean', follow_log_unary())  

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
            self.semantic.add_expr('!', self.last_token())
            self.unary()
        elif self.eat_lexeme('local'):
            self.semantic.add_expr('local', self.last_token())
            self.access('local')
            self.accesses('local')
        elif self.eat_lexeme('global'):
            self.semantic.add_expr('global', self.last_token())
            self.access('global')
            self.accesses('global')
        elif self.eat_code(Code.IDENTIFIER):
            self.semantic.add_expr(self.last_token().lexeme, self.last_token())
            self.id_value()
        elif self.eat_lexeme('('):
            self.semantic.add_expr('(', self.last_token())
            self.expr()

            if self.eat_lexeme(')'):
                self.semantic.add_expr(')', self.last_token())
            else:
                self.add_error(')', follow_unary()) 
        elif not (self.eat_code(Code.NUMBER) or self.eat_code(Code.STRING) or
            self.eat_lexeme('true') or self.eat_lexeme('false')):
            self.add_error('Num`, `Str` or `Boolean', follow_unary())
        else:
            self.semantic.add_expr(self.last_token().lexeme, self.last_token())

    def mult_2(self):
        if self.eat_lexeme('*'):
            self.semantic.add_expr('*', self.last_token())
            self.unary()
            self.mult_2()
        elif self.eat_lexeme('/'):
            self.semantic.add_expr('/', self.last_token())
            self.unary()
            self.mult_2()

    def mult_(self):
        self.unary()
        self.mult_2()

    def add_2(self):
        if self.eat_lexeme('+'):
            self.semantic.add_expr('+', self.last_token())
            self.mult_()
            self.add_2()
        elif self.eat_lexeme('-'):
            self.semantic.add_expr('-', self.last_token())
            self.mult_()
            self.add_2()

    def add_(self):
        self.mult_()
        self.add_2()

    def compare_2(self):
        if self.eat_lexeme('<'):
            self.semantic.add_expr('<', self.last_token())
            self.add_()
            self.compare_2()
        elif self.eat_lexeme('>'):
            self.semantic.add_expr('>', self.last_token())
            self.add_()
            self.compare_2()
        elif self.eat_lexeme('<='):
            self.semantic.add_expr('<=', self.last_token())
            self.add_()
            self.compare_2()
        elif self.eat_lexeme('>='):
            self.semantic.add_expr('>=', self.last_token())
            self.add_()
            self.compare_2()

    def compare_(self):
        self.add_()
        self.compare_2()

    def equate_2(self):
        if self.eat_lexeme('=='):
            self.semantic.add_expr('==', self.last_token())
            self.compare_()
            self.equate_2()
        elif self.eat_lexeme('!='):
            self.semantic.add_expr('!=', self.last_token())
            self.compare_()
            self.equate_2()

    def equate_(self):
        self.compare_()
        self.equate_2()

    def and_2(self):
        if self.eat_lexeme('&&'):
            self.semantic.add_expr('&&', self.last_token())
            self.equate_()
            self.and_2()

    def and_(self):
        self.equate_()
        self.and_2()
            
    def or_2(self):
        if self.eat_lexeme('||'):
            self.semantic.add_expr('||', self.last_token())
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
                self.add_error(']', follow_array()) 
        else:
            self.add_error('[', follow_array())

    def type_(self):
        if self.eat_lexeme('struct'):
            if not self.eat_code(Code.IDENTIFIER):
                self.add_error('Id', follow_type())
        elif not (self.eat_lexeme('int') or self.eat_lexeme('real') or
            self.eat_lexeme('boolean') or self.eat_lexeme('string')):
            self.add_error('Id', follow_type())

    def typedef(self):
        if self.eat_lexeme('typedef'):
            if self.verify(first_type()):
                self.type_()

                if self.eat_code(Code.IDENTIFIER):
                    if not self.eat_lexeme(';'):
                        self.add_error(';', follow_typedef())
                else:
                    self.add_error('Id', follow_typedef())
            else:
                self.add_error('type', follow_typedef())
        else:
            self.add_error('typedef', follow_typedef())

    def var(self, type):
        if self.eat_code(Code.IDENTIFIER):
            self.semantic.add_id_declaration(self.last_token(), { 'type': type.lexeme, 'conf': 'var' })
            self.arrays()
        else:
            self.add_error('Id', follow_var())
            
    def var_list(self, type):
        if self.eat_lexeme(','):
            if self.eat_code(Code.IDENTIFIER):
                self.semantic.add_id_declaration(self.last_token(), { 'type': type.lexeme, 'conf': 'var' })
                self.arrays()
                self.var_list(type)
            else:
                self.add_error('Id', follow_var_list())

    def var_id(self, identifier):
        if self.verify(first_var()):
            self.var(identifier)
            self.var_list(identifier)

            if not self.eat_lexeme(';'):
                self.add_error(';', follow_var_id())
        elif self.verify(first_stm_id()):
            self.stm_id()
        else:
            self.add_error('--`, `Id`, `[`, `(`, `++`, `.` or `=', follow_var_id())

    def var_decl(self):
        if self.verify(first_type()):
            self.type_()
            self.var(self.last_token())
            self.var_list(self.last_token()) 

            if not self.eat_lexeme(';'):
                self.add_error(';', follow_var_decl()) 
        elif self.verify(first_typedef()):
            self.typedef()
        elif self.verify(first_stm_scope()):
            self.stm_scope()
        elif self.eat_code(Code.IDENTIFIER):
            self.var_id(self.last_token())
        else:
            self.add_error('Var Declaration', follow_var_decl())

    def var_decls(self):
        if self.verify(first_var_decl()):
            self.var_decl()
            self.var_decls()

    def var_block(self):
        if self.eat_lexeme('var'):
            self.eat_opening('{')
            self.var_decls()

            if not self.eat_lexeme('}'):
                self.add_error('}', follow_var_block())

    def func_normal_stm(self):
        if self.eat_lexeme('{'):
            self.func_stms()
            
            if not self.eat_lexeme('}'):
                self.add_error('}', follow_func_normal_stm()) 
        elif self.verify(first_var_stm()):
            self.var_stm()
        elif self.eat_lexeme('return'):
            self.expr()
            
            if not self.eat_lexeme(';'):
                self.add_error(';', follow_func_normal_stm()) 
        elif not self.eat_lexeme(';'):
            self.add_error('{`, `id`, `local`, `global`, `print`, `read`, `;` or `return', follow_func_normal_stm())

    def else_stm(self):
        self.eat_lexeme('else')

    def func_stm(self):
        if self.eat_lexeme('if'):
            self.eat_opening('(')
            self.log_expr()

            if self.eat_lexeme(')'):
                if self.eat_lexeme('then'):
                    self.func_stm()
                    self.else_stm()
                    self.func_stm()
                    
                else:
                    self.add_error('then', follow_func_stm()) 
            else:
                self.add_error(')', follow_func_stm())  
        elif self.eat_lexeme('while'):
            self.eat_opening('(')
            self.log_expr()

            if self.eat_lexeme(')'):
                self.func_stm()
            else:
                self.add_error(')', follow_func_stm())
        elif self.verify(first_func_normal_stm()):
            self.func_normal_stm()
        else:
            self.add_error('Function', follow_func_stm())

    def func_stms(self):
        if self.verify(first_func_stm()):
            self.func_stm()
            self.func_stms()

    def func_block(self):
        self.eat_opening('{')
        self.var_block()
        self.func_stms()
        
        if not self.eat_lexeme('}'):
            self.add_error('}', follow_func_block())

    def array_expr(self):
        if self.eat_lexeme(','):
            self.array_def()

    def array_def(self):
        if self.verify(first_expr()):
            self.expr()
            self.array_expr()
        else:
            self.add_error('Expression', follow_array_def())

    def array_vector(self):
        if self.eat_lexeme(','):
            self.array_decl()

    def array_decl(self):
        self.eat_opening('{')
        self.array_def()

        if self.eat_lexeme('}'):
            self.array_vector()
        else:
            self.add_error('}', follow_array_decl())

    def decl_attribute(self):
        if self.verify(first_array_decl()):
            self.array_decl()
        elif self.verify(first_expr()):
            self.expr()
        else:
            self.add_error('{` or `Expression', follow_decl_atribute())

    def const(self, type):
        if self.eat_code(Code.IDENTIFIER):
            self.semantic.add_id_declaration(self.last_token(), { 'type': type.lexeme, 'conf': 'const' })
            self.arrays()
        else:
            self.add_error('Id', follow_const())
            
    def const_list(self, type):
        if self.eat_lexeme(','):
            if self.eat_code(Code.IDENTIFIER):
                self.semantic.add_id_declaration(self.last_token(), { 'type': type.lexeme, 'conf': 'const' })
                self.arrays()
                self.const_list(type)
            else:
                self.add_error('Id', follow_const_list())  
        elif self.eat_lexeme('='):
            self.decl_attribute()
            
            if not self.eat_lexeme(';'):
                self.add_error(';', follow_const_list())
        else: 
            self.add_error(',` or `=', follow_const_list())

    def const_id(self, identifier):
        if self.verify(first_const()):
            self.const(identifier)
            self.const_list(identifier)
        elif self.verify(first_stm_id()):
            self.stm_id()
        else:
            self.add_error('--`, `Id`, `[`, `(`, `++`, `.` or `=', follow_const_id())

    def const_decl(self):
        if self.verify(first_type()):
            self.type_()
            self.const(self.last_token())
            self.const_list(self.last_token()) 
        elif self.verify(first_typedef()):
            self.typedef()
        elif self.verify(first_stm_scope()):
            self.stm_scope()
        elif self.eat_code(Code.IDENTIFIER):
            self.const_id(self.last_token())
        else:
            self.add_error('Const Declaration', follow_const_decl())

    def const_decls(self):
        if self.verify(first_const_decl()):
            self.const_decl()
            self.const_decls()
    
    def const_block(self):
        if self.eat_lexeme('const'):
            self.eat_opening('{')
            self.const_decls()

            if not self.eat_lexeme('}'):
                self.add_error('}', follow_const_block()) 

    def extends(self):
        if self.eat_lexeme('extends'):
            if self.eat_lexeme('struct'):
                if not self.eat_code(Code.IDENTIFIER):
                    self.add_error('Id', follow_extends()) 
            else:
                self.add_error('struct', follow_extends())

    def struct_block(self):
        if self.eat_lexeme('struct'):
            if self.eat_code(Code.IDENTIFIER):
                self.semantic.change_scope(self.last_token().lexeme)
                self.extends()

                self.eat_opening('{')
                self.const_block()
                self.var_block()

                if not self.eat_lexeme('}'):
                    self.add_error('} or `Declarations', follow_struct_block()) 
            else:
                self.add_error('Id', follow_struct_block()) 
        else:
            self.add_error('struct', follow_struct_block())

    def param_mult_arrays(self):
        if self.eat_lexeme('['):
            if self.eat_code(Code.NUMBER):
                if self.eat_lexeme(']'):
                    self.param_mult_arrays()
                else:
                    self.add_error(']', follow_param_mult_arrays())
            else:
                self.add_error('Number', follow_param_mult_arrays())

    def param_arrays(self):
        if self.eat_lexeme('['):
            if self.eat_lexeme(']'):
                self.param_mult_arrays()
            else:
                self.add_error(']', follow_param_arrays())

    def params_list(self):
        if self.eat_lexeme(','):
            self.semantic.proc_decl_add_param(',')
            self.param()
            self.params_list()

    def param(self):
        if self.verify(first_param_type()):
            p_type = self.token
            self.param_type()

            if self.eat_code(Code.IDENTIFIER):
                self.semantic.proc_decl_add_param(p_type.lexeme + ' ' + self.last_token().lexeme)
                self.param_arrays()
            else:
                self.add_error('Id', follow_param())
        else:
            self.add_error('type` or `Id', follow_param())

    def params(self):
        if self.verify(first_param()):
            self.param()
            self.params_list()

    def param_type(self):
        if self.verify(first_type()):
            self.type_()
        elif not self.eat_code(Code.IDENTIFIER):
            self.add_error('type` or `Id', follow_param_type())

    def proc_decl(self):
        if self.eat_lexeme('procedure'):
            if self.eat_code(Code.IDENTIFIER):
                self.semantic.init_proc_decl(self.last_token())
                self.eat_opening('(')
                self.semantic.proc_decl_add_param('(')
                self.params()
                self.semantic.proc_decl_add_param(')')
                self.semantic.end_proc_decl()

                if self.eat_lexeme(')'):
                    self.func_block()
                else:
                    self.add_error(')', follow_proc_decl())
            elif self.eat_lexeme('start'):
                self.semantic.change_scope('start')

                self.eat_opening('(')

                if self.eat_lexeme(')'):
                    self.func_block()
                else:
                    self.add_error(')', follow_start_block()) 
            elif self.verify(follow_proc_decl()):
                self.add_error('Id`', follow_proc_decl())
            else:
                self.add_custom_error('The procedure `start` has not found.', follow_start_block())
        else:
            self.add_error('procedure', follow_proc_decl())

    def func_decl(self):
        if self.eat_lexeme('function'):
            if self.verify(first_param_type()):
                self.semantic.func_return = self.token;
            self.param_type()

            if self.eat_code(Code.IDENTIFIER):
                self.semantic.init_proc_decl(self.last_token())
                self.eat_opening('(')
                self.semantic.proc_decl_add_param('(')
                self.params()

                self.semantic.proc_decl_add_param(')')
                self.semantic.end_proc_decl()

                if self.eat_lexeme(')'):
                    self.func_block()
                else:
                    self.add_error(')', follow_func_decl())
            else:
                self.add_error('Id', follow_func_decl())
        else:
            self.add_error('function', follow_func_decl())

    def decl(self):
        if self.verify(first_func_decl()):
            self.func_decl()
        elif self.verify(first_proc_decl()):
            self.proc_decl()
        else:
            self.add_error('function` or `procedure', follow_decl())

    def decls(self):
        if self.verify(first_decl()):
            self.decl()
            self.decls()

    def structs(self):
        if self.verify(first_struct_block()):
            self.struct_block()
            self.structs()

    def program(self):
        if not self.verify(first_program()):
            self.add_error('struct`, `const`, `var` or `procedure', follow_program())
        self.structs()

        self.semantic.change_scope('global')

        if not self.verify(first_program()):
            self.add_error('const`, `var` or `procedure', follow_program())
        self.const_block()

        if not self.verify(first_program()):
            self.add_error('var` or `procedure', follow_program())
        self.var_block()

        if not self.verify(first_program()):
            self.add_error('procedure', follow_program())
        self.decls()

    def execute(self):
        self.program()
        