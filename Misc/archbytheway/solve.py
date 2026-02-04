
import sys

def solve():
    with open('arch.archbtw', 'r') as f:
        content = f.read()

    tokens = content.split()
    bf_code = ""
    mapping = {
        'arch': '+',
        'linux': '-',
        'the': '[',
        'way': ']',
        'i': '>',
        'use': '<',
        'btw': '.'
    }

    for token in tokens:
        if token in mapping:
            bf_code += mapping[token]
    
    print("Brainfuck code length:", len(bf_code))
    # print(bf_code)
    
    # Brainfuck interpreter
    tape = [0] * 30000
    ptr = 0
    code_ptr = 0
    loop_stack = []
    
    # Map loop positions
    loop_map = {}
    temp_stack = []
    for i, cmd in enumerate(bf_code):
        if cmd == '[':
            temp_stack.append(i)
        elif cmd == ']':
            if not temp_stack:
                raise ValueError("Unmatched ]")
            start = temp_stack.pop()
            loop_map[start] = i
            loop_map[i] = start
            
    if temp_stack:
        raise ValueError("Unmatched [")

    output = ""
    
    while code_ptr < len(bf_code):
        cmd = bf_code[code_ptr]
        
        if cmd == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif cmd == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif cmd == '>':
            ptr += 1
        elif cmd == '<':
            ptr -= 1
        elif cmd == '.':
            output += chr(tape[ptr])
            # print(chr(tape[ptr]), end='', flush=True)
        elif cmd == ',':
            pass # No input expected
        elif cmd == '[':
            if tape[ptr] == 0:
                code_ptr = loop_map[code_ptr]
        elif cmd == ']':
            if tape[ptr] != 0:
                code_ptr = loop_map[code_ptr]
        
        code_ptr += 1

    print("\nDecoded Output:")
    print(output)

if __name__ == "__main__":
    solve()
