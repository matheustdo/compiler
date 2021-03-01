import os
import re
from lexicon import lexicon

'''
This function inits the output folder if it is not existant.
'''
def init_output_folder(pathname): 
    if not os.path.exists(pathname):
        os.mkdir(pathname)
        
'''
This function receives the input folder pathname and return a list containing valid input files.
'''
def get_input_files(pathname):
    if not os.path.exists(pathname):
        print('A pasta input/ não foi encontrada no diretório raíz.')

    entries = os.listdir(pathname)
    valid_files = []

    for entry in entries:
        if re.search('^entrada[0-9]+.txt$', entry): 
            valid_files.append(entry)
    
    return valid_files

'''
This function receives a filename, its output pathname and then the file is created 
or overwritten with the informed content.
'''
def write_file(output_folder, filename, content): 
    output_file = open(output_folder + filename, "w")
    output_file.write(content)
    output_file.close()

'''
This function tokenizes the input string and returns an array containing generated tokens.
'''
def get_tokens(string): 
    tokens = []
    new_token = ''

    for char in string:
        if char.isspace():
            if len(new_token) > 0:
                type = lexicon.get(new_token)
                if(type):
                    tokens.append(new_token)
                new_token = ''
        else:
            new_token += char
    
    return tokens

input_path = 'input/'
output_path = 'output/'
valid_files = get_input_files(input_path)
init_output_folder(output_path)

for valid_file in valid_files:
    # read the input file
    input_file = open(input_path + valid_file, "r")
    input_content = input_file.read()
    input_file.close()

    # generate output content
    tokens = get_tokens(input_content)
    output_content = ''
    for token in tokens:
        output_content += token + '\n'

    # create and write an output file
    write_file(output_path, valid_file, output_content)
