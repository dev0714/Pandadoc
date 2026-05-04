#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any


DEFAULT_BASE_URL = "https://api.pandadoc.com/public/v1"


def request_json(base_url: str, api_key: str, method: str, path: str, body: dict[str, Any] | None = None) -> Any:
    url = base_url.rstrip("/") + "/" + path.lstrip("/")
    headers = {
        "Authorization": f"API-Key {api_key}",
    }
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as error:
        payload = error.read().decode("utf-8")
        raise RuntimeError(
            f"PandaDoc API request failed ({error.code}): {payload or error.reason}"
        ) from error


def read_current_member(base_url: str, api_key: str) -> dict[str, str]:
    response = request_json(base_url, api_key, "GET", "/members/current")
    if not isinstance(response, dict):
        raise RuntimeError("PandaDoc current member response did not return an object.")

    return {
        "user_id": str(response.get("user_id") or ""),
        "membership_id": str(response.get("membership_id") or ""),
        "email": str(response.get("email") or ""),
        "first_name": str(response.get("first_name") or ""),
        "last_name": str(response.get("last_name") or ""),
        "is_active": str(response.get("is_active") or ""),
        "workspace": str(response.get("workspace") or ""),
        "workspace_name": str(response.get("workspace_name") or ""),
        "role": str(response.get("role") or ""),
        "email_verified": str(response.get("email_verified") or ""),
    }


def read_template_details(base_url: str, api_key: str, template_uuid: str) -> dict[str, str]:
    response = request_json(base_url, api_key, "GET", f"/templates/{template_uuid}/details")
    if not isinstance(response, dict):
        raise RuntimeError("PandaDoc template details response did not return an object.")

    template_id = str(response.get("id") or response.get("template_id") or template_uuid)
    template_name = str(response.get("name") or response.get("template_name") or "")

    return {
        "id": template_id,
        "name": template_name,
        "status": str(response.get("status") or response.get("template_status") or ""),
        "workspace": str(response.get("workspace") or ""),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the PandaDoc API key, workspace, and optional template access."
    )
    parser.add_argument("--api-key", default=os.getenv("PANDADOC_API_KEY"))
    parser.add_argument("--base-url", default=os.getenv("PANDADOC_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--template-uuid", default=os.getenv("PANDADOC_TEMPLATE_UUID"))
    args = parser.parse_args()

    if not args.api_key:
        raise SystemExit("Missing required value: api_key")

    summary: dict[str, Any] = {
        "base_url": args.base_url,
        "auth_ok": False,
        "template_ok": None,
    }

    member = read_current_member(args.base_url, args.api_key)
    summary["auth_ok"] = True
    summary["member"] = member
    print(
        "PandaDoc auth OK for "
        f"{member['email'] or 'unknown email'}"
        f" in workspace {member['workspace_name'] or member['workspace'] or 'unknown'}"
    )

    if args.template_uuid:
        template = read_template_details(args.base_url, args.api_key, args.template_uuid)
        summary["template_ok"] = True
        summary["template"] = template
        print(
            "PandaDoc template OK: "
            f"{template['name'] or 'unknown template'} ({template['id']})"
        )

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
