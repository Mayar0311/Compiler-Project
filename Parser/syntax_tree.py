class Node:
    def __init__(self, type_name, children=None, value=None):
        self.type_name = type_name
        self.children = children if children is not None else []
        self.value = value

    def __str__(self, level=0):
        ret = "  " * level + f"{self.type_name}"
        if self.value is not None:
            ret += f": {self.value}"
        ret += "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return self.__str__()

class ProgramNode(Node):
    def __init__(self, statements):
        super().__init__("Program", children=statements)

class StmtSequenceNode(Node):
    def __init__(self, statements):
        super().__init__("StmtSequence", children=statements)

class IfNode(Node):
    def __init__(self, condition, then_part, else_part=None):
        children = [condition, then_part]
        if else_part:
            children.append(else_part)
        super().__init__("If", children=children)

class RepeatNode(Node):
    def __init__(self, body, condition):
        super().__init__("Repeat", children=[body, condition])

class AssignNode(Node):
    def __init__(self, identifier, expression):
        super().__init__("Assign", children=[expression], value=identifier)

class ReadNode(Node):
    def __init__(self, identifier):
        super().__init__("Read", value=identifier)

class WriteNode(Node):
    def __init__(self, expression):
        super().__init__("Write", children=[expression])

class OpNode(Node):
    def __init__(self, op, left, right):
        super().__init__("Op", children=[left, right], value=op)

class ConstNode(Node):
    def __init__(self, value):
        super().__init__("Const", value=value)

class IdNode(Node):
    def __init__(self, name):
        super().__init__("Id", value=name)
