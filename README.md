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
**sudah**, **sedang**, and **akan**, which precede the verb. Coordination is expressed using conjunctions such as
**dan** (and) and **atau** (or) (Sneddon, 1996).

To keep the model tractable and focused on grammar construction, the language is restricted to a 
simplified subset with the following characteristics:

-- **Simple sentences:** a noun phrase (NP) followed by a verb phrase (VP), ending with a period.
-- **Coordinated sentences:** multiple clauses joined using dan or atau.
-- **Noun phrases:** a pronoun or noun, optionally combined with a conjunction.
-- **Verb phrases:** an optional sequence of particles, followed by a verb and an optional object.

The following elements are deliberately excluded to maintain a controlled grammar and emphasize
syntactic structure: morphological affixes (*me-*, *di-*), reduplication (*buku-buku*), 
passive voice, and complex embedded clauses.

The initial grammar is intentionally constructed with ambiguity and left recursion. These issues 
are then systematically removed to obtain a clean grammar compatible with an LL(1) parser, a 
top-down parsing strategy that uses a single lookahead symbol to produce a leftmost derivation 
(Aho et al., 2006).

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

# E2 — Generating and Cleaning a Restricted Context-Free Grammar
### Indonesian Language Parser

---

## Description

Grammars are a cornerstone of computational linguistics and compiler design, providing a formal
foundation for understanding, generating, and validating the structure of a language. A
Context-Free Grammar (CFG) is defined as a 4-tuple G = (V, Σ, R, S), where V is a finite set of
variables (non-terminals), Σ is a finite set of terminals disjoint from V, R is a finite set of
production rules of the form A → α where A ∈ V and α ∈ (V ∪ Σ)*, and S ∈ V is the start symbol
(Hopcroft et al., 2001, Chapter 5, pp. 171–175). In this evidence, a CFG is designed, cleaned,
and implemented as a parser for a controlled subset of **Indonesian (Bahasa Indonesia)**.

Indonesian was chosen because its structure maps cleanly onto the SVO (Subject–Verb–Object) model
that CFGs handle well. As described by Sneddon (1996, Chapters 2–4), Indonesian sentences follow a
Subject–Verb–Object order with no verb conjugation and no grammatical gender, making it an ideal
candidate for a controlled grammar demonstration. Tense and aspect are expressed through optional
particles (*sudah*, *sedang*, *akan*) placed before the verb, and coordination is expressed through
conjunctions (*dan*, *atau*).

The grammar recognizes the following sentence structures:

- **Simple clauses:** a noun phrase (NP) followed by a verb phrase (VP), ending with a period.
- **Coordinated sentences:** multiple clauses joined by *dan* (and) or *atau* (or) at the sentence
  level.
- **Noun phrases:** a single pronoun or noun, or two nouns/pronouns joined by a conjunction.
- **Verb phrases:** an optional sequence of tense particles, followed by a verb, followed by an
  optional object NP.

The following elements are deliberately **excluded** to keep the grammar controlled and focused on
demonstrating CFG cleaning techniques: morphological affixes (*me-*, *di-*), reduplication
(*buku-buku*), passive voice, and complex embedded clauses.

To implement this solution, an **LL(1) parser** is used — a top-down, left-to-right parsing
strategy that constructs a leftmost derivation using exactly one token of lookahead (Aho et al.,
2006, Chapter 4, pp. 217–228). Arriving at an LL(1)-compatible grammar requires two cleaning
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

The grammar is constructed in three stages. Each stage addresses a specific formal property
required for an LL(1) parser. The progression is: initial grammar → eliminate ambiguity →
eliminate left recursion.

---

### Stage 1 — Initial Grammar

The initial grammar captures the intended language structure directly and intuitively. The period
is enforced only at the top level through a separate `Clause` non-terminal, keeping sentence
composition and punctuation cleanly separated:

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

**Terminals:** 'saya', 'dia', 'mereka', 'kami', 'buku', 'nasi', 'air', 'guru', 'murid',
'kucing', 'anjing', 'makan', 'minum', 'membaca', 'menulis', 'melihat', 'sudah', 'sedang',
'akan', 'dan', 'atau', '.'

