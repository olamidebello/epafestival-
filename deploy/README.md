# Server deployment

Debian 12 / Ubuntu server with root or sudo access. This static game needs Nginx and Git; no database, Node service or build step is required.

## Run directly on the server

```bash
sudo apt-get update
sudo apt-get install -y git ansible
sudo git clone https://github.com/olamidebello/epafestival-.git /opt/epa-festival-deployer
cd /opt/epa-festival-deployer
sudo ansible-playbook -i deploy/inventory.ini deploy/deploy.yml
```

For later updates:

```bash
cd /opt/epa-festival-deployer
sudo git pull --ff-only
sudo ansible-playbook -i deploy/inventory.ini deploy/deploy.yml
```

To deploy a specific commit, add `-e epa_ref=FULL_COMMIT_SHA`. To deploy over SSH, replace the inventory's localhost line with your server host and run from your control machine. Use existing SSH keys and `--ask-become-pass` if sudo requires a password. No credentials are stored in this repository.

## Domain, Olamidepanel and HTTPS

Point epafestival.africandroid.world DNS to the server. The playbook adds only `/etc/nginx/conf.d/epa-festival.conf`; it does not remove default sites or alter other websites. It stops if the domain already appears in a different Nginx configuration. On a panel-managed server, resolve domain ownership/routing with the panel before running: do not create a second conflicting vhost. This playbook assumes standard Debian/Ubuntu Nginx includes conf.d; its exact-release health check fails and restores the previous configuration if routing does not reach this host. Apache, panel reverse proxies, firewall ports and custom Nginx include layouts need operator configuration.

Initial deployment serves HTTP. For HTTPS, provision a trusted certificate using your existing panel or certificate tool, then run:

```bash
sudo ansible-playbook -i deploy/inventory.ini deploy/deploy.yml -e epa_tls=true
```

The default certificate paths are `/etc/letsencrypt/live/epafestival.africandroid.world/fullchain.pem` and `privkey.pem`; override `epa_certificate` and `epa_certificate_key` if needed. This enables TLS alongside HTTP. Configure HTTPS redirection at your panel or edge proxy if required. Browser offline caching requires HTTPS or localhost. The playbook does not change DNS, issue certificates, open firewall ports, or verify external HTTPS.

## Release safety

The server pulls main by default, stages `dist/` in a commit-specific release directory, validates Nginx, atomically switches the current symlink and verifies actual game content plus its commit header through a local request using the domain Host header. Activation/health failures restore the prior symlink and managed vhost. Failed source pulls leave the active release alone. Existing releases remain available; no automatic deletion is performed. System package installation is not rolled back.

Syntax check: `ansible-playbook -i deploy/inventory.ini deploy/deploy.yml --syntax-check`. Run deployment during a suitable maintenance window. No live server deployment is performed merely by adding these files.
