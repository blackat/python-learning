# Writing tips

## Workflow to encode code into online-python.com

### Create `scripts/encode.py`

```python
#!/usr/bin/env python3
# Usage:
#   python3 scripts/encode.py                    # reads from clipboard
#   python3 scripts/encode.py path/to/file.py    # reads from file
#   cat file.py | python3 scripts/encode.py      # reads from stdin

import urllib.parse
import sys

def encode(code: str) -> str:
    encoded = urllib.parse.quote(code)
    return f"https://www.online-python.com/?code={encoded}"

if len(sys.argv) > 1:
    # Read from file
    with open(sys.argv[1]) as f:
        code = f.read()
elif not sys.stdin.isatty():
    # Read from stdin / pipe
    code = sys.stdin.read()
else:
    # Read from clipboard
    import subprocess
    code = subprocess.run("pbpaste", capture_output=True, text=True).stdout

url = encode(code)

# Print and copy to clipboard
print(url)
subprocess.run("pbcopy", input=url, text=True)
print("✅ URL copied to clipboard")
```

#### How to run from clipboard

```bash
# Directly run
python3 scripts/encode.py

# Alias
alias encode="python3 /Users/blackat/Development/Github/python-learning/scripts/encode.py"
```

But there are 3 ways to run it

```bash
# From a file
python3 scripts/encode.py src/exercises/ch01_oop/exercises/exercise_01.py

# From clipboard — copy code in VS Code, then:
python3 scripts/encode.py

# From stdin
cat mycode.py | python3 scripts/encode.py
```

In all cases the URL is printed **and** copied to your clipboard automatically — just paste into your markdown.

#### Run t

#### Example of workflow

```bash
The snippet I showed earlier isn't that useful — you still need to manually paste the encoded URL into it. Skip it.

The workflow is just:

1. Write your code block in the `.md` file
2. Select the code, copy it (`Cmd+C`)
3. Run `uv run encode` in the terminal — it reads from clipboard and copies the URL
4. Paste the URL into your markdown link

```md
```python
class A:
    def hello(self):
        return "Hello from A"
```

[▶ Run this example](PASTE_URL_HERE)
```

That's it — 3 keystrokes after writing the code.
```