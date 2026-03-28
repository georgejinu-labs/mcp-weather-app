# MCP weather app

A small [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that exposes **weather** and **forecast** tools over HTTP. It uses [wttr.in](https://github.com/chubin/wttr.in) (`format=j1`) for data—no API key required. Built with [FastMCP](https://gofastmcp.com/) and the **streamable HTTP** transport.

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
| `src/server.py` | Registers MCP tools and runs `mcp.run(transport="streamable-http")` |
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
3. Read `src/server.py`—how tools are exposed to the host.
4. Read `src/client/client_fast.py`—from HTTP URL to `list_tools` / `call_tool`.

## Connecting from an MCP host (e.g. Cursor)

Point your client at the same base URL the sample uses (`http://localhost:8000/mcp/` or your deployed URL), with the server process running. Exact UI steps depend on the host; the server side is this repo’s `src/server.py`.

## Clone and publish (optional)

Replace URLs and folder names with your own.

```powershell
git clone https://github.com/georgejinu-labs/mcp-weather-app.git
cd mcp-weather-app
```

Before making a repo public: confirm no secrets in the tree; this project does not require API keys for wttr.in.

## License

No license file is included by default. Add a `LICENSE` file if you publish the project so others know how they may use the code.
