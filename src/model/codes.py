'''
This enum contains codes of lexeme types.
'''
from enum import Enum

class Code(Enum):
    KEYWORD = 'PRE'
    IDENTIFIER = "IDE"
    NUMBER = 'NRO'
    DELIMITER = "DEL"
    OP_RELATIONAL = 'REL'
    OP_LOGICAL = 'LOG'
    OP_ARITHMETIC = 'ART' 
    INVALID_SYMBOL = 'SIB'
    STRING = 'CAD'
    COMMENT = 'COM'

    MF_NUMBER = 'NMF' 
    MF_COMMENT = 'CoMF'
    MF_OPERATOR = 'OpMF'
    MF_STRING = 'CMF'

