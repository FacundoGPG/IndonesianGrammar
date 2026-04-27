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

The initial grammar captures the intended language structure directly and intuitively:

```
S       → S Conj S | NP VP '.'
NP      → NP Conj NP | Pronoun | Noun
VP      → Particle VP | Verb NP | Verb

Pronoun  → 'saya' | 'dia' | 'mereka' | 'kami'
Noun     → 'buku' | 'nasi' | 'air' | 'guru' | 'murid' | 'kucing' | 'anjing'
Verb     → 'makan' | 'minum' | 'membaca' | 'menulis' | 'melihat'
Particle → 'sudah' | 'sedang' | 'akan'
Conj     → 'dan' | 'atau'
```

**Non-terminals:** S, NP, VP, Pronoun, Noun, Verb, Particle, Conj

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

> *saya makan nasi . dan dia minum air . atau mereka melihat buku .*

This string can be parsed in two different ways:

- **Tree A:** `(saya makan nasi . dan dia minum air .) atau (mereka melihat buku .)`
- **Tree B:** `(saya makan nasi .) dan (dia minum air . atau mereka melihat buku .)`

Both derivations are valid under `S → S Conj S`, making the grammar ambiguous. The same problem
exists in `NP → NP Conj NP`.

**Problem 2 — Left recursion.** A grammar has direct left recursion when a non-terminal A has a
production of the form `A → A α` (Aho et al., 2006, Chapter 4, pp. 212–213). Both `S → S Conj S`
and `NP → NP Conj NP` exhibit this. Left recursion causes top-down parsers to loop infinitely,
since parsing S requires first parsing S, which requires parsing S again — never consuming any
input.

---

### Stage 2 — Elimination of Ambiguity

> *[Paste your syntactic tree diagrams here — one showing Tree A, one showing Tree B for the
> ambiguous sentence, to illustrate the problem visually before presenting the fix.]*

Ambiguity is eliminated by introducing **precedence levels** among conjunctions, mirroring the
standard technique used in arithmetic grammar design (Aho et al., 2006, Chapter 4, pp. 217–228).
The conjunction *dan* (and) is assigned higher binding precedence than *atau* (or), so *dan*
groups its operands before *atau* does. This is achieved by splitting S into two levels:

- `S_atau` handles *atau*-level coordination (lowest precedence, evaluated last)
- `S_dan` handles *dan*-level coordination (higher precedence, evaluated first)

For NP, ambiguity is resolved by making NP non-recursive — instead of `NP → NP Conj NP`, we
enumerate the allowed NP forms explicitly:

```
S       → S_atau '.'
S_atau  → S_dan S_atau'
S_atau' → 'atau' S_dan S_atau' | ε
S_dan   → NP VP S_dan'
S_dan'  → 'dan' NP VP S_dan' | ε

NP      → Pronoun | Noun | Pronoun Conj Pronoun | Noun Conj Noun

VP      → ParticleSeq Verb ObjOpt
ParticleSeq → Particle ParticleSeq | ε
ObjOpt  → NP | ε

Pronoun  → 'saya' | 'dia' | 'mereka' | 'kami'
Noun     → 'buku' | 'nasi' | 'air' | 'guru' | 'murid' | 'kucing' | 'anjing'
Verb     → 'makan' | 'minum' | 'membaca' | 'menulis' | 'melihat'
Particle → 'sudah' | 'sedang' | 'akan'
Conj     → 'dan' | 'atau'
```

Now the sentence *saya makan nasi . dan dia minum air . atau mereka melihat buku .* has **exactly
one parse tree:** the *dan* clause binds first, then *atau* joins the result with the third clause.
Ambiguity has been removed.

> *[Paste your syntactic tree diagram here — the single unambiguous parse tree for the example
> sentence above.]*

**Problem remaining:** `S_atau'` and `ParticleSeq` are right-recursive, which is acceptable for
LL(1). However, if the grammar had been written with left recursion in these rules, the next step
would be required. Let us verify there is no left recursion before proceeding.

