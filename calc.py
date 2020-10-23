"""
	Author: Douglas De León, Isabel Ortiz, Pablo Ruiz
	Version: 1.0
	Date: Oct 22, 2020
"""

import ply.lex as lex
import ply.yacc as yacc
import matplotlib.pyplot as plt
import networkx as nx

counterot = 0


def graph(p):
    global counterot
    counterot += 1
    displacer = ' '
    recreator = ''
    for x in range(0, counterot):
        displacer += ' '
        recreator += ' '
    current_graph = nx.DiGraph()
    if type(p) == tuple:
        current_graph.add_node(p[0] + recreator)
        if type(p[1]) == tuple:
            current_graph.add_node(str(p[1][0]) + displacer)
            current_graph.add_edge(p[0] + recreator, p[1][0] + displacer)
            temp1 = graph(p[1])
            current_graph.add_nodes_from(temp1)
            current_graph.add_edges_from(temp1.edges())
        else:

            current_graph.add_node(str(p[1]) + displacer)
            current_graph.add_edge(p[0] + recreator, p[1] + displacer)
            if p[1] == p[2]:
                current_graph.add_node(str(p[2]) + displacer + ' ')
                current_graph.add_edge(p[0] + recreator, p[2] + displacer + ' ')


        if (len(p) > 2):
            if type(p[2]) == tuple:
                current_graph.add_node(str(p[2][0]) + displacer)
                current_graph.add_edge(p[0] + recreator, str(p[2][0]) + displacer)
                mptmp = graph(p[2])
                current_graph.add_nodes_from(mptmp)
                current_graph.add_edges_from(mptmp.edges())
            else:
                current_graph.add_node(str(p[2]) + displacer)
                current_graph.add_edge(p[0] + recreator, p[2] + displacer)

    else:
        current_graph.add_node(str(p) + displacer)
    return current_graph


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
    'EQUALS'
)

t_ignore = ' \t'

t_NEGACION = r'\~'
t_CONJUNCION = r'\^'
t_DISYUNCION = r'o'
t_BICONDICIONAL = r'<=>'
t_CONDICIONAL = r'=>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'\='


def t_VAR(t):
    r'[p-z]'
    t.type = 'VAR'
    return t


def t_CONST(t):
    r'0|1'
    t.value = bool(int(t.value))
    return t


def t_error(t):
    print("Invalid Token:", t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

# PARSER
precedence = (
    ('left', 'BICONDICIONAL', 'CONDICIONAL'),
    ('left', 'NEGACION', 'CONJUNCION', 'DISYUNCION'),
)


def p_create(p):
    """
  create : expression
         | equal_var
         | empty 
  """
    print("TREE", p[1])
    if p[1] is not None:
        nx.draw(graph(p[1]), with_labels=True)
        plt.savefig('output.png')
        plt.show()  # display


def p_equal_var(p):
    """
  equal_var : VAR EQUALS expression
  """
    p[0] = ('=', p[1], p[3])


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


def p_parens(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_error(p):
    lexer.skip()
    print("Syntax error in input!")


parser = yacc.yacc()
env = {}


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
        print(result)

    except Exception:
        print()
