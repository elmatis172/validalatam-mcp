# Installing validalatam-mcp (guide for AI agents such as Cline)

`validalatam-mcp` is a stdio MCP server published on PyPI. It is a thin HTTP client for the hosted ValidaLatam API (https://validalatam.ia-latam.app); nothing needs to be built or cloned.

## Requirements
- Python 3.10+ with `pip`, **or** `uv` (provides `uvx`).

## Option A (recommended): uvx
No install step needed. Add this to the MCP settings file (for Cline: `cline_mcp_settings.json`):

```json
{
  "mcpServers": {
    "validalatam": {
      "command": "uvx",
      "args": ["validalatam-mcp"],
      "env": { "RAPIDAPI_KEY": "" }
    }
  }
}
```

## Option B: pip
```bash
pip install validalatam-mcp
```
Then configure:
```json
{
  "mcpServers": {
    "validalatam": {
      "command": "validalatam-mcp",
      "args": [],
      "env": { "RAPIDAPI_KEY": "" }
    }
  }
}
```
If the `validalatam-mcp` script is not on PATH, use `"command": "python", "args": ["-m", "validalatam_mcp.server"]` with the Python interpreter where it was installed.

## API key (optional)
- `RAPIDAPI_KEY` is **optional**. Without it the server works immediately using the public endpoint, which allows a small free number of validations per day per IP.
- For more volume, the user can get a key (free Basic plan available) at https://rapidapi.com/MatiasPengue/api/validalatam and put it in `RAPIDAPI_KEY`. Ask the user for the key; do not invent one. Leave it empty or remove the `env` block if they don't have one.
- `VALIDALATAM_BASE_URL` (optional) overrides the API base URL; default `https://validalatam.ia-latam.app`.

## Verify
After configuring, the server should expose 4 tools: `validate_document`, `validate_batch`, `generate_test_data`, `list_document_types`.
Quick test: call `validate_document` with `{"type": "AUTO", "value": "20-12345678-6"}`; it should return `"valid": true, "type": "AR_CUIT"`.
