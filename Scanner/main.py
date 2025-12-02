# Define DFA states and transiions
# Id, numbers, comments
# Symbols
# Reserved words
transitions = {
    "start": {"letter": "Inid", "digit": "Inum", "{": "InComment",
              "+": "plus", "-": "minus", ";": "semicolon", ":": ":", "<": "lessthan", "=": "equal", "*": "mult", "/": "div", "(": "openbracket", ")": "closedbracket",
              "i": "i", "t": "t", "e": "e", "r": "r", "u": "u", "w": "w",
              },
    "Inid": {"letter": "Inid"},
    "Inum": {"digit": "Inum"},
    "InComment": {"other": "InComment", "}": "start"},

    ":": {"=": "assign"},
    # First letter states
    "i": {"f": "if", "letter": "Inid"},  # Final "if" state
    "t": {"h": "th", "letter": "Inid"},
    "e": {"n": "en", "l": "el", "letter": "Inid"},
    "r": {"e": "re", "letter": "Inid"},
    "u": {"n": "un", "letter": "Inid"},
    "w": {"r": "wr", "letter": "Inid"},
    # Second letter states
    "th": {"e": "the", "letter": "Inid"},
    "en": {"d": "end", "letter": "Inid"},   # Final "end" state
    "el": {"s": "els", "letter": "Inid"},
    "re": {"p": "rep", "a": "rea", "letter": "Inid"},
    "un": {"t": "unt", "letter": "Inid"},
    "wr": {"i": "wri", "letter": "Inid"},
    # Third letter states
    "the": {"n": "then", "letter": "Inid"},    # Final "then" state
    "els": {"e": "else", "letter": "Inid"},    # Final "else" state
    "rep": {"e": "repe", "letter": "Inid"},
    "rea": {"d": "read", "letter": "Inid"},    # Final "read" state
    "unt": {"i": "unti", "letter": "Inid"},
    "wri": {"t": "writ", "letter": "Inid"},
    # Fourth letter states
    "repe": {"a": "repea", "letter": "Inid"},
    "unti": {"l": "until", "letter": "Inid"}, # Final "until" state
    "writ": {"e": "write", "letter": "Inid"}, # Final "write" state
    # Fifth letter states
    "repea": {"t": "repeat", "letter": "Inid"},  # Final "repeat" state
}

# Define token types
final_states = {
    "Inid": "IDENTIFIER",
    "Inum": "NUMBER",
    "plus": "PLUS",
    "minus": "MINUS",
    "semicolon": "SEMICOLON",
    "assign": "ASSIGN",
    "lessthan": "LESSTHAN",
    "equal": "EQUAL",
    "mult": "MULT",
    "div": "DIV",
    "openbracket": "OPENBRACKET",
    "closedbracket": "CLOSEDBRACKET",
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "end": "END",
    "repeat": "REPEAT",
    "until": "UNTIL",
    "read": "READ",
    "write": "WRITE",
}

# character type
def char_type(ch):
    if ch.isalpha():
        return "letter"
    elif ch.isdigit():
        return "digit"
    elif ch.isspace():
        return "whitespace"
    else:
        return ch if ch in ('{', '}') else "other"


# Tokenizer function
def tokenize(input_string):
    state = "start"
    token = ""
    tokens = []
    comment_mode = False
    reserved_mode = False

    if state == "Inid" or state == "Inum" or state == "InComment" :
        reserved_mode = False

    for ch in input_string:
        # Comment
        if comment_mode:
            if ch == "}":
                comment_mode = False
            continue

        if ch == "{":
            comment_mode = True
            continue

        ctype = char_type(ch)

        if token == "" and (ch == "i" or ch == "t" or ch == "e" or ch == "r" or ch == "u" or ch == "w"):
            reserved_mode = True

        if (reserved_mode and ch.isalpha()) or (ctype == "other" and ch in transitions["start"]):
            ctype = ch

        # Ignore whitespace
        if ctype == "whitespace" or ctype == "other":
            if state in final_states:
                tokens.append((final_states[state], token))
            state = "start"
            token = ""
            continue

        # Handles identifiers and numbers state transitions
        if state in transitions and ctype in transitions[state]:
            state = transitions[state][ctype]
            token += ch
        elif char_type(ch) == "letter":
            ctype = char_type(ch)
            reserved_mode = False
            state = transitions[state][ctype]
            token += ch
        else:
            if state in final_states:
                tokens.append((final_states[state], token))
            token = ch if state != "start" else ""
            state = transitions["start"][ctype]

    if state in final_states:
        tokens.append((final_states[state], token))

    return tokens


# Example usage
# input_string = "var1 123 { ignore this} var2 456"
# tokens = tokenize(input_string)
# for token in tokens:
#     print(token[0], ":", token[1])
#     print()

def process_files():
    try:
        # Ask user for input file name
        input_filename = input("Enter the input file name (e.g., input.txt): ").strip()
        
        # Try multiple locations for the input file
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_filename = os.path.join(script_dir, "output.txt")
        possible_paths = [
            input_filename,  # Current directory
            os.path.join(script_dir, input_filename),  # Script directory
            os.path.join(script_dir, 'dist', input_filename),  # dist subdirectory
        ]
        
        file_found = False
        for path in possible_paths:
            if os.path.exists(path):
                input_filename = path
                file_found = True
                break
        
        if not file_found:
            raise FileNotFoundError(f"Could not find '{input_filename}' in any of the expected locations")

        with open(input_filename, "r") as infile:
            input_string = infile.read()

        print("\n--- File Content ---")
        print(input_string)
        print("--------------------")

        tokens = tokenize(input_string)

        print("\n--- Tokenization Result ---")
        with open(output_filename, "w") as outfile:
            for token_type, token_value in tokens:
                line = f"{token_value}, {token_type}"
                print(line)
                outfile.write(line + "\n")

        print("\nTokenization complete.")
        print(f"Results written to '{output_filename}'.")
        
        return tokens

    except FileNotFoundError:
        print("Error: Input file not found.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


if __name__ == "__main__":
    print(process_files())
    input("\nPress Enter to exit...")