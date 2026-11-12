import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import normalise_subject, find_duplicates

def row(t, subject, requester, created="2026-11-08"):
    return {"ticket": t, "subject": subject, "requester": requester, "created": created}

class TestTicketMergeDuplicates(unittest.TestCase):
    def test_duplicates_found(self):
        g = find_duplicates([row("T-1", "Wi-Fi down", "ali"), row("T-2", "Wi-Fi down", "ali")])
        self.assertEqual(g, [("wi fi down", "ali", ["T-1", "T-2"])])
    def test_case_insensitive(self):
        g = find_duplicates([row("T-1", "Wi-Fi DOWN", "ali"), row("T-2", "wi-fi down", "ali")])
        self.assertEqual(len(g), 1)
    def test_re_prefix_stripped(self):
        g = find_duplicates([row("T-1", "Wi-Fi down", "ali"), row("T-2", "Re: Wi-Fi down", "ali")])
        self.assertEqual(len(g), 1)
    def test_different_requesters_not_merged(self):
        g = find_duplicates([row("T-1", "Wi-Fi down", "ali"), row("T-2", "Wi-Fi down", "sara")])
        self.assertEqual(g, [])
    def test_different_subjects_not_merged(self):
        g = find_duplicates([row("T-1", "Wi-Fi down", "ali"), row("T-2", "Printer jammed", "ali")])
        self.assertEqual(g, [])
    def test_oldest_first(self):
        g = find_duplicates([row("T-9", "Wi-Fi down", "ali", "2026-11-08"),
                             row("T-1", "Wi-Fi down", "ali", "2026-11-07")])
        self.assertEqual(g[0][2], ["T-1", "T-9"])
    def test_empty_input(self):
        self.assertEqual(find_duplicates([]), [])
