'''
This file has all needed functions to tokenize elements.
'''
import re
import lexicon

letter = re.compile(r'[a-zA-Z]')
letter_digit_underscore = re.compile(r'[a-zA-Z0-9_]')

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
        return {'token': '< ' + number + ', number_error, ' + str(line_index + 1) + ' >', 'column_index': column_index}
    else:
        return {'token': '< ' + number + ', number, ' + str(line_index + 1) + ' >', 'column_index': column_index}

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
        return {'token': '< ' + id_or_word + ', word , ' + str(line_index + 1) + ' >', 'column_index': column_index}
    else:
        return {'token': '< ' + id_or_word + ', identifier , ' + str(line_index + 1) + ' >', 'column_index': column_index}

'''
This functions tokenizes a delimiter using the line and column index, the delimiter character
and returns its token and next char column
'''
def tokenize_delimiter(line_index, column_index, delimiter): 
    return {'token': '< ' + delimiter + ', delimiter, ' + str(line_index + 1) + ' >', 'column_index': column_index + 1}

'''
This function tokenizes input lines and returns an array containing generated tokens.
'''
def get_tokens(input_lines): 
    tokens = []
    column_index = 0
    
    for line_index, line in enumerate(input_lines):  
        while column_index < len(line):
            if line[column_index] in lexicon.delimiters:
                result_pair = tokenize_delimiter(line_index, column_index, line[column_index])
                column_index = result_pair['column_index']
                tokens.append(result_pair['token'])
            elif line[column_index] in lexicon.digits:
                result_pair = tokenize_number(line_index, column_index, line)
                column_index = result_pair['column_index']
                tokens.append(result_pair['token'])
            elif letter.match(line[column_index]):
                result_pair = tokenize_id_or_word(line_index, column_index, line)
                column_index = result_pair['column_index']
                tokens.append(result_pair['token'])
            else:
                column_index += 1
            
    return tokens