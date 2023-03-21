#!/usr/bin/env python3
import json
import re
import sys

def parse_salt_lint_output(output):
    pattern = r'\[(\d+)\] (.+?)\n(.*?):(\d+)'
    matches = re.finditer(pattern, output, re.MULTILINE)

    diagnostics = {
        "source": {
            "name": "salt-lint",
            "url": "https://example.com/url/to/salt-lint"
        },
        "severity": "ERROR",
        "diagnostics": []
    }

    for match in matches:
        rule_number = match.group(1)
        rule_message = match.group(2)
        file_path = match.group(3)
        line_number = int(match.group(4)) - 1

        if rule_number.startswith('2'):
            rule_url = f"https://salt-lint.readthedocs.io/en/latest/rules/formatting/#{rule_number}"
        elif rule_number.startswith('8'):
            rule_url = f"https://salt-lint.readthedocs.io/en/latest/rules/recommendations/#{rule_number}"
        elif rule_number.startswith('9'):
            rule_url = f"https://salt-lint.readthedocs.io/en/latest/rules/deprecations/#{rule_number}"
        else:
            rule_url = "https://salt-lint.readthedocs.io/en/latest/rules/"

        diagnostic = {
            "message": f"{rule_number}: {rule_message}",
            "location": {
                "path": file_path,
                "range": {
                    "start": {
                        "line": line_number,
                        "column": 0
                    },
                    "end": {
                        "line": line_number,
                        "column": 0
                    }
                }
            },
            "severity": "ERROR",
            "code": {
                "value": rule_number,
                "url": rule_url
            }
        }

        diagnostics["diagnostics"].append(diagnostic)

    return diagnostics

if __name__ == "__main__":
    input_text = sys.stdin.read()
    rdjson_output = parse_salt_lint_output(input_text)
    for diagnostic in rdjson_output:
        print(json.dumps(diagnostic))
