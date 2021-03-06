'''
This file contains constants of the language lexicon.
'''
reserved_words = ['var', 'const', 'typedef', 'struct', 'extends', 'procedure',
                 'function', 'start', 'return', 'if', 'else', 'then', 'while',
                 'read', 'print', 'int', 'real', 'boolean', 'string', 'true',
                 'false', 'global', 'local']

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

delimiters = [';', ',', '(', ')', '{', '}', '[', ']', '.']

letter = r'[a-zA-Z]'

letter_digit_underscore = r'[a-zA-Z0-9_]'

arithmetic_operators = ['+', '-', '*', '/']