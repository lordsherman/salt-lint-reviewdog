#!/usr/bin/env python3
import json
import re
import sys

def parse_salt_lint_output(output):
    pattern = r'\[(\d+)\] (.+?)\n(.*?):(\d+)'
    matches = re.finditer(pattern, output, re.MULTILINE)

    diagnostics = []
    for match in matches:
        diagnostic = {
            "source": "salt-lint",
            "severity": "ERROR",
            "message": f"{match.group(1)}: {match.group(2)}",
            "location": {
                "path": match.group(3),
                "range": {
                    "start": {"line": int(match.group(4)) - 1, "column": 0},
                    "end": {"line": int(match.group(4)) - 1, "column": 0},
                },
            },
        }
        diagnostics.append(diagnostic)

    return diagnostics

if __name__ == "__main__":
    input_text = sys.stdin.read()
    rdjson_output = parse_salt_lint_output(input_text)
    print(json.dumps(rdjson_output, indent=2))
