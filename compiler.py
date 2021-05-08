'''
Main compiler code:
'''
from src.util import filer
from src.model.code import Code
from src.controller.lexer import Lexer
from src.controller.parser import Parser

INPUT_PATH = 'input/'
OUTPUT_PATH = 'output/'
INPUT_PREFIX = 'entrada'
OUTPUT_PREFIX = 'saida'
valid_files = filer.get_input_files(INPUT_PATH, INPUT_PREFIX)
filer.init_output_folder(OUTPUT_PATH)

print('\033[1;34m> There are ' + str(len(valid_files)) + ' valid input files on /input.\033[0;0m')
print('\033[1;34m> Reading files...\033[0;0m')

for valid_file in valid_files:
    # read the input file
    input_lines = filer.get_file_lines(INPUT_PATH, valid_file)

    # generate output content
    lexer = Lexer(input_lines)
    lexer.execute()
    lexical_tokens = lexer.lexical_tokens
    lexical_tokens_length = len(lexical_tokens)

    parser = Parser(lexical_tokens)
    parser.execute()
    syntactic_tokens = parser.syntactic_tokens
    syntactic_tokens_length = len(syntactic_tokens)

    output_content = ''
    lexical_errors_amount = 0
    syntactic_errors_amount = 0

    for token_index, token in enumerate(syntactic_tokens):
        output_content += str(token)
        if token.code == Code.INVALID_SYMBOL or token.code == Code.MF_COMMENT or token.code == Code.MF_NUMBER or token.code == Code.MF_OPERATOR or token.code == Code.MF_STRING:
            lexical_errors_amount += 1
        if token.code == Code.MF_SYNTAX:
            syntactic_errors_amount += 1

        if token_index + 1 < syntactic_tokens_length:
            output_content += '\n'

    output_content += '\n\n===================\n'

    if lexical_errors_amount + syntactic_errors_amount > 0:
        output_content += 'Your code has a total of:\n'
        output_content += str(lexical_errors_amount) + ' lexical errors.\n'
        output_content += str(syntactic_errors_amount) + ' syntactic errors.\n'
        print('\033[1;31m> ' + valid_file + ' analyzed and ' + str(lexical_errors_amount + syntactic_errors_amount) + ' errors were found.\033[0;0m')
    else:
        output_content += 'Analysis done successfully! \n0 errors had found.'
        print('\033[0;32m> ' + valid_file + ' analyzed and no errors were found.\033[0;0m')

    # create and write an output file
    filer.write_file(OUTPUT_PATH, OUTPUT_PREFIX + valid_file[len(INPUT_PREFIX):], output_content)

print('\033[1;34m> ' + str(len(valid_files)) + ' files were generated on output/.\033[0;0m')
