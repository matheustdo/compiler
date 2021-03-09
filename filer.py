'''
This file contains aux functions to manage files.
'''
import os
import re

'''
This function inits the output folder if it is not existant.
'''
def init_output_folder(path_name): 
    if not os.path.exists(path_name):
        os.mkdir(path_name)
        
'''
This function receives the input folder path name, the filename prefix and returns a list containing valid input files.
'''
def get_input_files(path_name, prefix_name):
    if not os.path.exists(path_name):
        print('The directory input/ does not exists.')

    entries = os.listdir(path_name)
    valid_files = []

    for entry in entries:
        if os.path.isfile(path_name + entry) and re.match('entrada[0-9]+.txt', entry): 
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