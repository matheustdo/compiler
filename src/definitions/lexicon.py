'''
This file contains constants of the language lexicon.
'''

KEYWORDS = ['var', 'const', 'typedef', 'struct', 'extends', 'procedure',
                 'function', 'start', 'return', 'if', 'else', 'then', 'while',
                 'read', 'print', 'int', 'real', 'boolean', 'string', 'true',
                 'false', 'global', 'local']

DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

LETTER = r'[a-zA-Z]'

LETTER_DIGIT_UNDERSCORE = r'[a-zA-Z0-9_]'

DELIMITERS = [';', ',', '(', ')', '{', '}', '[', ']', '.']

ARITHMETIC_OPERATORS_BEGINNING = ['+', '-', '*']

ARITHMETIC_OPERATORS_EXTENDED = ['++', '--']

RELATIONAL_OPERATORS_BEGINNING = ['<', '>', '=',]

RELATIONAL_OPERATORS_EXTENDED = ['<=', '>=', '==', '!=']

LOGICAL_OPERATORS_BEGGINING = ['&', '|']

LOGICAL_OPERATORS_EXTENDED = ['&&', '||', '!']

LOGICAL_AND_RELATIONAL = ['<', '>', '=','<=', '>=', '==', '!=', '&', '|', '&&', '||', '!']

COMMENT_EXTENDED = ['//', '/*', '*/']

COMMOM_ARITHMETIC_COMMENT = '/'

COMMOM_RELATIONAL_LOGICAL = '!'

STRING_DELIMITER = chr(34)

SYMBOL = r'[\x20-\x21\x23-\x7E]'

LETTER_DIGIT_SYMBOL = r'[a-zA-Z0-9\x20-\x21\x23-\x7E]'
