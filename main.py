"""An AI agent's first payday, told in exactly six words.

The sentence is fixed. Before it is written out, a list of
small named checks audits it from several angles: is there
anything there, does it fit the limit, is it free of control
characters, is it really six words, are its edges tidy, does
it end like a sentence, and does it carry letters rather than
marks or digits alone. The first check that objects prints
its reason to stderr and exits with code 1, so nothing bad
is ever saved. No input, no network, no randomness, no clock:
the same sentence goes out on every run, byte for byte.
"""

import sys
from pathlib import Path

ENTRY = "First paycheck: spent it on context."
LIMIT = 60
DEST = Path("/output/entry.txt")
END_MARKS = ".!?"


def fail(reason):
    print(f"invalid: {reason}", file=sys.stderr)
    raise SystemExit(1)


def check_something_there(text):
    if not text or text.strip() == "":
        fail("entry is empty")


def check_fits(text):
    if len(text) > LIMIT:
        fail("entry is longer than 60 characters")


def check_no_control_chars(text):
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        fail("entry contains control characters")


def check_six_words(text):
    # The whole point is the count: six words, no more, no fewer.
    if len(text.split()) != 6:
        fail("entry must be exactly six words")


def check_tidy_edges(text):
    # No leading or trailing space, no doubled space, no newlines.
    if text != text.strip() or "  " in text or "\n" in text or "\r" in text:
        fail("entry has ragged edges or line breaks")


def check_ends_like_a_sentence(text):
    if not text or text[-1] not in END_MARKS:
        fail("entry must end with . ! or ?")


def check_not_only_marks(text):
    if not any(ch.isalnum() for ch in text):
        fail("entry is punctuation only")


def check_not_only_digits(text):
    if text.isdigit():
        fail("entry is digits only")


def check_carries_letters(text):
    if not any(ch.isalpha() for ch in text):
        fail("entry has no letters")


def check_no_digits(text):
    # A six-word story should be told in words, not numbers.
    if any(ch.isdigit() for ch in text):
        fail("entry must not contain digits")


def check_no_links(text):
    # A payday story should not smuggle in a web address.
    if "http" in text or "www." in text:
        fail("entry must not contain a link")


CHECKS = (
    check_something_there,
    check_fits,
    check_no_control_chars,
    check_six_words,
    check_tidy_edges,
    check_ends_like_a_sentence,
    check_not_only_marks,
    check_not_only_digits,
    check_carries_letters,
    check_no_digits,
    check_no_links,
)


def validate(text):
    for check in CHECKS:
        check(text)


def main():
    validate(ENTRY)
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(ENTRY + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
