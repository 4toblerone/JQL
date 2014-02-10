"""Create lexical analyzer/define tokens"""


predicate = {
  "select" : "SELECT",
  "delete" : "DELETE",
  "insert" : "INSERT",
  "replace" : "REPLACE"
}

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'



def t_COMMA(token):
    r','
    return token

def t_EXCLAMATIONEQUAL(token):
    r'!='
    return token

def t_EQUAL(token):
    r'='
    return token

def t_EXCLAMATION(token):
    r'!'
    return token

def t_2XEQUAL(token):
    r'=='
    return token



def t_STRING(t):
        r'"[^"]*"'
        t.value = t.value[1:-1] # drop "surrounding quotes"
        return t

def t_WORD(t):
    r'[a-z]+'
    if t.value in predicate:
      #t.type = predicate.get(t.value)
      t.type = predicate.get(t.value,'ID')
    return t

def t_NUMBER(token):
    r'[0-9]+'
    token.value = int(token.value)
    return token

def t_WHITESPACES(token):
    r'" "'
    pass

def t_error(t):
    print 'Illegal character'
    t.lexer.skip(1)

t_ignore = ' \t\v\r' # shortcut for whitespaces



tokens = [
          'PLUS',
          'MINUS',
          'TIMES',
          'DIVIDE',
          'LCURLYB',
          'RCURLYB',
          'LBRACKET',
          'RBRACKET',
          'COMMA',
          'DOTCOMMA',
          'EQUAL',
          'EXCLAMATION',
          '2XEQUAL',
          'EXCLAMATIONEQUAL',
          'STRING',
          'WORD',
          'NUMBER',
          'WHITESPACES'
          ] + list(predicate.values())

