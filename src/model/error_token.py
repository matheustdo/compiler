'''
This class represents the error token.
'''
from src.model.code import Code

class ErrorToken():
    def __init__(self, line_begin_index, error_message):
        self.code = Code.MF_SYNTAX
        self.line_begin_index = line_begin_index
        self.error_message = error_message
    
    def __str__(self):
        return str(self.line_begin_index + 1) + '  ' + self.error_message