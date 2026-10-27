# Epa: Spirit of Oro-Ago

Feel the Rhythm. Celebrate the Heritage.

Playable browser prototype with original SVG village artwork, fictional story cards, drum and dance timing games with synthesized audio, preparation quests, palette customization, persistent device progress, Heritage Stars, and a unity-gated celebration.

Serve `dist/` with any static HTTP server. No build or dependencies required. Target custom domain: epafestival.africandroid.world (not configured by this source).

## Boundaries
This is a solo 2D prototype. Online multiplayer, a navigable 3D world, shared squares, and full group performances are future work. No accounts, purchases, or network score sharing. Browser storage holds progress. Reset clears local progress.

Characters, patterns, illustrations, and challenges are invented. Specific cultural claims, costumes, music, and masquerade portrayals require Oro-Ago custodian review. Sacred rites are excluded.

## Expanded first-release settings
Player name, symbolic avatars, palette themes, timing difficulty, larger text, reduced motion, help, and JSON save backup/recovery are available under Player & settings. The service worker caches core assets for later offline solo visits. See ROADMAP.md for the expanded specification and implementation boundaries.

## Local creative expansion
The living 2D square adds movement, day/night/weather, character styling and saved outfits, decoration placement and saved layouts, a layered rhythm composer, saved dance routines, fictional neighbor choices, badges, canvas photo export, key remapping and battery/audio/timing settings. Original generated brand assets are integrated; see BRANDING.md. Multiplayer, cloud services and administration remain unimplemented; ROADMAP.md records the boundary precisely.

## Olamidepanel deployment
Run `sudo bash scripts/deploy-olamidepanel.sh` from an updated checkout on the panel server. See [deployment paths and port handling](deploy/OLAMIDEPANEL.md). The dedicated playbook reuses existing domain certificates and coordinates with the panel publisher; it does not require a separate application port.

For automatic HTTP/HTTPS routing and certificate repair on the existing panel server, run `bash scripts/repair-olamidepanel.sh` as root. See [repair documentation](deploy/OLAMIDEPANEL.md#one-command-http--https-repair) for DNS requirements and diagnostic reports.

## Mobile installation and legal pages
The installable mobile web app supports compatible Android browsers, Safari home-screen installation on iPhone/iPad, and desktop browser installation. This is a PWA, not a native APK or App Store release. The live server install page is `https://epafestival.africandroid.world/install.html`; HTTPS must be configured first. The game footer links to installation, Terms and Conditions, Privacy Policy, and Copyright. The copyright holder is Olamide Olatayo Bello.

The repair playbook updates Epa's African Apps Store listing automatically if `africanappsstore.service` exists on the same host. Existing accounts and other catalog entries are preserved. Run it on the store host separately if the store is hosted elsewhere. The listing is an installable web app and provides no fabricated APK download.

## Ìgbómìnà (Oro-Ago) language workspace
The Language menu offers English and an Ìgbómìnà (Oro-Ago) option with an explicit English fallback while authentic local wording is pending. It exports a text template for community translation and accepts a local, text-only JSON pack with named, source-supplied review. No dialect wording is invented, standard Yoruba is not substituted, and file-declared review is not independently authenticated. Partial packs retain English for untranslated text; imported language files stay on the device. Reviewed cultural stories and pronunciation still require local speakers/custodians.

New guest sessions default to the Ìgbómìnà (Oro-Ago) language selection. Explicit language choices are preserved. Until a reviewed community pack supplies translations, English is visibly identified as the fallback.

## Pull and deploy on the server
From any directory on the existing Olamidepanel host:

```bash
git -C /opt/epa-festival-deployer pull --ff-only
bash /opt/epa-festival-deployer/scripts/pull-and-deploy.sh
```

The script delegates to the existing locked repair workflow: install required deployment tools, pull current source, stage public files, repair the Epa-only Nginx route, obtain/retain its HTTPS certificate, verify the game, and publish the Epa store listing if African Apps Store runs on the same host. Existing backups, rollback and diagnostics remain in effect. It does not invent missing Ìgbómìnà translations; the visible English fallback remains until reviewed local wording is supplied.

For direct Ansible use, run `ansible-playbook -i deploy/inventory.ini deploy/pull-and-deploy.yml` from the repository. The default inventory runs locally, so execute it on the actual server or supply your SSH inventory.
