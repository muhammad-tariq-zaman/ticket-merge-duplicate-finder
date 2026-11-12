"""Find helpdesk tickets that are probably duplicates of each other.

Usage: python3 main.py tickets.csv
CSV columns: ticket,subject,requester,created (ISO date).
Subjects are normalised before comparing: lowercased, leading
"re:" / "fwd:" removed, punctuation stripped, whitespace
collapsed. Two tickets from the SAME requester with the same
normalised subject are a likely duplicate group. Different
requesters with the same subject are NOT merged — they may be
the same outage reported by different people. Oldest ticket
first in each group.
"""
import argparse, csv, re, sys
from collections import defaultdict

def normalise_subject(subject):
    text = subject.strip().lower()
    while True:
        new = re.sub(r"^(re|fwd|fw):\s*", "", text)
        if new == text:
            break
        text = new
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def find_duplicates(rows):
    by_key = defaultdict(list)
    for row in rows:
        key = (normalise_subject(row["subject"]), row["requester"].strip().lower())
        by_key[key].append(row)
    out = []
    for (subject, requester), group in by_key.items():
        if len(group) > 1:
            tickets = sorted(group, key=lambda r: (r["created"].strip(), r["ticket"].strip()))
            out.append((subject, requester, [t["ticket"].strip() for t in tickets]))
    return sorted(out, key=lambda g: g[2][0])

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        groups = find_duplicates(list(csv.DictReader(f)))
    for subject, requester, tickets in groups:
        print(f"{requester}: DUPLICATE ({len(tickets)} tickets: {', '.join(tickets)}) — \"{subject}\"")
    if not groups:
        print("No duplicate tickets found.")
    else:
        print(f"{len(groups)} duplicate group(s) found.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
