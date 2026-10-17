import httpx
import respx

from validalatam_mcp import server

BASE = server.DEFAULT_BASE


@respx.mock
def test_validate_document(monkeypatch):
    monkeypatch.delenv("RAPIDAPI_KEY", raising=False)
    route = respx.post(f"{BASE}/validate").mock(return_value=httpx.Response(200, json={"valid": True, "type": "BR_CPF"}))
    assert server.validate_document("BR_CPF", "529.982.247-25")["valid"] is True
    assert route.calls.last.request.content == b'{"type":"BR_CPF","value":"529.982.247-25"}'


@respx.mock
def test_batch_truncates(monkeypatch):
    monkeypatch.delenv("RAPIDAPI_KEY", raising=False)
    route = respx.post(f"{BASE}/batch").mock(return_value=httpx.Response(200, json={"results": []}))
    server.validate_batch([{"type": "AUTO", "value": "1"}] * 1500)
    import json
    assert len(json.loads(route.calls.last.request.content)["items"]) == 1000


@respx.mock
def test_generate_and_types(monkeypatch):
    monkeypatch.delenv("RAPIDAPI_KEY", raising=False)
    g = respx.get(f"{BASE}/generate/AR_CUIT").mock(return_value=httpx.Response(200, json={"items": []}))
    respx.get(f"{BASE}/types").mock(return_value=httpx.Response(200, json={"types": ["AR_CUIT"]}))
    server.generate_test_data("AR_CUIT", 3, 7)
    assert g.calls.last.request.url.params["count"] == "3"
    assert server.list_document_types() == {"types": ["AR_CUIT"]}


@respx.mock
def test_rapidapi_key(monkeypatch):
    monkeypatch.setenv("RAPIDAPI_KEY", "k")
    r = respx.get(f"https://{server.RAPID_HOST}/types").mock(return_value=httpx.Response(200, json={}))
    server.list_document_types()
    assert r.calls.last.request.headers["X-RapidAPI-Key"] == "k"


@respx.mock
def test_http_error(monkeypatch):
    monkeypatch.delenv("RAPIDAPI_KEY", raising=False)
    respx.get(f"{BASE}/types").mock(return_value=httpx.Response(500))
    try:
        server.list_document_types()
        assert False
    except httpx.HTTPStatusError:
        pass


def test_tools_registered():
    import asyncio
    names = {t.name for t in asyncio.run(server.mcp.list_tools())}
    assert names == {"validate_document", "validate_batch", "generate_test_data", "list_document_types"}


@respx.mock
def test_direct_429_returns_upgrade_hint(monkeypatch):
    monkeypatch.delenv("RAPIDAPI_KEY", raising=False)
    respx.post(f"{BASE}/validate").mock(return_value=httpx.Response(
        429, json={"error": "free_daily_limit_exceeded", "message": "limit", "reset_at": "2026-10-18T00:00:00Z"}))
    out = server.validate_document("BR_CPF", "52998224725")
    assert out["error"] == "free_daily_limit_exceeded"
    assert out["upgrade_url"] == server.RAPIDAPI_URL and "RAPIDAPI_KEY" in out["how_to_fix"]
    assert out["reset_at"] == "2026-10-18T00:00:00Z"


@respx.mock
def test_rapidapi_headers_and_user_agent(monkeypatch):
    monkeypatch.setenv("RAPIDAPI_KEY", "k")
    r = respx.post(f"https://{server.RAPID_HOST}/batch").mock(return_value=httpx.Response(200, json={"results": []}))
    server.validate_batch([{"type": "AUTO", "value": "1"}])
    h = r.calls.last.request.headers
    assert h["X-RapidAPI-Host"] == server.RAPID_HOST and h["User-Agent"] == server.USER_AGENT


@respx.mock
def test_blank_key_uses_direct(monkeypatch):
    monkeypatch.setenv("RAPIDAPI_KEY", "  ")
    r = respx.get(f"{BASE}/types").mock(return_value=httpx.Response(200, json={}))
    server.list_document_types()
    assert r.called and "X-RapidAPI-Key" not in r.calls.last.request.headers
