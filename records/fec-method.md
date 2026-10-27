---
title: FEC tracking method
purpose: How money figures in the El-Sayed and Rogers files are pulled, checked and rated. Read before changing deliverables/dossier-el-sayed/10-money-map.md.
---
# FEC tracking method

Last full refresh: October 26, 2026; rechecked October 27 (summaries unchanged; filing lists read; document pages timing out) (committee summaries through the pre-general reports, coverage to October 14).

## Committees tracked

| Committee | FEC ID | Role | Detail ends |
|---|---|---|---|
| Abdul for U.S. Senate | C00902668 | His principal campaign committee | Oct 14 |
| Fighting for Michigan PAC | C00919373 | Super PAC, independent expenditures for him | Aug 31 |
| Unity and Justice Fund | C00881011 | Super PAC, CAIR-endorsed | Aug 31 |
| American Priorities | C00932723 | Super PAC, formed Jan 2, 2026 | Sep 30 |
| Fig and Olive Action PAC | C00932715 | Related PAC; the $370,000 gift to American Priorities came from the corporation, not this PAC | Sep 30 |
| Emgage PAC | C00453704 | Checked in section 19 | see section 19 |
| Rogers for Senate | C00849810 | Rogers principal committee | latest report |
| Rogers for MI Senate Republican Nominee Fund 2026 | C00892026 | Rogers authorized committee | latest report |
| Rogers candidate page | S4MI00595 | Combined Rogers totals | Oct 22 |

Not yet pulled: the joint fundraising account that received the $1 million Ocasio-Cortez transfer (name and ID to be taken from his Form 3 or the Bridge article's source), Rogers's leadership PAC MR PAC (C00850610), and Great Lakes Conservatives Fund.

## Rules

1. Pull every committee type: candidate, authorized, joint fundraising, leadership PAC, super PAC. Record the committee ID, report, coverage end and date retrieved for each figure.
2. Prefer the committee's own FEC filing (docquery) for line items and the FEC summary page for totals. Third-party trackers and news are Reported until matched to a filing.
3. Independent expenditures are often listed twice, as support for one candidate and opposition to the other. Never add notices without removing the pairs. Large exports are capped at 500,000 rows, so split by period.
4. Compare candidates only on the same cutoff date, and say when cutoffs differ.
5. A flagged donation is a fact about money, not a finding about belief or intent. Flag a donor only for a documented reason (an organization with a court or agency record, an itemized filing, a named source). Never match on a name, ethnicity or faith. Rate each link; the weakest link governs.
6. No automated or AI-converted figure goes into a deliverable until a person has checked it against the original filing.

## Access notes

FEC committee and candidate summary pages and docquery committee filing lists can be read through the fetch tool; individual docquery filing pages sometimes return server errors or 504 timeouts (October 27), so retry later rather than looping. The FEC API and candidate search are blocked to it. The browser pane can read docquery filings. Summary pages can trail new filings by up to 48 hours.

## Filing calendar (confirm on the FEC calendar)

- Pre-general reports were due October 22, 2026 (coverage October 1 to 14).
- 24-hour independent expenditure reports apply in the last 20 days before November 3.
- Post-general report: due 30 days after the election.
- Monthly filers (Fighting for Michigan, Unity and Justice Fund) file on their own schedule.

## Open reconciliations

- Unity and Justice Fund: summary independent expenditures $241,605 against a reported $400,000 canvassing estimate (Sep 19, amended).
- Section 06 cites about $95 million of medical debt cleared; Bridge's June 25 figure is $57.4 million.
- Third-party tracker VoteLog (Oct 25) outside-spending totals do not reconcile internally; not used.
- Read the 48-hour notices (campaign F6 filings, Oct 17 to 25) and the F24 independent expenditure reports listed on Oct 27: campaign FEC-2029651 through FEC-2041631; Fighting for Michigan FEC-2041242, 2034972, 2028472, 2025041, 2018670, 2017736; American Priorities FEC-2034059, 2021062, 2018408; Unity and Justice Fund FEC-2035221, 2029916, 2028909, 2028905, 2018557 (amended), 2017579. Also the Unity and Justice Fund pre-general (FEC-2040102) and October monthly (FEC-2033512), and the campaign amendments filed Oct 15, Oct 22 and Aug 11 (reasons unknown).

## Foreign-money screen (run Oct 27, 2026)

`tools/fec_screen.py` (user runs it in his own Terminal with his own free API key) pulls ZZ-state rows and all organization rows into records/fec-screen/. First run: no foreign donor in the loaded data; the API lagged the newest filings. See records/fec-screen/FINDINGS.md. Re-run after the FEC loads the October reports. Do not publish private donors' names; keep them in the CSV.
