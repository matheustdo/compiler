'''
This file has all needed functions to the syntax analysis.
'''
from src.model.parser import Parser

'''
This function will do the syntax analysis of the given tokens.
'''
def parse_tokens(tokens): 
    parser = Parser(tokens)
    print(parser.current_token())
    parser.skip_token()