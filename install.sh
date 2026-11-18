#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
command -v python >/dev/null || { echo "Install Python first: pkg install python"; exit 1; }
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
echo "Installed. Run: phone-agent init && phone-agent doctor"
