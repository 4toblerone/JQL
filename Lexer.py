import lex
import TokenDef


class Lexer(object):

    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    @staticmethod
    def breakDownStringToTokens(text):
        lexer = lex.lex(module=TokenDef)
        lexer.input(text)
        tokenList = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokenList.append(tok)
        return tokenList
        """for sometoken in tokenList:
            print sometoken.type """

#proba = Lexer()
# print proba.breakDownStringToTokens("{var } 1 select dele ' neki string'
# < > fdsa -> remove from <= => = == = get where and add fdsfsd")
