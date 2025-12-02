def exp():
    simple_exp()
    if token in ('<', '='):
        comparison_op()
        simple_exp()
    else:
        pass  # epsilon

def comparison_op():
    if token == '<':
        match('<')
    elif token == '=':
        match('=')
    else:
        error()

def simple_exp():
    term()
    while token in ('+', '-'):
        addop()
        term()

def addop():
    if token == '+':
        match('+')
    elif token == '-':
        match('-')
    else:
        error()

def term():
    factor()
    while token in ('*', '/'):
        mulop()
        factor()

def mulop():
    if token == '*':
        match('*')
    elif token == '/':
        match('/')
    else:
        error()

def factor():
    if token == '(':
        match('(')
        exp()
        match(')')
    elif token == 'number':
        match('number')
    else:
        error()