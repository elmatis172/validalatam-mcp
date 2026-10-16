// Minimal zero-dependency JS/TS client for the ValidaLatam API on RapidAPI (Node 18+, Deno, Bun, browsers).
// import { ValidaLatam } from "./index.mjs"; const v = new ValidaLatam(process.env.RAPIDAPI_KEY);
// const { valid, formatted } = await v.validate("AR_CUIT", "27-46447810-3");
const HOST = "validalatam.p.rapidapi.com";

export class ValidaLatam {
  constructor(apiKey, { host = HOST } = {}) {
    this.base = `https://${host}`;
    this.headers = { "X-RapidAPI-Key": apiKey, "X-RapidAPI-Host": host, "Content-Type": "application/json" };
  }
  async #req(path, init = {}) {
    const r = await fetch(this.base + path, { ...init, headers: this.headers });
    if (!r.ok) throw new Error(`ValidaLatam ${r.status}: ${await r.text()}`);
    return r.json();
  }
  validate(type, value, country) {
    const q = new URLSearchParams({ value, ...(country ? { country } : {}) });
    return this.#req(`/validate/${type}?${q}`);
  }
  batch(items) { return this.#req("/batch", { method: "POST", body: JSON.stringify({ items }) }); }
  generate(type, count = 5, seed = 0) { return this.#req(`/generate/${type}?count=${count}&seed=${seed}`); }
  types() { return this.#req("/types"); }
}
