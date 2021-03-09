'''
Main lexical analyzer code:
'''
import filer
import tokenizer

input_path = 'input/'
output_path = 'output/'
input_prefix = 'entrada'
output_prefix = 'saida'
valid_files = filer.get_input_files(input_path, input_prefix)
filer.init_output_folder(output_path)

for valid_file in valid_files:
    # read the input file
    input_file = open(input_path + valid_file, "r")
    input_lines = filer.get_file_lines(input_path, valid_file)

    # generate output content
    tokens = tokenizer.get_tokens(input_lines)
    tokens_length = len(tokens)
    output_content = ''
    
    for token_index, token in enumerate(tokens):
        output_content += str(token)
        if token_index + 1 < tokens_length:
            output_content += '\n'

    # create and write an output file
    filer.write_file(output_path, output_prefix + valid_file[len(input_prefix):], output_content)

