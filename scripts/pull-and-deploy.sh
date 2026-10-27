#!/usr/bin/env bash
# Run from any working directory; the repair workflow owns locking and Git updates.
set -euo pipefail
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
exec bash "$script_dir/repair-olamidepanel.sh" "$@"
