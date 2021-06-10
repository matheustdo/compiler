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
        if identifier.lexeme in self.symbols[self.scope]:
            print(identifier, 'This identifier has already been declared.')
            self.add_error(identifier, 'This identifier has already been declared.')
            return False
        self.add(self.scope, identifier.lexeme, attributes)
        return True

    def add_error(self, token, description):
            error_token = ErrorToken(token.line_begin_index, description, Code.MF_SEMANTIC)
            self.semantic_tokens.append(error_token)

    def log(self):
        print(self.symbols)

