# validalatam-mcp

<!-- mcp-name: io.github.elmatis172/validalatam-mcp -->

MCP server for the **[ValidaLatam API](https://validalatam.ia-latam.app)** — validate, normalize and format Latin American tax IDs, national IDs and bank accounts: AR CUIT/CUIL/DNI/CBU/CVU, BR CPF/CNPJ, MX RFC/CURP/CLABE, CL RUT, CO NIT, PE RUC, UY CI/RUT, EC Cédula/RUC, PY RUC, IBAN.

This is a thin client: every tool call is an HTTP request to the hosted API. No validation algorithms are included here.

**API key / plans on RapidAPI: https://rapidapi.com/MatiasPengue/api/validalatam**

[English](#english) | [Español](#español)

## English

### Install
```bash
uvx --from git+https://github.com/elmatis172/validalatam-mcp validalatam-mcp
# or
pip install git+https://github.com/elmatis172/validalatam-mcp
validalatam-mcp
```
(Once published to PyPI: `uvx validalatam-mcp` / `pip install validalatam-mcp`.)

### Claude Desktop (`claude_desktop_config.json`) / Cursor (`~/.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "validalatam": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/elmatis172/validalatam-mcp", "validalatam-mcp"],
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
| `RAPIDAPI_KEY` | – | Recommended. If set, calls go through RapidAPI (`validalatam.p.rapidapi.com`) and use your plan's quota (free Basic plan available). Without it, the public endpoint allows a small free number of validations per day per IP (a batch counts each document). |
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
uvx --from git+https://github.com/elmatis172/validalatam-mcp validalatam-mcp
# o
pip install git+https://github.com/elmatis172/validalatam-mcp
```

### Claude Desktop / Cursor
Usá el mismo bloque JSON de arriba en `claude_desktop_config.json` o `~/.cursor/mcp.json`. `RAPIDAPI_KEY` es opcional pero recomendado: sin clave, el endpoint público permite unas pocas validaciones gratis por día y por IP (un batch cuenta cada documento). Con clave se usa la cuota de tu plan en RapidAPI (hay un plan Basic gratis).

### Herramientas
`validate_document`, `validate_batch`, `generate_test_data` (datos FALSOS de prueba), `list_document_types`.

## License / Licencia
MIT
