# mcp-app-calculator

A small [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that exposes calculator-style tools over HTTP. It is built with [FastMCP](https://gofastmcp.com/) and uses the **streamable HTTP** transport.

This repo is a compact reference you can clone, run locally, extend, and publish—useful if you are learning how MCP servers and HTTP clients fit together.

## Requirements

- Python 3.10 or newer
- [uv](https://docs.astral.sh/uv/) (recommended) or a virtual environment plus `pip` (see below)
- [Git](https://git-scm.com/) if you want to version the project or push to GitHub

## Project setup (from scratch)

These steps assume you are starting on a new machine with nothing checked out yet.

### 1. Install Python and uv

- Install Python 3.10+ from [python.org](https://www.python.org/downloads/) or your OS package manager, and confirm `python --version`.
- Install uv: follow the [official install guide](https://docs.astral.sh/uv/getting-started/installation/) for Windows, macOS, or Linux.

### 2. Get the code

**If this is your own repo (you will push it):**

```powershell
cd C:\path\where\you\keep\repos
git clone https://github.com/georgejinu-labs/mcp-app-calculator.git
cd mcp-app-calculator
```

**If you are learning from someone else’s copy:** use their URL, or fork the repository on GitHub first and clone **your fork** so you can push changes without needing write access to the original.

### 3. Install dependencies with uv

From the repository root (where `pyproject.toml` and `uv.lock` live):

```powershell
uv sync
```

That creates a project virtual environment (often `.venv` next to `pyproject.toml`) and installs the packages pinned in `uv.lock`.

### 4. Smoke test

In one terminal, start the server:

```powershell
uv run python src/server.py
```

In another terminal, run a client:

```powershell
uv run python src/client/client_fast.py
```

You should see a successful connection and the result of calling the `add` tool.

### Alternative setup (pip and `venv`)

If you prefer not to use uv:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install "fastmcp>=3.1.1" "mcp>=1.26.0"
```

Then run scripts with that activated environment, for example:

```powershell
python src/server.py
```

On macOS or Linux, activate with `source .venv/bin/activate` instead of the `Activate.ps1` line.

## Run the MCP server

```powershell
uv run python src/server.py
```

By default the server listens at **http://127.0.0.1:8000/mcp** (path `/mcp`). Keep this process running while you use a client.

## Example clients

The repository includes two sample clients that talk to the same URL. Start the server first, then in another terminal:

**FastMCP high-level client** (`src/client/client_fast.py`):

```powershell
uv run python src/client/client_fast.py
```

**Lower-level MCP SDK client** (`src/client/client.py`):

```powershell
uv run python src/client/client.py
```

Both examples call the `add` tool with `a=5` and `b=3`.

## Tests

Unit tests live under `tests/` and target the pure logic in `src/tools/calculator.py` (the MCP server delegates to that module).

```powershell
uv run pytest
```

For a quieter summary:

```powershell
uv run pytest -q
```

If you use pip only, install pytest in your virtual environment (`pip install pytest`) and run `pytest` from the repo root (the same `pythonpath` is set in `pyproject.toml` for pytest).

## Suggested learning order

1. Skim the [MCP introduction](https://modelcontextprotocol.io/) so you know what “tools” and transports mean in this context.
2. Read `src/tools/calculator.py` and `tests/test_calculator.py`—pure functions and how they are tested.
3. Read `src/server.py`—this is where tools are registered and the HTTP transport is started.
4. Read `src/client/client_fast.py`—shortest path from “HTTP URL” to `call_tool`.
5. Read `src/client/client.py`—same outcome using the lower-level `mcp` client session APIs.
6. Try adding a second tool (for example `multiply`) on the server, cover it with tests, and call it from one of the clients.

## Publishing to GitHub (public repository)

Use this as a checklist before you make the repo public.

1. **Initialize Git locally** (if you have not committed yet):

   ```powershell
   cd C:\path\to\mcp-app-calculator
   git init
   git add pyproject.toml uv.lock README.md .gitignore src tests
   git commit -m "Initial commit: MCP calculator server and example clients"
   ```

2. **Create an empty repository** on GitHub (no README/license there if you already have them locally—avoids merge noise). Copy the remote URL GitHub shows.

3. **Add the remote and push:**

   ```powershell
   git remote add origin https://github.com/georgejinu-labs/mcp-app-calculator.git
   git branch -M main
   git push -u origin main
   ```

4. **Before going public, verify:**

   - No secrets in the repo (API keys, `.env` files, private URLs). This project does not need secrets for local demos; keep it that way.
   - `.gitignore` excludes virtual environments and caches so you do not upload `.venv` or `__pycache__`.
   - Add a **LICENSE** file if you want others to know how they may use your code (GitHub can add one when you create the repo, or you can commit a file such as `LICENSE` with MIT/Apache-2.0 text).
   - Optional: turn on GitHub **Dependabot** or **branch protection** later as the project grows.

## Tools

| Name | Description | Arguments |
|------|-------------|-----------|
| `add` | Add two integers | `a` (int), `b` (int) |

## Project layout

| Path | Role |
|------|------|
| `src/tools/calculator.py` | Pure calculator tool logic used by the server (and unit tests) |
| `src/server.py` | MCP server definition and `mcp.run(transport="streamable-http")` |
| `src/client/client_fast.py` | Demo using `fastmcp.Client` |
| `src/client/client.py` | Demo using `mcp` streamable HTTP session APIs |
| `tests/test_calculator.py` | Pytest unit tests for `tools.calculator.add` |
| `pyproject.toml` | Project metadata, dependencies, and pytest settings |
| `uv.lock` | Locked versions for reproducible installs with uv |

## License

No license file is present in this repository yet. If you publish on GitHub publicly, add a `LICENSE` file so others know what they are allowed to do with the code.
