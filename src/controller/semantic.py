'''
This class does the semantic analysis.
'''

from src.model.token import Token
from src.model.error_token import ErrorToken
from src.model.code import Code
from src.definitions.lexicon import LETTER
from src.definitions.lexicon import LOGICAL_AND_RELATIONAL
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
        self.return_found = False
        self.reading_function = False
        self.access = ''
        self.reading_access = False
        self.access_token = ''
        self.access_assign = ''
        self.proc_call_token = None
        self.proc_call_str = ''
        self.reading_proc_call = False
        self.proc_call_array = []
        self.var_decl = False
        self.array_counting = False
        self.array_count = 0
        self.int_expr = ''
        self.int_expr_array = []
        self.int_reading_expr = False

    def add(self, scope, key, item):
        self.symbols[scope][key] = item

    def add_id_declaration(self, identifier, type_token, conf): 
        if not hasattr(identifier, 'lexeme') or not hasattr(type_token, 'lexeme'):
            return

        proc_declared = False

        for key in self.symbols:
            try:
                proc_key = key[:(key.index('('))] + '('
                if identifier.lexeme + '(' == proc_key:
                    proc_declared = True
                    break
            except:
                proc_declared = False

        if proc_declared or identifier.lexeme in self.symbols[self.scope]:
            self.add_error(identifier, 'This identifier has already been declared: `' + identifier.lexeme + '`')
        else:
            type_lexeme = type_token.lexeme

            if '@types' in self.symbols[self.scope]:
                if type_token.lexeme in self.symbols[self.scope]['@types']:
                    type_lexeme = self.symbols[self.scope]['@types'][type_token.lexeme]['type']
            elif '@types' in self.symbols['global']:
                if type_token.lexeme in self.symbols['global']['@types']:
                    type_lexeme = self.symbols[self.scope]['@types'][type_token.lexeme]['type']
            self.add(self.scope, identifier.lexeme, { 'type': type_lexeme, 'conf': conf, 'array': 0})

    def verify_id_not_declared(self, identifier, scope):
        if not hasattr(identifier, 'lexeme'):
            return

        if not self.reading_access:
            is_a_function = False

            for key in self.symbols:
                try:
                    proc_key = key[:(key.index('('))] + '('
                    if identifier.lexeme + '(' == proc_key:
                        is_a_function = True
                        break
                except:
                    is_a_function = False

            
            if not is_a_function:
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
        if not hasattr(identifier, 'lexeme'):
            return

        is_a_function = False

        for key in self.symbols:
            try:
                proc_key = key[:(key.index('('))] + '('
                if identifier.lexeme + '(' == proc_key:
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
                        if self.scope != 'global':
                            self.add_error(identifier, 'Const attribution is not allowed: `global.' + identifier.lexeme + '`')
            else:
                if identifier.lexeme in self.symbols[self.scope]:
                    if (self.symbols[self.scope][identifier.lexeme]['conf'] == 'const'):
                        if self.scope != 'global':
                            self.add_error(identifier, 'Const attribution is not allowed: `local.' + identifier.lexeme + '`')

    def add_error(self, token, description):
        if not token is None:
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

    def get_type_expression(self, identifier, expr_array):
        if not hasattr(identifier, 'lexeme'):
            return

        expr = ''
        custom_type = ''
        
        for x in expr_array:
            if hasattr(x, 'lexeme'):
                expr += x.lexeme

        x = re.findall(LETTER, expr)
        
        if len(x) == 0:        
            if any(l_and_r in expr for l_and_r in LOGICAL_AND_RELATIONAL) > 0:
                return 'boolean'
            else:
                try:
                    if isinstance(eval(expr), int):
                        return 'int'
                    else:
                        return 'real'
                except:
                    return 'invalid'
            """ if self.symbols[scope][identifier.lexeme]['type'] == 'int':
                if isinstance(eval(expr), int):
                    return 'int'
                else:
                    self.add_error(identifier, 'You cannot assign `' + str(eval(expr)) +'` to `int`')
            elif self.symbols[scope][identifier.lexeme]['type'] == 'real':
                return 'real'
            else:
                self.add_error(identifier, 'You cannot assign `' + str(eval(expr)) +'` to ' + '`' + self.symbols[scope][identifier.lexeme]['type'] + '`') """
        else:
            is_int = 0
            is_real = 0
            is_boolean = 0
            is_string = 0
            last_scope = ''
            index = 0
            array_len = len(expr_array)

            if any(l_and_r in expr for l_and_r in LOGICAL_AND_RELATIONAL) > 0:
                is_boolean = 1
            
            while index < array_len:
                token = expr_array[index]
                if token.lexeme == 'global':
                    last_scope = 'global'
                elif token.lexeme == 'local':
                    last_scope = 'local'
                elif token.code == Code.IDENTIFIER:
                    proc_declared = False

                    if index + 1 < array_len and expr_array[index + 1].lexeme == '(':
                        for key in self.symbols:
                            try:
                                proc_key = key[:(key.index('(') + 1)]
                                if token.lexeme + '(' == proc_key:
                                    proc_declared = True
                                    break
                            except:
                                proc_declared = False
                            
                    if proc_declared:
                        initial_index = index
                        resp = self.open_function(identifier, index, expr_array)
                        last_index = resp[0]

                        part1 = expr_array[0:initial_index]
                        part2 = expr_array[last_index:array_len]
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
                            
                        expr_array = new_expr_array
                        array_len = len(new_expr_array)
                        index = len(part1) - 1

                    else:
                        new_index = index
                        access_list = last_scope

                        if last_scope == 'global' or last_scope == 'local':
                            access_list += '.'
                        
                        array_found = 0

                        while new_index < array_len:
                            if array_found == 0 and expr_array[new_index].code == Code.IDENTIFIER:
                                access_list += expr_array[new_index].lexeme
                            elif array_found == 0 and expr_array[new_index].lexeme == '.':
                                access_list += '.'
                            elif expr_array[new_index].lexeme == '[':
                                if array_found == 0:
                                    access_list += expr_array[new_index].lexeme
                                array_found += 1
                            elif expr_array[new_index].lexeme == ']':
                                array_found -= 1
                                if array_found == 0:
                                    access_list += expr_array[new_index].lexeme
                            elif array_found == 0:
                                break

                            new_index += 1
                            
                        found_type = self.get_access_type(access_list, token, True)

                        if found_type == 'int':
                            is_int = 1
                        elif found_type == 'real':
                            is_real = 1
                        elif found_type == 'boolean':
                            is_boolean = 1
                        elif found_type == 'string':
                            is_string = 1
                        else:
                            custom_type = found_type
                        """ else:
                            if not ('(' in token.lexeme and ')' in token.lexeme):
                                self.add_error(identifier, 'Identifier not declared: `' + token.lexeme + '`') """
                        
                        index = new_index
                        last_scope = ''
                elif token.code == Code.NUMBER:
                    try:
                        if isinstance(eval(token.lexeme), int):
                            is_int = 1
                        else:
                            is_real = 1
                    except:
                        pass
                elif token.lexeme == 'true' or token.lexeme == 'false':
                    is_boolean = 1  
                elif token.code == Code.STRING:
                    is_string = 1
                
                index += 1

            expr = ''

            for x in expr_array:
                expr += x.lexeme

            if is_int + is_real + is_string > 1:
                self.add_error(identifier, 'There are more than one types in a single expression `' + expr + '`. Conversions are not allowed here.')
            elif is_boolean == 1:
                return 'boolean'
            elif is_int == 1:
                return 'int'
            elif is_real == 1:
                return 'real'
            elif is_string == 1:
                return 'string'
            
            if custom_type != '':
                return custom_type
            return 'invalid'
    
    def verify_assign_type(self, identifier, scope):
        if not hasattr(identifier, 'lexeme'):
            return
            
        if self.access_assign != '':
            type_found = self.get_type_expression(identifier, self.expr_array)
            if self.access_assign == 'invalid' or type_found == 'invalid' or self.access_assign != type_found:
                self.add_error(identifier, 'You cannot assign `' + type_found +'` to ' + '`' + self.access_assign + '`')
        else:
            if scope == 'local' or scope == '':
                scope = self.scope
                
            if identifier.lexeme in self.symbols[scope]:
                type_found = self.get_type_expression(identifier, self.expr_array)
                
                if not type_found == 'invalid' and self.symbols[scope][identifier.lexeme]['type'] != type_found:
                    self.add_error(identifier, 'You cannot assign `' + type_found +'` to ' + '`' + self.symbols[scope][identifier.lexeme]['type'] + '`')
            elif identifier.lexeme in self.symbols['global']:
                type_found = self.get_type_expression(identifier, self.expr_array)

                if not type_found == 'invalid' and self.symbols['global'][identifier.lexeme]['type'] != type_found:
                    self.add_error(identifier, 'You cannot assign `' + type_found +'` to ' + '`' + self.symbols['global'][identifier.lexeme]['type'] + '`')
        
        self.access_assign = ''
        self.expr = ''
        self.expr_array = []
        self.reading_expr = False
    
    def verify_return_type(self, token):
        if not hasattr(token, 'lexeme'):
            return

        if '@return' in self.symbols[self.scope]:
            return_type = self.symbols[self.scope]['@return']

            type_found = self.get_type_expression(token, self.expr_array)
                
            if not return_type == type_found:
                self.add_error(token, 'You cannot return `' + type_found +'` into ' + '`' + return_type + '`')
        else:
            self.add_error(token, 'A procedure does not contain any return.')
        
        self.expr = ''
        self.expr_array = []
        self.reading_expr = False
        self.return_found = False
        self.reading_function = False

    def verify_function_returned(self, token):
        if not hasattr(token, 'lexeme'):
            return

        if self.reading_function:
            if not self.return_found:
                self.add_error(token, 'The function should have a return value.')
        self.return_found = False
        self.reading_function = False

    def verify_is_int(self, token):
        if not hasattr(token, 'lexeme'):
            return

        type_found = self.get_type_expression(token, self.int_expr_array)
        
        if not 'int' == type_found:
            self.add_error(token, 'You cannot use a non int as an array index.')
        
        self.int_expr = ''
        self.int_expr_array = []
        self.int_reading_expr = False

    def init_int_expr(self):
        self.int_expr = ''
        self.int_expr_array = []
        self.int_reading_expr = True

    def add_int_expr(self, expr_increment, token):
        if self.int_reading_expr:
            self.int_expr += expr_increment
            self.int_expr_array.append(token)

    def add_expr(self, expr_increment, token):
        if self.reading_expr:
            self.expr += expr_increment
            self.expr_array.append(token)

    def init_expr(self):
        self.expr = ''
        self.expr_array = []
        self.reading_expr = True

    def open_function(self, identifier, init_index_array, array):
        end_index_array = init_index_array + 1
        open_amount = 0
        first_open = True
        func_array = [array[init_index_array]]
        func_len = len(array)
        error = False
        child_error = False
        func_str = array[init_index_array].lexeme
        function_name = array[init_index_array].lexeme
        
        # gets the function array in the initial array
        while end_index_array < func_len:
            token = array[end_index_array]
            if not first_open and open_amount == 0:
                break
            elif token.lexeme == '(':
                if first_open or open_amount > 0:
                    open_amount += 1
                elif open_amount == 0:
                    break
            elif token.lexeme == ')':
                if open_amount == 0:
                    break
                else:
                    open_amount -= 1

            func_array.append(token)
            end_index_array += 1
            first_open = False

        params_index = 3
        open_amount = 0
        func_str += '('
        cur_param = [func_array[2]]
        func_array_w_types = [func_array[0], func_array[1]]
        no_params = False

        if params_index >= len(func_array):
            no_params = True
            func_str += ')'

        while params_index < len(func_array):
            token = func_array[params_index]
            
            if token.lexeme == '(':
                open_amount += 1
                cur_param.append(token)
            elif token.lexeme == ')' and open_amount > 0:
                open_amount -= 1
                cur_param.append(token)
            elif open_amount == 0 and (token.lexeme == ',' or token.lexeme == ')'):
                param_type = self.get_type_expression(identifier, cur_param)
                func_str += param_type
                func_str += token.lexeme

                tk = ''
                if param_type == 'int':
                    tk = Token('0', Code.NUMBER, identifier.line_begin_index, identifier.line_end_index, identifier.column_begin_index, identifier.column_end_index)
                elif param_type == 'real':
                    tk = Token('0.0', Code.NUMBER, identifier.line_begin_index, identifier.line_end_index, identifier.column_begin_index, identifier.column_end_index)
                elif param_type == 'string':
                    tk = Token('" "', Code.KEYWORD, identifier.line_begin_index, identifier.line_end_index, identifier.column_begin_index, identifier.column_end_index)
                elif param_type == 'boolean':
                    tk = Token('true', Code.KEYWORD, identifier.line_begin_index, identifier.line_end_index, identifier.column_begin_index, identifier.column_end_index)
                else:
                    tk = Token('object', Code.IDENTIFIER, identifier.line_begin_index, identifier.line_end_index, identifier.column_begin_index, identifier.column_end_index)
                
                func_array_w_types.append(tk)
                func_array_w_types.append(token)
                cur_param = []
            else:
                cur_param.append(token)

            params_index += 1

        #verify if the function exists:
        func_declared = False
        found_key = ''
        return_type = func_str
        
        if no_params:
            if func_str in self.symbols:
                func_declared = True
                found_key = func_str
        else:
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
                                    
                        if function_name + '(' + params_str + ')' == func_str:
                            func_declared = True
                            found_key = key
                            break
                except:
                    func_declared = False

        if func_declared:
            if '@return' in self.symbols[found_key]:
                return_type = self.symbols[found_key]['@return']
                if return_type == 'int':
                    return_type = '0'
                elif return_type == 'real':
                    return_type = '0.0'
                elif return_type == 'string':
                    return_type = '" "'
                elif return_type == 'boolean':
                    return_type = 'true'
            else:
                self.add_error(array[init_index_array], 'A procedure does not returns any type:`' + func_str + '`.')
        elif not child_error:
            self.add_error(array[init_index_array], 'This function does not exists: `' + func_str + '`.')
            error = True

        if not error:
            error = child_error
            
        return [end_index_array, return_type, error]

    def verify_const_declaration_expr(self, type):
        if not hasattr(type, 'lexeme'):
            return

        type_found = self.get_type_expression(type, self.expr_array)
            
        if type.lexeme != type_found:
            self.add_error(type, 'You cannot assign `' + type_found +'` into ' + '`' + type.lexeme + '`')
        
        self.expr = ''
        self.expr_array = []
        self.reading_expr = False

    def verify_struct_exists(self, token):
        if not hasattr(token, 'lexeme'):
            return

        if not token.lexeme in self.symbols:
            self.add_error(token, 'The structs: `' + token.lexeme + '` does not exists.')

    def verify_id_on_access(self, last_token, cur_token, scope):
        if not (last_token.lexeme == 'global' or last_token.lexeme == 'local'):
            if scope == 'local' or scope == '':
                scope = self.scope

            if last_token.lexeme in self.symbols[scope]:
                type_found = self.symbols[scope][last_token.lexeme]['type']

                if type_found == 'int' or type_found == 'real' or type_found == 'boolean' or type_found == 'string':
                    self.add_error(cur_token, 'You cannot access variables of the type: `' + type_found + '`')
                elif not cur_token.lexeme in self.symbols[type_found]:
                    self.add_error(cur_token, '`' + cur_token.lexeme + '` does not exists on: `' + last_token.lexeme + '`')

        """ if not last_token in self.symbols:
        if not identifier.lexeme in self.symbols[self.scope] and not identifier.lexeme in self.symbols['global']:
            self.add_error(identifier, 'Identifier not declared: `' + identifier.lexeme + '`') """

    def init_access_reading(self, begining_token):
        self.reading_access = True
        self.access_token = begining_token
        
    def add_access_reading(self, token):
        if not hasattr(token, 'lexeme'):
            return

        if self.reading_access:
            self.access += token.lexeme

    def get_access_type(self, access, token, from_get_type=False):
        if not hasattr(token, 'lexeme'):
            return

        array_count = access.count('[');
        aux_string = access.replace("[", "").replace("]", "")
        last_array = 0
        access_array = aux_string.split('.');
        first_item = True
        last_scope = access_array[0]
        cur_str = access_array[0]
        error = False
        
        if last_scope != 'global' and last_scope != 'local':
            if last_scope in self.symbols[self.scope]:
                last_scope = self.symbols[self.scope][last_scope]['type']
            elif last_scope in self.symbols['global']:
                last_scope = self.symbols['global'][last_scope]['type']
            else:
                self.add_error(token, 'This identifier does not exist: `' + cur_str + '`')
                return 'invalid'

        if from_get_type and len(access_array) == 1:
            lexeme = access_array[0]

            if lexeme in self.symbols[self.scope]:
                if 'array' in self.symbols[self.scope][lexeme]:
                    last_array = self.symbols[self.scope][lexeme]['array']
            elif lexeme in self.symbols['global']:
                if 'array' in self.symbols['global'][lexeme]:
                    last_array = self.symbols['global'][lexeme]['array']

        for index, item in enumerate(access_array):
            if not first_item:
                cur_str += '.'
                cur_str += item
                
                if last_scope == 'global':
                    if item in self.symbols['global']:
                        if 'array' in self.symbols['global'][item]:
                            last_array = self.symbols['global'][item]['array']
                        last_scope = self.symbols['global'][item]['type']
                    else:
                        self.add_error(token, 'This identifier does not exist: `' + cur_str + '`')
                        error = True
                        break
                elif last_scope == 'local':
                    if item in self.symbols[self.scope]:
                        if 'array' in self.symbols[self.scope][item]:
                            last_array = self.symbols[self.scope][item]['array']
                        last_scope = self.symbols[self.scope][item]['type']
                    else:
                        self.add_error(token, 'This identifier does not exist: `' + cur_str + '`')
                        error = True
                        break
                else:
                    if last_scope in self.symbols:
                        if item in self.symbols[last_scope]:
                            if 'array' in self.symbols[last_scope][item]:
                                last_array = self.symbols[last_scope][item]['array']
                            last_scope = self.symbols[last_scope][item]['type']
                        else:
                            self.add_error(token, 'This identifier does not exist: `' + cur_str + '`')
                            error = True
                            break
                    else:
                        if index + 1 < len(access_array):
                            self.add_error(token, 'This identifier does not exist: `' + cur_str + '`')
                            error = True
                            break
            first_item = False
            
        if from_get_type: 
            if array_count < last_array:
                self.add_error(token, 'You are not accessing the correct last array dimension: `' + access + '`')
            elif array_count > last_array:
                if last_array == 0:
                    self.add_error(token, 'This identifier is not an array: `' + access + '`')
                else:
                    self.add_error(token, 'You cannot access an inexistent dimension: `' + access + '`')
        elif not self.reading_expr:
            if array_count > last_array:
                if last_array == 0:
                    self.add_error(token, 'This identifier is not an array: `' + access + '`')
                else:
                    self.add_error(token, 'You cannot access an inexistent dimension: `' + access + '`')
            

        if error:
            return 'invalid'

        return last_scope

    def end_access_reading(self, will_assign):
        if self.reading_access and self.access != '':
            type_found = self.get_access_type(self.access, self.access_token)
            if will_assign:
                self.access_assign = type_found
        self.access = ''
        self.reading_access = False
        self.access_token = ''
            
    def verify_type_not_exists(self, type_token):
        if not hasattr(type_token, 'lexeme'):
            return

        if (type_token.lexeme == 'int' or type_token.lexeme == 'struct' 
            or type_token.lexeme == 'string' or type_token.lexeme == 'boolean'
            or type_token.lexeme == 'real'):
            return

        if '@types' in self.symbols[self.scope]:
            if not type_token.lexeme in self.symbols[self.scope]['@types'] and not type_token.lexeme in self.symbols['global']['@types']:
                self.add_error(type_token, 'This type has not defined: `' + type_token.lexeme + '`')   
        elif '@types' in self.symbols['global']:
            if not type_token.lexeme in self.symbols['global']['@types']:
                self.add_error(type_token, 'This type has not defined: `' + type_token.lexeme + '`')
        else:
            self.add_error(type_token, 'This type has not defined: `' + type_token.lexeme + '`')

    def add_type(self, new_type, type_token): 
        if not hasattr(new_type, 'lexeme') or not hasattr(type_token, 'lexeme'):
            return

        if '@types' in self.symbols[self.scope]:
            if new_type.lexeme in self.symbols[self.scope]['@types']:
                self.add_error(new_type, 'This type is already defined: `' + new_type.lexeme + '`')
            else:
                self.symbols[self.scope]['@types'][new_type.lexeme] = { 'type': type_token.lexeme }
        else:
            self.symbols[self.scope]['@types'] = {}
            self.symbols[self.scope]['@types'][new_type.lexeme] = { 'type': type_token.lexeme }

    def extends(self, child, parent):
        if not hasattr(child, 'lexeme') or not hasattr(parent, 'lexeme'):
            return

        if parent.lexeme in self.symbols:
            self.symbols[child.lexeme] = self.symbols[parent.lexeme].copy()
        else:
            self.add_error(parent, 'You cannot extend from an inexistent struct: `' + parent.lexeme + '`')

    def proc_call_add_param(self, token):
        if not hasattr(token, 'lexeme'):
            return

        if self.reading_proc_call:
            self.proc_call_str += token.lexeme
            self.proc_call_array.append(token)

    def init_proc_call(self, token):
        if not hasattr(token, 'lexeme'):
            return

        self.proc_call_token = token
        self.proc_call_str = token.lexeme
        self.reading_proc_call = True
        self.proc_call_array = [token]

    def verify_proc_not_declared(self):
        if self.reading_proc_call:
            cur_param = []
            params = []
            open_counter = 0
            index = 2

            while index < len(self.proc_call_array) :
                token = self.proc_call_array[index]
                
                if token.lexeme == '(':
                    cur_param.append(token)
                    open_counter += 1
                elif token.lexeme == ')':
                    if open_counter == 0 :
                        params.append(cur_param)
                        cur_param = []
                    else:
                        cur_param.append(token)
                        open_counter -= 1
                elif token.lexeme == ',' and open_counter == 0:
                    params.append(cur_param)
                    cur_param = []
                else:
                    cur_param.append(token)
                index += 1

            types = []
            no_params = True

            for param in params:
                if param:
                    no_params = False
                    types.append(self.get_type_expression(self.proc_call_token, param))
            
            proc = self.proc_call_token.lexeme + '('

            for index, p in enumerate(types):
                proc += p
                if index + 1< len(types):
                    proc += ','

            proc += ')'
        
            ## verify existance on symbols table:
            if no_params:
                if not proc in self.symbols:
                    self.add_error(self.proc_call_token, 'This func/procedure does not exist: `' + proc + '`')
            else:
                keys = []
                found = False

                for key in self.symbols:
                    if self.proc_call_token.lexeme + '(' in key:
                        keys.append(key)

                for key in keys:
                    name = key[(key.index('(') + 1):key.index(')')]
                    params_name = name.split(',')
                    keys_params = ''

                    for index, p_n in enumerate(params_name):
                        if len(p_n.split()) > 0:
                            keys_params += p_n.split()[0]
                            if index  +1 < len(params_name):
                                keys_params += ','

                    if proc == self.proc_call_token.lexeme + '(' + keys_params + ')':
                        found = True

                if not found:
                    self.add_error(self.proc_call_token, 'This func/procedure does not exist: `' + proc + '`')

        self.proc_call_token = None
        self.proc_call_str = ''
        self.reading_proc_call = False
        self.proc_call_array = []

    def increment_array(self, identifier):
        if not hasattr(identifier, 'lexeme'):
            return

        if self.var_decl:
            if identifier.lexeme in self.symbols[self.scope]:
                if 'array' in self.symbols[self.scope][identifier.lexeme]:
                    self.symbols[self.scope][identifier.lexeme]['array'] += 1
                else:
                    self.symbols[self.scope][identifier.lexeme]['array'] = 1

    def add_error_empty_array(self, token):
        if not self.var_decl:
            self.add_error(token, 'You should insert a index on that array.')

    def init_var_decl(self):
        self.var_decl = True

    def end_var_decl(self):
        self.var_decl = False

    def init_array_count(self):
        self.array_counting = True
        self.array_count = 0
        
    def add_array_count(self):
        if self.array_counting:
            self.array_count += 1

    def end_array_count(self, identifier):
        if not hasattr(identifier, 'lexeme'):
            return

        if self.array_counting and not self.reading_access:
            is_a_function = False

            for key in self.symbols:
                try:
                    proc_key = key[:(key.index('('))] + '('
                    if identifier.lexeme + '(' == proc_key:
                        is_a_function = True
                        break
                except:
                    is_a_function = False

            if is_a_function:
                self.add_error(identifier, 'You cannot access a function/procedure using indexes: `' + identifier.lexeme + '`')
            else:
                if identifier.lexeme in self.symbols[self.scope]:
                    array = self.symbols[self.scope][identifier.lexeme]['array']
                    
                    if self.array_count > array:
                        self.add_error(identifier, 'You cannot access an inexistent dimension at: `' + identifier.lexeme + '`')
                elif identifier.lexeme in self.symbols['global']:
                    array = self.symbols['global'][identifier.lexeme]['array']
                    
                    if self.array_count > array:
                        self.add_error(identifier, 'You cannot access an inexistent dimension at: `' + identifier.lexeme + '`')
                else:
                    self.add_error(identifier, 'Identifier not declared: `' + identifier.lexeme + '`')

        self.array_counting = False
        self.array_count = 0

    def add_start_error(self, token):
        if not hasattr(token, 'lexeme'):
            return

        self.add_error(token, 'You already declared a start() procedure.')

    def log(self):
        print(self.symbols)

