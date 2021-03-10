'''
This file has all needed functions to tokenize elements.
'''
import re
import lexicon
from token import Token

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
        return Token(number, 'number_error', line_index, line_index, column_index, end_column_index)
    else:
        return Token(number, 'number', line_index, line_index, column_index, end_column_index)

'''
This function converts an id or a word into a token and returns its token.
'''
def tokenize_id_or_word(line_index, column_index, line):
    id_or_word = line[column_index]
    end_column_index = column_index

    while end_column_index + 1 < len(line) and letter_digit_underscore.match(line[end_column_index + 1]):
        id_or_word += line[end_column_index + 1]
        end_column_index += 1

    if id_or_word in lexicon.reserved_words:
        return Token(id_or_word, 'word', line_index, line_index, column_index, end_column_index)
    else:
        return Token(id_or_word, 'identifier', line_index, line_index, column_index, end_column_index)

'''
This functions tokenizes a delimiter and returns its token.
'''
def tokenize_delimiter(line_index, column_index, delimiter): 
    return Token(delimiter, 'delimiter', line_index, line_index, column_index, column_index)

'''
This functions tokenizes an arithmetic operator and returns its token.
'''
def tokenize_arithmetic_op(line_index, column_index, line):
    arithmetic_op = line[column_index]
    end_column_index = column_index
    
    if arithmetic_op + line[end_column_index + 1] in lexicon.arithmetic_operators_extended:
        arithmetic_op += line[end_column_index + 1] 
        end_column_index += 1

    return Token(arithmetic_op, 'arithmetic_op', line_index, line_index, column_index, end_column_index)

'''
This functions tokenizes a relational operator and returns its token.
'''
def tokenize_relational_op(line_index, column_index, line):
    relational_op = line[column_index]
    end_column_index = column_index
    
    if relational_op + line[end_column_index + 1] in lexicon.relational_operators_extended:
        relational_op += line[end_column_index + 1] 
        end_column_index += 1

    return Token(relational_op, 'relational_op', line_index, line_index, column_index, end_column_index)

'''
This functions tokenizes a logical operator and returns its token.
'''
def tokenize_logical_op(line_index, column_index, line):
    logical_op = line[column_index]
    end_column_index = column_index
    
    if logical_op + line[end_column_index + 1] in lexicon.logical_operators_extended:
        logical_op += line[end_column_index + 1] 
        end_column_index += 1
    elif not logical_op in lexicon.common_relational_logical:
        return Token(logical_op, 'logical_op_error', line_index, line_index, column_index, end_column_index)

    return Token(logical_op, 'logical_op', line_index, line_index, column_index, end_column_index)

'''
This function tokenizes a string and returns its token.
'''
def tokenize_string(line_index, column_index, line):
    string = line[column_index]
    end_column_index = column_index
    end_found = False
    invalid_symbol_found = False

    while end_column_index + 1 < len(line) and not end_found and not invalid_symbol_found:
        char = line[end_column_index + 1]

        if letter_digit_symbol.match(char):
            string += char
            end_column_index += 1
        elif char in lexicon.string_delimiter:
            # If a quotation mark is found, the last char is verified, and if it is a backslash, the string is not ended.
            if line[end_column_index] != chr(92):
                end_found = True
            string += char
            end_column_index += 1
        else:
            invalid_symbol_found = True

    if end_found and not invalid_symbol_found:
        return Token(string, 'string', line_index, line_index, column_index, end_column_index)

    return Token(string, 'string_error', line_index, line_index, column_index, end_column_index)

'''
This function ignores a comment and returns a token without lexeme to save performance.
'''
def ignore_comment(line_index, column_index, init, input_lines):
    end_line_index = line_index
    end_column_index = column_index + 2

    if init == '//':
        return Token('', 'comment', line_index, end_line_index, column_index, len(input_lines[line_index]) - 1)

    end_reached = False
    comment = init
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

            end_column_index += 1

        if not end_reached:
            end_line_index += 1
            end_column_index = 0

    return Token(comment, 'comment', line_index, end_line_index, column_index, end_column_index)


'''
This function chooses which tokenize function should be called to get a relational or logical operator.
'''
def tokenize_relational_or_logical_op(line_index, column_index, line):
    char = line[column_index]
    next_char = line[column_index + 1]

    if char + next_char in lexicon.relational_operators_extended:
        return tokenize_relational_op(line_index, column_index, line)

    return tokenize_logical_op(line_index, column_index, line)

'''
This function chooses which tokenize function should be called to get an arithmetic operator or a comment.
'''
def tokenize_arithmetic_or_comment(line_index, column_index, line, input_lines):
    char = line[column_index]
    next_char = line[column_index + 1]
    
    if char + next_char in lexicon.comment_extended:
        return ignore_comment(line_index, column_index, char + next_char, input_lines)
    else:
        return tokenize_arithmetic_op(line_index, column_index, line)

'''
This function tokenizes input lines and returns an array containing generated tokens.
'''
def get_tokens(input_lines): 
    tokens = []
    line_index = 0
    column_index = 0

    while line_index < len(input_lines):  
        line = input_lines[line_index]

        while column_index < len(line):
            char = line[column_index]
            token = Token(char, 'invalid_symbol', line_index, line_index, column_index, column_index)

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
                token = tokenize_id_or_word(line_index, column_index, line)

            line_index = token.line_end_index
            column_index = token.column_end_index + 1

            # Add the token to tokens list only if its lexeme is not a blank space or a comment.
            if not token.lexeme.isspace() and token.type != 'commenat':
                tokens.append(token)

        line_index += 1
        column_index = 0 
        
    return tokens