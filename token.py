class Token:
    def __init__(self, lexeme, type, line_index, column_index):
        self.lexeme = lexeme
        self.type = type
        self.line_index = line_index
        self.column_index = column_index
    
    def __str__(self):
        return '< ' + self.lexeme + ', ' + self.type + ', ' + str(self.line_index + 1) + ', ' + str(self.column_index + 1) + ' >'