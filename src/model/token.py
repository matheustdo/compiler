'''
This class represents the token.
'''
class Token:
    def __init__(self, lexeme, code, line_begin_index, line_end_index, column_begin_index, column_end_index):
        self.lexeme = lexeme
        self.code = code
        self.line_begin_index = line_begin_index
        self.line_end_index = line_end_index
        self.column_begin_index = column_begin_index
        self.column_end_index = column_end_index
    
    def __str__(self):
        return str(self.line_begin_index + 1) + '  ' + self.code.value  + '  ' + self.lexeme