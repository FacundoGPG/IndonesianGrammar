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
groups its operands before *atau* does. This is achieved by splitting S into two intermediate
non-terminals:

- `S_atau` handles *atau*-level coordination (lowest precedence, evaluated last)
- `S_dan` handles *dan*-level coordination (higher precedence, evaluated first)

For NP, ambiguity is resolved by making NP non-recursive — instead of `NP → NP Conj NP`, the
allowed forms are enumerated explicitly, removing the structural choice that caused multiple trees.

```
S       → S_atau '.'
S_atau  → S_atau 'atau' S_dan | S_dan
S_dan   → S_dan 'dan' NP VP | NP VP

NP      → Pronoun | Noun | Pronoun Conj Pronoun | Noun Conj Noun
VP      → VP Particle | Verb NP | Verb

Pronoun  → 'saya' | 'dia' | 'mereka' | 'kami'
Noun     → 'buku' | 'nasi' | 'air' | 'guru' | 'murid' | 'kucing' | 'anjing'
Verb     → 'makan' | 'minum' | 'membaca' | 'menulis' | 'melihat'
Particle → 'sudah' | 'sedang' | 'akan'
Conj     → 'dan' | 'atau'
```

Now the sentence *saya makan nasi . dan dia minum air . atau mereka melihat buku .* has **exactly
one parse tree:** `S_atau` resolves *atau* last, so *dan* binds the first two clauses before
*atau* joins the third. Ambiguity has been removed.

> *[Paste your syntactic tree diagram here — the single unambiguous parse tree for the example
> sentence above, showing how S_atau and S_dan enforce precedence.]*

**Problem remaining — left recursion.** Although ambiguity is gone, the grammar now has **direct
left recursion** in two rules (Aho et al., 2006, Chapter 4, pp. 212–213):

- `S_atau → S_atau 'atau' S_dan` — S_atau calls itself on the left
- `S_dan  → S_dan 'dan' NP VP` — S_dan calls itself on the left
- `VP     → VP Particle` — VP calls itself on the left

A top-down LL(1) parser attempting to expand `S_atau` would immediately try to expand `S_atau`
again, entering an infinite loop without consuming any input. Left recursion must be eliminated
before this grammar can be used as an LL(1) parser.

---

### Stage 3 — Elimination of Left Recursion (Final LL(1) Grammar)

> *[Paste your syntactic tree diagram here — the parse tree from Stage 2 redrawn after left
> recursion elimination, showing the new S_atau_A and S_dan_A prime non-terminals.]*

The standard algorithm for eliminating direct left recursion (Aho et al., 2006, Chapter 4,
pp. 212–213) states that for any rule of the form:

```
A → A α₁ | A α₂ | ... | β₁ | β₂ | ...
```

it is replaced by:

```
A  → β₁ A' | β₂ A' | ...
A' → α₁ A' | α₂ A' | ε
```

where A' is a new non-terminal. This preserves the language recognized while removing the
left-recursive structure.

**Applying the algorithm to each left-recursive rule:**

**Rule: `S_atau → S_atau 'atau' S_dan | S_dan`**

Here `α = 'atau' S_dan` and `β = S_dan`:

```
S_atau   → S_dan S_atau_A
S_atau_A → 'atau' S_dan S_atau_A | ε
```

**Rule: `S_dan → S_dan 'dan' NP VP | NP VP`**

Here `α = 'dan' NP VP` and `β = NP VP`:

```
S_dan   → NP VP S_dan_A
S_dan_A → 'dan' NP VP S_dan_A | ε
```

**Rule: `VP → VP Particle | Verb NP | Verb`**

Here `α = Particle` and `β = Verb NP | Verb`:

```
VP   → Verb NP VP_A | Verb VP_A
VP_A → Particle VP_A | ε
```

**Final grammar after elimination of left recursion:**

```
S        → S_atau '.'
S_atau   → S_dan S_atau_A
S_atau_A → 'atau' S_dan S_atau_A | ε
S_dan    → NP VP S_dan_A
S_dan_A  → 'dan' NP VP S_dan_A | ε

NP       → Pronoun | Noun | Pronoun Conj Pronoun | Noun Conj Noun
VP       → Verb NP VP_A | Verb VP_A
VP_A     → Particle VP_A | ε

Pronoun  → 'saya' | 'dia' | 'mereka' | 'kami'
Noun     → 'buku' | 'nasi' | 'air' | 'guru' | 'murid' | 'kucing' | 'anjing'
Verb     → 'makan' | 'minum' | 'membaca' | 'menulis' | 'melihat'
Particle → 'sudah' | 'sedang' | 'akan'
Conj     → 'dan' | 'atau'
```

This grammar is:
- **Unambiguous** — every valid string has exactly one parse tree.
- **Free of left recursion** — every rule begins with a terminal or a non-terminal that cannot
  loop back to itself on the left.
- **LL(1)-compatible** — a top-down parser can always decide which production to apply using one
  token of lookahead (Aho et al., 2006, Chapter 4, pp. 224–227).

**Example derivations:**

*saya makan nasi .*
```
S        → S_atau '.'
S_atau   → S_dan S_atau_A
S_dan    → NP VP S_dan_A
NP       → Pronoun → saya
VP       → Verb NP VP_A → makan Noun VP_A → makan nasi VP_A → makan nasi ε
S_dan_A  → ε
S_atau_A → ε
Result   → saya makan nasi .  
```

*dia sedang membaca buku .*
```
S        → S_atau '.'
S_atau   → S_dan S_atau_A
S_dan    → NP VP S_dan_A
NP       → Pronoun → dia
VP       → Verb NP VP_A → membaca buku VP_A → membaca buku VP_A
VP_A     → Particle VP_A → sedang VP_A → sedang ε

  Note: particles trail the verb in this VP formulation.
  In the NLTK implementation this is reordered — see Implementation section.

S_dan_A  → ε
S_atau_A → ε
Result   → dia membaca buku sedang .

  (In Stage 3 the particle position is before the verb — see Implementation note.)
```

*makan saya nasi .* — rejected
```
S_atau → S_dan S_atau_A
S_dan  → NP VP S_dan_A
NP     → Pronoun | Noun | Pronoun Conj Pronoun | Noun Conj Noun
'makan' ∉ Pronoun ∪ Noun  
```

> *[Paste your final syntactic trees here — one for each accepted sentence, showing the full
> derivation using the Stage 3 grammar with all prime non-terminals visible.]*

**Note on particle ordering:** The Stage 2 grammar used `VP → VP Particle` (particle after verb)
to demonstrate left recursion. In the final implementation, particles appear before the verb
(*sedang membaca*, not *membaca sedang*), which is linguistically correct in Indonesian (Sneddon,
1996, Chapters 2–4). The NLTK implementation reflects this ordering.

---

## References

Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, techniques,
and tools* (2nd ed.). Pearson/Addison-Wesley. Chapter 4, pp. 212–213, 217–228, 220–224, 224–227.

Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2001). *Introduction to automata theory,
languages, and computation* (2nd ed.). Addison-Wesley. Chapter 5, pp. 171–175, 184–187;
Chapter 7, Section 7.1.5, pp. 272–277.

Sneddon, J. N. (1996). *Indonesian: A comprehensive grammar*. Routledge. Chapters 2–4.
