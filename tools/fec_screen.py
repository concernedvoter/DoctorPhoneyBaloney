#!/usr/bin/env python3
"""FEC foreign-address and pass-through screen for the El-Sayed committees.

Run from the repo root in your own Terminal (not inside Claude):

    export FEC_API_KEY="your key"      # free at https://api.data.gov/signup/
    python3 tools/fec_screen.py

What it does (public data only, read-only):
  1. Foreign-address receipts: Schedule A rows whose contributor state is ZZ,
     the FEC code for a non-US address, for each committee below.
  2. Organization receipts: every non-individual contributor to each committee,
     so pass-through entities (nonprofits, LLCs, PACs) can be traced.
  3. A summary file with counts and dollar totals.

Output goes to records/fec-screen/ as CSV files. Nothing is written outside the
repo. A foreign address is a lead to verify, not a violation: US citizens abroad
and green card holders may give. Check every row against the filing image before
any use, and do not publish private individuals' names without a documented basis.
"""
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

API = "https://api.open.fec.gov/v1/schedules/schedule_a/"
OUT = os.path.join("records", "fec-screen")
CYCLES = [2026]  # two-year transaction period; covers 2025 and 2026 receipts

COMMITTEES = {
    "C00902668": "Abdul for U.S. Senate",
    "C00919373": "Fighting for Michigan PAC",
    "C00881011": "Unity and Justice Fund",
    "C00932723": "American Priorities",
    "C00932715": "Fig and Olive Action PAC",
}

FIELDS = [
    "committee_id", "committee_name", "contributor_name", "entity_type",
    "contributor_street_1", "contributor_city", "contributor_state",
    "contributor_zip", "contributor_employer", "contributor_occupation",
    "contribution_receipt_date", "contribution_receipt_amount", "memo_text",
    "report_year", "image_number", "pdf_url",
]


def get(params, key):
    q = dict(params)
    q["api_key"] = key
    url = API + "?" + urllib.parse.urlencode(q)
    for attempt in range(6):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 502, 503, 504):
                wait = 30 * (attempt + 1)
                print("  HTTP %d, waiting %ds" % (e.code, wait), file=sys.stderr)
                time.sleep(wait)
                continue
            raise
        except (urllib.error.URLError, TimeoutError):
            time.sleep(10 * (attempt + 1))
    raise SystemExit("Giving up after repeated errors: " + url.split("api_key")[0])


def pull(committee, cycle, extra, key, label):
    """Page through Schedule A for one committee with keyset pagination."""
    params = {
        "committee_id": committee,
        "two_year_transaction_period": cycle,
        "per_page": 100,
        "sort": "-contribution_receipt_date",
        "sort_hide_null": "false",
    }
    params.update(extra)
    rows, pages = [], 0
    while True:
        data = get(params, key)
        res = data.get("results", [])
        rows.extend(res)
        pages += 1
        last = (data.get("pagination") or {}).get("last_indexes")
        if not res or not last:
            break
        params["last_index"] = last["last_index"]
        if last.get("last_contribution_receipt_date"):
            params["last_contribution_receipt_date"] = last["last_contribution_receipt_date"]
        if pages % 20 == 0:
            print("  %s %s: %d rows so far" % (committee, label, len(rows)), file=sys.stderr)
        time.sleep(1.0)
    return rows


def flat(row, committee):
    out = {k: row.get(k, "") for k in FIELDS}
    out["committee_id"] = committee
    out["committee_name"] = COMMITTEES[committee]
    return out


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main():
    key = os.environ.get("FEC_API_KEY", "").strip()
    if not key or key == "DEMO_KEY":
        print("Set FEC_API_KEY to your own free key (https://api.data.gov/signup/). "
              "DEMO_KEY is too rate limited for this.", file=sys.stderr)
        raise SystemExit(1)
    if not os.path.isdir("records"):
        raise SystemExit("Run this from the repo root (the folder that contains records/).")
    os.makedirs(OUT, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    summary = ["FEC screen run %s" % stamp, ""]
    for cid, name in COMMITTEES.items():
        foreign, orgs = [], []
        for cyc in CYCLES:
            print("%s %s: foreign-address rows" % (cid, name), file=sys.stderr)
            foreign += pull(cid, cyc, {"contributor_state": "ZZ"}, key, "ZZ")
            print("%s %s: organization rows" % (cid, name), file=sys.stderr)
            orgs += pull(cid, cyc, {"is_individual": "false"}, key, "orgs")
        f_rows = [flat(r, cid) for r in foreign]
        o_rows = [flat(r, cid) for r in orgs]
        write_csv(os.path.join(OUT, "%s-foreign-address.csv" % cid), f_rows)
        write_csv(os.path.join(OUT, "%s-organizations.csv" % cid), o_rows)

        def total(rows):
            t = 0.0
            for r in rows:
                try:
                    t += float(r["contribution_receipt_amount"] or 0)
                except ValueError:
                    pass
            return t

        summary.append("%s %s" % (cid, name))
        summary.append("  foreign-address rows: %d, total $%.2f" % (len(f_rows), total(f_rows)))
        summary.append("  organization rows: %d, total $%.2f" % (len(o_rows), total(o_rows)))
        summary.append("")
    with open(os.path.join(OUT, "SUMMARY.txt"), "w", encoding="utf8") as f:
        f.write("\n".join(summary) + "\n")
    print("\n".join(summary))
    print("Wrote CSV files to %s. Tell Claude when it finishes." % OUT)


if __name__ == "__main__":
    main()
