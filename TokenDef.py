"""Create lexical analyzer/define tokens"""


predicate = {
  "select" : "SELECT",
  "delete" : "DELETE",
  "insert" : "INSERT",
  "replace" : "REPLACE"
}

states= (("JSONSTRING","exclusive"),)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

def t_start_jsonstring(token):
   r"[uU]?[rR]?'"
   token.lexer.push_state("JSONSTRING")
   token.type = "JSONSTRING_START"
   if "r" in token.value or "R" in token.value:
      token.lexer.is_raw = True
   token.value = token.value.split("'", 1)[0]
   return token

def t_JSONSTRING_simple(token):
    r"[^'\\\n]+"
    token.type = "JSONSTRING"
    return token

def t_JSONSTRING_end(token):
    r"'"
    token.type = "JSONSTRING_END"
    token.lexer.pop_state()
    token.lexer.is_raw = False
    return token

def t_COMMA(token):
    r','
    return token

def t_EXCLAMATIONEQUAL(token):
    r'!='
    return token

def t_LESSOREQUAL(token):
  r'<='
  return token

def t_EQUALORGREATER(token):
  r'=>'
  return token

def t_2XEQUAL(token):
    r'=='
    return token

def t_EQUAL(token):
    r'='
    return token

def t_EXCLAMATION(token):
    r'!'
    return token


def t_REMOVE(token):
  r'remove'
  return token

def t_FROM(token):
  r'from'
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

def t_ARROW(token):
    r'->'
    return token


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
          'WHITESPACES',
          'JSONSTRING_START',
          'JSONSTRING_END',
          'JSONSTRING',
          'ARROW',
          'LESSOREQUAL',
          'EQUALORGREATER',
          'REMOVE',
          'FROM'
          ] + list(predicate.values())

