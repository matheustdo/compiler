'''
This class does the semantic analysis.
'''

from src.model.error_token import ErrorToken
from src.model.code import Code
from src.definitions.lexicon import LETTER
import re

class Semantic:
    def __init__(self):
        self.symbols = {
            'global': {

            }
        }
        self.semantic_tokens = []
        self.scope = 'global'
        self.proc_key_token = None
        self.proc_key = ''
        self.expr = ''
        self.expr_array = []

    def add(self, scope, key, item):
        self.symbols[scope][key] = item

    def add_id_declaration(self, identifier, attributes): 
        if identifier.lexeme in self.symbols[self.scope]:
            self.add_error(identifier, 'This identifier has already been declared: `' + identifier.lexeme + '`')
        else:
            self.add(self.scope, identifier.lexeme, attributes)

    def verify_id_not_declared(self, identifier, scope):
        if scope == 'global':
            if not identifier.lexeme in self.symbols[scope]:
                self.add_error(identifier, 'Identifier not declared: `global.' + identifier.lexeme + '`')
        elif scope == 'local':
            if not identifier.lexeme in self.symbols[self.scope]:
                self.add_error(identifier, 'Identifier not declared: `local.' + identifier.lexeme + '`')
        else:
            if not identifier.lexeme in self.symbols[self.scope] and not identifier.lexeme in self.symbols['global']:
                self.add_error(identifier, 'Identifier not declared: `' + identifier.lexeme + '`')

    def verify_attribution(self, identifier, scope):
        if scope == 'global':
            if identifier.lexeme in self.symbols[scope]:
                if (self.symbols[scope][identifier.lexeme]['conf'] == 'const'):
                    self.add_error(identifier, 'Const attribution is not allowed: `global.' + identifier.lexeme + '`')
                elif (self.symbols[scope][identifier.lexeme]['conf'] == 'func'):
                    self.add_error(identifier, 'Func attribution is not allowed: `global.' + identifier.lexeme + '`')
        else:
            if identifier.lexeme in self.symbols[self.scope]:
                if (self.symbols[self.scope][identifier.lexeme]['conf'] == 'const'):
                    self.add_error(identifier, 'Const attribution is not allowed: `local.' + identifier.lexeme + '`')
                elif (self.symbols[self.scope][identifier.lexeme]['conf'] == 'func'):
                    self.add_error(identifier, 'Func attribution is not allowed: `local.' + identifier.lexeme + '`')

    def add_error(self, token, description):
        error_token = ErrorToken(token.line_begin_index, description, Code.MF_SEMANTIC)
        self.semantic_tokens.append(error_token)

    def change_scope(self, new_scope):
        if not new_scope in self.symbols:
            self.symbols[new_scope] = { }
        
        self.scope = new_scope

    def proc_decl_add_param(self, param):
        self.proc_key += param

    def end_proc_decl(self):
        if self.proc_key == '':
            return
            
        aux_dict = { }
        params = self.proc_key[(self.proc_key.index('(') + 1):self.proc_key.index(')')]
        type_list = ''
        
        for item in params.split(','):
            if len(item.split()) > 0:
                aux_dict[item.split()[1]] = { 'type': item.split()[0], 'conf': 'var' }
                type_list += item.split()[0] + ' '
        proc_name = self.proc_key[:self.proc_key.index('(')] + '('
        
        if self.proc_key in self.symbols['global'] or self.proc_key in self.symbols:
            self.add_error(self.proc_key_token, 'This function/procedure already exists: `' + self.proc_key + '`')
        else:
            for key in self.symbols:
                if proc_name in key:
                    params2 = key[(key.index('(') + 1):key.index(')')]
                    type_list2 = ''

                    for item2 in params2.split(','):
                        if len(item2.split()) > 0:
                            type_list2 += item2.split()[0] + ' '
                    if type_list == type_list2:
                        self.add_error(self.proc_key_token, 'This function/procedure already exists: `' + self.proc_key + '`')
                        break

            self.symbols[self.proc_key] = aux_dict
            self.scope = self.proc_key

        self.proc_key_token = None
        self.proc_key = ''

    def init_proc_decl(self, identifier):
        if identifier.lexeme in self.symbols['global']:
            self.add_error(identifier, 'A function cannot have the same name as a global declaration: `global.' + identifier.lexeme + '`')
            return

        self.proc_key_token = identifier
        self.proc_key = identifier.lexeme
    
    def verify_assign_type(self, identifier):
        if identifier.lexeme in self.symbols[self.scope]:
            x = re.findall(LETTER, self.expr)
            
            if len(x) == 0:
                if self.symbols[self.scope][identifier.lexeme]['type'] == 'int':
                    if not isinstance(eval(self.expr), int):
                        self.add_error(identifier, 'You cannot assign `' + str(eval(self.expr)) +'` to `int`')
                elif not self.symbols[self.scope][identifier.lexeme]['type'] == 'real':
                    self.add_error(identifier, 'You cannot assign `' + str(eval(self.expr)) +'` to ' + '`' + self.symbols[self.scope][identifier.lexeme]['type'] + '`')
            else:
                is_int = 0
                is_real = 0
                is_boolean = 0
                is_string = 0

                for token in self.expr_array:
                    if token.code == Code.IDENTIFIER:
                        if token.lexeme in self.symbols[self.scope]:
                            if self.symbols[self.scope][token.lexeme]['type'] == 'int':
                                is_int = 1
                            elif self.symbols[self.scope][token.lexeme]['type'] == 'real':
                                is_real = 1
                            elif self.symbols[self.scope][token.lexeme]['type'] == 'boolean':
                                is_boolean = 1
                            elif self.symbols[self.scope][token.lexeme]['type'] == 'string':
                                is_string = 1
                        else:
                            self.add_error(identifier, 'Identifier not declared: `' + token.lexeme + '`')
                    elif token.code == Code.NUMBER:
                        if isinstance(eval(token.lexeme), int):
                            is_int = 1
                        else:
                            is_real = 1
                    elif token.lexeme == 'true' or token.lexeme == 'false':
                        is_boolean = 1  
                    elif token.code == Code.STRING:
                        is_string = 1
                
                if is_int + is_real + is_boolean + is_string > 1:
                    self.add_error(identifier, 'There are more than one type in a single expression `' + self.expr + '`. Conversions are not allowed here.')

        self.expr = ''
        self.expr_array = []

    def add_expr(self, expr_increment, token):
        self.expr += expr_increment
        self.expr_array.append(token)

    def init_expr(self):
        self.expr = ''
        self.expr_array = []

    def log(self):
        print(self.symbols)

