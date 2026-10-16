"""Thin MCP server (stdio) for the hosted ValidaLatam API. No validation logic runs locally.

Env vars:
  VALIDALATAM_BASE_URL  default https://validalatam.ia-latam.app
  RAPIDAPI_KEY          optional; if set, requests go through RapidAPI (validalatam.p.rapidapi.com)
"""
import os
from typing import Any

import httpx
try:
    from mcp.server.mcpserver import MCPServer as FastMCP  # mcp >= 2
except ImportError:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP

DEFAULT_BASE = "https://validalatam.ia-latam.app"
RAPID_HOST = "validalatam.p.rapidapi.com"

mcp = FastMCP("validalatam")


def _client() -> httpx.Client:
    key = os.environ.get("RAPIDAPI_KEY")
    if key:
        return httpx.Client(base_url=f"https://{RAPID_HOST}", timeout=15,
                            headers={"X-RapidAPI-Key": key, "X-RapidAPI-Host": RAPID_HOST})
    return httpx.Client(base_url=os.environ.get("VALIDALATAM_BASE_URL", DEFAULT_BASE).rstrip("/"), timeout=15,
                        headers={"User-Agent": "validalatam-mcp/0.1.0"})


def _call(method: str, path: str, **kw) -> Any:
    with _client() as c:
        r = c.request(method, path, **kw)
        r.raise_for_status()
        return r.json()


@mcp.tool()
def validate_document(type: str, value: str, country: str | None = None) -> dict:
    """Validate/normalize/format a LatAm document (AR_CUIT, BR_CPF, BR_CNPJ, MX_RFC, MX_CURP, CL_RUT, CO_NIT, PE_RUC, IBAN...). type='AUTO' auto-detects."""
    body = {"type": type, "value": value}
    if country:
        body["country"] = country
    return _call("POST", "/validate", json=body)


@mcp.tool()
def validate_batch(items: list[dict]) -> Any:
    """Validate up to 1000 items, each {type, value, country?}."""
    return _call("POST", "/batch", json={"items": items[:1000]})


@mcp.tool()
def generate_test_data(type: str, count: int = 5, seed: int = 0) -> Any:
    """Generate clearly FAKE, check-digit-valid test values for a document type."""
    return _call("GET", f"/generate/{type}", params={"count": count, "seed": seed})


@mcp.tool()
def list_document_types() -> Any:
    """List supported document type codes."""
    return _call("GET", "/types")


def main():
    mcp.run()


if __name__ == "__main__":
    main()
