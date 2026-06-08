# grammar.py — defines the grammar, parser, and tokenizer

import nltk
from nltk import CFG

# Final grammar (Stage 3)
GRAMMAR_STRING = """
S -> S_atau '.'

S_atau -> S_dan S_atau_A | S_dan
S_atau_A -> 'atau' S_dan S_atau_A | 'atau' S_dan

S_dan -> Clause S_dan_A | Clause
S_dan_A -> 'dan' Clause S_dan_A | 'dan' Clause

Clause -> NP VP

NP -> Pronoun | Noun | Pronoun Conj Pronoun | Noun Conj Noun

VP -> Verb | Verb NP | Particle VP

Pronoun -> 'saya' | 'dia' | 'mereka' | 'kami'
Noun -> 'buku' | 'nasi' | 'air' | 'guru' | 'murid' | 'kucing' | 'anjing'
Verb -> 'makan' | 'minum' | 'membaca' | 'menulis' | 'melihat'
Particle -> 'sudah' | 'sedang' | 'akan'
Conj -> 'dan' | 'atau'
"""

# Load grammar and initialize the chart parser
grammar = CFG.fromstring(GRAMMAR_STRING)
parser = nltk.ChartParser(grammar)


def tokenize(sentence: str):
    """
    Splits the sentence into a list of tokens.
    Lowercases the input and ensures '.' is treated as a separate token.
    Example: "saya makan nasi." -> ['saya', 'makan', 'nasi', '.']
    """
    sentence = sentence.strip().lower()
    if sentence.endswith('.'):
        sentence = sentence[:-1].strip() + ' .'
    return sentence.split()


def parse_sentence(sentence: str):
    """
    Tokenizes the sentence and attempts to parse it against the grammar.
    Returns a list of parse trees. Empty list means the sentence is rejected.
    """
    tokens = tokenize(sentence)
    return list(parser.parse(tokens))
