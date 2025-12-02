import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Parser.parser_main import parse
import traceback

def test_parser(input_string):
    print("=" * 60)
    print("INPUT CODE:")
    print("=" * 60)
    print(input_string)
    print("=" * 60)
    
    try:
        tree = parse(input_string)
        print("\nSYNTAX TREE:")
        print("-" * 60)
        print(tree)
        print("=" * 60)
        print("✓ Parsing successful")
    except Exception as e:
        print("\nPARSING FAILED:")
        print("-" * 60)
        traceback.print_exc()
        print("=" * 60)

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
