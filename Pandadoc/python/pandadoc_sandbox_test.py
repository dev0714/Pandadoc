#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request


def request_json(base_url, api_key, method, path, body=None):
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
        raise RuntimeError(f"PandaDoc API request failed ({error.code}): {payload or error.reason}") from error


def create_create_body(args):
    tokens = []
    if args.client_first_name:
        tokens.append({"name": "Client.FirstName", "value": args.client_first_name})
    if args.client_last_name:
        tokens.append({"name": "Client.LastName", "value": args.client_last_name})

    body = {
        "template_uuid": args.template_uuid,
        "name": args.name,
        "recipients": [
            {
                "email": args.recipient_email,
                "first_name": args.recipient_first_name,
                "last_name": args.recipient_last_name,
                "role": args.recipient_role,
            }
        ],
    }
    if tokens:
        body["tokens"] = tokens
    body = {key: value for key, value in body.items() if value is not None}
    body["recipients"] = [
        {key: value for key, value in recipient.items() if value is not None}
        for recipient in body["recipients"]
    ]
    return body


def wait_for_draft(base_url, api_key, document_id, poll_interval, max_attempts):
    for attempt in range(max_attempts):
        response = request_json(base_url, api_key, "GET", f"/documents/{document_id}")
        status = response.get("status") or response.get("document_status")
        if status == "document.draft":
            return
        if status == "document.error":
            raise RuntimeError(f"Document {document_id} failed to process.")
        if attempt < max_attempts - 1:
            time.sleep(poll_interval)
    raise RuntimeError(f"Timed out waiting for document {document_id} to reach draft status.")


def read_session_url(payload):
    for key in ("url", "session_url", "sessionUrl"):
        value = payload.get(key)
        if value:
            return value
    for key in ("id", "session_id", "sessionId"):
        value = payload.get(key)
        if value:
            return f"https://app.pandadoc.com/s/{value}"
    raise RuntimeError("PandaDoc session response did not include a signing URL or session id.")


def main():
    parser = argparse.ArgumentParser(description="Test the PandaDoc sandbox template signing flow.")
    parser.add_argument("--api-key", default=os.getenv("PANDADOC_API_KEY"))
    parser.add_argument("--base-url", default=os.getenv("PANDADOC_BASE_URL", "https://api.pandadoc.com/public/v1"))
    parser.add_argument("--template-uuid", default=os.getenv("PANDADOC_TEMPLATE_UUID"))
    parser.add_argument("--name", default=os.getenv("PANDADOC_DOCUMENT_NAME", "Sandbox Signing Test"))
    parser.add_argument("--recipient-email", default=os.getenv("PANDADOC_RECIPIENT_EMAIL"))
    parser.add_argument("--recipient-first-name", default=os.getenv("PANDADOC_RECIPIENT_FIRST_NAME"))
    parser.add_argument("--recipient-last-name", default=os.getenv("PANDADOC_RECIPIENT_LAST_NAME"))
    parser.add_argument("--recipient-role", default=os.getenv("PANDADOC_RECIPIENT_ROLE"))
    parser.add_argument("--client-first-name", default=os.getenv("PANDADOC_CLIENT_FIRST_NAME"))
    parser.add_argument("--client-last-name", default=os.getenv("PANDADOC_CLIENT_LAST_NAME"))
    parser.add_argument("--poll-interval", type=float, default=float(os.getenv("PANDADOC_POLL_INTERVAL", "1")))
    parser.add_argument("--max-attempts", type=int, default=int(os.getenv("PANDADOC_MAX_ATTEMPTS", "30")))
    parser.add_argument("--session-payload", default=os.getenv("PANDADOC_SESSION_PAYLOAD"))
    args = parser.parse_args()

    required = {
        "api_key": args.api_key,
        "template_uuid": args.template_uuid,
        "recipient_email": args.recipient_email,
        "recipient_role": args.recipient_role,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise SystemExit(f"Missing required values: {', '.join(missing)}")

    create_body = create_create_body(args)
    create_response = request_json(args.base_url, args.api_key, "POST", "/documents", create_body)
    document_id = create_response.get("id") or create_response.get("document_id")
    if not document_id:
        raise RuntimeError("Create response did not include a document id.")

    wait_for_draft(args.base_url, args.api_key, document_id, args.poll_interval, args.max_attempts)

    request_json(
        args.base_url,
        args.api_key,
        "POST",
        f"/documents/{document_id}/send",
        {"silent": True},
    )

    session_body = json.loads(args.session_payload) if args.session_payload else {}
    session_body.setdefault("recipient", args.recipient_email)
    session_response = request_json(
        args.base_url,
        args.api_key,
        "POST",
        f"/documents/{document_id}/session",
        session_body,
    )

    output = {
        "document_id": document_id,
        "signing_url": read_session_url(session_response),
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
