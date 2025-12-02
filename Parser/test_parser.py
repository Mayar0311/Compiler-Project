import sys
import os

# Add Scanner directory to path to import tokenizer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Scanner'))
from main import tokenize

# Global variables
tokens = []
current_index = 0
current_token = None
current_value = None

def get_next_token():
    global current_index, current_token, current_value
    if current_index < len(tokens):
        current_token, current_value = tokens[current_index]
        current_index += 1
        return current_token
    else:
        current_token = None
        current_value = None
        return None

def error(message):
    print(f"Parse Error: {message}")
    print(f"Current token: {current_token} ('{current_value}')")
    print(f"Position: {current_index}/{len(tokens)}")
    sys.exit(1)

def match(expected_token):
    global current_token
    if current_token == expected_token:
        print(f"Matched: {current_token} ('{current_value}')")
        get_next_token()
    else:
        error(f"Expected {expected_token} but found {current_token}")

# Import expression functions (placeholder for now)
def exp():
    print(f"Parsing expression starting with: {current_token}")
    # Simple expression parsing - just consume tokens for now
    simple_exp()
    if current_token == 'LESSTHAN':
        match('LESSTHAN')
        simple_exp()

def simple_exp():
    term()
    while current_token in ['PLUS', 'MINUS']:
        if current_token == 'PLUS':
            match('PLUS')
        else:
            match('MINUS')
        term()

def term():
    factor()
    while current_token in ['MULT', 'DIV']:
        if current_token == 'MULT':
            match('MULT')
        else:
            match('DIV')
        factor()

def factor():
    if current_token == 'OPENBRACKET':
        match('OPENBRACKET')
        exp()
        match('CLOSEDBRACKET')
    elif current_token == 'NUMBER':
        match('NUMBER')
    elif current_token == 'IDENTIFIER':
        match('IDENTIFIER')
    else:
        error(f"Unexpected token in factor: {current_token}")

# Import statement functions
def program():
    stmt_sequence()
    print("\n✓ Parsing completed successfully!")

def stmt_sequence():
    statement()
    while current_token == 'SEMICOLON':
        match('SEMICOLON')
        statement()

def statement():
    if current_token == 'IF':
        if_stmt()
    elif current_token == 'REPEAT':
        repeat_stmt()
    elif current_token == 'IDENTIFIER':
        assign_stmt()
    elif current_token == 'READ':
        read_stmt()
    elif current_token == 'WRITE':
        write_stmt()
    else:
        error("Unexpected token in statement")

def if_stmt():
    match('IF')
    exp()
    match('THEN')
    stmt_sequence()
    if current_token == 'ELSE':
        match('ELSE')
        stmt_sequence()
    match('END')

def repeat_stmt():
    match('REPEAT')
    stmt_sequence()
    match('UNTIL')
    exp()

def assign_stmt():
    match('IDENTIFIER')
    match('ASSIGN')
    exp()

def read_stmt():
    match('READ')
    match('IDENTIFIER')

def write_stmt():
    match('WRITE')
    exp()

# Test function
def test_parser(input_string):
    global tokens, current_index, current_token, current_value
    
    print("=" * 60)
    print("INPUT CODE:")
    print("=" * 60)
    print(input_string)
    print("=" * 60)
    
    # Tokenize the input
    tokens = tokenize(input_string)
    current_index = 0
    
    print("\nTOKENS:")
    print("-" * 60)
    for token_type, token_value in tokens:
        print(f"{token_value:15} -> {token_type}")
    print("=" * 60)
    
    # Initialize parser
    get_next_token()
    
    print("\nPARSING:")
    print("-" * 60)
    
    # Parse the program
    try:
        program()
    except SystemExit:
        pass

# Test cases
if __name__ == "__main__":
    # Test 1: Simple assignment
    print("\n\nTEST 1: Simple Assignment")
    test_parser("x := 5")
    
    # Test 2: Read and Write
    print("\n\nTEST 2: Read and Write")
    test_parser("read y; write y")
    
    # Test 3: If statement
    print("\n\nTEST 3: If Statement")
    test_parser("if x < 10 then write x end")
    
    # Test 4: If-Else statement
    print("\n\nTEST 4: If-Else Statement")
    test_parser("if x < 10 then write x else write 0 end")
    
    # Test 5: Repeat statement
    print("\n\nTEST 5: Repeat Statement")
    test_parser("repeat x := x + 1 until x < 10")
    
    # Test 6: Complex program
    print("\n\nTEST 6: Complex Program")
    test_parser("""
    read x;
    if x < 0 then
        x := 0
    else
        x := x * 2
    end;
    write x
    """)
    
    # Test 7: Nested statements
    print("\n\nTEST 7: Nested Statements")
    test_parser("""
    repeat
        read x;
        if x < 10 then
            write x
        end
    until x < 0
    """)
