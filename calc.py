import sys
import ply.lex as lex
import ply.yacc as yacc

# LEXER
tokens = (
    'NEGACION',
    'CONJUNCION',
    'DISYUNCION',
    'BICONDICIONAL',
    'CONDICIONAL',
    'LPAREN',
    'RPAREN',
    'VAR',
    'CONST',
)

t_ignore = ' \t'

t_NEGACION= r'\~'
t_CONJUNCION = r'\^'
t_DISYUNCION = r'o'
t_BICONDICIONAL = r'<=>'
t_CONDICIONAL = r'=>'
t_LPAREN = r'\('
t_RPAREN = r'\)'


def t_VAR( t ) :
    r'[p-z]'
    t.type = 'VAR'
    return t


def t_CONST( t ) :
    r'0|1'
    t.value = bool(int(t.value))
    return t


def t_error( t ):
  print("Invalid Token:", t.value[0])
  t.lexer.skip(1)

lexer = lex.lex()

# PARSER
precedence = (
    ( 'left', 'BICONDICIONAL', 'CONDICIONAL' ),
    ( 'left', 'NEGACION', 'CONJUNCION', 'DISYUNCION' ),
)




def p_expression(p):
    """
    expression : expression CONJUNCION expression
               | expression DISYUNCION expression
               | expression BICONDICIONAL expression
               | expression CONDICIONAL expression
    """
    p[0] = (p[2], p[1], p[3])


def p_negation(p):
    """
    expression : NEGACION expression
    """
    p[0] = (p[1], p[2])


def p_expression_var_const(p):
    """
    expression : VAR
               | CONST
    """
    p[0] = p[1]


def p_empty(p):
    """
    empty :
    """
    p[0] = None


def p_parens( p ) :
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_error( p ):
    print("Syntax error in input!")

parser = yacc.yacc()



while True:
    try:
        s = input(">>")
    except EOFError:
        break

    lexer.input(s)
    print("\nPRODUCCION GRAMATICAL: ")
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
        
    print("\nARBOL DE PARSER: ")
    try:
        result = tuple(parser.parse(s))
        result = tuple(result)
        print(result)
    except Exception:
        print()



