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

### Reload readiness diagnostics
Nginx reload acknowledgement can precede activation of new workers. The installer now retries named-route checks up to 20 times and still requires exact release headers and asset hashes. It verifies that the dedicated vhost is loaded by the active Nginx include configuration. On failure, `health.last_failure` records the HTTP status, redirect location, release header and expected/received hashes without logging page contents. A persistent mismatch still triggers rollback.

### Explicit address listeners
Olamidepanel may bind existing sites separately to loopback, public IPv4, Docker bridge addresses, and IPv6. A wildcard-only Epa vhost cannot participate in an address-specific hostname group. The installer now discovers existing literal port-80/443 listener groups from active HTTP vhosts and joins them for Epa, without inheriting another site's default_server, bind, or socket options. It does not edit the other vhosts. The report records `joined_listener_groups` for verification. Certificate requirements still apply: adding listeners does not issue an HTTPS certificate.

## One-command HTTP + HTTPS repair

A phone can open HTTPS even after a successful HTTP-only deployment. Without an Epa TLS vhost, another site's port-443 fallback may appear. Use the repair entry point:

```bash
git -C /opt/epa-festival-deployer pull --ff-only
bash /opt/epa-festival-deployer/scripts/repair-olamidepanel.sh
```

This runs `deploy/repair-olamidepanel.yml`: refresh the public game and existing listener-group fixes, validate public A/AAAA addresses against local/panel addresses, test a dedicated ACME challenge file, obtain or renew a Let's Encrypt certificate using Certbot webroot mode, install a renewal hook, enable the existing Certbot timer, activate the certificate-backed game vhost, redirect HTTP to Epa HTTPS, and verify all nine public HTTPS game assets against release hashes. Other sites' certificates and routing files are not changed by Certbot because the Nginx plugin is not used.

The challenge document root is `/var/www/epa-festival-acme`; it is deliberately separate from the immutable game release and is used across renewals. The hook is `/etc/letsencrypt/renewal-hooks/deploy/epa-festival-reload`. HTTPS results are saved in `/var/lib/epa-festival/https-report.json`; ordinary activation/rollback results remain in `/var/lib/epa-festival/report.json`.

By running the repair you request certificate issuance and the script accepts the certificate authority's terms through Certbot. It uses `epa_acme_email` when supplied, otherwise the panel's configured ACME email. If neither exists it registers without an email; set `-e epa_acme_email=YOUR_EMAIL` to provide a real monitored address. No email address is guessed.

The script cannot change registrar DNS, an upstream firewall or cached data in a visitor's browser. It rejects wrong public DNS, unreachable ACME validation, invalid certificates, wrong HTTPS hostnames and mismatched public game files rather than reporting success. A failed certificate step leaves the successfully deployed HTTP game in place. Existing activation snapshots and rollback still apply to the later TLS route activation. Certificate/account issuance itself is not rolled back. Public verification is performed from the server, so a separate device remains the final external check.

After a successful HTTPS result, open exactly `https://epafestival.africandroid.world/`. If the phone retains Sprintforge from the previous fallback, close its old tab and reopen the address in a new private tab to test without that tab's cached page.

### Mobile app, legal pages and store update
The current release includes `/install.html`, install logic, 192/512 app icons and an Apple home-screen icon, plus `/terms.html`, `/privacy.html`, and `/copyright.html`. The copyright notice names Olamide Olatayo Bello. Exact-content verification now covers these files as well as the game artwork and code.

`repair-olamidepanel.sh` detects the existing African Apps Store service after the game passes HTTPS verification. On the same host it pulls the store tools into `/opt/epa-festival-store/source`, backs up the existing store database/frontend and adds only the Epa PWA listing through `tools/install_epa.py --discover`. It does not overwrite unrelated store accounts, APKs or listings. The explicit Epa publication step makes Epa visible; other listings’ administrator visibility choices are preserved. Skip this integration with `-e epa_update_store=false`. If the store runs elsewhere, deploy its integration on that server instead. A GitHub source update alone does not alter either running service.

### Repair only the store listing
If the game/HTTPS deployment passed but the catalog visibility check failed, run `git -C /opt/epa-festival-store/source pull --ff-only`, then `python3 /opt/epa-festival-store/source/tools/install_epa.py --discover --publish --verify-public`. The installer reads the running service’s effective STORE_DATA/PORT environment, including EnvironmentFile values, verifies its local catalog, and then checks a fresh public API response. It backs up the chosen database and affects only the Epa row.

## Separate store server (current deployment topology)
The game and African Apps Store are hosted on different servers. Store synchronization from the game playbook is now disabled by default (`epa_update_store=false`). Keep game updates on the game server. Run this separate command on the **Apps Store server**:

```bash
apt-get update
apt-get install -y git ansible python3
ansible-pull -U https://github.com/olamidebello/africanappsstore.git -C main -d /opt/epa-festival-store/source -i localhost, -c local ansible/deploy-epa.yml
```

That playbook discovers the existing running `africanappsstore.service`, backs up its real database/frontend, publishes only Epa's catalog row, and verifies both the local service and the public store API. It does not require Olamidepanel, a game checkout, or game assets on the store server. It retains store accounts, other listings, existing ports and TLS configuration. Use sudo if you are not root. Existing manually customized Git checkouts may require resolving local edits before pulling.
