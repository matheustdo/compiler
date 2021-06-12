'''
This class does the semantic analysis.
'''

from src.model.error_token import ErrorToken
from src.model.code import Code

class Semantic:
    def __init__(self):
        self.symbols = {
            'global': {

            }
        }
        self.semantic_tokens = []
        self.scope = 'global'

    def add(self, scope, key, item):
        self.symbols[scope][key] = item
        self.log()

    def add_id_declaration(self, identifier, attributes): 
        print(self.scope)
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
        self.log()

    def create_fp_scope(self, identifier):
        if identifier.lexeme in self.symbols['global'] or identifier.lexeme in self.symbols:
            self.add_error(identifier, 'There is another Id with the same name in the global scope: `global.' + identifier.lexeme + '`')
        else:
            self.symbols[identifier.lexeme] = { }
            self.scope = identifier.lexeme

    def log(self):
        print(self.symbols)

