# Epa: Spirit of Oro-Ago — expanded specification

Slogan: Feel the Rhythm. Celebrate the Heritage.

## Implemented playable prototype
- Illustrated town square presented as a 2D activity hub, original SVG scenery.
- Basic player customization: name, symbolic avatar, and three shared clothing/square palette themes.
- Three fictional character story cards, three preparation quests, drum and dance timing challenges.
- Easy/Normal/Hard timing windows, visible beat indicators and feedback, large touch buttons, keyboard controls.
- Heritage Stars, five unique unity milestones, celebration unlock, replay and best scores.
- Guest local saves, export/import progress with validation, larger text, reduced-motion setting, help/tutorial.
- Service-worker caching for solo core assets after a successful initial visit. External fonts fall back offline.

These are prototype implementations, not a complete 3D adventure. The finale is an unlockable celebration summary, not a full group performance. The tutorial is instructional rather than a guided playable sequence. Character customization is symbolic and does not include a 3D character editor. No verified cultural history or vocabulary is included yet.

## Next: deepen solo play
Navigable market, workshops, gathering places; connected story quests; computer-controlled companions; clothing patterns, instrument decoration and earnable cosmetic inventory; badges/titles; sensitivity calibration and optional controller support; difficulty-specific rankings; practice sections; animated final performance; photo mode with name hiding; complete playable onboarding. Add subtitles to any future voiced content. Test contrast and non-color cues, phone layouts, offline reloads and save recovery.

## Then: connected community
Optional accounts, cloud saves and versioned recovery; authoritative private cooperative rooms with invitation expiry; preset chat, mute/block/report, parental controls; shared squares with explicit visit permissions; team rehearsals and tournaments separated by difficulty; reconnection and connection status. Scores and rewards must be server-validated before competitive rankings. No paid competitive advantages. All cosmetics earnable with transparent progression.

## Cultural content and languages
English first; Yoruba interface, pronunciation, and translations require fluent-speaker review. Cultural cards must distinguish fictional stories from verified history, vocabulary, and community testimony. Every cultural item needs source attribution, custodian consent where relevant, reviewer identity, locale, version, review notes and status: draft → in review → approved/rejected → archived. Publish verified claims only from approved versions. Sacred rites remain outside gameplay unless custodians expressly authorize inclusion. Do not imply regional Epa accounts are necessarily specific to Oro-Ago.

## Administration (future server implementation)
| Role | Scope |
| --- | --- |
| Owner | Role assignments, settings, release approvals, quest/cosmetic/event configuration, full audit access |
| Moderator | Reports, player protection actions and appeals; no cultural approval or role escalation |
| Event organizer | Event drafts, schedules, approved challenges and announcements; no personal account administration |
| Cultural reviewer | Review cultural content, sources, portrayal permissions and translation versions; no player moderation |

Server-enforced permissions and append-only audit events are required. Moderation actions, content approvals, role changes, announcements and economy changes must record actor, timestamp, action, target, previous/new version, and reason. Dashboards must not expose reports or player data through client-only authorization. No admin functionality exists in the present static prototype.

## Release acceptance
Core progression must be completable from a new guest save. Replaying cannot duplicate unity milestones. Touch and keyboard play must both work. Reload must preserve progress. Save import must reject invalid files without destroying current progress. Verified material must never bypass review. Multiplayer must not be advertised as available before real multi-client tests pass.

## Hosting
Requested destination: https://epafestival.africandroid.world
The private Sites deployment is separate. Custom domain DNS/server integration remains unconfigured. No ownership or DNS change is implied by this specification.
