from syntax_tree import OpNode, ConstNode, IdNode

def exp(parser):
    left = simple_exp(parser)
    if parser.current_token in ('LESSTHAN', 'EQUAL'):
        op = parser.current_token
        parser.match(op)
        right = simple_exp(parser)
        return OpNode(op, left, right)
    return left

def simple_exp(parser):
    left = term(parser)
    while parser.current_token in ('PLUS', 'MINUS'):
        op = parser.current_token
        parser.match(op)
        right = term(parser)
        left = OpNode(op, left, right)
    return left

def term(parser):
    left = factor(parser)
    while parser.current_token in ('MULT', 'DIV'):
        op = parser.current_token
        parser.match(op)
        right = factor(parser)
        left = OpNode(op, left, right)
    return left

def factor(parser):
    if parser.current_token == 'OPENBRACKET':
        parser.match('OPENBRACKET')
        node = exp(parser)
        parser.match('CLOSEDBRACKET')
        return node
    elif parser.current_token == 'NUMBER':
        val = parser.current_value # Assuming parser has current_value for numbers
        parser.match('NUMBER')
        return ConstNode(val)
    elif parser.current_token == 'IDENTIFIER':
        name = parser.current_value # Assuming parser has current_value for identifiers
        parser.match('IDENTIFIER')
        return IdNode(name)
    else:
        parser.error(f"Unexpected token in factor: {parser.current_token}")