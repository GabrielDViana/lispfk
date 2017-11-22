import ox
from sys import argv
import pprint

#Gets input files in command line, first = self code, second = lisp code
lispfk, fibonacci = argv
fibonacci = open(fibonacci).read()

#make_lexer to fibonacci code in lisp
lexer = ox.make_lexer([
    ('OPARENTHESYS', r'[(]'),
    ('CPARENTHESYS', r'[)]'),
    ('DEFUN','defun'),
    ('COND','cond'),
    ('PRINT','print'),
    ('NUMBER', r'\d+'),
    ('VAR', r'[-a-zA-Z]+'),
    ('COMMENT', r';.*'),
    ('OPERANDS', r'[&=+-]'),
    ('WHITESPACE', r'\s+'),
    ('NEWLINE', r'\n+'),
])

#all tokens used in fibonacci algorithm
tokens = [
    'OPARENTHESYS',
    'CPARENTHESYS',
    'DEFUN',
    'COND',
    'PRINT',
    'NUMBER',
    'VAR',
    'OPERANDS'
]

parser = ox.make_parser([
    ('block : OPARENTHESYS CPARENTHESYS', lambda x,y: '()'),
    ('block : OPARENTHESYS expr CPARENTHESYS', lambda x,y,z: y),
    ('expr : term expr', lambda x,y: (x,) + y),
    ('expr : term', lambda x: (x,)),
    ('term : block', lambda x: x),
    ('term : DEFUN', lambda x: x),
    ('term : COND', lambda x: x),
    ('term : PRINT', lambda x: x),
    ('term : NUMBER', lambda x: x),
    ('term : VAR', lambda x: x),
    ('term : OPERANDS', lambda x: x),
], tokens)

tokens = [
    token for token in (lexer(fibonacci))
    if token.type not in ('WHITESPACE', 'COMMENT', 'NEWLINE')
]

print(lexer(fibonacci))
pprint.pprint(parser(tokens))
