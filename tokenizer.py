'''
This file has all needed functions to tokenize elements.
'''
import re
import lexicon
from token import Token

letter = re.compile(lexicon.letter)
letter_digit_underscore = re.compile(lexicon.letter_digit_underscore)

'''
This function tokenizes a possible number and returns its token.
'''
def tokenize_number(line_index, column_index, line): 
    number = line[column_index]
    end_index = column_index
    dot_found = False
    decimal_inserted = False
    
    while end_index + 1 < len(line) and (line[end_index + 1] in lexicon.digits or (not dot_found and line[end_index + 1] == '.')):
        number += line[end_index + 1]

        if(dot_found):
            decimal_inserted = True
        elif(line[end_index + 1] == '.'):
            dot_found = True

        end_index += 1

    # If the number contains a "dot", it should have decimal numbers.
    if dot_found and not decimal_inserted:
        return Token(number, 'number_error', line_index, column_index, end_index)
    else:
        return Token(number, 'number', line_index, column_index, end_index)

'''
This function converts an id or a word into a token and returns its token.
'''
def tokenize_id_or_word(line_index, column_index, line):
    id_or_word = line[column_index]
    end_index = column_index

    while end_index + 1 < len(line) and letter_digit_underscore.match(line[end_index + 1]):
        id_or_word += line[end_index + 1]
        end_index += 1

    if id_or_word in lexicon.reserved_words:
        return Token(id_or_word, 'word', line_index, column_index, end_index)
    else:
        return Token(id_or_word, 'identifier', line_index, column_index, end_index)

'''
This functions tokenizes a delimiter and returns its token.
'''
def tokenize_delimiter(line_index, column_index, delimiter): 
    return Token(delimiter, 'delimiter', line_index, column_index, column_index)

'''
This functions tokenizes an arithmetic operator and return its token.
'''
def tokenize_arithmetic_op(line_index, column_index, line):
    arithmetic_op = line[column_index]
    end_index = column_index
    
    if arithmetic_op + line[end_index + 1] in lexicon.arithmetic_operators_extended:
        arithmetic_op += line[end_index + 1] 
        end_index += 1

    return Token(arithmetic_op, 'arithmetic_op', line_index, column_index, end_index)

'''
This functions tokenizes a relational operator and return its token.
'''
def tokenize_relational_op(line_index, column_index, line):
    relational_op = line[column_index]
    end_index = column_index
    
    if relational_op + line[end_index + 1] in lexicon.relational_operators_extended:
        relational_op += line[end_index + 1] 
        end_index += 1

    return Token(relational_op, 'relational_op', line_index, column_index, end_index)

'''
This functions tokenizes a logical operator and return its token.
'''
def tokenize_logical_op(line_index, column_index, line):
    logical_op = line[column_index]
    end_index = column_index
    
    if logical_op + line[end_index + 1] in lexicon.logical_operators_extended:
        logical_op += line[end_index + 1] 
        end_index += 1
    elif not logical_op in lexicon.common_relational_logical:
        return Token(logical_op, 'logical_op_error', line_index, column_index, end_index)

    return Token(logical_op, 'logical_op', line_index, column_index, end_index)

'''
This functions chooses which tokenize function should be called to get a relational or logical operator.
'''
def tokenize_relational_or_logical_op(line_index, column_index, line):
    relational_or_logical_op = line[column_index]
    end_index = column_index

    if relational_or_logical_op + line[end_index + 1] in lexicon.relational_operators_extended:
        return tokenize_relational_op(line_index, column_index, line)

    return tokenize_logical_op(line_index, column_index, line)

'''
This function tokenizes input lines and returns an array containing generated tokens.
'''
def get_tokens(input_lines): 
    tokens = []
    column_index = 0

    for line_index, line in enumerate(input_lines):  
        while column_index < len(line):
            char = line[column_index]
            
            if char in lexicon.delimiters:
                token = tokenize_delimiter(line_index, column_index, line[column_index])
                column_index = token.column_end_index + 1
                tokens.append(token)
            elif char in lexicon.digits:
                token = tokenize_number(line_index, column_index, line)
                column_index = token.column_end_index + 1
                tokens.append(token)
            elif char in lexicon.arithmetic_operators_beginning:
                token = tokenize_arithmetic_op(line_index, column_index, line)
                column_index = token.column_end_index + 1
                tokens.append(token)
            elif char in lexicon.relational_operators_beginning:
                token = tokenize_relational_op(line_index, column_index, line)
                column_index = token.column_end_index + 1
                tokens.append(token)
            elif char in lexicon.logical_operators_beginning:
                token = tokenize_logical_op(line_index, column_index, line)
                column_index = token.column_end_index + 1
                tokens.append(token)
            elif char in lexicon.common_relational_logical:
                token = tokenize_relational_or_logical_op(line_index, column_index, line)
                column_index = token.column_end_index + 1
                tokens.append(token)
            elif letter.match(line[column_index]):
                token = tokenize_id_or_word(line_index, column_index, line)
                column_index = token.column_end_index + 1
                tokens.append(token)
            else:
                column_index += 1
        column_index = 0 
            
    return tokens