'''
This file has all needed functions to tokenize and lexer elements.
'''
import re
from src.definitions import lexicon
from src.model.token import Token
from src.model.code import Code

letter = re.compile(lexicon.LETTER)
letter_digit_underscore = re.compile(lexicon.LETTER_DIGIT_UNDERSCORE)
letter_digit_symbol = re.compile(lexicon.LETTER_DIGIT_SYMBOL)

class Lexer:
    def __init__(self, input_lines):
        self.input_lines = input_lines
        self.lexical_tokens = []

    '''
    This function tokenizes a possible number and returns its token.
    '''
    def tokenize_number(self, line_index, column_index, line):
        number = line[column_index]
        end_column_index = column_index
        dot_found = False
        decimal_inserted = False

        while end_column_index + 1 < len(line) and (line[end_column_index + 1] in lexicon.DIGITS or (not dot_found and line[end_column_index + 1] == '.')):
            number += line[end_column_index + 1]

            if dot_found:
                decimal_inserted = True
            elif line[end_column_index + 1] == '.':
                dot_found = True

            end_column_index += 1

        # If the number contains a "dot", it should have decimal numbers.
        if dot_found and not decimal_inserted:
            return Token(number, Code.MF_NUMBER, line_index, line_index, column_index, end_column_index)
        else:
            return Token(number, Code.NUMBER, line_index, line_index, column_index, end_column_index)

    '''
    This function converts an id or a keyword into a token and returns its token.
    '''
    def tokenize_id_or_keyword(self, line_index, column_index, line):
        id_or_keyword = line[column_index]
        end_column_index = column_index

        while end_column_index + 1 < len(line) and letter_digit_underscore.match(line[end_column_index + 1]):
            id_or_keyword += line[end_column_index + 1]
            end_column_index += 1

        if id_or_keyword in lexicon.KEYWORDS:
            return Token(id_or_keyword, Code.KEYWORD, line_index, line_index, column_index, end_column_index)
        else:
            return Token(id_or_keyword, Code.IDENTIFIER, line_index, line_index, column_index, end_column_index)

    '''
    This functions tokenizes a delimiter and returns its token.
    '''
    def tokenize_delimiter(self, line_index, column_index, delimiter):
        return Token(delimiter, Code.DELIMITER, line_index, line_index, column_index, column_index)

    '''
    This functions tokenizes an arithmetic operator and returns its token.
    '''
    def tokenize_arithmetic_op(self, line_index, column_index, line):
        arithmetic_op = line[column_index]
        end_column_index = column_index

        if end_column_index + 1 < len(line) and arithmetic_op + line[end_column_index + 1] in lexicon.ARITHMETIC_OPERATORS_EXTENDED:
            arithmetic_op += line[end_column_index + 1]
            end_column_index += 1

        return Token(arithmetic_op, Code.OP_ARITHMETIC, line_index, line_index, column_index, end_column_index)

    '''
    This functions tokenizes a relational operator and returns its token.
    '''
    def tokenize_relational_op(self, line_index, column_index, line):
        relational_op = line[column_index]
        end_column_index = column_index

        if end_column_index + 1 < len(line) and relational_op + line[end_column_index + 1] in lexicon.RELATIONAL_OPERATORS_EXTENDED:
            relational_op += line[end_column_index + 1]
            end_column_index += 1

        return Token(relational_op, Code.OP_RELATIONAL, line_index, line_index, column_index, end_column_index)

    '''
    This functions tokenizes a logical operator and returns its token.
    '''
    def tokenize_logical_op(self, line_index, column_index, line):
        logical_op = line[column_index]
        end_column_index = column_index

        if end_column_index + 1 < len(line) and logical_op + line[end_column_index + 1] in lexicon.LOGICAL_OPERATORS_EXTENDED:
            logical_op += line[end_column_index + 1]
            end_column_index += 1
        elif not logical_op in lexicon.COMMOM_RELATIONAL_LOGICAL:
            return Token(logical_op, Code.MF_OPERATOR, line_index, line_index, column_index, end_column_index)

        return Token(logical_op, Code.OP_LOGICAL, line_index, line_index, column_index, end_column_index)

    '''
    This function tokenizes a string and returns its token.
    '''
    def tokenize_string(self, line_index, column_index, line):
        string = line[column_index]
        end_column_index = column_index
        end_found = False
        invalid_symbol_found = False

        while end_column_index + 1 < len(line) and not end_found:
            char = line[end_column_index + 1]

            # If a quotation mark is found, the last char is verified, and if it is a backslash, the string is not ended.
            if char in lexicon.STRING_DELIMITER:
                if line[end_column_index] != chr(92):
                    end_found = True
            elif not letter_digit_symbol.match(char):
                invalid_symbol_found = True
            if char != '\n':
                string += char
            end_column_index += 1


        if end_found and not invalid_symbol_found:
            return Token(string, Code.STRING, line_index, line_index, column_index, end_column_index)

        return Token(string, Code.MF_STRING, line_index, line_index, column_index, end_column_index)

    '''
    This function ignores a comment and returns a token without lexeme to save performance.
    '''
    def ignore_comment(self, line_index, column_index, init):
        comment = init
        end_line_index = line_index
        end_column_index = column_index + 2

        if init == '//':
            comment = self.input_lines[end_line_index][column_index:]
            return Token(comment, Code.COMMENT, line_index, end_line_index, column_index, len(self.input_lines[line_index]) - 1)

        end_reached = False

        while end_line_index < len(self.input_lines) and not end_reached:
            line = self.input_lines[end_line_index]

            while end_column_index < len(line) and not end_reached:
                char = line[end_column_index]
                comment += char

                if char == '*' and end_column_index + 1 < len(line):
                    next_char = line[end_column_index + 1]
                    if next_char == '/':
                        comment += next_char
                        end_reached = True

                end_column_index += 1

            if not end_reached:
                end_line_index += 1
                end_column_index = 0

        if end_reached:
            return Token(comment, Code.COMMENT, line_index, end_line_index, column_index, end_column_index)

        return Token(comment, Code.MF_COMMENT, line_index, end_line_index, column_index, end_column_index)


    '''
    This function chooses which tokenize function should be called to get a relational or logical operator.
    '''
    def tokenize_relational_or_logical_op(self, line_index, column_index, line):
        char = line[column_index]

        # if the current char and the next is a complete relational operator
        if column_index + 1 < len(line) and char + line[column_index + 1] in lexicon.RELATIONAL_OPERATORS_EXTENDED:
            return self.tokenize_relational_op(line_index, column_index, line)

        return self.tokenize_logical_op(line_index, column_index, line)

    '''
    This function chooses which tokenize function should be called to get an arithmetic operator or a comment.
    '''
    def tokenize_arithmetic_or_comment(self, line_index, column_index, line):
        char = line[column_index]

        # if the current char and the next is a comment initialization
        if column_index + 1 < len(line) and char + line[column_index + 1] in lexicon.COMMENT_EXTENDED:
            return self.ignore_comment(line_index, column_index, char + line[column_index + 1])
        else:
            return self.tokenize_arithmetic_op(line_index, column_index, line)

    '''
    This function tokenizes input lines and returns an array containing generated tokens.
    '''
    def execute(self):
        line_index = 0
        column_index = 0
        line_index_changed = False
        
        while line_index < len(self.input_lines):
            line = self.input_lines[line_index]
            line_index_changed = False

            while column_index < len(line):
                char = line[column_index]
                token = Token(char, Code.INVALID_SYMBOL, line_index, line_index, column_index, column_index)

                if char in lexicon.DELIMITERS:
                    token = self.tokenize_delimiter(line_index, column_index, line[column_index])
                elif char in lexicon.DIGITS:
                    token = self.tokenize_number(line_index, column_index, line)
                elif char in lexicon.ARITHMETIC_OPERATORS_BEGINNING:
                    token = self.tokenize_arithmetic_op(line_index, column_index, line)
                elif char in lexicon.RELATIONAL_OPERATORS_BEGINNING:
                    token = self.tokenize_relational_op(line_index, column_index, line)
                elif char in lexicon.LOGICAL_OPERATORS_BEGGINING:
                    token = self.tokenize_logical_op(line_index, column_index, line)
                elif char in lexicon.STRING_DELIMITER:
                    token = self.tokenize_string(line_index, column_index, line)
                elif char in lexicon.COMMOM_RELATIONAL_LOGICAL:
                    token = self.tokenize_relational_or_logical_op(line_index, column_index, line)
                elif char in lexicon.COMMOM_ARITHMETIC_COMMENT:
                    token = self.tokenize_arithmetic_or_comment(line_index, column_index, line)
                elif letter.match(line[column_index]):
                    token = self.tokenize_id_or_keyword(line_index, column_index, line)

                # Add the token to tokens list only if its lexeme is not a blank space or a comment.
                if not token.lexeme.isspace() and token.code != Code.COMMENT:
                    self.lexical_tokens.append(token)

                column_index = token.column_end_index + 1

                # if the token index was changed, the columns loop should be broke.
                if line_index != token.line_end_index:
                    line_index = token.line_end_index
                    line_index_changed = True
                    break

            # indexes should be changed only if the line_index was not changed on the last column loop.
            if not line_index_changed:
                line_index += 1
                column_index = 0

        return self.lexical_tokens