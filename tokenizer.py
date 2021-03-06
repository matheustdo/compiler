'''
This file has all needed functions to tokenize elements.
'''
import re
import lexicon
from token import Token

letter = re.compile(lexicon.letter)
letter_digit_underscore = re.compile(lexicon.letter_digit_underscore)

'''
This function tokenize a possible number and returns the token and next char column.
'''
def tokenize_number(line_index, column_index, line): 
    number = line[column_index]
    column_index += 1
    dot_found = False
    decimal_inserted = False
    
    while column_index < len(line) and (line[column_index] in lexicon.digits or (not dot_found and line[column_index] == '.')):
        number += line[column_index]

        if(dot_found):
            decimal_inserted = True
        elif(line[column_index] == '.'):
            dot_found = True

        column_index += 1

    # If the number contains a "dot", it should have decimal numbers.
    if dot_found and not decimal_inserted:
        return Token(number, 'number_error', line_index, column_index)
    else:
        return Token(number, 'number', line_index, column_index)

'''
This function converts an id or a word into a token and returns the token and next char column.
'''
def tokenize_id_or_word(line_index, column_index, line):
    id_or_word = line[column_index]
    column_index += 1

    while column_index < len(line) and letter_digit_underscore.match(line[column_index]):
        id_or_word += line[column_index]
        column_index += 1

    if id_or_word in lexicon.reserved_words:
        return Token(id_or_word, 'word', line_index, column_index)
    else:
        return Token(id_or_word, 'identifier', line_index, column_index)

'''
This functions tokenizes a delimiter using the line and column index, the delimiter character
and returns its token and next char column
'''
def tokenize_delimiter(line_index, column_index, delimiter): 
    return Token(delimiter, 'delimiter', line_index, column_index)

'''
This function tokenizes input lines and returns an array containing generated tokens.
'''
def get_tokens(input_lines): 
    tokens = []
    column_index = 0
    
    for line_index, line in enumerate(input_lines):  
        while column_index < len(line):
            if line[column_index] in lexicon.delimiters:
                token = tokenize_delimiter(line_index, column_index, line[column_index])
                column_index = token.column_index + 1
                tokens.append(token)
            elif line[column_index] in lexicon.digits:
                token = tokenize_number(line_index, column_index, line)
                column_index = token.column_index + 1
                tokens.append(token)
            elif letter.match(line[column_index]):
                token = tokenize_id_or_word(line_index, column_index, line)
                column_index = token.column_index + 1
                tokens.append(token)
            else:
                column_index += 1
            
    return tokens