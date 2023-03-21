FROM python:3.9-slim

# Install salt-lint and reviewdog
RUN pip install salt-lint && \
    apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    curl -sfL https://raw.githubusercontent.com/reviewdog/reviewdog/master/install.sh | sh -s -- -b /usr/local/bin/

# Add salt_lint_to_rdjson.py script
COPY salt_lint_to_rdjson.py /usr/local/bin/salt_lint_to_rdjson.py
RUN chmod +x /usr/local/bin/salt_lint_to_rdjson.py

ENTRYPOINT ["/bin/bash", "-c", "find . -type f -name '*.sls' -exec salt-lint {} \\; | /usr/local/bin/salt_lint_to_rdjson.py | reviewdog -f=rdjson -reporter=github-pr-review -diff='git diff' -level=error -tee"]