**Start symbol:** S

Example sentences this grammar accepts:
- *saya makan nasi .* → I eat rice.
- *dia sedang membaca buku .* → She is reading a book.
- *mereka akan minum air .* → They will drink water.

**Problems with this grammar:**

This grammar is correct in what it recognizes, but it has two critical problems that prevent it
from being used as an LL(1) parser.

**Problem 1 — Ambiguity.** A grammar is ambiguous if there exists a string that can be derived
by more than one distinct parse tree (Hopcroft et al., 2001, Chapter 5, pp. 184–187). The rule
`S → S Conj S` creates exactly this problem. Consider the sentence:

> *saya makan nasi dan dia minum air atau mereka melihat buku .*

This string can be parsed in two structurally different ways:

- **Tree A:** `(saya makan nasi dan dia minum air) atau (mereka melihat buku)`

<img width="670" height="217" alt="TreeA_stage1" src="https://github.com/user-attachments/assets/0c279f3f-d298-4908-aec1-f50961b1c222" />

- **Tree B:** `(saya makan nasi) dan (dia minum air atau mereka melihat buku)`

<img width="608" height="217" alt="TreeB_stage1" src="https://github.com/user-attachments/assets/2d6d05ca-50a7-4207-96e8-5417b28ae64c" />


Both derivations are valid under `S → S Conj S`, making the grammar ambiguous. The same
ambiguity arises in `NP → NP Conj NP`, where coordinated noun phrases can be grouped in
multiple ways — for example, `saya dan dia atau mereka` can be read as
`(saya dan dia) atau mereka` or `saya dan (dia atau mereka)`.

> *[Paste your two full syntactic tree diagrams here — Tree A and Tree B for the ambiguous
> sentence above.]*

**Problem 2 — Left recursion.** A grammar has direct left recursion when a non-terminal A has a
production of the form `A → A α` (Aho et al., 2006, Chapter 4, pp. 212–213). Both `S → S Conj S`
and `NP → NP Conj NP` exhibit this. Left recursion causes top-down parsers to loop infinitely,
since expanding S immediately requires expanding S again — without consuming any input token.

---

### Stage 2 — Elimination of Ambiguity

Ambiguity is eliminated by introducing **precedence levels** among conjunctions, mirroring the
standard technique used in expression grammar design (Aho et al., 2006, Chapter 4, pp. 217–228).
The conjunction *dan* (and) is assigned higher binding precedence than *atau* (or), so *dan*
groups its operands before *atau* does. This is achieved by splitting S into two intermediate
non-terminals:

- `S_atau` handles *atau*-level coordination (lowest precedence, evaluated last)
- `S_dan` handles *dan*-level coordination (higher precedence, evaluated first)

For NP, ambiguity is resolved by enumerating the allowed NP forms explicitly rather than using
a recursive rule. This removes recursive coordination within NP, preventing multiple groupings
such as `(saya dan dia) atau mereka` vs `saya dan (dia atau mereka)`.

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

Now the sentence *saya makan nasi dan dia minum air atau mereka melihat buku .* has **exactly
one parse tree:** `S_dan` binds the first two clauses together first, then `S_atau` joins the
result with the third clause. The structural ambiguity is gone.

> *[Paste your single unambiguous parse tree here for the sentence above, showing S_atau and
> S_dan enforcing precedence.]*

**Problem remaining — left recursion.** Although ambiguity is resolved, the grammar now has
**direct left recursion** in three rules (Aho et al., 2006, Chapter 4, pp. 212–213):

- `S_atau → S_atau 'atau' S_dan` — S_atau calls itself as its first symbol
- `S_dan  → S_dan 'dan' Clause` — S_dan calls itself as its first symbol
- `VP     → Particle VP` is right-recursive (acceptable), but `Verb` rules are fine too —
  no left recursion in VP ✅

