from expressions import exp

# Read from scanner output file
with open('Scanner/output.txt', 'r') as f:
    tokens = [line.strip() for line in f if line.strip()]
    token_index = 0
    
def get_token():
    global current_token, token_index
    if token_index < len(tokens):
        current_token = tokens[token_index][0]
        token_index += 1
    else:
        current_token = 'EOF'
    return current_token

current_token = get_token()

def match(token):
    global current_token
    if current_token == token:
        current_token = get_token()
    else:
        error(f"Expected token {token} but found {current_token}")

def error(message):
    print(f"Parser Error: {message}")
    print(f"Current token: {current_token}")


def program():
    stmt_sequence()
    print("\n✓ Parsing completed successfully!")

def stmt_sequence():
    statement()
    while current_token == 'SEMICOLON':
        match('SEMICOLON')
        statement()
    print("stmt_sequence() completed")

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
    print("statement() completed")

def if_stmt():
    match('IF')
    exp()
    match('THEN')
    stmt_sequence()
    if current_token == 'ELSE':
        match('ELSE')
        stmt_sequence()
    match('END')
    print("if_stmt() completed")

def repeat_stmt():
    match('REPEAT')
    stmt_sequence()
    match('UNTIL')
    exp()
    print("repeat_stmt() completed")

def assign_stmt():
    match('IDENTIFIER')
    match('ASSIGN')
    exp()
    print("assign_stmt() completed")

def read_stmt():
    match('READ')
    match('IDENTIFIER')
    print("read_stmt() completed")

def write_stmt():
    match('WRITE')
    exp()
    print("write_stmt() completed")

def exp():
    print("exp() called - placeholder implementation")
    # Placeholder for expression parsing logic


if __name__ == "__main__":
    print("Starting parser test...\n")
    try:
        program()
    except Exception as e:
        print(f"\nParser failed with error: {e}")
