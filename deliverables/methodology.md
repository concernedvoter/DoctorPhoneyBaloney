---
title: "Candidate Research Methodology"
type: deliverable
exported: 2026-10-23 (doc rev 13, as of 2026-10-22)
---
# Candidate Research Methodology

As of 2026-10-22

A repeatable method for researching a political candidate from the public record: every claim sourced, rated and held to the same standard for every candidate.

## Principles

Every finding follows seven rules, applied the same way to every candidate.

1. **Source every claim.** No fact enters a published document without a source a reader can check.
2. **Rate every claim.** Each fact carries one of four ratings (next section), so the reader sees its strength.
3. **Prefer the primary record.** Court filings, votes, the candidate's own words and video outrank news coverage, and coverage outranks commentary.
4. **Read the source in full before relying on it.** A headline, search snippet or someone else's summary is a lead, not a source.
5. **Judge people by their own acts.** A relative's or associate's history is context, never a finding about the candidate.
6. **Use exact language.** Say what the record shows ("floated amending," "conflicts with the record"), not a stronger word it does not prove ("wants to abolish," "lied").
7. **One standard for all.** Any rule that lowers a rating for one candidate lowers it for the other.

## Evidence ratings

Every claim gets exactly one rating; a chain of claims gets one per link.

| Rating | Meaning | Example |
|---|---|---|
| Documented | Seen in a primary source: court record, roll call, official filing, the candidate's own site, signed op-ed, video or transcript | A signature confirmed on a published letter; a debate quote in the transcript |
| Reported | One outlet, a secondhand account, an inference, or background knowledge not re-verified | A quote from a deleted video carried by one publication |
| Disputed | Credible sources or the parties contest it, or a court has criticized the finding | A judge's finding that an appeals court later said went too far |
| Not supported | Searched for and not found, or contradicted by the record | A claim that a lawsuit got someone removed from a list when the docket shows the suit was lost |

Upgrade a rating only when the primary source is in hand and read. Downgrade it as soon as a better source contradicts it.

## Workflow

Work moves from a question to a rated, sourced finding in eight steps.

1. **Frame the question.** Write it as a testable claim, such as "Candidate X has ties to group Y."
2. **Gather leads.** Search news, fact-checks, opposition research, the candidate's own site and social media. Treat everything found here as a lead.
3. **Trace each lead to its primary source.** Find the docket, roll call, filing, video or original post the coverage relies on.
4. **Save the source.** Download PDFs and save web pages into a source folder, named so they can be found again. Note the URL and date retrieved.
5. **Read it in full.** Extract the text, search for every name involved, and read the passages in context. Confirm who said what, when, and on what page.
6. **Rate and write.** Write the finding in exact language with its rating and citation. Note what the source does not say.
7. **Check against the other side.** Find the candidate's response and the strongest counterargument, and include both.
8. **Log and review.** Record the source, finding and rating in the log; list unresolved items as open leads; re-check ratings when new sources arrive.

## Sources

Use the highest tier available, and label advocacy sources as such even when they reproduce real documents.

| Tier | Examples | Use |
|---|---|---|
| 1. Primary record | Court opinions, dockets and exhibits; roll call votes; FEC filings; candidate websites, op-eds, videos, debate transcripts; official Church texts | Can support Documented |
| 2. Established reporting | Wire services, major newspapers, public radio, nonpartisan fact-checkers | Reported until the primary record is found |
| 3. Advocacy and partisan | Campaigns, party committees, think tanks and interest groups on either side | Leads only; cite the documents they reproduce, not their conclusions |
| Excluded | Wikipedia, anonymous posts, AI summaries | Never cited |

**Where to find primary records**

- **Federal court records:** CourtListener (free RECAP archive) and PACER (paid, per page). Search by case name and docket number, then by document number.
- **Trial exhibits:** often filed on the docket or reproduced by groups that followed the case; match the exhibit number before relying on a copy.
- **Published opinions:** the court's own website (for example, the Fifth Circuit's opinion archive).
- **Votes and bills:** congress.gov and clerk.house.gov roll calls.
- **Campaign money:** fec.gov.
- **Deleted pages and videos:** the Internet Archive's Wayback Machine.
- **Church teaching:** vatican.va (Catechism, encyclicals), usccb.org (Faithful Citizenship, pastoral messages), state Catholic conferences.

## Video transcripts

Videos of debates, town halls and social media clips are transcribed locally so quotes can be checked word for word and cited by timestamp.

