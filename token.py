class Token:
    def __init__(self, lexeme, type, line_begin_index, line_end_index, column_begin_index, column_end_index):
        self.lexeme = lexeme
        self.type = type
        self.line_begin_index = line_begin_index
        self.line_end_index = line_end_index
        self.column_begin_index = column_begin_index
        self.column_end_index = column_end_index
    
    def __str__(self):
        return str(self.line_begin_index + 1) + '\t' + self.type  + '\t'+ self.lexeme