Checking each rule:
- `S_atau  → S_dan S_atau'` — starts with S_dan, not S_atau ✅
- `S_atau' → 'atau' S_dan S_atau' | ε` — starts with terminal 'atau' ✅
- `S_dan   → NP VP S_dan'` — starts with NP, not S_dan ✅
- `S_dan'  → 'dan' NP VP S_dan' | ε` — starts with terminal 'dan' ✅
- `NP      → Pronoun | Noun | ...` — starts with terminals ✅
- `ParticleSeq → Particle ParticleSeq | ε` — starts with Particle, not ParticleSeq ✅

The grammar after ambiguity removal contains **no left recursion**. The two steps overlap here
because resolving ambiguity through precedence stratification simultaneously produced right-
recursive (not left-recursive) rules. This is the final grammar.

---

### Stage 3 — Final Grammar (LL(1) Ready)

After eliminating ambiguity and confirming no left recursion remains, the final grammar is:

```
S           → S_atau '.'
S_atau      → S_dan S_atau'
S_atau'     → 'atau' S_dan S_atau' | ε
S_dan       → NP VP S_dan'
S_dan'      → 'dan' NP VP S_dan' | ε

NP          → Pronoun | Noun | Pronoun Conj Pronoun | Noun Conj Noun
VP          → ParticleSeq Verb ObjOpt
ParticleSeq → Particle ParticleSeq | ε
ObjOpt      → NP | ε

Pronoun     → 'saya' | 'dia' | 'mereka' | 'kami'
Noun        → 'buku' | 'nasi' | 'air' | 'guru' | 'murid' | 'kucing' | 'anjing'
Verb        → 'makan' | 'minum' | 'membaca' | 'menulis' | 'melihat'
Particle    → 'sudah' | 'sedang' | 'akan'
Conj        → 'dan' | 'atau'
```

This grammar is:
- **Unambiguous** — every valid string has exactly one parse tree.
- **Free of left recursion** — no non-terminal can derive a string beginning with itself.
- **LL(1)-compatible** — a top-down parser can always decide which rule to apply using only one
  token of lookahead (Aho et al., 2006, Chapter 4, pp. 224–227).

**Example derivations:**

*saya makan nasi .*
```
S → S_atau '.'
  → S_dan S_atau' '.'
  → NP VP S_dan' S_atau' '.'
  → Pronoun VP S_dan' S_atau' '.'
  → saya ParticleSeq Verb ObjOpt S_dan' S_atau' '.'
  → saya ε makan ObjOpt S_dan' S_atau' '.'
  → saya makan Noun S_dan' S_atau' '.'
  → saya makan nasi ε ε '.'   ✅
```

*dia sedang membaca buku .*
```
S → S_atau '.'
  → S_dan S_atau' '.'
  → NP VP S_dan' S_atau' '.'
  → dia ParticleSeq Verb ObjOpt S_dan' S_atau' '.'
  → dia sedang ParticleSeq Verb ObjOpt S_dan' S_atau' '.'
  → dia sedang ε membaca ObjOpt S_dan' S_atau' '.'
  → dia sedang membaca Noun ε ε '.'
  → dia sedang membaca buku .   ✅
```

*makan saya nasi .* — rejected (verb cannot open an NP)
```
S → S_atau '.'
  → S_dan S_atau' '.'
  → NP VP ...
NP → Pronoun | Noun | ...
'makan' ∉ Pronoun ∪ Noun   ❌
```

> *[Paste your syntactic tree diagrams here — one for each accepted example sentence above,
> showing the full parse tree structure with all intermediate non-terminals visible.]*

---

## References

Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, techniques,
and tools* (2nd ed.). Pearson/Addison-Wesley. Chapter 4, pp. 212–213, 217–228, 220–224, 224–227.

Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2001). *Introduction to automata theory,
languages, and computation* (2nd ed.). Addison-Wesley. Chapter 5, pp. 171–175, 184–187;
Chapter 7, Section 7.1.5, pp. 272–277.

Sneddon, J. N. (1996). *Indonesian: A comprehensive grammar*. Routledge. Chapters 2–4.
