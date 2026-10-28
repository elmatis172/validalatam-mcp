# validalatam-mcp

<!-- mcp-name: io.github.elmatis172/validalatam-mcp -->

[![Listed on mcpservers.org](https://mcpservers.org/badge.svg)](https://mcpservers.org/servers/elmatis172/validalatam-mcp) [![elmatis172/validalatam-mcp MCP server](https://glama.ai/mcp/servers/elmatis172/validalatam-mcp/badges/score.svg)](https://glama.ai/mcp/servers/elmatis172/validalatam-mcp) [![Validalatam MCP server](https://mcprush.com/badge/validalatam-mcp/card.svg)](https://mcprush.com/to/validalatam-mcp?ref=badge)

MCP server for the **[ValidaLatam API](https://validalatam.ia-latam.app)** — validate, normalize and format Latin American tax IDs, national IDs and bank accounts: AR CUIT/CUIL/DNI/CBU/CVU, BR CPF/CNPJ, MX RFC/CURP/CLABE, CL RUT, CO NIT, PE RUC, UY CI/RUT, EC Cédula/RUC, PY RUC, IBAN.

This is a thin client: every tool call is an HTTP request to the hosted API. No validation algorithms are included here.

**API key / plans on RapidAPI: https://rapidapi.com/MatiasPengue/api/validalatam**

[English](#english) | [Español](#español)

## English

### Install
```bash
uvx validalatam-mcp
# or
pip install validalatam-mcp
validalatam-mcp
```
Published on [PyPI](https://pypi.org/project/validalatam-mcp/). Step-by-step guide for AI agents (Cline, etc.): [llms-install.md](llms-install.md).

### Claude Desktop (`claude_desktop_config.json`) / Cursor (`~/.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "validalatam": {
      "command": "uvx",
      "args": ["validalatam-mcp"],
      "env": { "RAPIDAPI_KEY": "optional-your-key" }
    }
  }
}
```

### Tools
- `validate_document(type, value, country?)` — `type="AUTO"` auto-detects
- `validate_batch(items)` — up to 1000 `{type, value, country?}`
- `generate_test_data(type, count, seed)` — clearly fake, check-digit-valid values
- `list_document_types()`

### Configuration
| Env var | Default | Purpose |
|---|---|---|
| `RAPIDAPI_KEY` | – | Recommended. If set, calls go through RapidAPI (`validalatam.p.rapidapi.com`) and use your plan's quota (free Basic plan available). Without it, the public endpoint is a **demo limited to 10 requests per IP per day**, and `validate_batch` / `generate_test_data` are not available (they require RapidAPI: Basic free, Pro 9 USD/mo, Ultra 29, Mega 99 — https://rapidapi.com/MatiasPengue/api/validalatam/pricing). The first tool result shows a short notice about this. |
| `VALIDALATAM_BASE_URL` | `https://validalatam.ia-latam.app` | Override API base URL |

### Docker
```bash
docker build -t validalatam-mcp . && docker run -i --rm validalatam-mcp
```

### Client SDKs
Zero-dependency clients in `sdks/python/validalatam_client.py` and `sdks/js/index.mjs`.

### Development
```bash
pip install -e ".[test]" && pytest
```

## Español

Servidor MCP para la **[API ValidaLatam](https://validalatam.ia-latam.app)**: valida, normaliza y formatea CUIT/CUIL, DNI, CBU/CVU, CPF, CNPJ, RFC, CURP, CLABE, RUT, NIT, RUC, CI, cédulas e IBAN. Es un cliente liviano: cada herramienta llama por HTTP a la API alojada; no incluye los algoritmos de validación.

**Clave de API y planes en RapidAPI: https://rapidapi.com/MatiasPengue/api/validalatam**

### Instalación
```bash
uvx validalatam-mcp
# o
pip install validalatam-mcp
```

### Claude Desktop / Cursor
Usá el mismo bloque JSON de arriba en `claude_desktop_config.json` o `~/.cursor/mcp.json`. `RAPIDAPI_KEY` es opcional pero recomendado: sin clave, el endpoint público es una demo limitada a 10 requests por día y por IP, y `validate_batch` / `generate_test_data` requieren RapidAPI (Pro 9 USD/mes, https://rapidapi.com/MatiasPengue/api/validalatam/pricing). Con clave se usa la cuota de tu plan en RapidAPI (hay un plan Basic gratis).

### Herramientas
`validate_document`, `validate_batch`, `generate_test_data` (datos FALSOS de prueba), `list_document_types`.

## License / Licencia
MIT
