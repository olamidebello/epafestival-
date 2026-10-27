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

## Local creative expansion (implemented)
The 2D canvas square now supports keyboard/touch walking and running, greetings/clapping, moving fictional residents, a crowd scaled to core quest progress, day/night cycle selection, clouds/rain, lantern palettes and reduced decorative motion. Players choose skin/hair/clothing colors, five hairstyles, three body silhouettes, invented patterns/accessories, five activity labels and up to five saved outfits. Roles are cosmetic labels, not separate skill trees.

The square designer places, moves and removes four object types, with up to five device-saved layouts. The workshop provides a three-track/eight-step rhythm composer with tempo and three earnable synthesized sound sets. The dance studio saves up to eight movements and replays a simple 2D rehearsal. Neighbor conversations offer two responses and a one-time friendship reward; they do not constitute a complete branching narrative.

Play settings include movement-key remapping, challenge speed, timing offset/calibration, volume, battery mode, weather, effects and name hiding in downloadable canvas photographs. Rhythm challenges include an Expert timing window, combo feedback and device best scores separated by difficulty (these are local records, not trustworthy competitive rankings).

Brand assets include a generated drum/sun/community emblem and two original illustrated key artworks. The 3D-style key art is illustrative; the playable world is 2D. Advanced fields are included in backup/recovery, and core creative assets are cached by the service worker after first online use. Offline behavior, controllers and all devices still require broader acceptance testing.

## Expanded specification still to implement
True connected story branches and responsibilities; full 3D character animation and cloth physics; drum strike animation matched to individual player hits; natural motion blending and cinematic camera paths; adjustable camera and group photography; full performance recording with input replay; duet scoring and real synchronized teams; rotating event service/community goals; separate casual/competitive server rankings; challenge publishing and moderated creation gallery; subtitles/narration for reviewed content; full controller support; optional accounts/cloud-save recovery.

Owner/moderator/event-organizer/cultural-reviewer dashboards must cover players, permissions, quests, events, translations, cultural review, shared creations, moderation reports, announcements, backups and audit history. Every online score and reward must be validated server-side. There is no live admin dashboard, multiplayer lobby, cloud save or reviewed Yoruba language pack in this static release.
