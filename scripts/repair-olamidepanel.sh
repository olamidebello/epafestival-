#!/usr/bin/env bash
set -euo pipefail
if [[ ${EUID} -ne 0 ]]; then
  exec sudo bash "$0" "$@"
fi
exec 9>/run/epa-festival-deployer.lock
flock -n 9 || { echo 'An Epa deployment is already running.' >&2; exit 1; }
for path in /opt/olamidepanel/panel/database.py /opt/olamidepanel/venv/bin/python /etc/olamidepanel/database.json; do
  [[ -f "$path" ]] || { echo "Missing Olamidepanel path: $path" >&2; exit 1; }
done
apt-get update
apt-get install -y git ansible ca-certificates
checkout=/opt/epa-festival-deployer
if [[ -d "$checkout/.git" ]]; then
  [[ "$(git -C "$checkout" remote get-url origin)" == 'https://github.com/olamidebello/epafestival-.git' ]] || { echo 'Unexpected deployment checkout origin.' >&2; exit 1; }
  git -C "$checkout" pull --ff-only
else
  git clone https://github.com/olamidebello/epafestival-.git "$checkout"
fi
ansible-playbook -i "$checkout/deploy/inventory.ini" "$checkout/deploy/repair-olamidepanel.yml" "$@"
