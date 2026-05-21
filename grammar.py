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

grammar = CFG.fromstring(GRAMMAR_STRING)
parser = nltk.ChartParser(grammar)


def tokenize(sentence: str):
    """
    Very simple tokenizer:
    - lowercase
    - ensures '.' is separate
    """
    sentence = sentence.strip().lower()
    if sentence.endswith('.'):
        sentence = sentence[:-1].strip() + ' .'
    return sentence.split()


def parse_sentence(sentence: str):
    """
    Returns list of parse trees.
    Empty list = rejected sentence.
    """
    tokens = tokenize(sentence)
    return list(parser.parse(tokens))