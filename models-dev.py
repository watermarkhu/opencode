#!/usr/bin/env python3
"""Fetch all models from models.dev and print their name and API endpoint."""

import json
import sys
import urllib.request


def fetch_providers(url: str = "https://models.dev/api.json") -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "opencode-models-dev-script/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def main() -> None:
    try:
        providers = fetch_providers()
    except Exception as exc:
        print(f"Error fetching models.dev: {exc}", file=sys.stderr)
        sys.exit(1)

    rows = []
    for provider in providers.values():
        provider_api = provider.get("api", "")
        provider_name = provider.get("name", provider.get("id", ""))
        for model in provider.get("models", {}).values():
            model_api = model.get("provider", {}).get("api") or provider_api
            rows.append((provider_name, model.get("name", model.get("id", "")), model_api))

    rows.sort(key=lambda r: (r[0].lower(), r[1].lower()))

    col_provider = max(len("Provider"), max(len(r[0]) for r in rows))
    col_model = max(len("Model"), max(len(r[1]) for r in rows))
    col_api = max(len("API"), max(len(r[2]) for r in rows))

    header = f"{'Provider':<{col_provider}}  {'Model':<{col_model}}  {'API':<{col_api}}"
    print(header)
    print("-" * len(header))
    for provider_name, model_name, api in rows:
        print(f"{provider_name:<{col_provider}}  {model_name:<{col_model}}  {api}")


if __name__ == "__main__":
    main()
