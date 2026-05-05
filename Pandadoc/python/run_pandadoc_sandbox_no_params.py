#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path


# Fill these in once, then run the file directly from VS Code.
API_KEY = "53f922dbe0eb82775d20b0e6d45a2cd381a586be"
TEMPLATE_UUID = "fMoPWRitapFTXB9qTW8cwH"
RECIPIENT_EMAIL = "Sudeer.joseph1@gmail.com"
RECIPIENT_ROLE = "Client"
CLIENT_FIRST_NAME = "Andre"
CLIENT_LAST_NAME = "Dharmalingam"
DOCUMENT_NAME = "Erasedebt POA"


def main() -> int:
    script_path = Path(__file__).with_name("pandadoc_sandbox_test.py")

    env = os.environ.copy()
    env["PANDADOC_API_KEY"] = API_KEY
    env["PANDADOC_TEMPLATE_UUID"] = TEMPLATE_UUID
    env["PANDADOC_RECIPIENT_EMAIL"] = RECIPIENT_EMAIL
    env["PANDADOC_RECIPIENT_ROLE"] = RECIPIENT_ROLE
    env["PANDADOC_CLIENT_FIRST_NAME"] = CLIENT_FIRST_NAME
    env["PANDADOC_CLIENT_LAST_NAME"] = CLIENT_LAST_NAME
    env["PANDADOC_DOCUMENT_NAME"] = DOCUMENT_NAME

    result = subprocess.run([sys.executable, str(script_path)], env=env)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
