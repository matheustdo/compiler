'''
This class does the iteration on tokens array.
'''
class ParserList:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def current_token(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        else:
            return None

    def skip_token(self):
        self.index += 1