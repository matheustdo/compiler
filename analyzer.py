import re
import lexicon
import filer

digit = re.compile(r'[0-9]')
letter = re.compile(r'[a-zA-Z]')
letter_digit_underscore = re.compile(r'[a-zA-Z0-9_]')

'''
This function tokenize a possible number and returns the token and its last char column.
'''
def tokenize_number(line_index, column_index, line): 
    number = line[column_index]
    column_index += 1
    dot_found = False
    decimal_inserted = False
    
    while column_index < len(line) and (digit.match(line[column_index]) or (not dot_found and line[column_index] == '.')):
        number += line[column_index]

        if(dot_found):
            decimal_inserted = True
        elif(line[column_index] == '.'):
            dot_found = True

        column_index += 1

    # If the number contains a "dot", it should have decimal numbers.
    if dot_found and not decimal_inserted:
        return {'token': '<' + number + ', number_error >', 'column_index': column_index}
    else:
        return {'token': '<' + number + ', number >', 'column_index': column_index}

'''
This function converts an id or a word into a token and returns the token and its last char column.
'''
def tokenize_id_or_word(line_index, column_index, line):
    id_or_word = line[column_index]
    column_index += 1

    while column_index < len(line) and letter_digit_underscore.match(line[column_index]):
        id_or_word += line[column_index]
        column_index += 1

    if id_or_word in lexicon.reserved_words:
        return {'token': '<' + id_or_word + ', word , ' + str(line_index + 1) + ' >', 'column_index': column_index}
    else:
        return {'token': '<' + id_or_word + ', identifier , ' + str(line_index + 1) + ' >', 'column_index': column_index}

'''
This function tokenizes input lines and returns an array containing generated tokens.
'''
def get_tokens(input_lines): 
    tokens = []
    column_index = 0
    
    for line_index, line in enumerate(input_lines):  
        while column_index < len(line):
            if digit.match(line[column_index]):
                result_pair = tokenize_number(line_index, column_index, line)
                column_index = result_pair['column_index']
                tokens.append(result_pair['token'])
            if letter.match(line[column_index]):
                result_pair = tokenize_id_or_word(line_index, column_index, line)
                column_index = result_pair['column_index']
                tokens.append(result_pair['token'])
            else:
                column_index += 1
            
    return tokens

input_path = 'input/'
output_path = 'output/'
valid_files = filer.get_input_files(input_path)
filer.init_output_folder(output_path)

for valid_file in valid_files:
    # read the input file
    input_file = open(input_path + valid_file, "r")
    input_lines = filer.get_file_lines(input_path, valid_file)

    # generate output content
    tokens = get_tokens(input_lines)
    output_content = ''
    for token in tokens:
        output_content += token + '\n'

    # create and write an output file
    filer.write_file(output_path, valid_file, output_content)

