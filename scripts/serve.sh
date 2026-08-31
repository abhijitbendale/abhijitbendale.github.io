#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 generate_projects_data.py
cd ..
python3 -m http.server 8000
