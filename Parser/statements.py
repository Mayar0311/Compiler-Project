from expressions import exp
from syntax_tree import ProgramNode, StmtSequenceNode, IfNode, RepeatNode, AssignNode, ReadNode, WriteNode

def program(parser):
    seq_node = stmt_sequence(parser)
    return ProgramNode([seq_node])

def stmt_sequence(parser):
    statements = []
    statements.append(statement(parser))
    while parser.current_token == 'SEMICOLON':
        parser.match('SEMICOLON')
        # Check for block terminators to allow trailing semicolons
        if parser.current_token in ('ELSE', 'END', 'UNTIL', 'EOF'):
            break
        statements.append(statement(parser))
    return StmtSequenceNode(statements)

def statement(parser):
    if parser.current_token == 'IF':
        return if_stmt(parser)
    elif parser.current_token == 'REPEAT':
        return repeat_stmt(parser)
    elif parser.current_token == 'IDENTIFIER':
        return assign_stmt(parser)
    elif parser.current_token == 'READ':
        return read_stmt(parser)
    elif parser.current_token == 'WRITE':
        return write_stmt(parser)
    else:
        parser.error("Unexpected token in statement")

def if_stmt(parser):
    parser.match('IF')
    condition = exp(parser)
    parser.match('THEN')
    then_stmts = stmt_sequence(parser)
    else_stmts = None
    if parser.current_token == 'ELSE':
        parser.match('ELSE')
        else_stmts = stmt_sequence(parser)
    parser.match('END')
    return IfNode(condition, then_stmts, else_stmts)

def repeat_stmt(parser):
    parser.match('REPEAT')
    body = stmt_sequence(parser)
    parser.match('UNTIL')
    condition = exp(parser)
    return RepeatNode(body, condition)

def assign_stmt(parser):
    identifier = parser.current_value
    parser.match('IDENTIFIER')
    parser.match('ASSIGN')
    expression = exp(parser)
    return AssignNode(identifier, expression)

def read_stmt(parser):
    parser.match('READ')
    identifier = parser.current_value
    parser.match('IDENTIFIER')
    return ReadNode(identifier)

def write_stmt(parser):
    parser.match('WRITE')
    expression = exp(parser)
    return WriteNode(expression)
