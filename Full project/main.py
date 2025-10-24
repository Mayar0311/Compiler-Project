with open("input.txt", "r") as file:
    content = file.read()
    print(content)
print("File read successfully.")

# Define DFA states and transitions
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
    "i": {"f": "if"},  # Final "if" state
    "t": {"h": "th"},
    "e": {"n": "en"},
    "r": {"e": "re"},
    "u": {"n": "un"},
    "w": {"r": "wr"},
    # Second letter states
    "th": {"e": "the"},
    "en": {"d": "end"},   # Final "end" state
    "re": {"p": "rep", "a": "rea"},
    "un": {"t": "unt"},
    "wr": {"i": "wri"},
    # Third letter states
    "the": {"n": "then"},    # Final "then" state
    "rep": {"e": "repe"},
    "rea": {"d": "read"},    # Final "read" state
    "unt": {"i": "unti"},
    "wri": {"t": "writ"},
    # Fourth letter states
    "repe": {"a": "repea"},
    "unti": {"l": "until"}, # Final "until" state
    "writ": {"e": "write"}, # Final "write" state
    # Fifth letter states
    "repea": {"t": "repeat"},  # Final "repeat" state
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

        if reserved_mode and ch.isalpha():
            ctype = ch
        elif ctype == "other" and ch in transitions["start"]:
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

# File Handling and Tokenization Execution
def process_files(input_filename="input.txt", output_filename="output.txt"):
    try:
        with open(input_filename, 'r') as infile:
            input_string = infile.read()

        tokens = tokenize(input_string)

        with open(output_filename, 'w') as outfile:
            for token_type, token_value in tokens:
                output_line = f"{token_value}, {token_type}\n"
                outfile.write(output_line)

        print(f"Tokenization complete. Results written to '{output_filename}'.")

    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' was not found. Please create it.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Example Usage:
process_files(input_filename="input.txt", output_filename="output.txt")