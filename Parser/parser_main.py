import sys
import os

# Add parent directory to path to import Scanner
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Scanner.main import tokenize
from statements import program

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.current_token = None
        self.current_value = None
        self._advance()

    def _advance(self):
        if self.token_index < len(self.tokens):
            self.current_token, self.current_value = self.tokens[self.token_index]
            self.token_index += 1
        else:
            self.current_token = 'EOF'
            self.current_value = None

    def match(self, expected_type):
        if self.current_token == expected_type:
            self._advance()
        else:
            self.error(f"Expected token {expected_type} but found {self.current_token}")

    def error(self, message):
        raise SyntaxError(f"Parser Error: {message} at token '{self.current_value}' ({self.current_token})")

def parse(input_string):
    tokens = tokenize(input_string)
    # Filter out comments if Scanner doesn't do it (Scanner seems to handle it but let's be safe)
    # Scanner returns (type, value) tuples.
    # Wait, Scanner.main.tokenize returns list of (type, value).
    # Let's check Scanner/main.py again.
    # It returns list of (token_type, token_value).
    # My Parser expects (token_type, token_value).
    
    # Re-checking Scanner/main.py:
    # tokens.append((final_states[state], token)) -> (type, value)
    # So tokens is [(type, value), ...]
    
    parser = Parser(tokens)
    tree = program(parser)
    return tree

if __name__ == "__main__":
    print("Enter code to parse (end with Ctrl+D or Ctrl+Z):")
    try:
        # Read all input from stdin
        input_string = sys.stdin.read()
        if not input_string.strip():
            # Fallback for testing if no input provided via stdin
            print("No input provided. Using default test case.")
            input_string = """
            read x;
            if x < 0 then
                x := 0 - x
            end;
            write x
            """
            print(f"Input Code:\n{input_string}")

        syntax_tree = parse(input_string)
        
        # Print to console
        print("\nSyntax Tree:")
        print(syntax_tree)
        
        # Write to file
        output_file = "parser_output.txt"
        with open(output_file, "w") as f:
            f.write(str(syntax_tree))
            
        print(f"\nParsing successful! Syntax tree saved to '{output_file}'")
        
    except Exception as e:
        print(f"\nError: {e}")
