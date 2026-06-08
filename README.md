# E2 — Generating and Cleaning a Restricted Context-Free Grammar
### Indonesian Language Parser

---

## Description

Context-Free Grammars (CFGs) provide a formal mechanism for describing the structure of a language 
and are widely used in both computational linguistics and compiler design. A CFG defines how valid
strings in a language can be generated through a set of production rules, making it suitable for 
constructing parsers that validate sentence structure.

In this project, a CFG is designed, cleaned, and implemented to recognize a controlled subset of 
Indonesian (Bahasa Indonesia).

Indonesian was selected because its syntax aligns well with simple grammatical models. The language
typically follows a Subject–Verb–Object (SVO) structure and does not use verb conjugation or 
grammatical gender. Instead, temporal meaning is often expressed through optional particles such as 
sudah (already), sedang (currently/in progress), and akan (will), which precede the verb. Coordination is expressed using conjunctions such as
**dan** (and) and **atau** (or) (Sneddon, 1996).

To keep the model tractable and focused on grammar construction, the language is restricted to a 
simplified subset with the following characteristics:

- **Simple sentences:** a noun phrase (NP) followed by a verb phrase (VP), ending with a period.
- **Coordinated sentences:** multiple clauses joined using dan or atau.
- **Noun phrases:** a pronoun or noun, optionally combined with a conjunction.
- **Verb phrases:** an optional sequence of particles, followed by a verb and an optional object.

The following elements are deliberately excluded to maintain a controlled grammar and emphasize
syntactic structure: morphological affixes (*me-*, *di-*), reduplication (*buku-buku*), 
passive voice, and complex embedded clauses.

To implement this solution, an LL(1) parser is used with a top-down, left-to-right parsing
strategy that constructs a leftmost derivation using exactly one token of lookahead (Aho et al.,
2006, Chapter 4, pp. 217–228). Arriving at a compatible LL(1) grammar requires two cleaning
steps: elimination of ambiguity and elimination of left recursion.

---

## Vocabulary

The following terminals are defined for this grammar:

| Category   | Words                                                                 | Translation                                               |
|------------|-----------------------------------------------------------------------|-----------------------------------------------------------|
| Pronouns   | *saya, dia, mereka, kami*                                             | I/me, he/she, they, we                                    |
| Nouns      | *buku, nasi, air, guru, murid, kucing, anjing*                        | book, rice, water, teacher, student, cat, dog             |
| Verbs      | *makan, minum, membaca, menulis, melihat*                             | eat, drink, read, write, see                              |
| Particles  | *sudah, sedang, akan*                                                 | already (past), currently (progressive), will (future)    |
| Conjunctions | *dan, atau*                                                         | and, or                                                   |



---

## Models

The grammar is built in three stages: initial grammar > eliminate ambiguity > eliminate left
recursion.

---

### Stage 1 — Initial Grammar

The period is enforced only at the top level via `Clause`, keeping punctuation separate from
sentence composition.

```
S      → S Conj S | Clause '.'
Clause → NP VP
NP     → NP Conj NP | Pronoun | Noun
VP     → Particle VP | Verb NP | Verb

Pronoun  → 'saya' | 'dia' | 'mereka' | 'kami'
Noun     → 'buku' | 'nasi' | 'air' | 'guru' | 'murid' | 'kucing' | 'anjing'
Verb     → 'makan' | 'minum' | 'membaca' | 'menulis' | 'melihat'
Particle → 'sudah' | 'sedang' | 'akan'
Conj     → 'dan' | 'atau'
```

**Non-terminals:** S, Clause, NP, VP, Pronoun, Noun, Verb, Particle, Conj  
**Start symbol:** S

This grammar has two problems that prevent LL(1) parsing:

**Ambiguity** — `S → S Conj S` allows the same string to produce two parse trees
(Hopcroft et al., 2001, Chapter 5, pp. 184–187). For example:

> *saya makan nasi dan dia minum air atau mereka melihat buku .* (*I eat rice and he/she drinks water or they see a book.*)

- **Tree A:** `(saya makan nasi  dan  dia minum air)  atau  (mereka melihat buku)`

<img width="670" height="217" alt="TreeA_stage1" src="https://github.com/user-attachments/assets/f55ba24a-c788-4436-b471-2c6215ff88d6" />

- **Tree B:** `(saya makan nasi)  dan  (dia minum air  atau  mereka melihat buku)`

<img width="608" height="217" alt="TreeB_stage1" src="https://github.com/user-attachments/assets/ca6b26d8-0edd-4143-953c-b15cbdb72304" />

The same ambiguity arises in `NP → NP Conj NP`, where coordinated noun phrases can be grouped
in multiple ways.

