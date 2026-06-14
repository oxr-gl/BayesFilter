# P23 Zhao--Cui P22 Preservation Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- P22 integrated readable companion and fixed-branch gradient note.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive branches.
- No HMC convergence claim.
- No production implementation readiness claim.
- No executable prototype claim.

## Decision

Decision: `P22_SPINE_COPIED_AND_EXTENDED_NO_FAILURE_FLAGS`.

P23 was created by copying the P22 TeX note as the base spine, then adding
P23 blocks in place.  No inherited P22 substantive text or derivation was
intentionally replaced by a shorter cross-reference.  The preservation status
allowed for required inherited spine rows is only `copied_verbatim` or
`extended_in_place`; cross-reference-only substitution is a failure condition.

## Exact Inherited-Anchor Preservation Table

| Inherited P22 block family | P22 source anchors | P23 destination anchors | Status | Shortened? | Cross-reference replacement? | P23 additions nearby | Failure flag |
|---|---|---|---|---|---|---|---|
| opening reader contract and non-summary rule | P22-C1, P22-C2 | P22-C1, P22-C2, P23-C1, P23-C2, P23-C3 | `extended_in_place` | no | no | P23-C1, P23-C2, P23-C3 | none |
| notation definitions | N1, N2, N3, N4, N5 | N1, N2, N3, N4, N5 | `copied_verbatim` | no | no | none | none |
| five-object orientation | P22-O1, P22-O2, P22-O3, P22-O4, P22-O5, P22-O6, P22-O7, P22-O8, P22-O9, P22-O10, P22-O11, P22-O12, P22-O13, P22-O14, P22-O15, P22-O16, P22-O17, P22-O18 | P22-O1, P22-O2, P22-O3, P22-O4, P22-O5, P22-O6, P22-O7, P22-O8, P22-O9, P22-O10, P22-O11, P22-O12, P22-O13, P22-O14, P22-O15, P22-O16, P22-O17, P22-O18 | `copied_verbatim` | no | no | P23-E1, P23-E2, P23-E3, P23-E4, P23-E5, P23-E6, P23-E7, P23-E8, P23-E9, P23-E10, P23-E11, P23-E12, P23-E13 before this block | none |
| Zhao--Cui Section 1 reconstruction | BF-1, BF-2, BF-3, BF-3a, BF-4, BF-5, BF-6, BF-7, BF-8, BF-9, BF-10, BF-11 | BF-1, BF-2, BF-3, BF-3a, BF-4, BF-5, BF-6, BF-7, BF-8, BF-9, BF-10, BF-11 | `copied_verbatim` | no | no | threaded P23-E references in surrounding text | none |
| Zhao--Cui Section 2 TT representation and basis | TT-1, TT-1a, TT-2, TT-2a, TT-3, TT-3a, TT-6, TT-7, TT-8, TT-9, TT-10, TT-11 | TT-1, TT-1a, TT-2, TT-2a, TT-3, TT-3a, TT-6, TT-7, TT-8, TT-9, TT-10, TT-11 | `extended_in_place` | no | no | P23-RANK1, P23-RANK2, P23-RANK3, P23-RANK4, P23-RANK5, P23-RANK6 | none |
| Zhao--Cui Section 2 TT marginalization | TT-4, TT-5 | TT-4, TT-5 | `copied_verbatim` | no | no | none | none |
| Zhao--Cui Section 2 Algorithm 1 | A1-1, A1-0, A1-2, A1-2a, A1-2b, A1-2c, A1-2d, A1-3, A1-4, A1-5, A1-6, A1-7 | A1-1, A1-0, A1-2, A1-2a, A1-2b, A1-2c, A1-2d, A1-3, A1-4, A1-5, A1-6, A1-7 | `extended_in_place` | no | no | P23-SWEEP1, P23-SWEEP2, P23-SWEEP3, P23-SWEEP4, P23-SWEEP5, P23-SWEEP6, P23-SWEEP7, P23-SWEEP8 | none |
| Zhao--Cui Section 3 squared-TT and defensive density | S1, S2, S3, S4, S5, S6 | S1, S2, S3, S4, S5, S6 | `copied_verbatim` | no | no | none | none |
| Zhao--Cui Section 3 mass matrices and marginalization | M1, M2, M3, M4, M5, M6, M7, M8, M9 | M1, M2, M3, M4, M5, M6, M7, M8, M9 | `copied_verbatim` | no | no | none | none |
| Zhao--Cui Section 3 KR maps | K1, K2, K3, K4, K5, K6, K7, K8, K9, K10, K11 | K1, K2, K3, K4, K5, K6, K7, K8, K9, K10, K11 | `extended_in_place` | no | no | P23-KR2-1, P23-KR2-2, P23-KR2-3, P23-KR2-4, P23-KR2-5, P23-KR2-6, P23-KR2-7, P23-KR2-8, P23-KR2-9, P23-KR2-10, P23-KR2-11, P23-KROPS1, P23-KROPS2, P23-KROPS3, P23-KROPS4, P23-KROPS5, P23-KROPS6, P23-KROPS7, P23-KROPS8, P23-KROPS9, P23-KROPS10 | none |
| Zhao--Cui Section 3 Algorithm 2 | A2-1, A2-2, A2-3, A2-4, A2-5 | A2-1, A2-2, A2-3, A2-4, A2-5 | `copied_verbatim` | no | no | none | none |
| Zhao--Cui Section 3 particle correction | F1, F2, F3, F4, F5, F6, F7 | F1, F2, F3, F4, F5, F6, F7 | `copied_verbatim` | no | no | none | none |
| Zhao--Cui Section 3 smoothing | B1, B2, B3, B4, B5, B6, B7, B8, B9 | B1, B2, B3, B4, B5, B6, B7, B8, B9 | `copied_verbatim` | no | no | none | none |
| Zhao--Cui Section 5 preconditioning | E1, P1, P2, P3, P4, P5, P6a, P6b, P6c, P6, P7, P7a, P7b, P7c, P7d, P7e, P7f, P7g, P7h, P7i, P7j, P7k, P7l, P8, P9, P10, P11, P11a, P11b, P11c, P12, P13, P13a, P14, P15, P16, P16a, P16b, P16b.1, P16b.2, P16b.3, P16b.4, P16c, P16d, P17, P18 | E1, P1, P2, P3, P4, P5, P6a, P6b, P6c, P6, P7, P7a, P7b, P7c, P7d, P7e, P7f, P7g, P7h, P7i, P7j, P7k, P7l, P8, P9, P10, P11, P11a, P11b, P11c, P12, P13, P13a, P14, P15, P16, P16a, P16b, P16b.1, P16b.2, P16b.3, P16b.4, P16c, P16d, P17, P18 | `extended_in_place` | no | no | P23-PREC1, P23-PREC2, P23-PREC3, P23-PREC4, P23-PREC5, P23-PREC6, P23-PREC7, P23-PREC8, P23-PREC9 | none |
| transition from Zhao--Cui annotation to fixed-branch extension | R1, R2, R3 | R1, R2, R3 | `copied_verbatim` | no | no | none | none |
| fixed-branch object/data structures | D1, D2, D3, D4, D5, D6, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12 | D1, D2, D3, D4, D5, D6, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12 | `extended_in_place` | no | no | P23-DOM1, P23-DOM2, P23-DOM3, P23-DOM4, P23-DOM5, P23-DOM6, P23-DOM7, P23-STAB1, P23-STAB2, P23-STAB3, P23-STAB4, P23-STAB5, P23-STAB6, P23-STAB7, P23-STAB8, P23-STAB9 | none |
| fixed-branch recursion | FB1, FB2, FB3, FB4, FB5, P20-B1, P20-B2, P20-B3 | FB1, FB2, FB3, FB4, FB5, P20-B1, P20-B2, P20-B3 | `copied_verbatim` | no | no | none | none |
| fixed-branch gradient setup | P19-1, P19-2, P19-3, P19-4, P19-5, P19-6, P19-7, P19-8, P19-9, P19-10, P19-11, P19-12, P19-13, P19-14, P19-15, P19-16, P19-17, P19-18, P19-19, P19-20, P19-21, P19-22, P19-23, P19-24, P19-25, P19-26, P19-27, P19-28, P19-29, P19-30, P19-31, P19-32, P19-33, P19-34, P19-35, P19-36, P19-37, P19-38, P19-39, P19-40, P19-41, P19-42, P19-43, P19-44, P19-45, P19-45a, P19-46, P19-47, P19-48, P19-49, P19-50, P19-51, P19-52, P19-53, P19-53a, P19-53b, P19-53c, P19-53d, P19-53e, P19-53f, P19-53g, P19-53h, P19-54, P19-55, P19-56, P19-57, P19-58, P19-59, P19-60, P19-61, P19-62, P19-63, P19-64, P19-65, P19-66, P19-67, P19-68, P19-69, P19-70, P19-71, P19-72, P19-73, P19-74, P19-74a, P19-74b, P19-74c, P19-74d, P19-75, P19-76, P22-K1, P22-K2, P22-K3, P22-K4, P22-K5, P22-K6, P22-K7, P22-K8 | P19-1, P19-2, P19-3, P19-4, P19-5, P19-6, P19-7, P19-8, P19-9, P19-10, P19-11, P19-12, P19-13, P19-14, P19-15, P19-16, P19-17, P19-18, P19-19, P19-20, P19-21, P19-22, P19-23, P19-24, P19-25, P19-26, P19-27, P19-28, P19-29, P19-30, P19-31, P19-32, P19-33, P19-34, P19-35, P19-36, P19-37, P19-38, P19-39, P19-40, P19-41, P19-42, P19-43, P19-44, P19-45, P19-45a, P19-46, P19-47, P19-48, P19-49, P19-50, P19-51, P19-52, P19-53, P19-53a, P19-53b, P19-53c, P19-53d, P19-53e, P19-53f, P19-53g, P19-53h, P19-54, P19-55, P19-56, P19-57, P19-58, P19-59, P19-60, P19-61, P19-62, P19-63, P19-64, P19-65, P19-66, P19-67, P19-68, P19-69, P19-70, P19-71, P19-72, P19-73, P19-74, P19-74a, P19-74b, P19-74c, P19-74d, P19-75, P19-76, P22-K1, P22-K2, P22-K3, P22-K4, P22-K5, P22-K6, P22-K7, P22-K8 | `extended_in_place` | no | no | P23-MD1, P23-MD2, P23-MD3, P23-MD4, P23-MD5, P23-MD6, P23-MD7, P23-MD8, P23-MD9, P23-GDAG1, P23-GDAG2, P23-GDAG3, P23-GDAG4, P23-GDAG5, P23-GDAG6, P23-GDAG7 | none |
| fixed-branch Proposition 1 | P19-77, P19-78, P19-79, P19-80, P19-81, P19-82, P19-83, P19-84 | P19-77, P19-78, P19-79, P19-80, P19-81, P19-82, P19-83, P19-84 | `copied_verbatim` | no | no | none | none |
| fixed-branch Proposition 2 | P19-85, P19-86, P19-87, P19-88, P19-89 | P19-85, P19-86, P19-87, P19-88, P19-89 | `extended_in_place` | no | no | P23-GDAG1, P23-GDAG2, P23-GDAG3, P23-GDAG4, P23-GDAG5, P23-GDAG6, P23-GDAG7 | none |
| inherited non-claims | P19-90, P19-91, P19-92, P19-93 | P19-90, P19-91, P19-92, P19-93 | `copied_verbatim` | no | no | none | none |
| finite-difference diagnostic and minimal mathematical example | P19-94, P19-95, P19-95a, P19-96, P22-FD0a, P19-97, P22-FD0b, P19-98, P19-99, P22-FD0c, P19-100, P22-FD0d, P22-FD0e, P22-FD1, P22-FD2, P22-FD3, P22-FD4, P22-FD5, P22-FD7, P22-FD8, P22-FD6, P22-FD9, P19-102, P19-103, P19-104, P19-105, P19-106, P19-107, P19-108, P19-109, P19-110 | P19-94, P19-95, P19-95a, P19-96, P22-FD0a, P19-97, P22-FD0b, P19-98, P19-99, P22-FD0c, P19-100, P22-FD0d, P22-FD0e, P22-FD1, P22-FD2, P22-FD3, P22-FD4, P22-FD5, P22-FD7, P22-FD8, P22-FD6, P22-FD9, P19-102, P19-103, P19-104, P19-105, P19-106, P19-107, P19-108, P19-109, P19-110 | `extended_in_place` | no | no | P23-MAN1, P23-MAN2, P23-MAN3, P23-MAN4, P23-MAN5, P23-MAN6, P23-MAN7 | none |
| integrated conclusion | P22-R1, P22-R2, P22-R3, P22-R4 | P22-R1, P22-R2, P22-R3, P22-R4 | `copied_verbatim` | no | no | no-executable scope P23-C3 | none |
