# ticket-merge-duplicate-finder

Find helpdesk tickets that are probably duplicates from a CSV: subjects are normalised (case, Re:/Fwd: prefixes, punctuation) and tickets from the SAME requester with the same normalised subject form a duplicate group — oldest ticket first.

## How to run

```sh
python3 main.py tickets.csv
```

## Example output

```
ali: DUPLICATE (2 tickets: T-1, T-2) — "wi fi down"
1 duplicate group(s) found.
```

Standard library only. Run the tests with `python3 -m unittest discover`.