**Left recursion** — `S → S Conj S` and `NP → NP Conj NP` both call themselves as their first
symbol, causing a top-down parser to loop infinitely (Aho et al., 2006, Chapter 4, pp. 212–213).

---

### Stage 2 — Elimination of Ambiguity

Ambiguity is resolved by assigning *dan* higher precedence than *atau*, splitting S into two
levels (Aho et al., 2006, Chapter 4, pp. 217–228). NP coordination is made non-recursive by
enumerating forms explicitly.

```
S      → S_atau '.'
S_atau → S_atau 'atau' S_dan | S_dan
S_dan  → S_dan 'dan' Clause | Clause
Clause → NP VP

NP     → Pronoun | Noun | Pronoun Conj Pronoun | Noun Conj Noun
VP     → Particle VP | Verb NP | Verb

Pronoun  → 'saya' | 'dia' | 'mereka' | 'kami'
Noun     → 'buku' | 'nasi' | 'air' | 'guru' | 'murid' | 'kucing' | 'anjing'
Verb     → 'makan' | 'minum' | 'membaca' | 'menulis' | 'melihat'
Particle → 'sudah' | 'sedang' | 'akan'
Conj     → 'dan' | 'atau'
```

The example sentence now has exactly one parse tree: `S_dan` binds the first two clauses, then
`S_atau` joins the third. Ambiguity is removed.

<img width="790" height="357" alt="Tree_Stage2" src="https://github.com/user-attachments/assets/0bf9a548-295a-4310-9eba-ba023fc105ef" />

**Problem remaining:** `S_atau → S_atau 'atau' S_dan` and `S_dan → S_dan 'dan' Clause` still
have direct left recursion.

---

### Stage 3 — Elimination of Left Recursion (Final Grammar)

The standard algorithm (Aho et al., 2006, Chapter 4, pp. 212–213) replaces `A → A α | β` with:

```
A  → β A'
A' → α A' | ε
```

Applied to each left-recursive rule:

**`S_atau → S_atau 'atau' S_dan | S_dan`** — here α = `'atau' S_dan`, β = `S_dan`:
```
S_atau   → S_dan S_atau_A
S_atau_A → 'atau' S_dan S_atau_A | ε
```

**`S_dan → S_dan 'dan' Clause | Clause`** — here α = `'dan' Clause`, β = `Clause`:
```
S_dan   → Clause S_dan_A
S_dan_A → 'dan' Clause S_dan_A | ε
```

All remaining rules start with terminals or non-terminals that are free of left recursion.

**Final grammar:**

```
S        → S_atau '.'
S_atau   → S_dan S_atau_A
S_atau_A → 'atau' S_dan S_atau_A | ε
S_dan    → Clause S_dan_A
S_dan_A  → 'dan' Clause S_dan_A | ε
Clause   → NP VP

NP       → Pronoun | Noun | Pronoun Conj Pronoun | Noun Conj Noun
VP       → Particle VP | Verb NP | Verb

Pronoun  → 'saya' | 'dia' | 'mereka' | 'kami'
Noun     → 'buku' | 'nasi' | 'air' | 'guru' | 'murid' | 'kucing' | 'anjing'
Verb     → 'makan' | 'minum' | 'membaca' | 'menulis' | 'melihat'
Particle → 'sudah' | 'sedang' | 'akan'
Conj     → 'dan' | 'atau'
```

This grammar is unambiguous, free of left recursion, and structured to be compatible with LL(1)
parsing, enabling deterministic top-down parsing with a single lookahead symbol
(Aho et al., 2006, Chapter 4, pp. 224–227).

<img width="545" height="287" alt="Tree_Stage3" src="https://github.com/user-attachments/assets/ac5c3441-01af-434c-b30b-caa1dbe08c1f" />

---

## Implementation

The parser is implemented in Python using the Natural Language Toolkit (NLTK), which provides
utilities for working with context-free grammars. Two files are used:

- `grammar.py` — defines the Stage 3 grammar, the NLTK `ChartParser`, and a `parse_sentence()`
  function used by the interface.
- `test_grammar.py` — an interactive interface where the user types a sentence and the parser
  responds with ACCEPTED or REJECTED, printing the parse tree on success.

**How to run:**

```bash
pip install nltk
python test_grammar.py
```

Type any sentence using the vocabulary above and end it with a period. Type `exit` to quit.

**Note on grammar adaptation:** NLTK's `CFG.fromstring()` does not reliably support ε-productions
(empty rules) across versions, these were rewritten as explicit alternatives. For example, instead of `S_atau_A → 'atau' S_dan S_atau_A | ε`, the grammar uses `S_atau_A → 'atau' S_dan S_atau_A | 'atau' S_dan`. This
does not change the language recognized by the grammar.

### Sentences accepted by the grammar

