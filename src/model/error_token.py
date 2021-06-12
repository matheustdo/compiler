'''
This class represents the error token.
'''

class ErrorToken():
    def __init__(self, line_begin_index, error_message, code):
        self.code = code
        self.line_begin_index = line_begin_index
        self.error_message = error_message
    
    def __str__(self):
        return str(self.line_begin_index + 1) + '  ' + self.code.value + ' ' + self.error_message +  ' '