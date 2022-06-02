# HS-Ties

This repo contains a rough-and-ready implementation of Harmonic Serialism that computes derivations from a given UR. If there are multiple optimal candidates at a given step, all derivations are computed.

## Operations

There are six operations implemented grouped under three categories:

* Change: a -> b and b -> a
* Insert: 0 -> b
* Footing: s -> (S) and ss -> (SS) [s and S represent unparsed and parsed syllables]
* Metathesis: xy -> yx [x and y represent any characters]

## Gen

The GEN function produces a candidate set using the operations defined above.

## Constraints

Constraints return a number of violations for a given candidate. Two faithfulness constraints are predefined:

* DEP: 1 violation for applying Insert operation
* IDENT: 1 violation for applying Change operation
* CONTIG: 1 violation for applying Metathesis operation

Markedness constraints are defined with a list of strings defining loci of violation.

## Eval

The EVAL function takes an input, a candidate set, and a ranked set of constraints and returns the optimal set of candidates.

## Running the script

The script was written to be run with Python 2. Derivations are computed with the use of a stack to accommodate ties. The examples coded are those reported in Lamont (2022).

The script outputs URs with the set of outputs:

```
python hs-ties.py
/aaaa/ -> [bbbb]
/ababa/ -> [aaaaa, bbbbb]
/ababababa/ -> [bbbbbbaaa, aaabbbbbb, aaabbbaaa, aaaaaaaaa, aaaaabbbb, bbbbbbbbb, bbbbaaaaa]
/aaaaa/ -> [ababa, babba, babab, abbab, abbba]
/bbbbbb/ -> [bbabababb, babbabbab, bbabbabb, babbababb, bbababbab]
/abababa/ -> [abbaaab, baaabba, baabbaa, aabbbaa, aabbaab]
/ssssss/ -> [s(SS)s(SS), s(SS)(SS)s, (SS)s(SS)s, (SS)(SS)(SS)]
/aaaaa/ -> [ababa, abaab, babab, baaba]
```

Lamont, Andrew. 2022. Directional Constraint Evaluation Solves the Problem of Ties in Harmonic Serialism. *Linguistic Inquiry*. 
https://doi.org/10.1162/ling_a_00417
