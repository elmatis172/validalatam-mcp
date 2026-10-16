"""Minimal zero-dependency Python client for the ValidaLatam API on RapidAPI.

    from validalatam_client import ValidaLatam
    v = ValidaLatam("YOUR_RAPIDAPI_KEY")
    v.validate("BR_CPF", "529.982.247-25")["valid"]
"""
import json
import urllib.parse
import urllib.request

HOST = "validalatam.p.rapidapi.com"


class ValidaLatam:
    def __init__(self, api_key: str, host: str = HOST, timeout: float = 10):
        self.base, self.timeout = f"https://{host}", timeout
        self.headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": host, "Content-Type": "application/json"}

    def _req(self, method, path, body=None):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(self.base + path, data=data, method=method, headers=self.headers)
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            return json.loads(r.read())

    def validate(self, doc_type: str, value: str, country: str | None = None) -> dict:
        q = {"value": value, **({"country": country} if country else {})}
        return self._req("GET", f"/validate/{doc_type}?{urllib.parse.urlencode(q)}")

    def batch(self, items: list[dict]) -> dict:
        return self._req("POST", "/batch", {"items": items})

    def generate(self, doc_type: str, count: int = 5, seed: int = 0) -> dict:
        return self._req("GET", f"/generate/{doc_type}?count={count}&seed={seed}")

    def types(self) -> dict:
        return self._req("GET", "/types")
