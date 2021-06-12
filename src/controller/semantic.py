'''
This class does the semantic analysis.
'''

from src.model.token import Token
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
        self.reading_expr = False
        self.expr = ''
        self.expr_array = []
        self.func_return = -1

    def add(self, scope, key, item):
        self.symbols[scope][key] = item

    def add_id_declaration(self, identifier, attributes): 
        proc_declared = False

        for key in self.symbols:
            try:
                proc_key = key[:(key.index('('))]
                if identifier.lexeme in proc_key:
                    proc_declared = True
                    break
            except:
                proc_declared = False

        if proc_declared or identifier.lexeme in self.symbols[self.scope]:
            self.add_error(identifier, 'This identifier has already been declared: `' + identifier.lexeme + '`')
        else:
            self.add(self.scope, identifier.lexeme, attributes)

    def verify_id_not_declared(self, identifier, scope):
        is_a_function = False

        for key in self.symbols:
            try:
                proc_key = key[:(key.index('('))]
                if identifier.lexeme in proc_key:
                    is_a_function = True
                    break
            except:
                is_a_function = False

        
        if not is_a_function and hasattr(identifier, 'lexeme'):
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
        is_a_function = False

        for key in self.symbols:
            try:
                proc_key = key[:(key.index('('))]
                if identifier.lexeme in proc_key:
                    is_a_function = True
                    break
            except:
                is_a_function = False
        
        if is_a_function:
            self.add_error(identifier, 'Func attribution is not allowed: `' + identifier.lexeme + '`')
        else:
            if scope == 'global':
                if identifier.lexeme in self.symbols[scope]:
                    if (self.symbols[scope][identifier.lexeme]['conf'] == 'const'):
                        self.add_error(identifier, 'Const attribution is not allowed: `global.' + identifier.lexeme + '`')
            else:
                if identifier.lexeme in self.symbols[self.scope]:
                    if (self.symbols[self.scope][identifier.lexeme]['conf'] == 'const'):
                        self.add_error(identifier, 'Const attribution is not allowed: `local.' + identifier.lexeme + '`')

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
        if self.func_return == -1: 
            aux_dict = { }
        else:
            aux_dict = { '@return': self.func_return.lexeme }

        params = self.proc_key[(self.proc_key.index('(') + 1):self.proc_key.index(')')]
        type_list = ''
        
        for item in params.split(','):
            if len(item.split()) > 0:
                if item.split()[1] in aux_dict:
                    self.add_error(self.proc_key_token, 'You cannot use params with the same name: `' + self.proc_key + '`')
                else:
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
        self.func_return = -1

    def init_proc_decl(self, identifier):
        if identifier.lexeme in self.symbols['global']:
            self.add_error(identifier, 'A function cannot have the same name as a declaration: `global.' + identifier.lexeme + '`')
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
                last_scope = ''
                index = 0
                array_len = len(self.expr_array)
                
                while index < array_len:
                    token = self.expr_array[index]
                    if token.lexeme == 'global':
                        last_scope = 'global'
                    elif token.lexeme == 'local':
                        last_scope = 'local'
                    elif token.code == Code.IDENTIFIER:
                        proc_declared = False

                        for key in self.symbols:
                            try:
                                proc_key = key[:(key.index('('))]
                                if token.lexeme in proc_key:
                                    proc_declared = True
                                    break
                            except:
                                proc_declared = False

                        if proc_declared:
                            initial_index = index
                            resp = self.open_function(index, self.expr_array, True)
                            last_index = resp[0]

                            sara = ''
                            for a in self.expr_array:
                                sara += a.lexeme + ' '

                            part1 = self.expr_array[0:initial_index]
                            part2 = self.expr_array[last_index:array_len]
                            new_expr_array = []

                            for part in part1:
                                new_expr_array.append(part)
                                
                            tk_str = resp[1]

                            tk = ''
                            if tk_str == '0':
                                tk = Token(tk_str, Code.NUMBER, identifier.line_begin_index, identifier.line_end_index, identifier.column_begin_index, identifier.column_end_index)
                            elif tk_str == '0.0':
                                tk = Token(tk_str, Code.NUMBER, identifier.line_begin_index, identifier.line_end_index, identifier.column_begin_index, identifier.column_end_index)
                            elif tk_str == '" "':
                                tk = Token(tk_str, Code.KEYWORD, identifier.line_begin_index, identifier.line_end_index, identifier.column_begin_index, identifier.column_end_index)
                            elif tk_str == 'true':
                                tk = Token(tk_str, Code.KEYWORD, identifier.line_begin_index, identifier.line_end_index, identifier.column_begin_index, identifier.column_end_index)
                            else:
                                tk = Token(tk_str, Code.IDENTIFIER, identifier.line_begin_index, identifier.line_end_index, identifier.column_begin_index, identifier.column_end_index)
                            new_expr_array.append(tk)

                            for part in part2:
                                new_expr_array.append(part)

                            sara = ''
                            for a in new_expr_array:
                                sara += a.lexeme + ' '
                                
                            self.expr_array = new_expr_array
                            array_len = len(new_expr_array)
                            index = len(part1) - 1

                        else:
                            read_scope = self.scope

                            if last_scope == 'global':
                                read_scope = 'global'

                            if token.lexeme in self.symbols[read_scope]:
                                if self.symbols[read_scope][token.lexeme]['type'] == 'int':
                                    is_int = 1
                                elif self.symbols[read_scope][token.lexeme]['type'] == 'real':
                                    is_real = 1
                                elif self.symbols[read_scope][token.lexeme]['type'] == 'boolean':
                                    is_boolean = 1
                                elif self.symbols[read_scope][token.lexeme]['type'] == 'string':
                                    is_string = 1
                            else:  
                                self.add_error(identifier, 'Identifier not declared: `' + token.lexeme + '`')
                            
                            if last_scope == 'global':
                                last_scope = ''
                            elif last_scope == 'local':
                                last_scope = ''
                    elif token.code == Code.NUMBER:
                        if isinstance(eval(token.lexeme), int):
                            is_int = 1
                        else:
                            is_real = 1
                    elif token.lexeme == 'true' or token.lexeme == 'false':
                        is_boolean = 1  
                    elif token.code == Code.STRING:
                        is_string = 1
                    
                    index += 1

                if is_int + is_real + is_boolean + is_string > 1:
                    self.add_error(identifier, 'There are more than one type in a single expression `' + self.expr + '`. Conversions are not allowed here.')
                

        self.expr = ''
        self.expr_array = []
        self.reading_expr = False

    def add_expr(self, expr_increment, token):
        self.expr += expr_increment
        self.expr_array.append(token)

    def init_expr(self):
        self.expr = ''
        self.expr_array = []
        self.reading_expr = True

    def open_function(self, init_index_array, array, is_first=False):
        end_index_array = init_index_array + 1
        open_amount = 0
        str_function = array[init_index_array].lexeme
        first_open = True
        function_name = array[init_index_array].lexeme
        child_error = False
        error = False
        has_scope = ''

        while end_index_array < len(array):
            if not first_open and open_amount == 0:
                break
            elif array[end_index_array].lexeme == '(':
                if first_open or open_amount > 0:
                    str_function += '('
                    open_amount += 1
                elif open_amount == 0:
                    break
            elif array[end_index_array].lexeme == ')':
                if open_amount == 0:
                    break
                else:
                    str_function += ')'
                    open_amount -= 1
            elif array[end_index_array].lexeme == 'global':
                end_index_array += 1
                has_scope = 'global'
            elif array[end_index_array].lexeme == 'local':
                end_index_array += 1
                has_scope = 'local'
            elif array[end_index_array].code == Code.IDENTIFIER:
                if end_index_array + 1 < len(array):
                    if array[end_index_array + 1].lexeme == '(':
                        opened_function = self.open_function(end_index_array, array)
                        end_index_array = opened_function[0] - 1
                        str_function += opened_function[1]
                        child_error = opened_function[2]
                    elif open_amount > 0:
                        if has_scope == 'global':
                            if array[end_index_array].lexeme in self.symbols['global']:
                                str_function += self.symbols['global'][array[end_index_array].lexeme]['type']
                        elif array[end_index_array].lexeme in self.symbols[self.scope]:
                            str_function += self.symbols[self.scope][array[end_index_array].lexeme]['type']
                    has_scope = ''
            elif array[end_index_array].lexeme == ',' and open_amount > 0:
                str_function += ','
            end_index_array += 1  
            first_open = False

        #verify if the function exists:
        func_declared = False
        found_key = ''
        #found_params = function_name +'('
        return_type = str_function
        
        for key in self.symbols:
            try:
                proc_key = key[:(key.index('('))]
                
                if function_name in proc_key:
                    params = key[(key.index('(') + 1):key.index(')')]
                    splitted_params = params.split(',')
                    params_str = ''

                    for i, param in enumerate(splitted_params):
                        if len(splitted_params) > 0:
                            params_str += param.split()[0]

                            if i + 1< len(splitted_params):
                                params_str += ','
                                
                    if function_name + '(' + params_str + ')' == str_function:
                        func_declared = True
                        found_key = key
                        break
            except:
                func_declared = False

        if func_declared:
            if '@return' in self.symbols[found_key]:
                return_type = self.symbols[found_key]['@return']
                if is_first:
                    if return_type == 'int':
                        return_type = '0'
                    elif return_type == 'real':
                        return_type = '0.0'
                    elif return_type == 'string':
                        return_type = '" "'
                    elif return_type == 'boolean':
                        return_type = 'true'
            else:
                self.add_error(array[init_index_array], 'A procedure does not returns any type:`' + str_function + '`.')
        elif not child_error:
            self.add_error(array[init_index_array], 'This function does not exists:`' + str_function + '`.')
            error = True


        if not error:
            error = child_error
        return [end_index_array, return_type, error]

    def log(self):
        print(self.symbols)

