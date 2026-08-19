# Level 1 — Git + Development Environment

## Git

**Core commands, in the order you'd actually use them:**

```bash
git init                          # start a new repo in the current folder
git clone <url>                   # copy an existing remote repo to your machine
git add <file>                    # stage a file (or `git add .` for everything)
git commit -m "message"           # save the staged changes as a snapshot
git push                          # send your commits to the remote (e.g. GitHub)
git pull                          # fetch + merge remote changes into your local branch
```

**Branches:**
```bash
git branch                        # list branches
git branch new-feature            # create a branch
git checkout new-feature          # switch to it
git checkout -b new-feature       # create + switch in one step
```

**Merging:**
```bash
git checkout main
git merge new-feature             # bring new-feature's changes into main
```
Conflicts show up as `<<<<<<<` / `=======` / `>>>>>>>` markers in the file — you edit the file by hand to resolve them, then `git add` the file and `git commit`.

**`.gitignore`** — a file listing what Git should *never* track. Typical Python/dev project:
```
.env
__pycache__/
*.pyc
venv/
.venv/
node_modules/
.DS_Store
```
This is the single most important line of defense for keeping secrets out of your repo — if `.env` is in `.gitignore`, `git add .` physically cannot stage it.

---

## Development Environment

**VS Code** — your editor. Key things to know: integrated terminal (`` Ctrl+` `` / `` Cmd+` ``), the Python extension (lets you pick which virtual environment/interpreter it uses, bottom-right corner), and built-in debugger (see below).

**Terminal** — where you run everything above plus Python/pip commands. On Windows, use PowerShell or WSL; on Mac/Linux, the default terminal is fine.

**Python virtual environment** — an isolated set of installed packages per-project, so Project A's dependencies don't clash with Project B's.
```bash
python -m venv venv               # create it (folder named "venv")
source venv/bin/activate          # activate it — Mac/Linux
venv\Scripts\activate             # activate it — Windows
deactivate                        # turn it off
```
You'll know it's active because your terminal prompt shows `(venv)` at the start.

**Installing packages:**
```bash
pip install openai groq langsmith   # install into the active venv
pip freeze > requirements.txt       # snapshot exact versions for others to reuse
pip install -r requirements.txt     # reinstall everything from that snapshot
```

**Basic debugging in VS Code:**
- Click left of a line number to set a breakpoint (red dot)
- Press F5 (or the Run/Debug panel) to start debugging
- Execution pauses at the breakpoint — inspect variables in the sidebar, step through line-by-line (Step Over/Into/Out), or use the Debug Console to evaluate expressions live

---

## API Keys, `.env`, and Environment Variables

**The core security concept: never put API keys directly in source code.**

If a key is hardcoded in a `.py` file and that file gets pushed to GitHub — even a private repo that later goes public, or gets forked, or is scanned by a bot — the key is now exposed. Automated scanners crawl public GitHub 24/7 specifically hunting for leaked keys like `sk-...` (OpenAI) or similar patterns, and a leaked key means someone else can rack up usage charges on **your** account.

**The fix: keep secrets in a `.env` file, and keep `.env` out of Git.**

1. Create a file named `.env` in your project root:
```
OPENAI_API_KEY=sk-your-actual-key-here
GROQ_API_KEY=gsk_your-actual-key-here
LANGSMITH_API_KEY=ls__your-actual-key-here
```

2. Add `.env` to `.gitignore` (shown above) — this is what actually prevents the leak.

3. In your Python code, load the values at runtime instead of typing them in:
```python
from dotenv import load_dotenv
import os

load_dotenv()  # reads .env and loads it into the process's environment

openai_key = os.getenv("OPENAI_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")
langsmith_key = os.getenv("LANGSMITH_API_KEY")
```
(Requires `pip install python-dotenv`.)

**How this actually works under the hood:** `.env` isn't magic — it's just a text file. `load_dotenv()` reads each `KEY=value` line and injects it into the *environment variables* of the currently running process, exactly as if you'd typed `export OPENAI_API_KEY=...` in your terminal before running the script. `os.getenv("OPENAI_API_KEY")` then just reads that variable back out. Libraries like the `openai` Python package are often written to auto-check `os.environ` for a key of that exact name, so sometimes you don't even need `os.getenv` explicitly — just having `load_dotenv()` run is enough.

**Also share a `.env.example`** (this one *is* safe to commit) so collaborators know which variables they need to fill in themselves:
```
OPENAI_API_KEY=
GROQ_API_KEY=
LANGSMITH_API_KEY=
```

**Summary of the whole flow:**
```
.env (real keys, gitignored)
    ↓ load_dotenv()
process environment variables
    ↓ os.getenv("KEY_NAME")
your Python code
```
The key never appears as a literal string anywhere in a file that Git tracks — which is the whole point.