"""Thin MCP server (stdio) for the hosted ValidaLatam API. No validation logic runs locally.

Env vars:
  VALIDALATAM_BASE_URL  default https://validalatam.ia-latam.app
  RAPIDAPI_KEY          optional; if set, requests go through RapidAPI (validalatam.p.rapidapi.com)
                        and count against your RapidAPI plan. Without it, the public endpoint is used,
                        limited to a demo of 10 requests per day per IP; batch/generate need a RapidAPI key.
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
RAPIDAPI_URL = "https://rapidapi.com/MatiasPengue/api/validalatam"
USER_AGENT = "validalatam-mcp/0.2.2"

PRICING_URL = RAPIDAPI_URL + "/pricing"
DEMO_NOTICE = ("Notice: without RAPIDAPI_KEY this MCP uses the public ValidaLatam endpoint, a demo limited to "
               "10 requests per IP per day. validate_batch and generate_test_data require a RapidAPI key "
               f"(Pro plan 9 USD/month, free Basic plan available): {PRICING_URL} - set it as RAPIDAPI_KEY.")
_notice_shown = False

mcp = FastMCP("validalatam", instructions=DEMO_NOTICE)


def _has_key() -> bool:
    return bool(os.environ.get("RAPIDAPI_KEY", "").strip())


def _with_notice(result: Any) -> Any:
    """Attach the demo notice to the first result of the session (direct mode only)."""
    global _notice_shown
    if _notice_shown or _has_key():
        return result
    _notice_shown = True
    if isinstance(result, dict):
        return {"notice": DEMO_NOTICE, **result}
    return {"notice": DEMO_NOTICE, "data": result}


def _client() -> httpx.Client:
    key = os.environ.get("RAPIDAPI_KEY", "").strip()
    if key:
        return httpx.Client(base_url=f"https://{RAPID_HOST}", timeout=15,
                            headers={"X-RapidAPI-Key": key, "X-RapidAPI-Host": RAPID_HOST,
                                     "User-Agent": USER_AGENT})
    return httpx.Client(base_url=os.environ.get("VALIDALATAM_BASE_URL", DEFAULT_BASE).rstrip("/"), timeout=15,
                        headers={"User-Agent": USER_AGENT})


def _call(method: str, path: str, **kw) -> Any:
    return _with_notice(_raw_call(method, path, **kw))


def _raw_call(method: str, path: str, **kw) -> Any:
    with _client() as c:
        r = c.request(method, path, **kw)
        if r.status_code == 429 and not os.environ.get("RAPIDAPI_KEY", "").strip():
            try:
                info = r.json()
            except ValueError:
                info = {}
            return {
                "error": "free_daily_limit_exceeded",
                "message": info.get("message") or "Free daily limit of the public ValidaLatam endpoint reached.",
                "how_to_fix": f"Get a RapidAPI key (free Basic plan available) at {RAPIDAPI_URL} "
                              "and set it as the RAPIDAPI_KEY env var of this MCP server.",
                "reset_at": info.get("reset_at"),
                "upgrade_url": PRICING_URL,
            }
        if r.status_code in (402, 403) and not _has_key():
            try:
                info = r.json()
            except ValueError:
                info = {}
            return {
                "error": info.get("error") or "rapidapi_required",
                "message": info.get("message") or f"{path} requires a RapidAPI key.",
                "how_to_fix": f"Subscribe at {PRICING_URL} (Pro 9 USD/month; free Basic plan available) "
                              "and set your key as the RAPIDAPI_KEY env var of this MCP server.",
                "upgrade_url": PRICING_URL,
            }
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
    """Validate up to 1000 items, each {type, value, country?}. Requires RAPIDAPI_KEY."""
    return _call("POST", "/batch", json={"items": items[:1000]})


@mcp.tool()
def generate_test_data(type: str, count: int = 5, seed: int = 0) -> Any:
    """Generate clearly FAKE, check-digit-valid test values for a document type. Requires RAPIDAPI_KEY."""
    return _call("GET", f"/generate/{type}", params={"count": count, "seed": seed})


@mcp.tool()
def list_document_types() -> Any:
    """List supported document type codes."""
    return _call("GET", "/types")


def main():
    mcp.run()


if __name__ == "__main__":
    main()
