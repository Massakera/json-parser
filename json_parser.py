import argparse
import sys
import re

# Token types
TOKEN_TYPES = {
    'LBRACE': r'\{',
    'RBRACE': r'\}',
    'STRING': r'"([^"\\]*(\\.[^"\\]*)*)"',
    'NUMBER': r'-?\d+(\.\d+)?([eE][+-]?\d+)?',
    'BOOLEAN': r'true|false',
    'NULL': r'null',
    'COLON': r':',
    'COMMA': r',',
    'EOF': r'$',
    'LBRACKET': r'\[',
    'RBRACKET': r'\]',
    'TRUE': r'true',  # Recognize lowercase 'true'
    'FALSE': r'false',  # Recognize lowercase 'false'
}


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

def lexer(input):
    tokens = []
    # Pattern to match any whitespace
    whitespace_pattern = re.compile(r'\s+')

    while input:
        # Skip whitespace before matching other tokens
        whitespace_match = whitespace_pattern.match(input)
        if whitespace_match:
            # Move input past the matched whitespace and continue
            input = input[whitespace_match.end():]

        match = None
        for type, pattern in TOKEN_TYPES.items():
            regex = re.compile(pattern)
            match = regex.match(input)
            if match:
                value = match.group(0)
                if type == 'STRING':
                    # Remove quotes for the value
                    value = value[1:-1]
                tokens.append(Token(type, value))
                input = input[match.end():]
                break
        if not match:
            if input:  # Only raise an error if there's non-whitespace input left
                raise ValueError(f"Unexpected character: {input[0]}")
            break  # Exit the loop if only whitespace is left

    tokens.append(Token('EOF', None))
    return tokens

def parse(tokens):
    def parse_value(tokens):
        # Ensure we're working with the list of tokens
        # First, check the type of the next token without removing it from the list
        next_token_type = tokens[0].type

        if next_token_type == 'LBRACE':
            return parse_object(tokens)  # Pass the remaining tokens for recursive parsing
        elif next_token_type == 'LBRACKET':
            return parse_array(tokens)  # Pass the remaining tokens for recursive parsing
        else:
            # For non-structure types, now pop the token and process it
            token = tokens.pop(0)
            if token.type == 'STRING':
                return token.value
            elif token.type == 'NUMBER':
                try:
                    return int(token.value)
                except ValueError:
                    return float(token.value)
            elif token.type == 'BOOLEAN':
                return token.value == 'true'
            elif token.type == 'NULL':
                return None
            else:
                raise ValueError(f"Unsupported value type: {token.type}")


        
    def parse_array(tokens):
        array = []
        tokens.pop(0)  # Consume the opening '['
        while tokens[0].type != 'RBRACKET':
            element = parse_value(tokens)  # Correctly pass the entire tokens list
            array.append(element)
            if tokens[0].type == 'COMMA':
                tokens.pop(0)  # Consume the comma, if present
        tokens.pop(0)  # Consume the closing ']'
        return array



    def parse_object(tokens):
        obj = {}
        tokens.pop(0)  # Consume the opening '{'
        while tokens[0].type != 'RBRACE':
            key_token = tokens.pop(0)
            if key_token.type != 'STRING':
                raise ValueError("Expected a string key")
            if tokens.pop(0).type != 'COLON':
                raise ValueError("Expected ':' after key")

            value_token = tokens[0]  # No need to pop here; parse_value will handle it.
            value = parse_value(tokens)  # This will consume the value token(s).
            
            obj[key_token.value] = value
            
            if tokens[0].type == 'COMMA':
                tokens.pop(0)  # Consume the comma, continue parsing the next key-value pair
            elif tokens[0].type != 'RBRACE':
                raise ValueError("Expected ',' or '}' after a key-value pair")
        tokens.pop(0)  # Consume the closing '}'
        return obj

    if not tokens:
        raise ValueError("Empty token list")
    
    ast = parse_object(tokens)
    if tokens[0].type != 'EOF':
        raise ValueError("Expected end of file after JSON object")
    return ast

def main(file_path):
    try:
        with open(file_path, 'r') as file:
            json_input = file.read()
        tokens = lexer(json_input)
        parsed = parse(tokens)
        print(parsed)
        sys.exit(0)
    except ValueError as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple JSON Parser')
    parser.add_argument('file', help='Path to the JSON file to parse')
    args = parser.parse_args()
    main(args.file)
