#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path


API_KEY = "YOUR_PANDADOC_API_KEY"
BASE_URL = "https://api.pandadoc.com/public/v1"
TEMPLATE_UUID = "YOUR_TEMPLATE_UUID"


def main() -> int:
    script_path = Path(__file__).with_name("pandadoc_auth_check.py")

    env = os.environ.copy()
    env["PANDADOC_API_KEY"] = API_KEY
    env["PANDADOC_BASE_URL"] = BASE_URL
    env["PANDADOC_TEMPLATE_UUID"] = TEMPLATE_UUID

    result = subprocess.run([sys.executable, str(script_path)], env=env)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
