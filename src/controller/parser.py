'''
This class does the iteration on tokens array and the syntactic analysis.
'''
class Parser:
    def __init__(self, lexical_tokens):
        self.lexical_tokens = lexical_tokens
        self.tokens_index = 0

        if len(lexical_tokens) > 0:
            self.token = lexical_tokens[0]
            self.syntactic_tokens = [lexical_tokens[0]]
        else:
            self.token = None
            self.syntactic_tokens = []

    def advance(self):
        self.tokens_index += 1
        
        if len(self.lexical_tokens) > 0:
            self.token = self.lexical_tokens[self.tokens_index]
        else:
            self.token = None

    def eat(self, lexeme):
        if self.token and lexeme == self.token.lexeme:
            self.advance()
            return True
        else:
            return False

    def program(self):
        """ if parser.current_token().lexeme == 'structs':
            print('FIRST_STRUCTS')
        if parser.current_token().lexeme == 'const':
            print('FIRST_CONST_BLOCK')
        if parser.current_token().lexeme == 'var':
            print('FIRST_CONST_BLOCK')
        if parser.current_token().lexeme == 'procedure':
            print('FIRST_START_BLOCK')
        else:
            parser.add_error('NO START BLOCK HAS FOUND') """

    def execute(self):
        self.program()