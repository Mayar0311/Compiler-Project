with open("input.txt", "r") as file:
    content = file.read()
    print(content)
print("File read successfully.")

# Define DFA states and transitions
transitions = {
    "start": {"letter": "Inid", "digit": "Inum", "{": "InComment"},
    "Inid": {"letter": "Inid"},  
    "Inum": {"digit": "Inum"},  
    "InComment": {"other": "InComment", "}": "start"}
}

# Define token types
final_states = {
    "Inid": "IDENTIFIER",
    "Inum": "NUMBER"
}

#character type
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

    for ch in input_string:
        if comment_mode:
            if ch == "}":
                comment_mode = False  
            continue  

        if ch == "{":
            comment_mode = True
            continue 

        ctype = char_type(ch)

        # Ignore whitespace
        if ctype == "whitespace" or ctype == "other":
            if state in final_states:
                tokens.append((final_states[state], token))
            state = "start"
            token = ""
            continue

        # State transitions
        if state in transitions and ctype in transitions[state]:
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
                output_line = f"{token_type} : {token_value}\n"
                outfile.write(output_line)
        
        print(f"Tokenization complete. Results written to '{output_filename}'.")

    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' was not found. Please create it.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example Usage:
process_files(input_filename="input.txt", output_filename="output.txt")