| Sentence | Translation |
|---|---|
| `saya makan nasi .` | I eat rice. |
| `dia minum air .` | He/she drinks water. |
| `kami membaca buku .` | We read a book. |
| `guru menulis buku .` | The teacher writes a book. |
| `murid melihat kucing .` | The student sees a cat. |
| `saya makan .` | I eat. (intransitive) |
| `dia minum .` | He/she drinks. |
| `mereka membaca .` | They read. |
| `saya sudah makan nasi .` | I already ate rice. |
| `dia sedang membaca buku .` | He/she is reading a book. |
| `kami akan minum air .` | We will drink water. |
| `guru sedang menulis .` | The teacher is writing. |
| `saya sudah akan makan nasi .` | I already will eat rice. (stacked particles) |
| `guru dan murid membaca buku .` | The teacher and the student read a book. |
| `kucing atau anjing minum air .` | The cat or the dog drinks water. |
| `saya makan nasi dan dia minum air .` | I eat rice and he/she drinks water. |
| `saya makan nasi atau dia minum air .` | I eat rice or he/she drinks water. |
| `saya makan nasi dan dia minum air atau mereka melihat buku .` | dan binds before atau. |
| `saya makan nasi dan dia minum air dan kami membaca buku .` | Three clauses with dan. |

<img width="1836" height="1142" alt="test_correct_grammar" src="https://github.com/user-attachments/assets/92f2e77c-9b85-406c-be5f-955d9d68f8cc" />

### Sentences rejected by the grammar

| Sentence | Reason |
|---|---|
| `makan saya nasi .` | Verb-first — violates SVO |
| `nasi saya makan .` | Object-first — violates SVO |
| `saya makan nasi` | No period at end |
| `saya berlari .` | Unknown verb *berlari* |
| `kupu makan nasi .` | Unknown noun *kupu* |
| `saya makan nasi dan .` | Dangling conjunction, no second clause |
| `atau saya makan nasi .` | Sentence starts with conjunction |
| `saya makan sudah nasi .` | Particle after verb — wrong order |
| `.` | Punctuation only |
| `saya .` | No verb |
| `makan .` | No subject |
| `saya makan nasi . .` | Double period |

<img width="313" height="218" alt="test_incorrect_grammar" src="https://github.com/user-attachments/assets/fa747edb-80ab-4d6b-91eb-63ea1d588c5d" />

---

## Analysis

### Chomsky Hierarchy — Before Cleaning (Stage 1)

The Stage 1 grammar belongs to **Type 2 — Context-Free** in the Chomsky hierarchy
(Hopcroft et al., 2001, Chapter 7, Section 7.1.5, pp. 272–277). Every production rule has
exactly one non-terminal on the left-hand side and a sequence of terminals and/or non-terminals
on the right-hand side. No rule is conditioned on surrounding context. However, the grammar is
not **Type 3 (Regular)** because rules such as `S → S Conj S` and `VP → Particle VP` require
a stack to track recursive structure — something a finite automaton cannot do.

The grammar is also ambiguous, making it unsuitable for deterministic parsing.

### Chomsky Hierarchy — After Cleaning (Stage 3)

The final grammar remains **Type 2 — Context-Free**. Eliminating ambiguity and left recursion
does not change the language, only the structure of the grammar. All strings accepted before
are still accepted after cleaning.

What does change is that the grammar becomes compatible with LL(1) parsing, enabling
deterministic top-down parsing.

### Time Complexity by Chomsky Level

| Type | Class | Parser | Time complexity | Example string |
|---|---|---|---|---|
| Type 3 | Regular | DFA / NFA | O(n) | `aababab` matched by `(ab)*` |
| Type 2 | Context-Free | LL(1), LR(1), Earley, CYK | O(n) to O(n³) | `saya makan nasi .` |
| Type 1 | Context-Sensitive | LBA | O(n²) to exponential | `aⁿbⁿcⁿ` |
| Type 0 | Recursively Enumerable | Turing machine | Undecidable in general | Any computable string |

The NLTK ChartParser (Earley-based) runs in O(n³) in the worst case. However, since the
final grammar is unambiguous and free of left recursion, parsing is efficient in practice for
the restricted sentences used in this project (Aho et al., 2006, Chapter 4, pp. 217–228).

---

## References

Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, techniques,
and tools* (2nd ed.). Pearson/Addison-Wesley. Chapter 4, pp. 212–213, 217–228, 220–224, 224–227.

Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2001). *Introduction to automata theory,
languages, and computation* (2nd ed.). Addison-Wesley. Chapter 5, pp. 171–175, 184–187;
Chapter 7, Section 7.1.5, pp. 272–277.

Sneddon, J. N. (1996). *Indonesian: A comprehensive grammar*. Routledge. Chapters 2–4.
