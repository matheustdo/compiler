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
        print(identifier)
        if identifier.lexeme in self.symbols[self.scope]:
            self.add_error(identifier, 'This identifier has already been declared: `' + identifier.lexeme + '`')
            return False
        self.add(self.scope, identifier.lexeme, attributes)
        return True

    def verify_id_not_declared(self, identifier):
        if identifier.lexeme in self.symbols[self.scope]:
            return True
        self.add_error(identifier, 'Identifier not declared.')
        return False

    def verify_attribution(self, identifier):
        if identifier.lexeme in self.symbols[self.scope]:
            if (self.symbols[self.scope][identifier.lexeme]['conf'] == 'const'):
                self.add_error(identifier, 'Const attribution is not allowed: `' + identifier.lexeme + '`')
                return False
            if (self.symbols[self.scope][identifier.lexeme]['conf'] == 'func'):
                self.add_error(identifier, 'Func attribution is not allowed: `' + identifier.lexeme + '`')
                return False
        return True

    def add_error(self, token, description):
            error_token = ErrorToken(token.line_begin_index, description, Code.MF_SEMANTIC)
            self.semantic_tokens.append(error_token)

    def log(self):
        print(self.symbols)

