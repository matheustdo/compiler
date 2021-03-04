import os
import re

file_format = re.compile(r'entrada[0-9]+.txt')

'''
This function inits the output folder if it is not existant.
'''
def init_output_folder(path_name): 
    if not os.path.exists(path_name):
        os.mkdir(path_name)
        
'''
This function receives the input folder path name and returns a list containing valid input files.
'''
def get_input_files(path_name):
    if not os.path.exists(path_name):
        print('A pasta input/ não foi encontrada no diretório raíz.')

    entries = os.listdir(path_name)
    valid_files = []

    for entry in entries:
        if os.path.isfile(path_name + entry) and file_format.match(entry): 
            valid_files.append(entry)
    
    return valid_files
    
'''
This function receives a file name, its input path name and then the file is readed 
and its lines return as a list.
'''
def get_file_lines(input_path, file_name): 
    input_file = open(input_path + file_name, "r")
    input_lines = input_file.readlines()
    input_file.close()
    return input_lines

'''
This function receives a file name, its output path name and then the file is created 
or overwritten with the informed content.
'''
def write_file(output_path, file_name, content): 
    output_file = open(output_path + file_name, "w")
    output_file.write(content)
    output_file.close()