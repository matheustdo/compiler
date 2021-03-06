'''
Main lexical analyzer code:
'''
import filer
import tokenizer

input_path = 'input/'
output_path = 'output/'
valid_files = filer.get_input_files(input_path)
filer.init_output_folder(output_path)

for valid_file in valid_files:
    # read the input file
    input_file = open(input_path + valid_file, "r")
    input_lines = filer.get_file_lines(input_path, valid_file)

    # generate output content
    tokens = tokenizer.get_tokens(input_lines)
    output_content = ''
    for token in tokens:
        output_content += str(token) + '\n'

    # create and write an output file
    filer.write_file(output_path, valid_file, output_content)

