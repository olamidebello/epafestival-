# Epa deployment on Olamidepanel

Run on the **existing Olamidepanel server** as root/sudo. This is a static browser game: Nginx serves `dist/` directly. There is no Node, Python web server, database for game accounts, Docker service or backend port to expose. The panel's existing Python environment is used only for its inventory adapter.

## Install/update

If already inside the Epa repository:

```bash
git pull --ff-only
sudo bash scripts/deploy-olamidepanel.sh
```

From a fresh server shell, bootstrap the deployment checkout idempotently:

```bash
sudo apt-get update
sudo apt-get install -y git
if [ -d /opt/epa-festival-deployer/.git ]; then
  sudo git -C /opt/epa-festival-deployer pull --ff-only
else
  sudo git clone https://github.com/olamidebello/epafestival-.git /opt/epa-festival-deployer
fi
sudo bash /opt/epa-festival-deployer/scripts/deploy-olamidepanel.sh
```

The wrapper installs Ansible, pulls latest source without discarding local changes, and runs the Olamidepanel playbook. Two concurrent wrapper runs are refused. To pin a revision, pass `-e epa_ref=FULL_COMMIT_SHA`. For a panel with multiple active root users, pass `-e epa_panel_owner=EXISTING_USERNAME`. Existing domain ownership is preserved. No passwords are printed or stored in the repository.

Direct Ansible command:

```bash
sudo ansible-playbook -i deploy/inventory.ini deploy/olamidepanel.yml
```

For SSH deployment replace localhost in `deploy/inventory.ini` with your existing SSH host/user. The current inventory deliberately targets the server on which you run the command; it does not guess an IP.

## Exact paths

| Item | Default path |
| --- | --- |
| Deployment checkout | `/opt/epa-festival-deployer` |
| Application source checkout | `/opt/epa-festival/source` |
| Source document directory | `/opt/epa-festival/source/dist` |
| Versioned public documents | `/opt/epa-festival/releases/<40-character-commit>` |
| Active Nginx document root | `/opt/epa-festival/current` (atomic release symlink) |
| Home page | `/opt/epa-festival/current/index.html` |
| Game code | `/opt/epa-festival/current/game.js`, `advanced.js` |
| Style, manifest, offline worker | `/opt/epa-festival/current/style.css`, `manifest.json`, `sw.js` |
| Logo and artworks | `/opt/epa-festival/current/assets/` |
| Dedicated domain vhost | `/etc/nginx/conf.d/epa-festival.conf` |
| Panel install | `/opt/olamidepanel` (`epa_panel_root` override) |
| Panel database configuration | `/etc/olamidepanel/database.json` (read locally; never copied to public root) |
| Panel app manifest | `/etc/olamidepanel/apps/epa-festival.json` |
| Existing publisher lock | `/var/lib/olamidepanel-provisioner/worker.lock` |
| Latest diagnostic report | `/var/lib/epa-festival/report.json` |
| Rollback snapshots | `/var/backups/epa-festival/<timestamp>/` |
| Existing certificate fallback | `/etc/letsencrypt/live/epafestival.africandroid.world/fullchain.pem` and `privkey.pem` |

Only public `dist/` assets enter the document root. No repository metadata, deployment scripts, panel credentials or backups are served.

## Ports and routing

| Endpoint | Port/handling |
| --- | --- |
| Public HTTP | TCP 80, exact `epafestival.africandroid.world` vhost |
| Public HTTPS | TCP 443 when an existing trusted certificate is available |
| Application/backend | None |
| Olamidepanel GUI/SSH/other apps | Existing listeners preserved |

The helper parses the active `nginx -T` inventory, identifies exact domain server blocks, and replaces only those blocks with one dedicated game route. Other domains in the same file remain intact. Duplicate exact-domain blocks are removed; duplicate symbolic aliases of the managed file are retired with rollback records. Shared multi-domain server blocks and nonstandard target ports require an explicit panel configuration change first and are refused. Wildcard/default sites are retained: the new exact domain wins ordinary Nginx hostname selection. All modified configuration files and previous roots are recorded.

Existing target certificate paths are reused. HTTPS is verified locally with the real hostname as SNI and full system certificate validation; certificates are not ignored. If TLS is present HTTP redirects to HTTPS, and the ACME challenge path remains reachable. If no certificate exists, HTTP deployment is allowed and reported clearly. Use `-e epa_require_tls=true` to require HTTPS and refuse deployment without a certificate. The playbook does not purchase domains, change DNS, issue certificates, change the panel GUI port, stop competing web servers, or broaden firewall rules.

## Panel coordination and rollback

Deployment holds the panel publisher lock and a database transaction. The target domain's current static-publisher request is backed up and changed to `external_backend` only after the game is healthy; this prevents the ordinary queued/waiting static publisher from replacing the game with its landing page. The existing owner is retained; a missing domain is registered to the chosen active panel account and audited. Future Epa updates should use this playbook, **not** requeue the panel's generic static-site publisher.

Every HTML, script, stylesheet, manifest, worker and artwork file is requested via the actual named Nginx route. Status, release header and SHA-256 content must match the staged source. Activation errors restore the old release, vhost content, relevant alias links and panel app manifest; the panel transaction rolls back. Old release directories remain available. Package installs are not rolled back. The report flags any rollback failure instead of claiming success.

## Diagnostics

```bash
sudo cat /var/lib/epa-festival/report.json
sudo nginx -t
sudo ss -ltnp
curl -I -H 'Host: epafestival.africandroid.world' http://127.0.0.1/index.html
curl -I https://epafestival.africandroid.world/
```

The report includes prior document roots, active release, changed configuration paths, listener inventory, TLS state, resolved DNS addresses and the backup location. A local success proves domain routing on that host, not external DNS/firewall reachability. DNS A/AAAA records, externally occupied ports and unrelated invalid global Nginx settings must be corrected at their actual source; the script reports them instead of stopping other sites or changing unrelated configuration. No claim is made that an untested live server has been repaired.

## Validation

```bash
ansible-playbook -i deploy/inventory.ini deploy/olamidepanel.yml --syntax-check
python3 -m unittest discover -s deploy/tests -v
```
