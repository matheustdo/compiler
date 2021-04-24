'''
Main compiler code:
'''
from src.util import filer
from src.model.codes import Code
from src.controller import lexer
from src.controller import parser

input_path = 'input/'
output_path = 'output/'
input_prefix = 'entrada'
output_prefix = 'saida'
valid_files = filer.get_input_files(input_path, input_prefix)
filer.init_output_folder(output_path)

print('\033[1;34m> There are ' + str(len(valid_files)) + ' valid input files on /input.\033[0;0m')
print('\033[1;34m> Reading files...\033[0;0m')

for valid_file in valid_files:
    # read the input file
    input_lines = filer.get_file_lines(input_path, valid_file)

    # generate output content
    tokens = lexer.get_tokens(input_lines)
    tokens_length = len(tokens)
    output_content = ''
    errors_amount = 0
    parser.parse_tokens(tokens)
    
    for token_index, token in enumerate(tokens):
        output_content += str(token)
        if token.code == Code.INVALID_SYMBOL or token.code == Code.MF_COMMENT or token.code == Code.MF_NUMBER or token.code == Code.MF_OPERATOR or token.code == Code.MF_STRING:
            errors_amount += 1

        if token_index + 1 < tokens_length:
            output_content += '\n'

    output_content += '\n\n===================\n'

    if errors_amount > 0:
        output_content += 'Your code has a total of ' + str(errors_amount) + ' lexical errors.'
        print('\033[1;31m> ' + valid_file + ' analyzed and ' + str(errors_amount) + ' lexical errors were found.\033[0;0m')
    else:
        output_content += 'Lexical analysis done successfully! \n0 lexical errors found.'
        print('\033[0;32m> ' + valid_file + ' analyzed and no lexical errors were found.\033[0;0m')
    
    # create and write an output file
    filer.write_file(output_path, output_prefix + valid_file[len(input_prefix):], output_content)

print('\033[1;34m> ' + str(len(valid_files)) + ' files were generated on output/.\033[0;0m')

