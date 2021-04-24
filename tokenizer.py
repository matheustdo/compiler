'''
This file has all needed functions to tokenize elements.
'''
import re
from src.definitions import lexicon
from src.model.token import Token
from src.model.codes import Code

letter = re.compile(lexicon.letter)
letter_digit_underscore = re.compile(lexicon.letter_digit_underscore)
letter_digit_symbol = re.compile(lexicon.letter_digit_symbol)

'''
This function tokenizes a possible number and returns its token.
'''
def tokenize_number(line_index, column_index, line): 
    number = line[column_index]
    end_column_index = column_index
    dot_found = False
    decimal_inserted = False
    
    while end_column_index + 1 < len(line) and (line[end_column_index + 1] in lexicon.digits or (not dot_found and line[end_column_index + 1] == '.')):
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
def tokenize_id_or_keyword(line_index, column_index, line):
    id_or_keyword = line[column_index]
    end_column_index = column_index

    while end_column_index + 1 < len(line) and letter_digit_underscore.match(line[end_column_index + 1]):
        id_or_keyword += line[end_column_index + 1]
        end_column_index += 1

    if id_or_keyword in lexicon.keywords:
        return Token(id_or_keyword, Code.KEYWORD, line_index, line_index, column_index, end_column_index)
    else:
        return Token(id_or_keyword, Code.IDENTIFIER, line_index, line_index, column_index, end_column_index)

'''
This functions tokenizes a delimiter and returns its token.
'''
def tokenize_delimiter(line_index, column_index, delimiter): 
    return Token(delimiter, Code.DELIMITER, line_index, line_index, column_index, column_index)

'''
This functions tokenizes an arithmetic operator and returns its token.
'''
def tokenize_arithmetic_op(line_index, column_index, line):
    arithmetic_op = line[column_index]
    end_column_index = column_index
    
    if end_column_index + 1 < len(line) and arithmetic_op + line[end_column_index + 1] in lexicon.arithmetic_operators_extended:
        arithmetic_op += line[end_column_index + 1] 
        end_column_index += 1

    return Token(arithmetic_op, Code.OP_ARITHMETIC, line_index, line_index, column_index, end_column_index)

'''
This functions tokenizes a relational operator and returns its token.
'''
def tokenize_relational_op(line_index, column_index, line):
    relational_op = line[column_index]
    end_column_index = column_index
    
    if end_column_index + 1 < len(line) and relational_op + line[end_column_index + 1] in lexicon.relational_operators_extended:
        relational_op += line[end_column_index + 1] 
        end_column_index += 1

    return Token(relational_op, Code.OP_RELATIONAL, line_index, line_index, column_index, end_column_index)

'''
This functions tokenizes a logical operator and returns its token.
'''
def tokenize_logical_op(line_index, column_index, line):
    logical_op = line[column_index]
    end_column_index = column_index
    
    if end_column_index + 1 < len(line) and logical_op + line[end_column_index + 1] in lexicon.logical_operators_extended:
        logical_op += line[end_column_index + 1] 
        end_column_index += 1
    elif not logical_op in lexicon.common_relational_logical:
        return Token(logical_op, Code.MF_OPERATOR, line_index, line_index, column_index, end_column_index)

    return Token(logical_op, Code.OP_LOGICAL, line_index, line_index, column_index, end_column_index)

'''
This function tokenizes a string and returns its token.
'''
def tokenize_string(line_index, column_index, line):
    string = line[column_index]
    end_column_index = column_index
    end_found = False
    invalid_symbol_found = False

    while end_column_index + 1 < len(line) and not end_found:
        char = line[end_column_index + 1]
        
        # If a quotation mark is found, the last char is verified, and if it is a backslash, the string is not ended.
        if char in lexicon.string_delimiter:
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
def ignore_comment(line_index, column_index, init, input_lines):
    comment = init
    end_line_index = line_index
    end_column_index = column_index + 2

    if init == '//':
        comment = input_lines[end_line_index][column_index:]
        return Token(comment, Code.COMMENT, line_index, end_line_index, column_index, len(input_lines[line_index]) - 1)

    end_reached = False
    
    while end_line_index < len(input_lines) and not end_reached:  
        line = input_lines[end_line_index]

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
def tokenize_relational_or_logical_op(line_index, column_index, line):
    char = line[column_index]

    # if the current char and the next is a complete relational operator
    if column_index + 1 < len(line) and char + line[column_index + 1] in lexicon.relational_operators_extended:
        return tokenize_relational_op(line_index, column_index, line)

    return tokenize_logical_op(line_index, column_index, line)

'''
This function chooses which tokenize function should be called to get an arithmetic operator or a comment.
'''
def tokenize_arithmetic_or_comment(line_index, column_index, line, input_lines):
    char = line[column_index]
    
    # if the current char and the next is a comment initialization
    if column_index + 1 < len(line) and char + line[column_index + 1] in lexicon.comment_extended:
        return ignore_comment(line_index, column_index, char + line[column_index + 1], input_lines)
    else:
        return tokenize_arithmetic_op(line_index, column_index, line)
        
'''
This function tokenizes input lines and returns an array containing generated tokens.
'''
def get_tokens(input_lines): 
    tokens = []
    line_index = 0
    column_index = 0
    line_index_changed = False

    while line_index < len(input_lines):  
        line = input_lines[line_index]
        line_index_changed = False
        
        while column_index < len(line):
            char = line[column_index]
            token = Token(char, Code.INVALID_SYMBOL, line_index, line_index, column_index, column_index)

            if char in lexicon.delimiters:
                token = tokenize_delimiter(line_index, column_index, line[column_index])
            elif char in lexicon.digits:
                token = tokenize_number(line_index, column_index, line)
            elif char in lexicon.arithmetic_operators_beginning:
                token = tokenize_arithmetic_op(line_index, column_index, line)
            elif char in lexicon.relational_operators_beginning:
                token = tokenize_relational_op(line_index, column_index, line)
            elif char in lexicon.logical_operators_beginning:
                token = tokenize_logical_op(line_index, column_index, line)
            elif char in lexicon.string_delimiter:
                token = tokenize_string(line_index, column_index, line)
            elif char in lexicon.common_relational_logical:
                token = tokenize_relational_or_logical_op(line_index, column_index, line)
            elif char in lexicon.common_arithmetic_comment:
                token = tokenize_arithmetic_or_comment(line_index, column_index, line, input_lines)
            elif letter.match(line[column_index]):
                token = tokenize_id_or_keyword(line_index, column_index, line)
            
            # Add the token to tokens list only if its lexeme is not a blank space or a comment.
            if not token.lexeme.isspace() and token.code != Code.COMMENT:
                tokens.append(token)
            
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
    
    return tokens