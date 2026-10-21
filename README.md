# Sayed Dossier Repo

Working repository for the sourced dossier on Abdul El-Sayed (Democratic nominee, Michigan U.S. Senate seat, general election November 3, 2026). Public records and published reporting only.

## Layout
- docs/links.md : links to the live dossier, voter guide and money map
- findings/ : one file per finding set, each claim with a source and a rating
- records/ : records requests tracker and open leads
- browser/tasks.md : lookups that need a real browser (state registry, FEC, Senate disclosures)
- sources/log.md : every source used, with date accessed and reliability notes
- books/ and transcripts/ : local source material, NOT committed (see .gitignore)
- scratch/ : temporary files, NOT committed

## Rating labels (use these and no others)
- Documented : primary source (filing, audit, court record, video with confirmed transcript)
- Reported : a single credible outlet, not independently re-verified
- Disputed : sources conflict
- Not supported : claimed but unproven on the current record

## Working with Claude
1. Keep the Mac awake, Chrome open, and the Claude extension signed in to the same Claude account and organization as the chat.
2. Open the chat in the Claude desktop app on the Mac and send a message so the session links to the computer.
3. Ask Claude to work through browser/tasks.md. It reads pages and records results in findings/ and sources/log.md.
4. Review changes with git diff before committing.