A top-down LL(1) parser attempting to expand `S_atau` would immediately attempt to expand
`S_atau` again, looping infinitely without consuming any input. Left recursion must be
eliminated before this grammar qualifies as LL(1).

---

### Stage 3 — Elimination of Left Recursion (Final Grammar)

The standard algorithm for eliminating direct left recursion (Aho et al., 2006, Chapter 4,
pp. 212–213) transforms any rule of the form:

```
A → A α | β
```

into:

```
A  → β A'
A' → α A' | ε
```

where `A'` is a fresh non-terminal and `ε` denotes the empty string. This preserves the
language recognized by the grammar while removing the left-recursive structure.

**Applying the algorithm step by step:**

**Rule 1: `S_atau → S_atau 'atau' S_dan | S_dan`**

Here `α = 'atau' S_dan` and `β = S_dan`:

```
S_atau   → S_dan S_atau_A
S_atau_A → 'atau' S_dan S_atau_A | ε
```

**Rule 2: `S_dan → S_dan 'dan' Clause | Clause`**

Here `α = 'dan' Clause` and `β = Clause`:

```
S_dan   → Clause S_dan_A
S_dan_A → 'dan' Clause S_dan_A | ε
```

All other rules are checked and confirmed free of left recursion:
- `Clause → NP VP` — starts with NP ✅
- `NP → Pronoun | Noun | ...` — starts with terminals ✅
- `VP → Particle VP | Verb NP | Verb` — starts with Particle or Verb (terminals) ✅

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
parsing, as it eliminates ambiguity and left recursion, enabling deterministic top-down parsing
with a single lookahead symbol (Aho et al., 2006, Chapter 4, pp. 224–227).

**Example derivations:**

*saya makan nasi .*
```
S        → S_atau '.'
S_atau   → S_dan S_atau_A
S_dan    → Clause S_dan_A
Clause   → NP VP
NP       → Pronoun → 'saya'
VP       → Verb NP → 'makan' Noun → 'makan' 'nasi'
S_dan_A  → ε
S_atau_A → ε
Result   → saya makan nasi .   ✅
```

*dia sedang membaca buku .*
```
S        → S_atau '.'
S_atau   → S_dan S_atau_A
S_dan    → Clause S_dan_A
Clause   → NP VP
NP       → Pronoun → 'dia'
VP       → Particle VP → 'sedang' VP → 'sedang' Verb NP → 'sedang' 'membaca' 'buku'
S_dan_A  → ε
S_atau_A → ε
Result   → dia sedang membaca buku .   ✅
```

*saya makan nasi dan dia minum air atau mereka melihat buku .*
```
S        → S_atau '.'
S_atau   → S_dan S_atau_A
S_dan    → Clause S_dan_A           [saya makan nasi]
S_dan_A  → 'dan' Clause S_dan_A     [dan dia minum air]
S_dan_A  → ε
S_atau_A → 'atau' S_dan S_atau_A    [atau mereka melihat buku]
S_atau_A → ε
Result   → saya makan nasi dan dia minum air atau mereka melihat buku .   ✅
```

*makan saya nasi .* — rejected (verb cannot begin an NP or Clause)
```
S_atau → S_dan S_atau_A
S_dan  → Clause S_dan_A
Clause → NP VP
NP     → Pronoun | Noun | Pronoun Conj Pronoun | Noun Conj Noun
'makan' ∉ {Pronoun terminals} ∪ {Noun terminals}   ❌
```

> *[Paste your syntactic tree diagrams here — one for each accepted derivation above, showing
> all intermediate non-terminals including S_atau_A and S_dan_A.]*

---

## References

Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, techniques,
and tools* (2nd ed.). Pearson/Addison-Wesley. Chapter 4, pp. 212–213, 217–228, 220–224, 224–227.

Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2001). *Introduction to automata theory,
languages, and computation* (2nd ed.). Addison-Wesley. Chapter 5, pp. 171–175, 184–187;
Chapter 7, Section 7.1.5, pp. 272–277.

Sneddon, J. N. (1996). *Indonesian: A comprehensive grammar*. Routledge. Chapters 2–4.
