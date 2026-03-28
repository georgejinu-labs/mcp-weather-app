# MCP weather app

A small [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that exposes **weather** and **forecast** tools. It uses [wttr.in](https://github.com/chubin/wttr.in) (`format=j1`) for data—no API key required. Built with [FastMCP](https://gofastmcp.com/).

Two entrypoints:

- **`src/server.py`** — **streamable HTTP** (default URL `http://127.0.0.1:8000/mcp/`).
- **`src/server-stdio.py`** — **stdio** transport for hosts and tools such as [MCP Inspector](https://github.com/modelcontextprotocol/inspector) or Cursor’s stdio MCP config.

Use it as a reference for splitting **tool logic** (testable Python) from **MCP registration** (thin server), and for wiring a **FastMCP client** to the same URL an IDE or agent would use.

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or a virtual environment plus `pip`
- Network access to `https://wttr.in` when calling the live tools

## Quick start

From the repository root (where `pyproject.toml` lives):

```powershell
uv sync
```

Start the server (keep this terminal open):

```powershell
uv run python src/server.py
```

By default the server listens at **http://127.0.0.1:8000/mcp/** (path `/mcp/`).

In another terminal, run the sample client:

```powershell
uv run python src/client/client_fast.py
```

You should see a connection message, listed tools, and sample output for `get_weather` and `get_forecast`.

### Alternative setup (pip and `venv`)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install "fastmcp>=3.1.1" "mcp>=1.26.0" httpx
```

(`httpx` is used by `tools/weather.py`; it is often pulled in with FastMCP, but installing it explicitly avoids surprises.)

On macOS or Linux, activate with `source .venv/bin/activate`.

## Tools

| Name | Description | Arguments |
|------|-------------|-----------|
| `get_weather` | Current conditions for a place | `city` (string, e.g. `London` or `~New+York`) |
| `get_forecast` | First forecast hour (same JSON source) | `city` (string) |

Weather text is built in `src/tools/weather.py`, which tolerates wttr.in field differences (for example missing `gustKmph` on current conditions, or `WindGustKmph` on hourly data).

## Project layout

| Path | Role |
|------|------|
| `src/tools/weather.py` | Fetch + format logic; optional injected `httpx.AsyncClient` for tests |
| `src/server.py` | Registers MCP tools; `mcp.run(transport="streamable-http")` |
| `src/server-stdio.py` | Same tools; `mcp.run(transport="stdio")` for Inspector / stdio hosts |
| `src/client/client_fast.py` | Demo: `fastmcp.Client` lists tools and calls `get_weather` / `get_forecast` |
| `tests/test_weather.py` | Pytest tests for formatting helpers |
| `pyproject.toml` | Dependencies, dev group (`pytest`), pytest `pythonpath = ["src"]` |

## Tests

Install dev dependencies (pytest) with uv:

```powershell
uv sync --group dev
```

Run tests from the repo root:

```powershell
uv run pytest
```

Quiet summary:

```powershell
uv run pytest -q
```

Tests focus on **pure formatters** (`format_current_weather`, `format_forecast`) so they stay fast and deterministic without mocking HTTP.

## Suggested learning order

1. Skim the [MCP introduction](https://modelcontextprotocol.io/) for tools and transports.
2. Read `src/tools/weather.py` and `tests/test_weather.py`—business logic separate from MCP.
3. Read `src/server.py` or `src/server-stdio.py`—same tools; pick HTTP or stdio transport.
4. Read `src/client/client_fast.py`—from HTTP URL to `list_tools` / `call_tool`.

## Connecting from an MCP host (e.g. Cursor)

### HTTP (`streamable-http`)

Point your client at the same base URL the sample uses (`http://localhost:8000/mcp/` or your deployed URL), with `src/server.py` running.

### STDIO (MCP Inspector, some IDE configs)

Use **`src/server-stdio.py`**. Common reasons Inspector shows *“Connection Error … proxy token”* are: the child process **exits immediately** (bad command/args, wrong cwd, import error) or the **script path is truncated** in the UI.

**Recommended: `uv` from the repo root**

`uv run` attaches to the project **only if the process working directory is the repo root** (the folder that contains `pyproject.toml`). MCP Inspector often starts children with cwd = your user folder or the app install path. If cwd is wrong, you get `ModuleNotFoundError: No module named 'fastmcp'` and Inspector stays **Disconnected**.

Set the inspector’s **working directory / cwd** explicitly to:

`C:\sources\georgejinu-labs\mcp-weather-app` (or your clone path).

Then use Command `uv` and arguments `run`, `python`, and either `src/server-stdio.py` or the full path to `server-stdio.py`.

| Field | Value |
|--------|--------|
| Transport | **STDIO** |
| Command | `uv` |
| Arguments | Add **three** separate arguments (not one comma-separated string): `run`, `python`, `src/server-stdio.py` |

If the UI expects a single JSON array, use:

```json
["run", "python", "src/server-stdio.py"]
```

Use the **full** script name `server-stdio.py`. A path that stops at `...\src\s` or `...\server-` is incomplete and will fail—Inspector will stay **Disconnected** because the child process exits immediately.

You must pass **`python`** as its own argument between `run` and the script. Wrong: `uv` + args `run`, `C:\...\server-stdio.py`. Right: `uv` + args `run`, `python`, `src/server-stdio.py` (or the full path to `server-stdio.py`).

**More reliable in Inspector: venv `python` (works even when cwd is wrong)**

If there is no cwd field—or it does not stick—**do not use `uv` inside Inspector**. Call the project interpreter and script with **absolute paths**; dependencies then load from `.venv` regardless of cwd.

| Field | Value |
|--------|--------|
| Command | `C:\sources\georgejinu-labs\mcp-weather-app\.venv\Scripts\python.exe` |
| Arguments | `C:\sources\georgejinu-labs\mcp-weather-app\src\server-stdio.py` |

Use a **single** argument: the full path to `server-stdio.py` (in the Arguments list, one entry). Run `uv sync` once from a terminal so `.venv` exists.

JSON form if the UI wants one array:

```json
["C:\\sources\\georgejinu-labs\\mcp-weather-app\\src\\server-stdio.py"]
```

(Command is still the `python.exe` path above—not `uv`.)

**Smoke test in a terminal:** from the repo root, run:

```powershell
cd C:\sources\georgejinu-labs\mcp-weather-app
uv run python src/server-stdio.py
```

You should see the FastMCP banner and a log line such as `Starting MCP server 'Weather Server' with transport 'stdio'`. After that, the process **stays running** and waits for MCP messages on stdin—leave it open while MCP Inspector (or another stdio client) connects, or press Ctrl+C to stop.

If you get a **traceback** instead, fix that before using Inspector.

## Clone and publish (optional)

Replace URLs and folder names with your own.

```powershell
git clone https://github.com/georgejinu-labs/mcp-weather-app.git
cd mcp-weather-app
```

Before making a repo public: confirm no secrets in the tree; this project does not require API keys for wttr.in.

## License

No license file is included by default. Add a `LICENSE` file if you publish the project so others know how they may use the code.
