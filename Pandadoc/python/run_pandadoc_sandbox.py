#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


def main() -> int:
    script_path = Path(__file__).with_name("pandadoc_sandbox_test.py")
    args = [sys.executable, str(script_path), *sys.argv[1:]]
    result = subprocess.run(args)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
