"""
Single-byte XOR cipher

The hex encoded string:

1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

... has been XOR'd against a single character. Find the key, decrypt the
message.

You can do this by hand. But don't: write code to do it for you.

How? Devise some method for "scoring" a piece of English plaintext. Character
frequency is a good metric. Evaluate each output and choose the one with the
best score. 
"""

import base64
from collections import Counter
from typing import Dict


# Idea: English character frequencies are known values...
# We can create a scoring heuristic by comparing the character frequencies in
# some string to the known values. The closer they are overall, the better the
# score should be.
# Then we can compare scores across different decodings of the text.
# We can construct a set of all potential decoded strings by XORing the text
# against every single valid character and then score all such candidates.
# The best score is then likely to be the proper decoding.

CHARACTER_FREQUENCY_PCTS = {
    "A": 8.34,
    "B": 1.54,
    "C": 2.73,
    "D": 4.14,
    "E": 12.60,
    "F": 2.03,
    "G": 1.92,
    "H": 6.11,
    "I": 6.71,
    "J": 0.23,
    "K": 0.87,
    "L": 4.24,
    "M": 2.53,
    "N": 6.80,
    "O": 7.70,
    "P": 1.66,
    "Q": 0.09,
    "R": 5.68,
    "S": 6.11,
    "T": 9.37,
    "U": 2.85,
    "V": 1.06,
    "W": 2.34,
    "X": 0.20,
    "Y": 2.04,
    "Z": 0.06
};


def get_text_char_freqs(text: bytes) -> Dict[int, int]:
    # Remove non-alphabetic characters
    text = bytes(list(filter(lambda c: chr(c).isalpha(), text)))
    char_counter = Counter(text)
    num_chars = len(text)
    return {char: (count / num_chars) * 100 for (char, count) in char_counter.most_common()}

def score_text(text: str) -> int:
    """Lower score indidcates a better candidate."""
    text_char_freqs = get_text_char_freqs(text)

    score = 0
    for (char, freq) in text_char_freqs.items():
        score += abs(freq - CHARACTER_FREQUENCY_PCTS[chr(char).upper()])

    return score

def execute_freq_attack(text: bytes, print_all: bool = False) -> bytes:
    decoded_text = base64.b16decode(text, True)
    
    candidates = {}
    for i in range(128):
        candidate = bytes([byte ^ i for byte in decoded_text])
        candidates[score_text(candidate)] = candidate

    if print_all:
        for score in sorted(candidates.keys()):
            print(f"score: {score} candidate: {candidates[score]}")

    return candidates[min(candidates.keys())]
