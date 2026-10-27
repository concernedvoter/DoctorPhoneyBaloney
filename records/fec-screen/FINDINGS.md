---
title: FEC foreign-address and pass-through screen, run October 27, 2026
purpose: What the tools/fec_screen.py run found and what it could not see. Read before citing any foreign-money statement.
---
# FEC screen: findings and limits

Run 2026-10-27 09:37 by the user from his own Terminal, FEC API Schedule A, two-year period 2026, five committees. Rows are in this folder; names of private individuals stay in the CSV files and out of deliverables.

## What was screened

1. Foreign-address receipts (FEC state code ZZ) for each committee.
2. All non-individual contributors for each committee (pass-through map).

## Results inside the data that loaded

| Committee | Foreign-address rows | Organization rows | Notes |
|---|---|---|---|
| Abdul for U.S. Senate (C00902668) | 4, net $550 | 29,780, $8.89 million | See below |
| Fighting for Michigan (C00919373) | 0 | 73, $582,250 | ActBlue $532,250 in 72 rows; Kazi Management St Croix LLC $50,000 |
| Unity and Justice Fund (C00881011) | 0 | 1, $1,827 | Incomplete, see limits |
| American Priorities (C00932723) | 0 | 2, $99,872 | Incomplete, see limits |
| Fig and Olive Action PAC (C00932715) | 0 | 0 | |

Campaign foreign-address rows, all four:
- One donor with a Puerto Rico address ($250, July 15, 2026). Puerto Rico is a U.S. territory; the FEC coded the address ZZ. Not foreign money.
- One donor with an address in Italy: $500 on June 22, returned June 30 as a returned item, and $300 on July 1. Both receipts carry the memo that U.S. citizenship was confirmed. Net $300. A U.S. citizen living abroad may give. Not foreign money on this record.

Campaign organization rows: 29,670 are ActBlue conduit entries ($8.70 million, each memo says earmarked through the organization). The rest are U.S. committees and companies in U.S. states or D.C. (for example Emgage Federal PAC $34,500, A New Policy PAC $30,175, UAW V-CAP $5,000, MCARE Federal $5,000, ACMER MERIT PAC $1,500, Fig and Olive Action PAC $920.23, which matches the dossier). No organization had a foreign address. Twenty-one rows are from the candidate's own name, memo "health insurance premium" or reimbursement, $24,236.95; they are not outside money and are not examined here.

Fighting for Michigan lead: Kazi Management St Croix LLC, Frederiksted, U.S. Virgin Islands, $50,000 on June 30, 2026 (no memo). The Virgin Islands are a U.S. territory, so this is not a foreign address. Who owns the LLC is not shown; no public source was found. Rating: Documented as a gift; ownership unknown; not a foreign-money finding.

## Limits (these matter more than the zeros)

- The API had not yet loaded his newest filings. Every campaign row traces to the August 11, 2026 amended filings and ends July 15, 2026. The July 16 to September 30 quarter ($30.7 million) and the October pre-general report are not in this run.
- The super PAC data are incomplete. Known large gifts are missing: for Fighting for Michigan, the Institute for Middle East Understanding ($400,000), Medicare for All PAC, UAW V-CAP, and individual donors; for the Unity and Justice Fund, CAIR Action and the $100,000 gifts; for American Priorities, Fig and Olive Action Inc ($370,000). Their reports were amended or filed in October.
- The ZZ test finds only donors whose address is outside the U.S. A foreign national with a U.S. address, or a straw donor, would not show up. The FEC does not record citizenship.
- Result: nothing in the loaded data shows foreign money. That cannot be extended to the missing filings.

## Next

Re-run `tools/fec_screen.py` in a few days, once the FEC loads the October filings. Also pull Schedule A for the joint fundraising account (ID needed).

Rating: foreign money in the covered window Not supported. Overall claim of foreign-funded campaign: Not supported.
