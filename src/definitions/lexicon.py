'''
This file contains constants of the language lexicon.
'''

keywords = ['var', 'const', 'typedef', 'struct', 'extends', 'procedure',
                 'function', 'start', 'return', 'if', 'else', 'then', 'while',
                 'read', 'print', 'int', 'real', 'boolean', 'string', 'true',
                 'false', 'global', 'local']

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

letter = r'[a-zA-Z]'

letter_digit_underscore = r'[a-zA-Z0-9_]'

delimiters = [';', ',', '(', ')', '{', '}', '[', ']', '.']

arithmetic_operators_beginning = ['+', '-', '*']

arithmetic_operators_extended = ['++', '--']

relational_operators_beginning = ['<', '>', '=',]

relational_operators_extended = ['<=', '>=', '==', '!=']

logical_operators_beginning = ['&', '|']

logical_operators_extended = ['&&', '||', '!']

comment_extended = ['//', '/*', '*/']

common_arithmetic_comment = '/'

common_relational_logical = '!'

string_delimiter = chr(34)

symbol = r'[\x20-\x21\x23-\x7E]'

letter_digit_symbol = r'[a-zA-Z0-9\x20-\x21\x23-\x7E]'