1. **Capture the source link.** Copy the original URL (YouTube, Instagram, X) of the full video, not a reposted clip, when one exists.
2. **Run the transcription script.** A local script (transcribe.py) downloads the audio, runs automatic speech recognition and labels speakers. The audio is downloaded with yt-dlp, the open-source Python video downloader (pip install yt-dlp), which also handles Instagram and X links. Speech recognition uses openai/whisper-large-v3 and speaker labeling uses pyannote/speaker-diarization-3.1, both open models from Hugging Face; the pyannote model requires a free Hugging Face account, accepting its terms, and an access token.
3. **Save one text file per video,** named by the video's ID (for example, transcripts/Cs6PQe8LqHo.txt), with the source URL on the first line.
4. **Keep the format:** one line per utterance, `[HH:MM:SS] SPEAKER_00: words`, so any quote can be found at its timestamp.
5. **Name the speakers by hand.** The labels (SPEAKER_00, SPEAKER_01) are guesses by the software; confirm who is speaking by watching, and note that speakers were inferred.
6. **Check every quote against the audio.** Speech recognition mishears names and terms; in this project "Muslim Brotherhood" came out as "muscle movement" and "Muslim neighborhood." Listen at the timestamp before quoting, and correct the quote, not the saved file.
7. **Rate transcript quotes by their source.** A candidate's own video, transcribed and checked against the audio, can be Documented; a clip of unknown origin or an unchecked auto-caption is Reported.
8. **Use professional transcripts where they exist,** such as Rev for televised forums, and compare them with the local transcript; note any differences in date or wording.

## Association chains

A claim that a candidate is "tied" to a group is broken into links, and each link is rated on its own.

1. **Map the path.** List every step from the candidate to the group: person to relative, relative to organization, organization to the group. Count the steps.
2. **Rate each link separately.** A path of five Documented links and one Disputed link is not a Documented path.
3. **Apply the weakest-link rule.** The whole chain is only as strong as its weakest link. Name that link and explain it plainly.
4. **Separate contact from membership.** A step is a contact or relationship. Membership, control or agreement needs its own evidence.
5. **Check what courts actually held.** Distinguish a charge, a finding, a judge's remark, an appeals court's correction and an unindicted co-conspirator listing; they carry very different weight.
6. **Read exhibits, not descriptions of them.** When a filing describes an exhibit, find the exhibit. Wording can change meaning (for example, an organization listed beside the word "Coordination" is not the same as a member).

**Family and associates.** Relatives' histories are reported as context only, never as findings about the candidate. Use neutral words, name a private relative only when the relative is already part of the public record, and state when no wrongdoing is alleged.

## Faith alignment scoring

Candidates are compared with Church teaching issue by issue, then placed on a two-axis compass. The method uses Catholic teaching here but works for any tradition with written teaching.

1. **Build the issue list from the Church's own documents.** For Catholics: Faithful Citizenship and its Introductory Note, the Catechism, and papal teaching.
2. **Sort issues by weight.** Separate intrinsic evils and grave matters (abortion, euthanasia, torture) from matters of prudential judgment (immigration policy, health care, war, guns, creation), where Catholics may disagree on means.
3. **Cite Scripture and the Catechism first, then pastoral statements.** Doctrine and Scripture set the principle; a bishops' message applies it and is weighed as prudential guidance.
4. **Rate each candidate on each issue:** Aligned, Partly aligned, In tension, or No clear position, with a one-line reason and the evidence rating.
5. **Place them on the compass.** Horizontal axis: life and family teaching. Vertical axis: social teaching. The horizontal axis carries more weight, as the bishops ask.
6. **Label it a judgment.** State that placement is the researcher's judgment from the rated record, not a Church verdict, and that the Church does not endorse candidates.

When a reader challenges a rating, check it against Scripture and the Catechism, not only recent statements, and change it if the stronger source supports the challenge.

## Fairness, corrections and record keeping

The method's credibility rests on correcting errors openly and keeping a trail anyone can follow.

- **Mirror test:** before publishing a rating, ask whether the same evidence would earn the same rating for the other candidate.
- **Include the response:** every finding against a candidate carries the candidate's own answer, or notes that none was given.
- **Show the counterargument:** persuasive material ends with the strongest points the other side would make.
- **Correct in place:** when a source shows an error, fix the text, adjust the rating, and log what changed and why. Do not quietly delete.
- **Source log:** one dated entry per source: file name, what it is, who published it, what it shows, what it does not show, and the rating.
- **Open leads list:** every unresolved question, with the specific document that would resolve it.
- **Folder layout:** keep primary records, saved web pages and transcripts in separate folders, and never edit an original file; work on copies.

## Tools and limitations

Free tools are enough to reproduce this work.

| Task | Tool |
|---|---|
| Extract text from PDFs | pdftotext (Poppler) |
| Read scanned exhibits | Tesseract OCR; view the page image to confirm |
| Search many documents for names | grep or any full-text search |
| Save web pages | Browser "Save page as," plus the Wayback Machine |
| Track sources and leads | A plain text log and leads list, ideally under version control |
| Graphics | Any design tool; encode ratings in both color and line style so they read in black and white |

**Limitations**

- Some primary records sit behind paywalls (PACER) or are sealed.
- Translations of foreign-language exhibits rely on the translator; get an independent translation for any word a finding turns on.
- OCR can misread names ("Gawad" for "Awad"); confirm every match by reading the line.
- Faith alignment placement is a judgment, and reasonable readers may weigh issues differently.
- Findings are as of the date above; candidates' positions change.
