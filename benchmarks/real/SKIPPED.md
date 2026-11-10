# Selection rule

Every problem that MathNet (https://mathnet.mit.edu, data version
`312a167f6df5`, built 2026-04-29) tags with the topic "Algebra › Algebraic
Expressions › Functional Equations" or one of its subtopics ("Existential
quantifiers", "Injectivity / surjectivity"), from every source and every year
in MathNet: 1164 problems.

Each problem was read from its MathNet record, which holds the statement and
the official solution, at `https://mathnet.mit.edu/explorer.html?p=<id>`.
The answer is taken from that official solution. Where the record has no
solution, the answer is taken from the problem's thread in the Art of Problem
Solving contest collections; if neither gives a solution, the problem is
skipped.

A problem is included when it is in scope as `INSTRUCTIONS.md` defines it,
exactly as its source states it. Two decisions were fixed before collecting:

* Only problems that ask to find or determine all functions count. A problem
  that asks whether such a function exists, or asks to prove a property of f,
  is skipped as "not 'find all f'", even when it could be written as an
  equation with an empty answer.
* When the same problem (same equation and domain) appears more than once,
  the earliest record is kept, and the others are skipped as duplicates.

## Rule 2

Rule 2 was added after rule 1 was compiled, and written down before any
problem it covers was classified. Rule 1 depends on MathNet's topic tags, and
MathNet covers the US contests and the IMO before 2006 only thinly, so rule 2
adds two sources:

* **(a)** Every other MathNet problem (same data version) whose statement
  contains a word for "function" in its language, together with function
  notation such as `f(` or `f:`. The words are function, fonction, función,
  função, Funktion, functie, funcție, funkcija, funkcja, funkce, функция,
  συνάρτηση, 函數 / 函数, 関数, 함수, ฟังก์ชัน, fonksiyon, függvény, hàm số,
  تابع and دالة. This gives 441 problems.
* **(b)** Every problem in Evan Chen's solution notes listed at
  https://web.evanchen.cc/problems.html whose statement mentions a function.
  The notes cover IMO, USAMO, USAJMO, USA TST, USA TSTST, USEMO, ELMO, ELSMO,
  EGMO and Taiwan TST: 184 files, excluding the statistics and reports pages.
  This gives 107 problems. The statement and the answer come from the notes,
  and the `url` is the notes PDF.

The scope rules, the two decisions above, and the duplicate rule apply as in
rule 1. Problems already covered by rule 1 are therefore skipped as
duplicates. On equal years the rule 1 record is kept.

One problem is excluded: **USAMO 2002 P4**. The solver was run on it during
development (issue #2) before this rule existed, so it cannot count as unseen.

# Skipped

| problem | url | reason |
|---|---|---|
| Asia Pacific Mathematics Olympiad (APMO) 1989, 5 | https://mathnet.mit.edu/explorer.html?p=apm_1989_f42c63 | extra hypothesis: f strictly increasing (equation also involves the inverse function g) |
| Asia Pacific Mathematics Olympiad (APMO) 1994, 1 | https://mathnet.mit.edu/explorer.html?p=apm_1994_71c0bd | not "find all f" satisfying an equation (inequality conditions); extra hypothesis: given values f(1)=1, f(-1)=-1 |
| Asia Pacific Mathematics Olympiad (APMO) 2002, 5 | https://mathnet.mit.edu/explorer.html?p=apm_2002_09c691 | extra hypothesis: only finitely many zeros |
| Asia Pacific Mathematics Olympiad (APMO) 2015, 2 | https://mathnet.mit.edu/explorer.html?p=apm_2015_af5968 | not "find all f" (existence question); domain not supported (integers >= 2); equation holds only on restricted values (a != b) |
| Asia Pacific Mathematics Olympiad (APMO) 2016, 5 | https://mathnet.mit.edu/explorer.html?p=apm_2016_e3d4e1 | domain not supported (R+) |
| Asia Pacific Mathematics Olympiad (APMO) 2019, 1 | https://mathnet.mit.edu/explorer.html?p=apm_2019_8b0117 | domain not supported (Z+); divisibility condition |
| Asia Pacific Mathematics Olympiad (APMO) 2023, 4 | https://mathnet.mit.edu/explorer.html?p=apm_2023_44bc62 | domain not supported (R>0); equation contains a parameter c |
| Rioplatense Mathematical Olympiad 2007, Nivel 3 - Segundo Día, 4 | https://mathnet.mit.edu/explorer.html?p=arg_2007_670f1d | domain not supported (Z); equation holds only on restricted values (x+y+z=0) |
| Rioplatense Mathematical Olympiad 2010, Level 3, 3.3 | https://mathnet.mit.edu/explorer.html?p=arg_2010_fbdb65 | domain and codomain differ (N -> R); equation holds only on restricted values |
| Rioplatense Mathematical Olympiad 2018, Level 1 - First Day, 2 | https://mathnet.mit.edu/explorer.html?p=arg_2018_4844e7 | not a functional equation (digit sums, number theory) |
| Rioplatense Mathematical Olympiad 2023, Level 2, 2.6. | https://mathnet.mit.edu/explorer.html?p=arg_2023_1574da | domain not supported (Z) |
| Rioplatense Mathematical Olympiad 2023, Level 3, 3.5. | https://mathnet.mit.edu/explorer.html?p=arg_2023_453301 | not "find all f" (asks for alpha); domain not supported (R+) |
| Austrian Mathematical Olympiad (Final Round) 2012, National Competition (Final Round, part 1), 1 | https://mathnet.mit.edu/explorer.html?p=aut_2012_2805d9 | domain not supported (Z); divisibility condition, not an equation |
| Austrian Mathematical Olympiad (Final Round) 2012, National Competition (Final Round, part 2, second day), 4 | https://mathnet.mit.edu/explorer.html?p=aut_2012_a6bb86 | not a functional equation (sequence, prove) |
| Austrian Mathematical Olympiad (Final Round) 2013, National Competition (Final Round, part 2, first day), Problem 2 | https://mathnet.mit.edu/explorer.html?p=aut_2013_5d240d | equation holds only on restricted values (x, y != 0); extra hypothesis: f(0) = 0; parameter k |
| Austrian Mathematical Olympiad (Final Round) 2014, National Competition (Final Round, part 2, first day), 2 | https://mathnet.mit.edu/explorer.html?p=aut_2014_d70aeb | domain not supported ([1, infinity)); equation holds only on restricted values |
| Austrian Mathematical Olympiad (Final Round) 2015, Problem 1. | https://mathnet.mit.edu/explorer.html?p=aut_2015_8964ac | not "find all f" (asks for a value n); domain not supported (Z>0) |
| Austrian Mathematical Olympiad (Final Round) 2015, National Competition (Final Round, part 2, first day), 1. | https://mathnet.mit.edu/explorer.html?p=aut_2015_8b9ba4 | not "find all f" (asks for a value n); domain not supported (Z>0) |
| Austrian Mathematical Olympiad (Final Round) 2016, Final Round, part 2, 1 | https://mathnet.mit.edu/explorer.html?p=aut_2016_9b312d | domain not supported (Q+); division by a variable; parameter alpha |
| Austrian Mathematical Olympiad (Final Round) 2017, Aufgabe 1. | https://mathnet.mit.edu/explorer.html?p=aut_2017_03f279 | not a functional equation (polynomial problem); extra hypothesis: P(2017) = 2016 |
| Austrian Mathematical Olympiad (Final Round) 2017, Problem 1 | https://mathnet.mit.edu/explorer.html?p=aut_2017_36301f | not a functional equation (polynomial problem); extra hypothesis: P(2017) = 2016 |
| Austrian Mathematical Olympiad (Final Round) 2017, Bundeswettbewerb für Fortgeschrittene – Lösungen, Aufgabe 1 | https://mathnet.mit.edu/explorer.html?p=aut_2017_ae2b5b | equation contains a real parameter alpha (answer depends on alpha) |
| Austrian Mathematical Olympiad (Final Round) 2018, Problem 1 | https://mathnet.mit.edu/explorer.html?p=aut_2018_a86453 | domain not supported (R>0); division by f; parameter alpha |
| Austrian Mathematical Olympiad (Final Round) 2019, National Competition—Preliminary Round, 12 | https://mathnet.mit.edu/explorer.html?p=aut_2019_6d3ae9 | not a functional equation (find pairs (a, b), floor) |
| Austrian Mathematical Olympiad (Final Round) 2021, National Competition—Final Round, 16 | https://mathnet.mit.edu/explorer.html?p=aut_2021_fde133 | equation contains a real parameter alpha (answer depends on alpha) |
| Austrian Mathematical Olympiad (Beginners' Competition) 2023, National Competition—Final Round - First day, 13 | https://mathnet.mit.edu/explorer.html?p=aut_2023_744ae2 | equation contains a real parameter alpha (answer depends on alpha) |
| Austrian Mathematical Olympiad (Final Round) 2024, National Competition—Preliminary Round, 9 | https://mathnet.mit.edu/explorer.html?p=aut_2024_2f61f5 | equation contains real parameters alpha, beta (answer depends on them) |
| Bulgarian Mathematical Olympiad 2003, Spring Mathematical Competition, Problem 12.3 | https://mathnet.mit.edu/explorer.html?p=bgr_2003_c66692 | not "find all f" (asks for a); extra hypothesis: formula on [2,3) |
| Bulgarian Mathematical Olympiad 2004, Regional round, Problem 12.6. | https://mathnet.mit.edu/explorer.html?p=bgr_2004_ae4e27 | not a functional equation (polynomial problem, two polynomials) |
| Bulgarian Mathematical Olympiad 2004, Team selection test for 45. IMO, Problem 10. | https://mathnet.mit.edu/explorer.html?p=bgr_2004_cd12ac | not "find all f" (asks for k); function of two variables on [0,1]^2, several conditions |
| Bulgarian Mathematical Olympiad 2005, Team selection test for 46. IMO, 3 | https://mathnet.mit.edu/explorer.html?p=bgr_2005_5a98c5 | domain not supported (R\{0}); division by f; equation holds only on restricted values |
| Bulgarian Mathematical Olympiad 2005, Regional round, 12.6 | https://mathnet.mit.edu/explorer.html?p=bgr_2005_d814d5 | not "find all f" (prove / count functions on a finite set) |
| Bulgarian Mathematical Olympiad 2006, National round, Problem 2. | https://mathnet.mit.edu/explorer.html?p=bgr_2006_4f1096 | domain not supported (R+); square root; equation holds only on restricted values (x > y) |
| Bulgarian Mathematical Olympiad 2006, 10, Problem 10.3. | https://mathnet.mit.edu/explorer.html?p=bgr_2006_523a99 | domain and codomain differ (Q+ -> R); extra hypothesis: f(1) = 1 and second equation |
| IMO TST 2006, Problem 2. | https://mathnet.mit.edu/explorer.html?p=bgr_2006_82901e | not a functional equation (polynomial problem, rational functions) |
| IMO TST 2007, 5 | https://mathnet.mit.edu/explorer.html?p=bgr_2007_b31c48 | not a single equation in one function (f and g, two conditions) |
| Bulgarian Mathematical Olympiad 2009, 4 | https://mathnet.mit.edu/explorer.html?p=bgr_2009_162ed7 | not a functional equation (polynomial problem, system of n polynomials) |
| Bulgarian Mathematical Olympiad 2010, 59. National Mathematical Olympiad Final round, Problem 5. | https://mathnet.mit.edu/explorer.html?p=bgr_2010_f13a67 | not "find all f" (prove); domain not supported (N) |
| Bulgarian Mathematical Olympiad 2011, Selection test for the 52. IMO, 6 | https://mathnet.mit.edu/explorer.html?p=bgr_2011_5f5bb6 | not "find all f" (prove); max of absolute values |
| Bulgarian Mathematical Olympiad 2013, Final round, 2 | https://mathnet.mit.edu/explorer.html?p=bgr_2013_a071f1 | extra hypothesis: bounded on (0, 1) |
| Bulgarian Mathematical Olympiad 2014, 63. National Mathematical Olympiad, Problem 5 | https://mathnet.mit.edu/explorer.html?p=bgr_2014_5d6a4c | domain and codomain differ (Q+ -> R+) |
| Bulgarian Mathematical Olympiad 2014, 63. National Mathematical Olympiad, Problem 3 | https://mathnet.mit.edu/explorer.html?p=bgr_2014_92afef | not "find all f" (prove; geometric assignment) |
| IMO TST 2015, 13-14 May 2015, Problem 5 | https://mathnet.mit.edu/explorer.html?p=bgr_2015_070000 | not "find all f" (prove an inequality); domain not supported (N) |
| Bulgarian Mathematical Olympiad 2015, Second day, April 19, 2015, Problem 4 | https://mathnet.mit.edu/explorer.html?p=bgr_2015_1d998e | not an equation (inequalities); domain not supported (R+) |
| Bulgarian Mathematical Olympiad 2024, 5.3 | https://mathnet.mit.edu/explorer.html?p=bgr_2024_63b187 | domain not supported (R+) |
| Belarusian Mathematical Olympiad 2010, FINAL ROUND - Category B, 8 | https://mathnet.mit.edu/explorer.html?p=blr_2010_5f2dd4 | not "find all f" (prove no function exists) |
| Belarusian Mathematical Olympiad 2010, FINAL ROUND - Category C, 8 | https://mathnet.mit.edu/explorer.html?p=blr_2010_f51383 | not "find all f" (asks for values f(-1), f(1)) |
| Belarusian Mathematical Olympiad 2011, SELECTION and TRAINING SESSION - Test 1, 1 | https://mathnet.mit.edu/explorer.html?p=blr_2011_23566d | not "find all f" (asks for a); trigonometric functions |
| Belarusian Mathematical Olympiad 2011, SELECTION and TRAINING SESSION - Test 2, 3 | https://mathnet.mit.edu/explorer.html?p=blr_2011_3006e4 | not a single equation in one function (two unknown functions f, g) |
| Belarusian Mathematical Olympiad 2011, ROUND 3, Category B, 3 | https://mathnet.mit.edu/explorer.html?p=blr_2011_8280e7 | not "find all f" (existence question); trigonometric functions |
| Belarusian Mathematical Olympiad 2011, ROUND 3 - Category A, 2 | https://mathnet.mit.edu/explorer.html?p=blr_2011_b4515b | not "find all f" (existence question); trigonometric functions |
| Selection and Training Session 2011, Test 7, 3 | https://mathnet.mit.edu/explorer.html?p=blr_2011_ed237f | division by a variable (x/y, 1/y); extra hypothesis: f(1 - f(1)) != 0 or = 0 |
| Belarusian Mathematical Olympiad 2012, FINAL ROUND - Category A, 2 | https://mathnet.mit.edu/explorer.html?p=blr_2012_75d5e8 | not "find all f" (asks for a) |
| Belarusian Mathematical Olympiad 2012, FINAL ROUND - Category B, 2 | https://mathnet.mit.edu/explorer.html?p=blr_2012_8d60e4 | not "find all f" (existence question) |
| Belarusian Mathematical Olympiad 2012, FINAL ROUND - Category A, 2 | https://mathnet.mit.edu/explorer.html?p=blr_2012_a46eba | not "find all f" (asks for alpha) |
| Belarusian Mathematical Olympiad 2012, SELECTION and TRAINING SESSION - Test 7, 2 | https://mathnet.mit.edu/explorer.html?p=blr_2012_c1bf9b | not a single equation in one function (two unknown functions f, g) |
| Belarusian Mathematical Olympiad 2012, SELECTION and TRAINING SESSION - Test 5, 3 | https://mathnet.mit.edu/explorer.html?p=blr_2012_cdbeb8 | not "find all f" (asks for triples (a, b, c)) |
| Belarusian Mathematical Olympiad 2013, SELECTION and TRAINING SESSION - Test 1, 2 | https://mathnet.mit.edu/explorer.html?p=blr_2013_086a33 | not an equation (inequality) |
| Belarusian Mathematical Olympiad 2013, FINAL ROUND - Category B, 3 | https://mathnet.mit.edu/explorer.html?p=blr_2013_338cde | not a functional equation (polynomial problem) |
| Belarusian Mathematical Olympiad 2013, FINAL ROUND - Category B, 3 | https://mathnet.mit.edu/explorer.html?p=blr_2013_8b99fa | not a functional equation (polynomial problem) |
| Belarusian Mathematical Olympiad 2013, FINAL ROUND - Category A, 3 | https://mathnet.mit.edu/explorer.html?p=blr_2013_f15432 | not a single equation in one function (two unknown functions f, h) |
| Belarusian Mathematical Olympiad 2013, Selection and Training Session - Test 8, 1 | https://mathnet.mit.edu/explorer.html?p=blr_2013_f2e863 | not a functional equation (logic puzzle) |
| Selection and Training Session 2014, Test 4, 3 | https://mathnet.mit.edu/explorer.html?p=blr_2014_044f80 | not "find all f" (existence question; two functions f, g) |
| Selection and Training Session 2014, Test 8, 3 | https://mathnet.mit.edu/explorer.html?p=blr_2014_6f0749 | domain not supported (Z) |
| Selection and Training Session 2014, Test 5, 3 | https://mathnet.mit.edu/explorer.html?p=blr_2014_7fdd32 | not a functional equation (polynomial problem with absolute values, asks for P(0)) |
| Selection and Training Session 2014, Test 7, 2 | https://mathnet.mit.edu/explorer.html?p=blr_2014_d00c18 | domain not supported (N); divisibility condition |
| Selection and Training Session 2015, Test 3, 1 | https://mathnet.mit.edu/explorer.html?p=blr_2015_202451 | not "find all f" (existence question; parameters a, b; surjective) |
| Belarusian Mathematical Olympiad 2015, Category C, 2 | https://mathnet.mit.edu/explorer.html?p=blr_2015_2b246d | not "find all f" (existence question); fractional part and trigonometric functions; two equations |
| Selection and Training Session 2015, Test 2, 4 | https://mathnet.mit.edu/explorer.html?p=blr_2015_81f29c | not a functional equation (polynomial problem, two polynomials) |
| Belarusian Mathematical Olympiad 2015, Category A, 4 | https://mathnet.mit.edu/explorer.html?p=blr_2015_e59a39 | domain not supported ([0, 1]); fractional part and trigonometric functions; two equations |
| Belarusian Mathematical Olympiad 2016, SELECTION and TRAINING SESSION - Test 2, 2 | https://mathnet.mit.edu/explorer.html?p=blr_2016_2ca321 | not "find all f" (asks for a); extra hypotheses |
| Belarusian Mathematical Olympiad 2016, SELECTION and TRAINING SESSION - Test 3, 1 | https://mathnet.mit.edu/explorer.html?p=blr_2016_489aaa | not a single equation in one function (two unknown functions f, g) |
| Belarusian Mathematical Olympiad 2016, SELECTION and TRAINING SESSION - Test 6, 1 | https://mathnet.mit.edu/explorer.html?p=blr_2016_a020b7 | domain not supported (Z) |
| Selection and Training Session 2018, Test 3, 1 | https://mathnet.mit.edu/explorer.html?p=blr_2018_6eab61 | not "find all f" (asks for a); domain not supported (R>=0) |
| Belarusian Mathematical Olympiad 2018, FINAL ROUND - Category B, 2 | https://mathnet.mit.edu/explorer.html?p=blr_2018_7d13d8 | not "find all f" (existence question, inequality); domain not supported (R+) |
| Belarusian Mathematical Olympiad 2018, FINAL ROUND - Category A, 1 | https://mathnet.mit.edu/explorer.html?p=blr_2018_84d908 | not "find all f" (asks for a); extra hypothesis: bijective |
| Belarusian Mathematical Olympiad 2019, SELECTION and TRAINING SESSION, 2 | https://mathnet.mit.edu/explorer.html?p=blr_2019_13511f | domain not supported (Z); extra hypothesis: surjective |
| Belarusian Mathematical Olympiad 2019, THIRD ROUND, 6 | https://mathnet.mit.edu/explorer.html?p=blr_2019_19d989 | not "find all f" (existence question); absolute value |
| Belarusian Mathematical Olympiad 2019, SELECTION and TRAINING SESSION, 1 | https://mathnet.mit.edu/explorer.html?p=blr_2019_1a1e6f | not "find all f" (yes/no question); domain not supported (N) |
| Belarusian Mathematical Olympiad 2019, THIRD ROUND, 6 | https://mathnet.mit.edu/explorer.html?p=blr_2019_3a29e4 | absolute value in the equation |
| Belarusian Mathematical Olympiad 2019, FINAL ROUND, 5 | https://mathnet.mit.edu/explorer.html?p=blr_2019_47d301 | not a functional equation (polynomial problem, two polynomials) |
| Belarusian Mathematical Olympiad 2019, THIRD ROUND, 6 | https://mathnet.mit.edu/explorer.html?p=blr_2019_6cbe71 | absolute value in the equation |
| Belarusian Mathematical Olympiad 2019, SELECTION and TRAINING SESSION, 1 | https://mathnet.mit.edu/explorer.html?p=blr_2019_8f812b | not "find all f" (existence question); domain not supported (N) |
| IMO TST 2020, Problems with solutions, P.3.TST.6 | https://mathnet.mit.edu/explorer.html?p=blr_2020_6fe221 | domain not supported (R+) |
| IMO TST 2024, Third Selection Test, 10 | https://mathnet.mit.edu/explorer.html?p=blr_2024_b71bb1 | equation holds only on restricted values (x != y) |
| Balkan Mathematical Olympiad Shortlist 2014, Number Theory, N6 | https://mathnet.mit.edu/explorer.html?p=bmo_2014_8cd9b9 | not "find all f" (prove); domain not supported (N) |
| Balkan Mathematical Olympiad (BMO) 2015, ALGEBRA, A6. | https://mathnet.mit.edu/explorer.html?p=bmo_2015_61b7e3 | not a functional equation (polynomial existence question) |
| Balkan Mathematical Olympiad (BMO) 2015, ALGEBRA, A4. | https://mathnet.mit.edu/explorer.html?p=bmo_2015_b72311 | domain not supported (R+) |
| Balkan Mathematical Olympiad Shortlist 2016, Algebra, A3. | https://mathnet.mit.edu/explorer.html?p=bmo_2016_681a69 | not an equation (bounded sum inequality); extra hypothesis: monotonic |
| Balkan Mathematical Olympiad 2017, NUMBER THEORY, NT2 | https://mathnet.mit.edu/explorer.html?p=bmo_2017_358dfc | domain not supported (Z>0); perfect-square condition |
| Balkan Mathematical Olympiad 2017, ALGEBRA, A3 | https://mathnet.mit.edu/explorer.html?p=bmo_2017_7d83b0 | domain not supported (N); divisibility condition |
| Balkan Mathematical Olympiad Shortlist (BMO Shortlist) 2019, NUMBER THEORY, TN1 | https://mathnet.mit.edu/explorer.html?p=bmo_2019_404973 | domain not supported (primes) |
| Balkan Mathematical Olympiad (BMO) 2021, ALGEBRA, A1 | https://mathnet.mit.edu/explorer.html?p=bmo_2021_204eb1 | not a single equation in one function (two unknown functions f, g); domain not supported (R+) |
| Balkan Mathematical Olympiad (BMO) 2021, ALGEBRA, A5 | https://mathnet.mit.edu/explorer.html?p=bmo_2021_236aa0 | domain not supported (R+) |
| Balkan Mathematical Olympiad (BMO) 2021, ALGEBRA, A3 | https://mathnet.mit.edu/explorer.html?p=bmo_2021_9081d1 | domain not supported (R+) |
| Balkan Mathematical Olympiad (BMO) 2021, ALGEBRA, A2 | https://mathnet.mit.edu/explorer.html?p=bmo_2021_c760a1 | not "find all f" satisfying an equation (inequality); division by a variable (1/x) |
| Balkan Mathematical Olympiad Shortlist (BMO Shortlist) 2022, ALGEBRA, A5. | https://mathnet.mit.edu/explorer.html?p=bmo_2022_34f8be | domain not supported ((0, infinity)) |
| Balkan Mathematical Olympiad Shortlist (BMO Shortlist) 2023, Algebra, A6 | https://mathnet.mit.edu/explorer.html?p=bmo_2023_a23af0 | domain not supported (R>0) |
| Balkan Mathematical Olympiad (BMO) 2024, Algebra, A6. | https://mathnet.mit.edu/explorer.html?p=bmo_2024_7b3222 | domain not supported (R+); second unknown (polynomial g); equation holds only on restricted values (x > y) |
| Balkan Mathematical Olympiad Shortlist 2025, Algebra, A1 | https://mathnet.mit.edu/explorer.html?p=bmo_2025_79faf0 | not a functional equation (polynomial problem) |
| Balkan Mathematical Olympiad Shortlist 2025, Algebra, A3 | https://mathnet.mit.edu/explorer.html?p=bmo_2025_9242c4 | not "find all f" (prove an inequality) |
| Brazilian Mathematical Olympiad (OBM) 1985, 5 | https://mathnet.mit.edu/explorer.html?p=bra_1985_3fc843 | not a functional equation (condition on parameters A, B with floor) |
| Brazilian Mathematical Olympiad (OBM) 1988, 3 | https://mathnet.mit.edu/explorer.html?p=bra_1988_224494 | domain not supported (positive integers) |
| Brazilian Mathematical Olympiad (OBM) 1989, 3 | https://mathnet.mit.edu/explorer.html?p=bra_1989_80cda1 | domain not supported (integers); not "find all f" |
| Brazilian Mathematical Olympiad (OBM) 1993, 5 | https://mathnet.mit.edu/explorer.html?p=bra_1993_2505dc | domain not supported (non-negative reals); not "find all f" (find a function); extra hypothesis: f(0) = 0 |
| Brazilian Mathematical Olympiad (OBM) 1995, 2 | https://mathnet.mit.edu/explorer.html?p=bra_1995_260227 | domain not supported (integers) |
| Brazilian Mathematical Olympiad (OBM) 1997, 3 | https://mathnet.mit.edu/explorer.html?p=bra_1997_e0ffed | not "find all f" (prove non-existence/existence; two functions) |
| Brazilian Mathematical Olympiad (OBM) 1998, 5 | https://mathnet.mit.edu/explorer.html?p=bra_1998_2f26bd | domain not supported (non-negative integers) |
| Brazilian Mathematical Olympiad (OBM) 2003, 5 | https://mathnet.mit.edu/explorer.html?p=bra_2003_9551e8 | not "find all f" (show that); domain not supported (positive reals) |
| Brazilian Mathematical Olympiad (OBM) 2006, FIRST DAY, 03 | https://mathnet.mit.edu/explorer.html?p=bra_2006_705e38 | MathNet statement and its official solution disagree (the solution solves a different equation) |
| Brazilian Mathematical Olympiad (OBM) 2009, Undergraduates, Problem 5 | https://mathnet.mit.edu/explorer.html?p=bra_2009_ebaedc | domain not supported (integers); two equations |
| Brazilian Mathematical Olympiad (OBM) 2010, Nível 3, 196. | https://mathnet.mit.edu/explorer.html?p=bra_2010_f4f3d3 | not "find all f" (compute values of a binary operation) |
| Brazilian Mathematical Olympiad (OBM) 2010, Grades 10–12, 1 | https://mathnet.mit.edu/explorer.html?p=bra_2010_f63b44 | equation holds only on restricted values (irrational a, b) |
| Brazilian Mathematical Olympiad (OBM) 2012, Grades 10–12, Problem 6 | https://mathnet.mit.edu/explorer.html?p=bra_2012_27ea6b | domain not supported ((0, infinity)); extra hypothesis: surjective |
| Brazilian Mathematical Olympiad (OBM) 2020, Nível 3, 25 | https://mathnet.mit.edu/explorer.html?p=bra_2020_45ee6b | not "find all f" (compute a value) |
| Brazilian Mathematical Olympiad (OBM), 16 | https://mathnet.mit.edu/explorer.html?p=bra_5d6e10 | not a functional equation (binary operation / invariant problem) |
| None, Lista 8, 5. | https://mathnet.mit.edu/explorer.html?p=bra_b804e1 | not "find all f" (compute values of a binary operation) |
| Baltic Way 1992, 12. | https://mathnet.mit.edu/explorer.html?p=btw_1992_b4b423 | not "find all f" (possible values of a limit); domain not supported (positive integers) |
| Baltic Way 1992, 11. | https://mathnet.mit.edu/explorer.html?p=btw_1992_dd6f17 | not "find all f" (show existence and uniqueness); domain not supported (Q+) |
| Baltic Way 1993, 6. | https://mathnet.mit.edu/explorer.html?p=btw_1993_2b53a4 | not "find all f" (prove that); domain not supported (interval) |
| Baltic Way 1995, 10. | https://mathnet.mit.edu/explorer.html?p=btw_1995_4216aa | domain not supported (R\{0}); multiple equations; extra hypothesis: f(1) = 1 |
| Baltic Way 1996, 13. | https://mathnet.mit.edu/explorer.html?p=btw_1996_415ffc | domain not supported (integers) |
| Baltic Way 1997, Problems, 1. | https://mathnet.mit.edu/explorer.html?p=btw_1997_365c76 | extra hypothesis: f different from the zero function |
| Baltic Way 2001, 11. | https://mathnet.mit.edu/explorer.html?p=btw_2001_7c12dc | not "find all f" (values of f(2001)); domain not supported (positive integers) |
| Baltic Way 2001, 16. | https://mathnet.mit.edu/explorer.html?p=btw_2001_eaabe2 | not "find all f" (value of f(2002)); domain not supported (positive integers) |
| Baltic Way 2002, Problems and solutions, 3. | https://mathnet.mit.edu/explorer.html?p=btw_2002_523240 | not a functional equation (sequence problem) |
| Baltic Way 2003, 1. | https://mathnet.mit.edu/explorer.html?p=btw_2003_a305c2 | domain not supported (Q+); two equations; division by a variable |
| Baltic Way 2005, Problems and solutions, 4. | https://mathnet.mit.edu/explorer.html?p=btw_2005_61774b | not a functional equation (polynomial problem; find three polynomials) |
| Baltic Way 2008, Problem 1. | https://mathnet.mit.edu/explorer.html?p=btw_2008_e8bd18 | not a functional equation (polynomial problem) |
| Baltic Way Shortlist 2009, Algebra, A-4 | https://mathnet.mit.edu/explorer.html?p=btw_2009_049af1 | not "find all f" (find all n) |
| Baltic Way Shortlist 2009, Algebra, A-7 | https://mathnet.mit.edu/explorer.html?p=btw_2009_e9a155 | domain and codomain differ (R -> R+) |
| Baltic Way 2010, ALGEBRA, EST1 | https://mathnet.mit.edu/explorer.html?p=btw_2010_15440d | not a functional equation (polynomial problem) |
| Baltic Way Shortlist 2011, Number Theory, N-03 | https://mathnet.mit.edu/explorer.html?p=btw_2011_6a7a46 | domain not supported (positive integers); divisibility condition |
| Baltic Way Shortlist 2011, Algebra, A-13 | https://mathnet.mit.edu/explorer.html?p=btw_2011_a1070f | not "find all f" (determine f(0)) |
| Baltic Way Shortlist 2011, Algebra, A-09 | https://mathnet.mit.edu/explorer.html?p=btw_2011_d46da3 | not "find all f" (show bounded); domain not supported (integers) |
| Baltic Way 2013, Algebra, A-01 | https://mathnet.mit.edu/explorer.html?p=btw_2013_7fd09d | not a functional equation (sequence problem) |
| Baltic Way 2014, Algebra, A-10 | https://mathnet.mit.edu/explorer.html?p=btw_2014_42c998 | not "find all f" (show that); extra hypothesis: strictly increasing, f(x) > x; involves inverse function |
| Baltic Way 2014, Algebra, A-14 | https://mathnet.mit.edu/explorer.html?p=btw_2014_4c495b | not "find all f" (prove that) |
| Baltic Way 2014, Algebra, A-08 | https://mathnet.mit.edu/explorer.html?p=btw_2014_6089d5 | domain not supported (positive integers); extra hypothesis: strictly increasing |
| Baltic Way Shortlist 2015, Algebra, A.15 | https://mathnet.mit.edu/explorer.html?p=btw_2015_231f81 | not a single equation in one function (pair f, g); division by a variable |
| Baltic Way Shortlist 2015, Algebra, A.12 | https://mathnet.mit.edu/explorer.html?p=btw_2015_328d91 | absolute value in equation |
| Baltic Way Shortlist 2015, Algebra, A.3 | https://mathnet.mit.edu/explorer.html?p=btw_2015_599b59 | not "find all f" (prove that) |
| Baltic Way Shortlist 2015, Algebra, A.14 | https://mathnet.mit.edu/explorer.html?p=btw_2015_ec330e | division by a variable (2f(xy)/x); equation holds only on restricted values (x != 0) |
| Baltic Way 2016, Number Theory, N9 | https://mathnet.mit.edu/explorer.html?p=btw_2016_9e808d | not "find all f" (find primes p, q and sets D); iterates with prime exponents |
| Baltic Way 2016, Algebra, A6 | https://mathnet.mit.edu/explorer.html?p=btw_2016_ac1ad3 | not "find all f" (find all a); two equations |
| Baltic Way Shortlist 2018, Algebra, A-6 | https://mathnet.mit.edu/explorer.html?p=btw_2018_b82888 | domain not supported (non-negative reals); too many variables (n variables) |
| Baltic Way Shortlist 2018, Number Theory, NT-7 | https://mathnet.mit.edu/explorer.html?p=btw_2018_bf1a6b | not "find all f" (prove that); domain not supported (positive integers) |
| Baltic Way 2019, Algebra, A7 | https://mathnet.mit.edu/explorer.html?p=btw_2019_83f7d8 | domain and codomain differ (R -> [-2019, 2019]) |
| Baltic Way 2020, Algebra, A-11. | https://mathnet.mit.edu/explorer.html?p=btw_2020_5a3d41 | not "find all f" satisfying an equation (inequality); domain not supported (R\{0}); division by a variable |
| Baltic Way 2020, Number Theory, NT-13. | https://mathnet.mit.edu/explorer.html?p=btw_2020_7da7ff | not "find all f" (find f(11)); domain not supported (integers) |
| Baltic Way 2020, Algebra, A-9. | https://mathnet.mit.edu/explorer.html?p=btw_2020_8d9f44 | not a functional equation (polynomial problem in two variables) |
| Baltic Way Shortlist 2021, Number Theory, N.7 | https://mathnet.mit.edu/explorer.html?p=btw_2021_153eee | not "find all f" (find all k); domain not supported (integers) |
| Baltic Way Shortlist 2021, Algebra, A.2 | https://mathnet.mit.edu/explorer.html?p=btw_2021_2e6e51 | equation contains a symbolic parameter n (exponent x^n, f(x)^n), not a fixed rational expression |
| Baltic Way Shortlist 2023, Algebra, A 10 | https://mathnet.mit.edu/explorer.html?p=btw_2023_100db6 | domain not supported (R\{0,1}); division by a variable |
| Baltic Way Shortlist 2023, Number Theory, N 1 | https://mathnet.mit.edu/explorer.html?p=btw_2023_955aea | domain not supported (positive integers); lcm; extra hypothesis: f(n) divides n |
| Baltic Way Shortlist 2023, Algebra, A 4 | https://mathnet.mit.edu/explorer.html?p=btw_2023_c14e22 | extra hypothesis: monotonic |
| Baltic Way Shortlist 2023, Algebra, A 2 | https://mathnet.mit.edu/explorer.html?p=btw_2023_f8098f | domain not supported (positive integers); extra hypothesis: strictly increasing, f(1) = 1 |
| Benelux Mathematical Olympiad (BxMO) 2010, Problem 2 | https://mathnet.mit.edu/explorer.html?p=bxm_2010_58391e | not a functional equation (polynomial problem) |
| Benelux Mathematical Olympiad (BxMO) 2016, Problem 3 | https://mathnet.mit.edu/explorer.html?p=bxm_2016_3cbdbb | domain and codomain differ (R -> Z) |
| Benelux Mathematical Olympiad (BxMO) 2023, Problem 1 | https://mathnet.mit.edu/explorer.html?p=bxm_2023_9b0016 | not "find all f" satisfying an equation (inequality) |
| Benelux Mathematical Olympiad (BxMO) 2025, Problem 1 | https://mathnet.mit.edu/explorer.html?p=bxm_2025_503188 | not "find all f" (does there exist) |
| Canadian Mathematical Olympiad (CMO) 1975, Problem 8 | https://mathnet.mit.edu/explorer.html?p=can_1975_e59c74 | not a functional equation (polynomial problem with parameter k) |
| Canadian Mathematical Olympiad (CMO) 1983, Problem 2 | https://mathnet.mit.edu/explorer.html?p=can_1983_53c06b | not a single equation of the supported form (curves invariant under a family of transformations; involves 2^r) |
| Canadian Mathematical Olympiad (CMO) 2002, 5. | https://mathnet.mit.edu/explorer.html?p=can_2002_aaa0da | domain not supported (non-negative integers) |
| Canadian Mathematical Olympiad (CMO) 2013, 1 | https://mathnet.mit.edu/explorer.html?p=can_2013_7e6f7b | not a functional equation (polynomial problem) |
| Canadian Mathematical Olympiad (CMO) 2015, 1 | https://mathnet.mit.edu/explorer.html?p=can_2015_53c922 | domain not supported (positive integers); inequality |
| Canadian Mathematical Olympiad (CMO) 2018, 4. | https://mathnet.mit.edu/explorer.html?p=can_2018_974d85 | not a functional equation (polynomial problem) |
| Canadian Mathematical Olympiad (CMO) 2021, Problem No. 4. | https://mathnet.mit.edu/explorer.html?p=can_2021_95fc45 | not "find all f" (find all m); domain not supported (positive integers) |
| Canadian Mathematical Olympiad (CMO), Problem 8 | https://mathnet.mit.edu/explorer.html?p=can_7f970c | not "find all f" (prove that); domain not supported (positive integers) |
| IMO TST 1999, 3. | https://mathnet.mit.edu/explorer.html?p=che_1999_bc4403 | domain not supported (R\{0}); division by a variable |
| IMO TST 2001, 6. | https://mathnet.mit.edu/explorer.html?p=che_2001_cba84e | not "find all f" (prove an inequality); domain not supported ([0,1]) |
| IMO TST 2002, 5. | https://mathnet.mit.edu/explorer.html?p=che_2002_8d06d8 | extra hypothesis: the set {f(x)/x : x != 0} is finite |
| IMO TST 2004, 11. | https://mathnet.mit.edu/explorer.html?p=che_2004_9956a4 | extra hypothesis: injective; division by a variable; equation holds only on restricted values (x != y) |
| IMO TST 2005, 11. | https://mathnet.mit.edu/explorer.html?p=che_2005_d6359f | domain not supported (naturals); divisibility condition |
| Swiss Mathematical Olympiad 2006, 5. | https://mathnet.mit.edu/explorer.html?p=che_2006_bbc0d6 | domain not supported (R>=0); extra hypothesis: f(1) = 0, f(x) > 0 for x > 1; division by a variable |
| IMO TST 2007, 11. | https://mathnet.mit.edu/explorer.html?p=che_2007_c7c9c5 | domain not supported (R+); variable exponent x^y |
| Swiss Mathematical Olympiad 2008, erste Prüfung, 2. | https://mathnet.mit.edu/explorer.html?p=che_2008_18e290 | not "find all f" satisfying an equation (inequality); domain not supported (R+) |
| IMO TST 2008, 9. | https://mathnet.mit.edu/explorer.html?p=che_2008_d6f449 | domain not supported (R+) |
| Swiss Mathematical Olympiad 2009, 6. | https://mathnet.mit.edu/explorer.html?p=che_2009_12217b | domain not supported (R>0); equation holds only on restricted values (x > y > z > 0) |
| Swiss Mathematical Olympiad 2009, 9. | https://mathnet.mit.edu/explorer.html?p=che_2009_97c646 | domain not supported (N); inequality; extra hypothesis: injective |
| IMO TST 2009, 6. | https://mathnet.mit.edu/explorer.html?p=che_2009_b42724 | not "find all f" (asks for all k); domain not supported (integers with prime factors in P) |
| IMO TST 2010, 10. | https://mathnet.mit.edu/explorer.html?p=che_2010_c81469 | not "find all f" (prove; polynomial problem) |
| IMO TST 2011, 7. | https://mathnet.mit.edu/explorer.html?p=che_2011_1f418e | not a functional equation (polynomial problem, condition on finitely many integers) |
| IMO TST 2011, 6. | https://mathnet.mit.edu/explorer.html?p=che_2011_ec6bd7 | domain not supported (Q+) |
| IMO TST 2012, 6. | https://mathnet.mit.edu/explorer.html?p=che_2012_9a9d1f | extra hypothesis: f surjective |
| IMO TST 2014, 1. | https://mathnet.mit.edu/explorer.html?p=che_2014_0113ae | domain not supported (N); divisibility condition, not an equation |
| IMO TST 2014, 4. | https://mathnet.mit.edu/explorer.html?p=che_2014_979df1 | not a functional equation (polynomial problem) |
| IMO TST 2015, 7. | https://mathnet.mit.edu/explorer.html?p=che_2015_008e32 | not "find all f" (asks for finite sets of functions closed under a relation) |
| IMO TST 2016, 2. | https://mathnet.mit.edu/explorer.html?p=che_2016_990596 | not a functional equation (polynomial problem) |
| IMO TST 2017, 1. | https://mathnet.mit.edu/explorer.html?p=che_2017_06535a | domain not supported (Z); divisibility condition; extra hypothesis f(p) > 0 |
| IMO TST 2017, 6. | https://mathnet.mit.edu/explorer.html?p=che_2017_902188 | domain and codomain differ (R>0 -> R>=0) |
| Swiss Mathematical Olympiad 2017, 2. | https://mathnet.mit.edu/explorer.html?p=che_2017_b5f7b4 | duplicate of netherlands-tst-2013-4 (Netherlands IMO TST 2013, Opgave 4.), which is kept |
| Swiss Mathematical Olympiad 2018, 5. | https://mathnet.mit.edu/explorer.html?p=che_2018_0e56c4 | not "find all f" (prove no function exists); domain not supported (R>0) |
| IMO TST 2018, 11. | https://mathnet.mit.edu/explorer.html?p=che_2018_3077de | not a single equation in one function (pairs (f, g)); extra hypothesis f >= 0 |
| IMO TST 2018, 1. | https://mathnet.mit.edu/explorer.html?p=che_2018_5ec88e | not a functional equation (polynomial problem) |
| Swiss Mathematical Olympiad 2019, 6. | https://mathnet.mit.edu/explorer.html?p=che_2019_ccae59 | not "find all f" (prove no function exists); domain not supported (Z) |
| IMO TST 2021, 11. | https://mathnet.mit.edu/explorer.html?p=che_2021_85aecb | not a single equation in one function (two functions f, g); extra hypothesis: g even |
| Swiss Mathematical Olympiad 2021, 6. | https://mathnet.mit.edu/explorer.html?p=che_2021_c42e0f | not "find all f" (prove); domain not supported (N) |
| IMO TST 2022, 12. | https://mathnet.mit.edu/explorer.html?p=che_2022_0e7552 | domain not supported (R>0) |
| IMO TST 2022, 7. | https://mathnet.mit.edu/explorer.html?p=che_2022_a1d192 | not a functional equation (polynomial problem with integer parameter n) |
| Swiss Mathematical Olympiad 2023, Second Exam, 5. | https://mathnet.mit.edu/explorer.html?p=che_2023_0dd769 | domain not supported (R \ {-1}); equation holds only on restricted values (x != 0, y != -x); division by a variable |
| None, 1. | https://mathnet.mit.edu/explorer.html?p=che_c73be1 | domain not supported (N); divisibility condition |
| China Mathematical Competition 2002, Part II Short-answer Questions, 10 | https://mathnet.mit.edu/explorer.html?p=chn_2002_1a4fac | not "find all f" (asks for a value); inequalities; extra hypothesis f(1) = 1 |
| International Mathematical Olympiad (IMO) 2004, First Day, 2 | https://mathnet.mit.edu/explorer.html?p=chn_2004_24a3f9 | not a functional equation (polynomial problem); equation holds only on restricted values (ab + bc + ca = 0) |
| China Mathematical Competition 2004, Part II Short-answer Questions, 8 | https://mathnet.mit.edu/explorer.html?p=chn_2004_dd0364 | extra hypothesis: f(0) = 1 |
| China Girls' Mathematical Olympiad (CGMO) 2006, First Day, 1. | https://mathnet.mit.edu/explorer.html?p=chn_2006_925acd | not "find all f" (prove f constant); domain and codomain differ ((0, inf) -> R); division by a variable |
| China TST 2007, Second Day, 4. | https://mathnet.mit.edu/explorer.html?p=chn_2007_18bed2 | domain not supported (Q+); division by f |
| China Southeastern Mathematical Olympiad 2007, Second Day, 5 | https://mathnet.mit.edu/explorer.html?p=chn_2007_29289a | not "find all f" (prove an inequality); absolute value |
| China Mathematical Competition 2007, Part III Word Problems, 15 | https://mathnet.mit.edu/explorer.html?p=chn_2007_3a832d | not "find all f" (prove a decomposition of periodic functions) |
| International Mathematical Olympiad (IMO) 2008, Second Day, 4. | https://mathnet.mit.edu/explorer.html?p=chn_2008_7bbb47 | domain not supported (R+); too many variables; equation holds only on restricted values (wx = yz); division |
| China Mathematical Competition 2008, Part II Short-Answer Questions, 7 | https://mathnet.mit.edu/explorer.html?p=chn_2008_e34514 | not a functional equation (iterates of a given linear function; asks for a + b) |
| China Mathematical Competition 2008, Part II Short-Answer Questions | https://mathnet.mit.edu/explorer.html?p=chn_2008_f8fcb5 | not "find all f" (asks for a value); inequalities with 2^x; extra hypothesis f(0) = 2008 |
| China Girls' Mathematical Olympiad (CGMO) 2010, Second Day, 5 | https://mathnet.mit.edu/explorer.html?p=chn_2010_8ae09b | not "find all f" (prove) |
| China TST 2010, Second Day, 6 | https://mathnet.mit.edu/explorer.html?p=chn_2010_ad1a21 | not a functional equation (existence of a real sequence) |
| China Mathematical Competition 2012, Part I Short-Answer Questions, 6 | https://mathnet.mit.edu/explorer.html?p=chn_2012_48b012 | not a functional equation (inequality; asks for range of a) |
| China Mathematical Olympiad (CMO) 2013, First Day, 3 | https://mathnet.mit.edu/explorer.html?p=chn_2013_260364 | not "find all f" (prove uniqueness, find f(2^m)); domain not supported (N) |
| China TST 2021, Test II, Second Day, 4 | https://mathnet.mit.edu/explorer.html?p=chn_2021_0faf8c | domain not supported (N+); equation holds only on restricted values (m >= n); uses Euler phi |
| China Mathematical Competition 2021, First Round, Test Paper A2, 6 | https://mathnet.mit.edu/explorer.html?p=chn_2021_978de9 | not "find all f" (asks for a value); extra hypothesis: f given on [0, 1) |
| China Mathematical Competition 2021, First Round, Test Paper A, 3 | https://mathnet.mit.edu/explorer.html?p=chn_2021_d67357 | not "find all f" (asks for a minimum); division by a variable; domain R \ {0} |
| China TST 2022, Test 4 Day 1, 3 | https://mathnet.mit.edu/explorer.html?p=chn_2022_514503 | not a single equation (multiset equality of two pairs) |
| China TST 2023, Test Four Day 2, 4 | https://mathnet.mit.edu/explorer.html?p=chn_2023_2f8df9 | domain not supported (Z) |
| China TST 2025, Test 2 · Day 2, Problem 12 | https://mathnet.mit.edu/explorer.html?p=chn_2025_82eea5 | not a functional equation (polynomial problem, prove) |
| IMO TST 2025, Test 4 · Day 2, Problem 12. | https://mathnet.mit.edu/explorer.html?p=chn_2025_e6abc2 | domain not supported (Z); not an equation (perfect-square condition); extra hypothesis: unbounded |
| Czech-Polish-Slovak Mathematical Match (CPS Match) 2007, 1 | https://mathnet.mit.edu/explorer.html?p=cps_2007_499616 | not a functional equation (polynomial problem) |
| Czech-Polish-Slovak Mathematical Match (CPS Match) 2009, 1 | https://mathnet.mit.edu/explorer.html?p=cps_2009_f5900f | domain not supported (R+) |
| None 2017, 6 | https://mathnet.mit.edu/explorer.html?p=cps_2017_835192 | domain and codomain differ ((0, inf) -> R); division by a variable |
| Czech-Polish-Slovak Mathematical Match (CPS Match) 2024, Problem 5 | https://mathnet.mit.edu/explorer.html?p=cps_2024_313d56 | equation contains a real parameter alpha (not a rational constant); answer is not a rational polynomial (f(0) = 1, f = 0 elsewhere) |
| Czech-Polish-Slovak Mathematical Match (CPS Match) 2025, Second day – 18 June 2025, 6 | https://mathnet.mit.edu/explorer.html?p=cps_2025_d5b524 | domain and codomain differ ((0, inf) -> [0, inf)) |
| Czech and Slovak Mathematical Olympiad (CSMO) 2013, First Round - take-home part, 4 | https://mathnet.mit.edu/explorer.html?p=cze_2013_bbd31a | domain not supported (R \ {0}) |
| Czech and Slovak Mathematical Olympiad (CSMO) 2016, First Round (take-home part), 4 | https://mathnet.mit.edu/explorer.html?p=cze_2016_9ebe82 | domain not supported (N); product over divisors, not an equation in 1-3 variables |
| Czech-Polish-Slovak Mathematical Match (CPS Match) 2022, 2 | https://mathnet.mit.edu/explorer.html?p=cze_2022_f5c106 | domain not supported ((0, inf)); division by f |
| IMO TST 2002, 2. Auswahlklausur, Aufgabe 1 | https://mathnet.mit.edu/explorer.html?p=deu_2002_622e90 | domain not supported (pairs of non-negative integers; two-argument f, piecewise recurrence) |
| IMO TST 2003, 2. Auswahlklausur, Aufgabe 1 | https://mathnet.mit.edu/explorer.html?p=deu_2003_eaebaf | duplicate of seed s46 |
| IMO TST 2004, 1. Auswahlklausur, Aufgabe 1 | https://mathnet.mit.edu/explorer.html?p=deu_2004_5cd442 | domain not supported (R \ {0, 1}); division by a variable |
| IMO TST 2006, 2. IMO-Auswahlklausur, Aufgabe 1 | https://mathnet.mit.edu/explorer.html?p=deu_2006_af6631 | domain not supported (R+) |
| IMO TST 2011, 1. IMO-Auswahlklausur, Aufgabe 3 | https://mathnet.mit.edu/explorer.html?p=deu_2011_82d296 | not "find all f" (inequality; prove / existence); domain not supported (Q+) |
| IMO TST 2012, 3 | https://mathnet.mit.edu/explorer.html?p=deu_2012_90480e | not a single equation in one function (pairs (f, g)) |
| IMO TST 2013, 2. Auswahlklausur, Aufgabe 2 | https://mathnet.mit.edu/explorer.html?p=deu_2013_045f0b | domain not supported (Z+); divisibility condition |
| IMO TST 2016, Aufgabe 2 | https://mathnet.mit.edu/explorer.html?p=deu_2016_991ae0 | domain not supported (Z) |
| IMO TST 2017, 3. Aufgabe | https://mathnet.mit.edu/explorer.html?p=deu_2017_483481 | domain not supported (N); divisibility condition |
| IMO TST 2019, Aufgabe 1 | https://mathnet.mit.edu/explorer.html?p=deu_2019_0b224e | domain not supported (Q+) |
| None, Problem 2 | https://mathnet.mit.edu/explorer.html?p=egm_e9ec0c | not "find all f" (asks for smallest number of colours k) |
| International Mathematical Olympiad (IMO) 1983, Primera sesión, 1. | https://mathnet.mit.edu/explorer.html?p=esp_1983_a103e1 | domain not supported (R+); extra hypothesis: f(x) -> 0 as x -> inf |
| International Mathematical Olympiad (IMO) 1986, 5. | https://mathnet.mit.edu/explorer.html?p=esp_1986_293a65 | domain not supported (R>=0); extra hypothesis: f(2) = 0, f(x) != 0 for 0 <= x < 2 |
| Spanish Mathematical Olympiad 2000, Segunda sesión, 36/6 | https://mathnet.mit.edu/explorer.html?p=esp_2000_b4b9f1 | not "find all f" (prove no function exists); domain not supported (N) |
| Spanish Mathematical Olympiad 2001, Sesión de Mañana, Problema 1 | https://mathnet.mit.edu/explorer.html?p=esp_2001_25a002 | domain not supported (N); two conditions, piecewise |
| Spanish Mathematical Olympiad 2001, Segunda sesión, 37/6 | https://mathnet.mit.edu/explorer.html?p=esp_2001_30284c | not "find all f" (recursively defined f, asks for values); domain not supported (N) |
| Spanish Mathematical Olympiad 2002, Primera sesión, 38/1 | https://mathnet.mit.edu/explorer.html?p=esp_2002_d18e5f | not a functional equation (polynomial problem) |
| Spanish Mathematical Olympiad 2004, Primera sesión, 40/3 | https://mathnet.mit.edu/explorer.html?p=esp_2004_07d62f | domain not supported (Z) |
| Spanish Mathematical Olympiad 2011, Problema 2.2 | https://mathnet.mit.edu/explorer.html?p=esp_2011_f664cf | domain not supported (N -> N u {0}); extra hypothesis: increasing, f(2) = 2 |
| Spanish Mathematical Olympiad 2012, 2. | https://mathnet.mit.edu/explorer.html?p=esp_2012_473db0 | duplicate of slovenia-tst-2010-3 (Slovenia IMO TST 2010, Second Selection Examination, 3), which is kept |
| Spanish Mathematical Olympiad 2012, Local Round, 4 | https://mathnet.mit.edu/explorer.html?p=esp_2012_ba0b2a | domain not supported (R+); extra hypothesis: continuous; division by a variable |
| International Mathematical Olympiad (IMO) 2013, 5 | https://mathnet.mit.edu/explorer.html?p=esp_2013_c89f9b | not "find all f" satisfying an equation (inequalities, prove f(x) = x); domain and codomain differ (Q>0 -> R) |
| International Mathematical Olympiad (IMO) 2014, 1 | https://mathnet.mit.edu/explorer.html?p=esp_2014_4d971e | not "find all f" (asks for f(2014)); domain not supported (N) |
| Iberoamerican Mathematical Olympiad (OIM) 2014, 2 | https://mathnet.mit.edu/explorer.html?p=esp_2014_f1cfa5 | not a functional equation (polynomial problem); extra hypothesis P(2014) = 1 |
| None 2015, Segunda Sesión, 4. | https://mathnet.mit.edu/explorer.html?p=esp_2015_8abec8 | domain not supported (Z); extra hypothesis: sum condition |
| Spanish Mathematical Olympiad 2019, SEGUNDO DÍA, 6. | https://mathnet.mit.edu/explorer.html?p=esp_2019_d4e977 | not a functional equation (polynomial problem with integer parameter k) |
| None, Problema 4 - 1 | https://mathnet.mit.edu/explorer.html?p=esp_295caa | domain not supported (N) |
| Spanish Mathematical Olympiad, 6. | https://mathnet.mit.edu/explorer.html?p=esp_3d2a73 | domain not supported (f: R+ -> R+) |
| None, Problema 4. | https://mathnet.mit.edu/explorer.html?p=esp_69b3b3 | not "find all f" (find parameters a, b of a linear f with f^2000(x) = x) |
| None, Problema 11 | https://mathnet.mit.edu/explorer.html?p=esp_6e62f6 | not "find all f" (existence question for f: Z -> Z, iterate) |
| Spanish Mathematical Olympiad, Problema 1.6 | https://mathnet.mit.edu/explorer.html?p=esp_ac958b | domain not supported (f: N -> N*); extra hypothesis: increasing |
| None, D1.- | https://mathnet.mit.edu/explorer.html?p=esp_bf187e | domain not supported (f: R+ -> R+); extra hypothesis: continuous; division by a variable |
| Spanish Mathematical Olympiad, Problema 3 | https://mathnet.mit.edu/explorer.html?p=esp_d2fb0a | non-polynomial solutions exist: at x = (1 ± sqrt 5)/2 the equation and its x -> 1 - x swap coincide, so f takes a free value there; the official answer f(x) = 1 - x^2 is incomplete |
| None, Problema 4. | https://mathnet.mit.edu/explorer.html?p=esp_f4bc8e | not "find all f" (values of f(2004)); domain not supported (N) |
| IMO TST 2011, TS-3 | https://mathnet.mit.edu/explorer.html?p=est_2011_b751e7 | not a functional equation (existence of a binary operation on Z) |
| Estonian Open Contests 2015, IMO Team Selection Contest I, S3 | https://mathnet.mit.edu/explorer.html?p=est_2015_012e27 | equation uses exponential 2^x, 2^y (not a polynomial expression) |
| Estonian Open Contests 2015, Open Contests - Seniors, O13 | https://mathnet.mit.edu/explorer.html?p=est_2015_45417f | not a single equation (f^d(x) = 2015 - x for every divisor d > 1 of 2015; iterates of order up to 2015) |
| IMO TST 2017, S6 | https://mathnet.mit.edu/explorer.html?p=est_2017_132cee | domain not supported (f: R+ -> R+) |
| Estonian Mathematical Olympiad 2020, Grade 12, F16 | https://mathnet.mit.edu/explorer.html?p=est_2020_6b68f4 | not a functional equation (condition: every shift of f is even or odd) |
| Estonian Open Contests 2020, Juniors, O9 | https://mathnet.mit.edu/explorer.html?p=est_2020_cbe1be | not "find all f" (existence question on integers) |
| Estonian Open Contests 2022, Selected Problems from the IMO Team Selection Contests, S1 | https://mathnet.mit.edu/explorer.html?p=est_2022_0ccccb | not a functional equation (inequality) |
| Estonian Open Contests 2022, Selected Problems from the Final Round of National Olympiad, F23 | https://mathnet.mit.edu/explorer.html?p=est_2022_7cb664 | not "find all f" (yes/no question; R+ domain) |
| Estonian Open Contests 2022, Selected Problems from Open Contests, O15 | https://mathnet.mit.edu/explorer.html?p=est_2022_c4337e | not "find all f" (values of f(1)); absolute value in equation |
| Estonian Mathematical Olympiad 2024, Seniors, O21 | https://mathnet.mit.edu/explorer.html?p=est_2024_3adfc9 | domain not supported (R\{1} -> R\{0}); extra hypothesis: f(0) = 1; equation holds only on restricted values; division by a variable |
| Estonian Mathematical Olympiad 2024, S6 | https://mathnet.mit.edu/explorer.html?p=est_2024_3bbcbf | not a functional equation (combinatorics on finite functions) |
| Estonian Mathematical Olympiad 2024, Grade 12, F22 | https://mathnet.mit.edu/explorer.html?p=est_2024_5db808 | not "find all f" (does there exist) |
| Estonian Mathematical Olympiad 2024, S5 | https://mathnet.mit.edu/explorer.html?p=est_2024_91fd97 | not a functional equation |
| Estonian Mathematical Olympiad 2025, Selected Problems from the Final Round of National Olympiad, F26 | https://mathnet.mit.edu/explorer.html?p=est_2025_c6939b | domain and codomain differ (R>=0 -> R); inequality; extra hypothesis: f(1) = 1 |
| French Mathematical Olympiad 2011, Exercice 2 | https://mathnet.mit.edu/explorer.html?p=fra_2011_7ae628 | equation holds only on restricted values (a, b irrational) |
| French Mathematical Olympiad 2012, Exercice 4 | https://mathnet.mit.edu/explorer.html?p=fra_2012_c057dc | not "find all f" (existence for which k; f: N* -> N*) |
| French Mathematical Olympiad 2013, Exercices du groupe A, Exercice 8 | https://mathnet.mit.edu/explorer.html?p=fra_2013_079066 | not a functional equation (polynomial problem, prove P = Q) |
| French Mathematical Olympiad 2013, Test du mercredi 9 janvier - Corrigé, Exercice 5 | https://mathnet.mit.edu/explorer.html?p=fra_2013_3e9211 | domain not supported (N*); extra hypothesis: f(2013) = 1 |
| International Mathematical Olympiad (IMO) 2014, Exercice 8 | https://mathnet.mit.edu/explorer.html?p=fra_2014_55d6e2 | domain not supported (R+*); division by a variable |
| International Mathematical Olympiad (IMO) 2014, Exercice 10 | https://mathnet.mit.edu/explorer.html?p=fra_2014_8e92eb | not a functional equation (polynomial problem) |
| French Mathematical Olympiad 2014, Test d'entrainement (envoi 6), Exercice 7. | https://mathnet.mit.edu/explorer.html?p=fra_2014_b9613b | not a functional equation (logic/combinatorics) |
| French Mathematical Olympiad 2014, Exercice 4 | https://mathnet.mit.edu/explorer.html?p=fra_2014_bb2f5f | domain not supported (N*); divisibility condition, not an equation |
| French Mathematical Olympiad 2014, Exercices du groupe A, Exercice 7 | https://mathnet.mit.edu/explorer.html?p=fra_2014_bf50a3 | domain not supported (N); perfect-square condition, not an equation |
| French Mathematical Olympiad 2017, Exercices communs, Exercice 5. | https://mathnet.mit.edu/explorer.html?p=fra_2017_ee42b4 | two-part problem: part a) has f: R -> Z (out of scope); part b) alone would be in scope, but the problem as stated is not |
| French Mathematical Olympiad Preparation 2018, Groupe A, Exercice 8. | https://mathnet.mit.edu/explorer.html?p=fra_2018_42556b | extra hypothesis: f bounded above |
| French Mathematical Olympiad Preparation 2018, TEST DU 20 FEVRIER, Exercice 3 | https://mathnet.mit.edu/explorer.html?p=fra_2018_8f0367 | not "find all f" (values of f(2018)); domain and codomain differ (Q -> R+) |
| French Mathematical Olympiad Preparation 2019, Test du 27 Novembre 2019 - Groupe Senior, Exercice 3 | https://mathnet.mit.edu/explorer.html?p=fra_2019_5d1f15 | not a functional equation (polynomial problem, prove) |
| French Mathematical Olympiad Preparation 2019, Exercices Seniors, Exercice 9 | https://mathnet.mit.edu/explorer.html?p=fra_2019_a6197e | not "find all f" (prove; finite sets) |
| French Mathematical Olympiad Preparation 2019, Exercice commun aux groupes Junior et Senior, Exercice 4 | https://mathnet.mit.edu/explorer.html?p=fra_2019_e0ec24 | domain not supported (N) |
| French Mathematical Olympiad Preparation 2020, Exercices Seniors, Exercice 16. | https://mathnet.mit.edu/explorer.html?p=fra_2020_419bfd | not a functional equation (polynomial problem, prove) |
| French Mathematical Olympiad Preparation 2020, Exercices Junior, Exercice 3 | https://mathnet.mit.edu/explorer.html?p=fra_2020_b1a03a | not "find all f" (yes/no questions on inequality conditions) |
| French Mathematical Olympiad Preparation 2020, Senior, Exercice 7. | https://mathnet.mit.edu/explorer.html?p=fra_2020_cdcf29 | domain not supported (N*); divisibility condition |
| French Mathematical Olympiad Preparation 2020, Exercices Seniors, Exercice 11. | https://mathnet.mit.edu/explorer.html?p=fra_2020_ead679 | duplicate of switzerland-2010-6 (Swiss Mathematical Olympiad 2010, 6.), which is kept |
| French Mathematical Olympiad Preparation 2021, Senior, Exercice 7 | https://mathnet.mit.edu/explorer.html?p=fra_2021_115efe | domain not supported (R>0 -> R>0) |
| French Mathematical Olympiad Preparation 2021, Senior, Exercice 7 | https://mathnet.mit.edu/explorer.html?p=fra_2021_d6b0f5 | domain not supported (N>=1 -> N>=0); extra hypothesis: second condition |
| French Mathematical Olympiad Preparation 2023, Senior, Exercice 18. | https://mathnet.mit.edu/explorer.html?p=fra_2023_2ef77b | domain not supported (N*); divisibility conditions |
| French Mathematical Olympiad Preparation 2023, Exercices Seniors, Exercice 17 | https://mathnet.mit.edu/explorer.html?p=fra_2023_5b6819 | domain not supported (N); not an equation |
| French Mathematical Olympiad Preparation 2023, Seniors, Exercice 17 | https://mathnet.mit.edu/explorer.html?p=fra_2023_6691e3 | equation contains a real parameter alpha (not a rational constant); answer depends on alpha |
| French Mathematical Olympiad Preparation 2023, Seniors, Exercice 15 | https://mathnet.mit.edu/explorer.html?p=fra_2023_eae528 | domain not supported (N*); iterate f^{f(n)} |
| French Mathematical Olympiad Preparation 2024, Exercices Juniors, Exercice 9 | https://mathnet.mit.edu/explorer.html?p=fra_2024_65efd8 | not a functional equation (sequence problem) |
| French Mathematical Olympiad Preparation 2024, Exercices Seniors, Exercice 18 | https://mathnet.mit.edu/explorer.html?p=fra_2024_a7000e | domain not supported (Z[X] -> Z[X]); divisibility condition |
| French Mathematical Olympiad, Exercices Juniors, Exercice 4 | https://mathnet.mit.edu/explorer.html?p=fra_a7c706 | duplicate of seed problem s22 |
| French Mathematical Olympiad Preparation, Exercices du groupe A, Exercice 7. | https://mathnet.mit.edu/explorer.html?p=fra_bd866e | not a functional equation (polynomial problem) |
| French Mathematical Olympiad Preparation, Exercices du groupe A, Exercice 9. | https://mathnet.mit.edu/explorer.html?p=fra_ebd596 | domain not supported (R+* -> R+*); division by a variable |
| Balkan Mathematical Olympiad (BMO) 2009, 4 | https://mathnet.mit.edu/explorer.html?p=grc_2009_78d09d | domain not supported (N*) |
| Hellenic Mathematical Olympiad 2014, Seniors, Problem 1. | https://mathnet.mit.edu/explorer.html?p=grc_2014_c08711 | not a functional equation (polynomial problem) |
| Balkan Mathematical Olympiad (BMO) 2016, Problem 1 | https://mathnet.mit.edu/explorer.html?p=grc_2016_fbfea7 | not a functional equation (inequality); extra hypothesis: injective |
| IMO TST 2019, B. Seniors, Problem 4. | https://mathnet.mit.edu/explorer.html?p=grc_2019_715bd1 | domain and codomain differ ((0, inf) -> R); division by a variable |
| IMO TST 2019, B. Seniors, Problem 1 | https://mathnet.mit.edu/explorer.html?p=grc_2019_b945e2 | domain not supported (R+ -> R+) |
| Hellenic Mathematical Olympiad 2020, B. Seniors, Problem 1 | https://mathnet.mit.edu/explorer.html?p=grc_2020_298d65 | not a functional equation (polynomial problem, two polynomials) |
| IMO TST 2024, B. Seniors, Problem 1. | https://mathnet.mit.edu/explorer.html?p=grc_2024_76c633 | not "find all f" (prove; inequality) |
| IMO TST 1997, Test 2, 3 | https://mathnet.mit.edu/explorer.html?p=hkg_1997_913d69 | domain not supported (Z); extra hypothesis: f(-1) = f(1) |
| IMO TST 1998, Test 2, 3 | https://mathnet.mit.edu/explorer.html?p=hkg_1998_4f83e1 | not "find all f" (find f(1997)); domain not supported (positive integers) |
| Hong Kong Mathematical Olympiad (HKMO) 1998, 4 | https://mathnet.mit.edu/explorer.html?p=hkg_1998_db7c33 | not "find all f" (prove inequalities) |
| IMO TST 1999, 4 | https://mathnet.mit.edu/explorer.html?p=hkg_1999_37cf36 | not a functional equation (polynomial problem); equation contains parameter m |
| Hong Kong Mathematical Olympiad (HKMO) 2004, 4 | https://mathnet.mit.edu/explorer.html?p=hkg_2004_b2f3d7 | not "find all f" (count functions on a finite set) |
| IMO TST 2005, Test 1, 1 | https://mathnet.mit.edu/explorer.html?p=hkg_2005_406bb1 | domain not supported (N); several conditions |
| IMO TST 2006, Test 1, 2. | https://mathnet.mit.edu/explorer.html?p=hkg_2006_cb0852 | not "find all f" (values of a two-variable function on nonnegative integers) |
| None 2009, Test 2, 1 | https://mathnet.mit.edu/explorer.html?p=hkg_2009_0e692e | domain not supported (Z); extra hypothesis: given values; unknown parameters a, b, c |
| IMO TST 2010, Test 2, 1 | https://mathnet.mit.edu/explorer.html?p=hkg_2010_98e4bb | extra hypothesis: set {f(x)/x : x != 0} is finite |
| Hong Kong Mathematical Olympiad (HKMO) 2012, Test 1, 2 | https://mathnet.mit.edu/explorer.html?p=hkg_2012_6effcc | not "find all f" (find a function); domain not supported (R>=0) |
| IMO TST 2014, Test 1, 1 | https://mathnet.mit.edu/explorer.html?p=hkg_2014_46b500 | not "find all f" (value f(8)); domain not supported (nonzero reals); division by a variable |
| Hong Kong Preliminary Selection Contest 2014, 4 | https://mathnet.mit.edu/explorer.html?p=hkg_2014_c1bd14 | not a functional equation (compute a sum for a linear f) |
| Hong Kong Preliminary Selection Contest 2014, 4 | https://mathnet.mit.edu/explorer.html?p=hkg_2014_d6b759 | not a functional equation (compute a sum for a linear f) |
| IMO TST 2014, Test 4, 2 | https://mathnet.mit.edu/explorer.html?p=hkg_2014_d81080 | not a single equation in one function (two conditions); equation holds only on restricted values (a not in S, x, y in S) |
| Hong Kong Pre-IMO Mock Exam 2017, Days 1 and 2, 2 | https://mathnet.mit.edu/explorer.html?p=hkg_2017_999230 | not a functional equation (f: R^2 -> R, polynomial-restriction condition) |
| IMO TST 2023, 4 | https://mathnet.mit.edu/explorer.html?p=hkg_2023_5530b1 | not a single equation (f(x + f(y)) equals one of two expressions) |
| IMO TST, 4 | https://mathnet.mit.edu/explorer.html?p=hkg_79a6b9 | extra hypothesis: continuous; not a single equation (two equations) |
| Croatia National Mathematical Competition (Final Round) 2011, Final round – National competition, 4.2 | https://mathnet.mit.edu/explorer.html?p=hrv_2011_dc5a8d | duplicate of croatia-2011-4-2 (Croatian Mathematical Olympiad 2011, Final round – National competition, 4.2), which is kept |
| Croatia National Mathematical Competition (Final Round) 2011, IMO and MEMO team selection - Final round for IMO team selection, A4 | https://mathnet.mit.edu/explorer.html?p=hrv_2011_fb2abf | domain not supported (Z) |
| Croatia National Mathematical Competition (Final Round) 2013, IMO and MEMO team selection (Day 2), A2. | https://mathnet.mit.edu/explorer.html?p=hrv_2013_de0e99 | not a functional equation (inequality); extra hypothesis: f(1) >= 0 |
| Croatia National Mathematical Competition (Final Round) 2014, Croatian Mathematical Olympiad, A2 | https://mathnet.mit.edu/explorer.html?p=hrv_2014_c5df3a | equation contains an arbitrary real parameter alpha (not a rational constant) |
| Croatian Mathematical Olympiad 2017, Final test for IMO team selection, N4. | https://mathnet.mit.edu/explorer.html?p=hrv_2017_d48c68 | domain not supported (N); divisibility condition, not an equation |
| Croatia National Mathematical Competition (Final Round) 2017, Final round – National competition, 3.3 | https://mathnet.mit.edu/explorer.html?p=hrv_2017_dc667b | not a functional equation (polynomial problem) |
| Croatian Mathematical Olympiad 2018, Final test for IMO team selection, A4 | https://mathnet.mit.edu/explorer.html?p=hrv_2018_7295f2 | not "find all f" (polynomial existence question) |
| Croatian Mathematical Olympiad 2018, Final round - National competition, 4.3 | https://mathnet.mit.edu/explorer.html?p=hrv_2018_e8cf6d | not "find all f" (prove that); domain not supported (N) |
| Croatian Mathematical Olympiad 2019, Day 2, N2 | https://mathnet.mit.edu/explorer.html?p=hrv_2019_6415a1 | not "find all f" (prove that); domain not supported (N) |
| Croatian Mathematical Olympiad 2019, Final test for MEMO team selection, A3 | https://mathnet.mit.edu/explorer.html?p=hrv_2019_ccdd53 | domain not supported (Q+) |
| Croatia National Mathematical Competition (Final Round) 2019, Final round – National competition, 4.5 | https://mathnet.mit.edu/explorer.html?p=hrv_2019_cd4a7a | domain not supported (N x N); extra divisibility condition |
| Ibero-American Mathematical Olympiad (OIM) 1985, 1st Iberoamerican, B2 | https://mathnet.mit.edu/explorer.html?p=ibe_1985_14c15a | not "find all f" (asks for f(1985)); domain not supported (N) |
| Ibero-American Mathematical Olympiad (OIM) 1987, 2nd Iberoamerican, A1 | https://mathnet.mit.edu/explorer.html?p=ibe_1987_065d5a | equation holds only on restricted values (x not 0, +-1); division by a variable |
| Ibero-American Mathematical Olympiad (OIM) 1991, 6th Iberoamerican, A3 | https://mathnet.mit.edu/explorer.html?p=ibe_1991_00e60d | not "find all f" (asks for a value); domain not supported ([0,1]) |
| Ibero-American Mathematical Olympiad (OIM) 1993, 8th Iberoamerican, A3 | https://mathnet.mit.edu/explorer.html?p=ibe_1993_404f12 | domain not supported (N); extra hypothesis: strictly increasing |
| IMO Shortlist 2007, Algebra, A4 | https://mathnet.mit.edu/explorer.html?p=imo_2007_35556d | domain not supported (R+) |
| IMO Shortlist 2007, Number Theory, N5 | https://mathnet.mit.edu/explorer.html?p=imo_2007_8c82a8 | domain not supported (N); divisibility condition, extra hypothesis: surjective |
| IMO Shortlist 2007, Algebra, A2 | https://mathnet.mit.edu/explorer.html?p=imo_2007_d1b775 | not "find all f" (inequality, asks for values of f(2007)); domain not supported (N) |
| International Mathematical Olympiad (IMO) 2008, Algebra, A4 | https://mathnet.mit.edu/explorer.html?p=imo_2008_4e4b33 | not "find all f" (prove that); domain not supported (Z) |
| International Mathematical Olympiad (IMO) 2008, Algebra, A6 | https://mathnet.mit.edu/explorer.html?p=imo_2008_96b2a5 | not "find all f" (prove that); domain and codomain differ (R -> N) |
| International Mathematical Olympiad (IMO) 2008, Algebra, A3 | https://mathnet.mit.edu/explorer.html?p=imo_2008_ac4e9a | not "find all f" (existence of a pair of functions with inequalities) |
| IMO Shortlist 2009, Algebra, A5 | https://mathnet.mit.edu/explorer.html?p=imo_2009_9f250a | not "find all f" (prove an inequality) |
| IMO Shortlist 2009, Number Theory, N3 | https://mathnet.mit.edu/explorer.html?p=imo_2009_b126b0 | not "find all f" (prove that); domain not supported (N) |
| IMO Shortlist 2010, Algebra, A5 | https://mathnet.mit.edu/explorer.html?p=imo_2010_18587d | domain not supported (Q+) |
| IMO Shortlist 2010, Number Theory, N5 | https://mathnet.mit.edu/explorer.html?p=imo_2010_970d18 | domain not supported (N); square condition, not an equation |
| IMO Shortlist 2010, Algebra, A6 | https://mathnet.mit.edu/explorer.html?p=imo_2010_c795de | not "find all f" (prove that); two unknown functions; domain not supported (N) |
| IMO Shortlist 2011, Algebra, A2 | https://mathnet.mit.edu/explorer.html?p=imo_2011_5fba9c | not a functional equation (sequence problem) |
| IMO Shortlist 2011, Algebra, A4 | https://mathnet.mit.edu/explorer.html?p=imo_2011_d1d467 | two unknown functions; domain not supported (N) |
| IMO Shortlist 2011, Number Theory, N3 | https://mathnet.mit.edu/explorer.html?p=imo_2011_f26960 | domain not supported (Z); divisibility condition with parameter n |
| IMO Shortlist 2013, Number Theory, N1 | https://mathnet.mit.edu/explorer.html?p=imo_2013_a67bc4 | domain not supported (N); divisibility condition |
| IMO Shortlist 2013, Algebra, A6 | https://mathnet.mit.edu/explorer.html?p=imo_2013_b1d43a | not a functional equation (polynomial problem) |
| IMO Shortlist 2013, Number Theory, N6 | https://mathnet.mit.edu/explorer.html?p=imo_2013_b65c98 | domain and codomain differ (Q -> Z); too many variables / division by a variable |
| IMO Shortlist 2013, Algebra, A5 | https://mathnet.mit.edu/explorer.html?p=imo_2013_ca3c20 | domain not supported (Z>=0) |
| IMO Shortlist 2014, Algebra, A6 | https://mathnet.mit.edu/explorer.html?p=imo_2014_609734 | domain not supported (Z) |
| IMO Shortlist 2015, Number Theory, N6 | https://mathnet.mit.edu/explorer.html?p=imo_2015_207240 | not "find all f" (prove that); domain not supported (N) |
| IMO Shortlist 2015, Number Theory, N8 | https://mathnet.mit.edu/explorer.html?p=imo_2015_2ed1a0 | domain not supported (Z); inequality condition, extra hypothesis: strictly increasing |
| IMO Shortlist 2015, Algebra, A5 | https://mathnet.mit.edu/explorer.html?p=imo_2015_557c5a | domain and codomain differ (Z -> odd integers) |
| IMO Shortlist 2016, Number Theory, N6 | https://mathnet.mit.edu/explorer.html?p=imo_2016_263da3 | domain not supported (N); divisibility condition |
| International Mathematical Olympiad (IMO) 2017, Combinatorics, C7 | https://mathnet.mit.edu/explorer.html?p=imo_2017_403e3f | not a functional equation (combinatorics on sets) |
| International Mathematical Olympiad (IMO) 2017, Algebra, A8 | https://mathnet.mit.edu/explorer.html?p=imo_2017_494fd9 | not "find all f" (prove an inequality from a conditional property) |
| IMO Shortlist 2018, Number Theory, N6 | https://mathnet.mit.edu/explorer.html?p=imo_2018_174f68 | not "find all f" (prove that); domain not supported (N) |
| IMO Shortlist 2018, Algebra, A5 | https://mathnet.mit.edu/explorer.html?p=imo_2018_d26063 | domain and codomain differ ((0,inf) -> R); division by a variable |
| IMO Shortlist 2019, Algebra, A1 | https://mathnet.mit.edu/explorer.html?p=imo_2019_abb25c | domain not supported (Z) |
| IMO Shortlist 2019, Algebra, A7 | https://mathnet.mit.edu/explorer.html?p=imo_2019_aeca2a | not "find all f" (prove statements about f-rare integers); domain not supported (Z) |
| IMO Shortlist 2019, Algebra, A6 | https://mathnet.mit.edu/explorer.html?p=imo_2019_c89fae | not a functional equation (polynomial problem) |
| IMO Shortlist 2020, Algebra, A8 | https://mathnet.mit.edu/explorer.html?p=imo_2020_839f00 | domain not supported (R+) |
| International Mathematical Olympiad (IMO) 2022, Combinatorics, C9. | https://mathnet.mit.edu/explorer.html?p=imo_2022_70d092 | not a functional equation (combinatorics; asks for a count) |
| International Mathematical Olympiad (IMO) 2022, Algebra, A3. | https://mathnet.mit.edu/explorer.html?p=imo_2022_e1fe8a | domain not supported (R>0); inequality / unique-existence condition |
| IMO Shortlist 2023, Number Theory, N8. | https://mathnet.mit.edu/explorer.html?p=imo_2023_3c0851 | domain not supported (N); iterate count depends on f |
| IMO Shortlist 2023, Algebra, A4. | https://mathnet.mit.edu/explorer.html?p=imo_2023_7d3fd0 | domain not supported (R>0); inequality, not an equation |
| IMO Shortlist 2024, Algebra, A7 | https://mathnet.mit.edu/explorer.html?p=imo_2024_55cccf | not "find all f" (disjunction of two equations; asks for a maximum count) |
| IMO Shortlist 2024, Number Theory, N7 | https://mathnet.mit.edu/explorer.html?p=imo_2024_7201b9 | domain not supported (N); equation holds iff m,n coprime |
| IMO Shortlist 2024, Algebra, A4 | https://mathnet.mit.edu/explorer.html?p=imo_2024_ce5613 | not "find all f" (asks for subsets S); domain not supported (N) |
| Indian National Mathematical Olympiad (INMO) 2008, 9 | https://mathnet.mit.edu/explorer.html?p=ind_2008_f42107 | domain not supported ((0,inf)) |
| IMO TST 2012, 10 | https://mathnet.mit.edu/explorer.html?p=ind_2012_37c5bf | domain and codomain differ (R+ -> R); inequalities, not an equation |
| IMO TST 2012, 4 | https://mathnet.mit.edu/explorer.html?p=ind_2012_73e543 | not "find all f" (prove that) |
| Indian National Mathematical Olympiad (INMO) 2012, 6. | https://mathnet.mit.edu/explorer.html?p=ind_2012_9dc9fe | domain not supported (Z); two equations, given values |
| IMO TST 2013, 8 | https://mathnet.mit.edu/explorer.html?p=ind_2013_c337db | not a functional equation (set problem) |
| Indian National Mathematical Olympiad (INMO) 2019, 6. | https://mathnet.mit.edu/explorer.html?p=ind_2019_5478cf | not "find all f" (prove that); function of two variables on nonzero reals |
| Indian National Mathematical Olympiad (INMO) 2020, 2. | https://mathnet.mit.edu/explorer.html?p=ind_2020_28e27a | not a functional equation (polynomial problem) |
| Indian National Mathematical Olympiad (INMO) 2021, Official Solutions, Problem 6 | https://mathnet.mit.edu/explorer.html?p=ind_2021_fdcbb4 | domain not supported (R[x], functions on polynomials) |
| IMO TST 2023, Problems and Solutions, 2 | https://mathnet.mit.edu/explorer.html?p=ind_2023_438140 | not "find all f" (prove that); domain not supported (N); two functions |
| EGMO TST 2023, Problems, Problem 1 | https://mathnet.mit.edu/explorer.html?p=ind_2023_6457a8 | not "find all f" (prove that); two unknown functions |
| IMO TST 2023, Problem 1 | https://mathnet.mit.edu/explorer.html?p=ind_2023_6854af | domain not supported (N); binary digit condition |
| Indian National Mathematical Olympiad (INMO) 2023, 3 | https://mathnet.mit.edu/explorer.html?p=ind_2023_aa198e | not "find all f" (asks for c); domain not supported (N) |
| IMO TST 2024, IMO TST 2024 Day 3, 3 | https://mathnet.mit.edu/explorer.html?p=ind_2024_147f67 | answer is not a rational polynomial (includes f(0) = 1/2, f(x) = 0 for x != 0) |
| EGMO TST 2024, EGMO TST 2024 Day 1, 3 | https://mathnet.mit.edu/explorer.html?p=ind_2024_bf04ec | domain not supported (N); condition on polynomial roots, not an equation |
| Irish Mathematical Olympiad 2010, 10 | https://mathnet.mit.edu/explorer.html?p=irl_2010_2c3319 | not a functional equation (polynomial problem) |
| Irish Mathematical Olympiad 2010, 28 | https://mathnet.mit.edu/explorer.html?p=irl_2010_7f8189 | not a functional equation (polynomial problem) |
| Irish Mathematical Olympiad 2010, 26 | https://mathnet.mit.edu/explorer.html?p=irl_2010_8882c9 | domain not supported (Z) |
| Irish Mathematical Olympiad 2011, 15 | https://mathnet.mit.edu/explorer.html?p=irl_2011_8ea913 | not "find all f" (prove that; symmetry conditions) |
| Irish Mathematical Olympiad 2018, Problems, 20 | https://mathnet.mit.edu/explorer.html?p=irl_2018_2741d9 | not a single equation in one function (two functions f, g); extra hypothesis: f(1) = 3 |
| Irish Mathematical Olympiad 2018, Problems, 16 | https://mathnet.mit.edu/explorer.html?p=irl_2018_f00a32 | not a functional equation (polynomial problem: find quadratics) |
| Irish Mathematical Olympiad 2020, Problems, 12 | https://mathnet.mit.edu/explorer.html?p=irl_2020_8f001b | not "find all f" (asks for f(1)); domain not supported (N); extra hypothesis: f(40) = 2020 |
| Irish Mathematical Olympiad 2020, Problems, 21 | https://mathnet.mit.edu/explorer.html?p=irl_2020_9b09ec | not "find all f" (asks for f(2020)); domain not supported (N) |
| Irish Mathematical Olympiad 2020, Problems, 26 | https://mathnet.mit.edu/explorer.html?p=irl_2020_f5285f | not "find all f" (asks for f(2020)); domain not supported (Z) |
| Irish Mathematical Olympiad 2021, Problems, 25 | https://mathnet.mit.edu/explorer.html?p=irl_2021_cc07f7 | not "find all f" (asks for values); domain not supported ([0,inf)) |
| Irish Mathematical Olympiad 2022, Problems, 11 | https://mathnet.mit.edu/explorer.html?p=irl_2022_403a3c | not a functional equation (fractional part fixed points) |
| Irish Mathematical Olympiad 2022, Problems, 36 | https://mathnet.mit.edu/explorer.html?p=irl_2022_5115f0 | not "find all f" (asks for f(2022)); domain not supported (N) |
| Irish Mathematical Olympiad 2022, Problems, 15 | https://mathnet.mit.edu/explorer.html?p=irl_2022_fd2532 | domain not supported (Z) |
| Irish Mathematical Olympiad 2023, Problems, 42 | https://mathnet.mit.edu/explorer.html?p=irl_2023_093c2b | not "find all f" (prove that); domain not supported ([0,inf)) |
| Irish Mathematical Olympiad 2023, Problems, 41 | https://mathnet.mit.edu/explorer.html?p=irl_2023_965c5b | not "find all f" (asks for f(2023)); domain not supported (Q+) |
| Irish Mathematical Olympiad 2023, Problems, 24 | https://mathnet.mit.edu/explorer.html?p=irl_2023_b6194e | not "find all f" (find one / prove that); domain not supported |
| Irish Mathematical Olympiad 2023, Problems, 28 | https://mathnet.mit.edu/explorer.html?p=irl_2023_e0471f | equation holds only on restricted values (xy != 1); division by a variable |
| Irish Mathematical Olympiad 2024, Problems, 13 | https://mathnet.mit.edu/explorer.html?p=irl_2024_145f5a | domain not supported (Z+); extra hypothesis: given values |
| Irish Mathematical Olympiad 2024, Problems, 33 | https://mathnet.mit.edu/explorer.html?p=irl_2024_334e6d | domain not supported (Z+) |
| Irish Mathematical Olympiad 2024, Problems, 24 | https://mathnet.mit.edu/explorer.html?p=irl_2024_51405c | domain not supported (Z) |
| Irish Mathematical Olympiad 2024, Problems, 25 | https://mathnet.mit.edu/explorer.html?p=irl_2024_73939e | domain not supported (R+ -> R+) |
| Irish Mathematical Olympiad 2024, Problems, 1 | https://mathnet.mit.edu/explorer.html?p=irl_2024_ff8fbe | domain not supported (Z -> Z) |
| Iranian Mathematical Olympiad 2010, Third Round, 9 | https://mathnet.mit.edu/explorer.html?p=irn_2010_8ae1da | domain not supported (R>=0 -> R>=0); also extra hypothesis: increasing |
| Iranian Mathematical Olympiad 2012, Third Round, 8 | https://mathnet.mit.edu/explorer.html?p=irn_2012_2d5434 | domain not supported (R+ -> R+); also involves an arbitrary polynomial g |
| Iranian Mathematical Olympiad 2012, Third Round, 5 | https://mathnet.mit.edu/explorer.html?p=irn_2012_fb65c2 | not "find all f" (prove an inequality) |
| Iranian Mathematical Olympiad 2014, Third Round, 3. | https://mathnet.mit.edu/explorer.html?p=irn_2014_0b90cd | not "find all f" (prove/existence questions about function iteration) |
| Iranian Mathematical Olympiad 2014, Team Selection Test, 16. | https://mathnet.mit.edu/explorer.html?p=irn_2014_1e64f8 | domain not supported (R+ -> R+); division by variable |
| Iranian Mathematical Olympiad 2014, Team Selection Test, 2. | https://mathnet.mit.edu/explorer.html?p=irn_2014_277bf3 | not a functional equation (polynomial problem) |
| Iranian Mathematical Olympiad 2014, Team Selection Test, 14. | https://mathnet.mit.edu/explorer.html?p=irn_2014_fb0ff4 | not "find all f" (does there exist; N -> N) |
| Iranian Mathematical Olympiad 2015, Third Round, 6 | https://mathnet.mit.edu/explorer.html?p=irn_2015_183689 | not "find all f" (prove; f: R -> Z) |
| Iranian Mathematical Olympiad 2016, Third Round, 2. | https://mathnet.mit.edu/explorer.html?p=irn_2016_8173e7 | not "find all f" (prove/existence; N -> N) |
| Iranian Mathematical Olympiad 2017, Second Round, 6 | https://mathnet.mit.edu/explorer.html?p=irn_2017_1a15b7 | domain not supported (Z+ -> Z+); divisibility and inequality conditions |
| Iranian Mathematical Olympiad 2017, Team Selection Test, 15 | https://mathnet.mit.edu/explorer.html?p=irn_2017_bc17c4 | domain not supported (R+ x R+ -> R+); also inequality condition |
| Iranian Mathematical Olympiad 2017, Third Round, 1 | https://mathnet.mit.edu/explorer.html?p=irn_2017_df4113 | not "find all f" (prove; two functions on R+) |
| Iranian Mathematical Olympiad 2018, Team Selection Test, 7 | https://mathnet.mit.edu/explorer.html?p=irn_2018_2b091d | extra hypothesis: set of difference quotients (f(x)-f(y))/(x-y) is an interval |
| Iranian Mathematical Olympiad 2018, Third Round, 2 | https://mathnet.mit.edu/explorer.html?p=irn_2018_69cc25 | domain not supported (R+ -> R+); division by variable |
| Iranian Mathematical Olympiad 2018, Third Round, 4 | https://mathnet.mit.edu/explorer.html?p=irn_2018_9b0ecd | domain not supported (Z+ -> Z+); divisibility |
| Iranian Mathematical Olympiad 2019, Team Selection Test, 13 | https://mathnet.mit.edu/explorer.html?p=irn_2019_6b689b | not a functional equation (polynomial problem, P(x, y)) |
| Iranian Mathematical Olympiad 2019, Team Selection Test, 5 | https://mathnet.mit.edu/explorer.html?p=irn_2019_d0c4f4 | answer is not a rational polynomial (equation depends only on f^2; official answer f = 0 or f(x) = ±x pointwise, which includes e.g. \|x\|) |
| Iranian Mathematical Olympiad 2019, Third Round - Algebra, 2 | https://mathnet.mit.edu/explorer.html?p=irn_2019_ea1a6f | domain not supported (R>=0 -> R>=0) |
| Iranian Mathematical Olympiad 2019, Third Round - Number Theory, 3 | https://mathnet.mit.edu/explorer.html?p=irn_2019_fbefd2 | domain not supported (R+ -> R+); perfect-square condition, not an equation |
| Iranian Mathematical Olympiad 2020, Third Round - Algebra, 6 | https://mathnet.mit.edu/explorer.html?p=irn_2020_1d99bc | not "find all f" (prove) |
| Iranian Mathematical Olympiad 2020, Team Selection Test, 4 | https://mathnet.mit.edu/explorer.html?p=irn_2020_201b58 | not "find all f" (prove) |
| Iranian Mathematical Olympiad 2020, Third Round - Algebra, 5 | https://mathnet.mit.edu/explorer.html?p=irn_2020_36e84a | not a functional equation (polynomial problem) |
| Iranian Mathematical Olympiad 2020, Third Round - Number Theory, 4 | https://mathnet.mit.edu/explorer.html?p=irn_2020_5a3ddc | domain not supported (N -> N) |
| Iranian Mathematical Olympiad 2020, Third Round - Algebra, 2 | https://mathnet.mit.edu/explorer.html?p=irn_2020_8fd9ad | equation holds only on restricted values (a + f(b) + f(f(c)) = 0) |
| Iranian Mathematical Olympiad 2021, Third Round - Algebra, 3 | https://mathnet.mit.edu/explorer.html?p=irn_2021_3c361f | not "find all f" (asks for finite sets of integers) |
| Iranian Mathematical Olympiad 2021, Third Round - Number Theory, 3 | https://mathnet.mit.edu/explorer.html?p=irn_2021_902361 | domain not supported (N -> N) |
| Iranian Mathematical Olympiad 2021, Team Selection Test, 8 | https://mathnet.mit.edu/explorer.html?p=irn_2021_f4f193 | domain not supported (N -> N); divisibility |
| Iranian Mathematical Olympiad 2022, Third Round - Number Theory, 2 | https://mathnet.mit.edu/explorer.html?p=irn_2022_481e5e | domain not supported (N -> N); divisibility |
| Iranian Mathematical Olympiad 2022, Team Selection Test, 12 | https://mathnet.mit.edu/explorer.html?p=irn_2022_4d3506 | domain and codomain differ (R -> set of sets A) |
| Iranian Mathematical Olympiad 2022, Third Round - Final Exam, 3 | https://mathnet.mit.edu/explorer.html?p=irn_2022_959cf7 | domain and codomain differ (Q[X] -> R) |
| Iranian Mathematical Olympiad 2023, Team Selection Test - Second Exam, 5 | https://mathnet.mit.edu/explorer.html?p=irn_2023_2e46d9 | domain not supported (Z>=0 -> Z>=0) |
| Iranian Mathematical Olympiad 2023, Team Selection Test - Second Exam, 3 | https://mathnet.mit.edu/explorer.html?p=irn_2023_4e6b9c | domain not supported (R+ -> R+); triangle-inequality condition, not an equation |
| Iranian Mathematical Olympiad 2023, Third Round - Midterm Exam, 1 | https://mathnet.mit.edu/explorer.html?p=irn_2023_6581bf | domain not supported (R+ -> R+) |
| Iranian Mathematical Olympiad 2023, Team Selection Test - First Exam, 5 | https://mathnet.mit.edu/explorer.html?p=irn_2023_6a8faf | domain and codomain differ (Z -> R); extra hypothesis: strictly increasing |
| Iranian Mathematical Olympiad 2023, Team Selection Test - Second Exam, 2 | https://mathnet.mit.edu/explorer.html?p=irn_2023_c339ef | not a functional equation (prove statement about jumps on [0, 1]) |
| Iranian Mathematical Olympiad 2023, Third Round - Algebra, 2 | https://mathnet.mit.edu/explorer.html?p=irn_2023_e9bfaa | domain not supported (N -> N); inequality condition |
| Iranian Mathematical Olympiad 2024, Third Round - Olympiad Exam, 4 | https://mathnet.mit.edu/explorer.html?p=irn_2024_046b9f | domain not supported (N -> N); divisibility |
| Iranian Mathematical Olympiad 2024, Team Selection Test - Second Exam, 2 | https://mathnet.mit.edu/explorer.html?p=irn_2024_07f6e4 | domain not supported (Q[x] -> Q[x]) |
| Iranian Mathematical Olympiad 2024, Third Round - Algebra, 2 | https://mathnet.mit.edu/explorer.html?p=irn_2024_bf9da8 | domain not supported (C -> C); absolute value |
| Iranian Mathematical Olympiad 2024, Third Round - Olympiad Exam, 2 | https://mathnet.mit.edu/explorer.html?p=irn_2024_c248a7 | not "find all f" (does there exist; N -> N) |
| Iranian Mathematical Olympiad 2025, Team Selection Test - First Exam, 6 | https://mathnet.mit.edu/explorer.html?p=irn_2025_831564 | domain not supported (R+ -> R+) |
| Iranian Mathematical Olympiad 2025, Third Round - Algebra, 2 | https://mathnet.mit.edu/explorer.html?p=irn_2025_8578aa | domain not supported (C -> C); absolute value; second unknown function g |
| Iranian Mathematical Olympiad 2025, Third Round - Olympiad Exam, 1 | https://mathnet.mit.edu/explorer.html?p=irn_2025_912017 | domain and codomain differ (Z -> C); extra hypothesis: periodic |
| Iranian Mathematical Olympiad 2025, Third Round - Combinatorics, 2 | https://mathnet.mit.edu/explorer.html?p=irn_2025_b4d62c | not a functional equation (combinatorics) |
| Italian Mathematical Olympiad 1997, 2. | https://mathnet.mit.edu/explorer.html?p=ita_1997_48de6c | not "find all f" (prove f is odd and periodic) |
| Italian Mathematical Olympiad 1998, Cesenatico, 6. | https://mathnet.mit.edu/explorer.html?p=ita_1998_60e37c | not "find all f" (prove; N -> N) |
| Italian Mathematical Olympiad 2008, 3. | https://mathnet.mit.edu/explorer.html?p=ita_2008_496a9a | domain and codomain differ (Z -> R); not an equation |
| Italian Mathematical Olympiad Project 2013, Problemi a risposta multipla, 9. | https://mathnet.mit.edu/explorer.html?p=ita_2013_431549 | not a functional equation (polynomial problem) |
| Italian Mathematical Olympiad Project 2019, Problemi a risposta multipla, 9. | https://mathnet.mit.edu/explorer.html?p=ita_2019_9bc37b | not a functional equation (polynomial problem) |
| Italian Mathematical Olympiad 2020, Problemi a risposta numerica, 14. | https://mathnet.mit.edu/explorer.html?p=ita_2020_f09a99 | not a functional equation (polynomial problem) |
| Italian Mathematical Olympiad 2022, Problemi a risposta multipla, 4. | https://mathnet.mit.edu/explorer.html?p=ita_2022_c3a6ac | not a functional equation (polynomial problem) |
| Junior Balkan Mathematical Olympiad (JBMO) 2003, Grade 9, 9.4 | https://mathnet.mit.edu/explorer.html?p=jbm_2003_cc9d09 | domain not supported (N* -> N*) |
| Japanese Mathematical Olympiad (JMO) 2008, Final, 4 | https://mathnet.mit.edu/explorer.html?p=jpn_2008_49ef98 | answer is not a rational polynomial (piecewise family f(0) = a, f(x) = 0 for x != 0) |
| Japanese Mathematical Olympiad (JMO) 2009, PROBLEMS, 8 | https://mathnet.mit.edu/explorer.html?p=jpn_2009_0c4c51 | not a functional equation (polynomial problem) |
| Japanese Mathematical Olympiad (JMO) 2009, PROBLEMS, 5 | https://mathnet.mit.edu/explorer.html?p=jpn_2009_52732e | domain not supported (R>=0 -> R>=0) |
| Japanese Mathematical Olympiad (JMO) 2011, First Stage, 10 | https://mathnet.mit.edu/explorer.html?p=jpn_2011_02ef8f | not "find all f" (asks min/max of f(23) + f(2011); inequality; N -> N) |
| Japanese Mathematical Olympiad (JMO) 2012, Final Round, 2 | https://mathnet.mit.edu/explorer.html?p=jpn_2012_3f1a68 | duplicate MathNet record of JMO 2012 Final Round 2 (japan-2012-final-2, kept); this copy has no solution |
| Japanese Mathematical Olympiad (JMO) 2013, PROBLEMS, 2 | https://mathnet.mit.edu/explorer.html?p=jpn_2013_b3ca6b | domain and codomain differ (Z -> R) |
| Japanese Mathematical Olympiad (JMO) 2022, FINAL ROUND, 2 | https://mathnet.mit.edu/explorer.html?p=jpn_2022_e889ae | domain not supported (N -> N) |
| Japanese Mathematical Olympiad (JMO) 2023, First Round, 12 | https://mathnet.mit.edu/explorer.html?p=jpn_2023_648f4e | not "find all f" (maximum size of a set of functions) |
| Japanese Mathematical Olympiad (JMO) 2023, First Round, 4 | https://mathnet.mit.edu/explorer.html?p=jpn_2023_67b630 | not a functional equation (computation) |
| Japanese Mathematical Olympiad (JMO) 2024, First Round, 11 | https://mathnet.mit.edu/explorer.html?p=jpn_2024_5a6712 | not "find all f" (asks a minimum value; N -> N) |
| Japanese Mathematical Olympiad (JMO) 2024, First Round, 8 | https://mathnet.mit.edu/explorer.html?p=jpn_2024_714449 | not "find all f" (counts tuples; N0 -> Z) |
| Japanese Mathematical Olympiad (JMO) 2024, Final Round, 2 | https://mathnet.mit.edu/explorer.html?p=jpn_2024_9efea6 | domain not supported (N -> N); lcm |
| Japanese Mathematical Olympiad (JMO) 2025, FIRST ROUND, 10 | https://mathnet.mit.edu/explorer.html?p=jpn_2025_957b3e | not "find all f" (counts functions on a finite set) |
| Korean Mathematical Olympiad (KMO) 2007, Second Day, 6 | https://mathnet.mit.edu/explorer.html?p=kor_2007_5b3a67 | not "find all f" (prove) |
| Korean Mathematical Olympiad (KMO) 2008, The First Day, March 22, 2008, 3 | https://mathnet.mit.edu/explorer.html?p=kor_2008_f70401 | domain and codomain differ (R+ -> R); extra hypothesis: f(1) = 2008 and bound; division by variable |
| Korean Mathematical Olympiad (KMO) 2013, The First Day, March 23, 2013, 2 | https://mathnet.mit.edu/explorer.html?p=kor_2013_c1caf4 | domain and codomain differ (R -> [0, inf)); equation holds only on restricted values (ab + bc + cd = 0) |
| Korean Mathematical Olympiad (KMO) 2023, March 25, 2023 (Day 1), 2 | https://mathnet.mit.edu/explorer.html?p=kor_2023_5952ef | not "find all f" (prove) |
| Moldova Mathematical Olympiad 2017, Clasa a XI-a, prima zi, 11.2. | https://mathnet.mit.edu/explorer.html?p=mda_2017_a580f8 | extra hypothesis: continuity |
| Moldova Mathematical Olympiad 2017, Clasa a X-a, ziua întâi, Problema 10.2 | https://mathnet.mit.edu/explorer.html?p=mda_2017_fb5096 | not a functional equation (inequality; given strictly monotone f, find g) |
| Moldova Mathematical Olympiad 2019, Clasa a X-a, 10.5 | https://mathnet.mit.edu/explorer.html?p=mda_2019_0acab7 | extra hypothesis: \|f(x)\| >= 1; division by 1 + f(x)f(y) |
| Moldova Mathematical Olympiad 2019, Ziua a doua, Clasa a XII-a, 12.5 | https://mathnet.mit.edu/explorer.html?p=mda_2019_29991a | not "find all f" (asks antiderivatives); domain not supported ((0, inf)); continuity; division by variable |
| Moldova Mathematical Olympiad 2019, Prima zi, 11. 3. | https://mathnet.mit.edu/explorer.html?p=mda_2019_d06e71 | domain and codomain differ (R+* -> R); extra hypothesis: continuity; division by variable |
| Moldova Mathematical Olympiad 2022, clasa a X-a, 10.4. | https://mathnet.mit.edu/explorer.html?p=mda_2022_276580 | not "find all f" (asks about zeros of functions in the solution set M) |
| Moldova Mathematical Olympiad 2022, Clasa a IX-a, Problema 9.2. | https://mathnet.mit.edu/explorer.html?p=mda_2022_fa7088 | extra hypothesis: f(0) > 0 |
| Moldova Mathematical Olympiad 2023, Clasa X-a, 10.5. | https://mathnet.mit.edu/explorer.html?p=mda_2023_b28f6a | not a functional equation (polynomial problem) |
| Moldova Mathematical Olympiad 2023, Prima zi, Clasa a IX-a, 9.4. | https://mathnet.mit.edu/explorer.html?p=mda_2023_bfcba9 | equation contains arbitrary real parameters a, b (not rational constants) |
| Moldova Mathematical Olympiad 2023, Clasa a XI-a. A doua zi, 11.8. | https://mathnet.mit.edu/explorer.html?p=mda_2023_e9dd66 | extra hypothesis: continuity |
| Middle European Mathematical Olympiad (MEMO) 2015, A, T-2 | https://mathnet.mit.edu/explorer.html?p=mem_2015_24b602 | domain not supported (R\{0} -> R\{0}) |
| Middle European Mathematical Olympiad (MEMO) 2015, A, I-1 | https://mathnet.mit.edu/explorer.html?p=mem_2015_36f8f1 | domain not supported (N -> N); extra hypothesis: surjective |
| Middle European Mathematical Olympiad (MEMO) 2016, Individual Competition, I-4 | https://mathnet.mit.edu/explorer.html?p=mem_2016_939071 | domain not supported (N -> N); divisibility |
| Middle European Mathematical Olympiad (MEMO) 2017, Team Competition, T - 1 | https://mathnet.mit.edu/explorer.html?p=mem_2017_69f90a | not a single equation in one function (pairs of polynomials P, Q) |
| Middle European Mathematical Olympiad (MEMO) 2018, Individual competition, I-1 | https://mathnet.mit.edu/explorer.html?p=mem_2018_ff0f0d | domain and codomain differ (Q+ -> (alpha, inf)); division by parameter alpha |
| Middle European Mathematical Olympiad (MEMO) 2022, T-7 | https://mathnet.mit.edu/explorer.html?p=mem_2022_1e9693 | domain not supported (N -> N); also monotonicity hypothesis and perfect-square conditions, not an equation |
| Middle European Mathematical Olympiad (MEMO) 2023, Team, T-1 | https://mathnet.mit.edu/explorer.html?p=mem_2023_54c451 | not "find all f" (largest number of distinct values; Z -> Z and Z>0 -> Z>0) |
| Middle European Mathematical Olympiad (MEMO) 2023, Individual, I-1 | https://mathnet.mit.edu/explorer.html?p=mem_2023_7aad50 | not an equation (inequality f(x)f(y) <= f(xy) + alpha x + beta y with parameters) |
| Middle European Mathematical Olympiad (MEMO) 2023, Individual, I-1 | https://mathnet.mit.edu/explorer.html?p=mem_2023_8fb709 | not an equation (inequality f(x)f(y) <= f(xy) + alpha x + beta y with parameters) |
| Middle European Mathematical Olympiad (MEMO) 2023, Team, T-1 | https://mathnet.mit.edu/explorer.html?p=mem_2023_f15ae9 | not "find all f" (largest number of distinct values; Z -> Z and Z>0 -> Z>0) |
| Balkan Mathematical Olympiad (BMO) 2008, State competition, IV year, 3 | https://mathnet.mit.edu/explorer.html?p=mkd_2008_6f2f5a | duplicate of seed problem s30 |
| International Mathematical Olympiad (IMO) 2008, 1 | https://mathnet.mit.edu/explorer.html?p=mkd_2008_7a2663 | domain not supported (N -> N); inequality and injectivity hypothesis |
| Balkan Mathematical Olympiad (BMO) 2009, IV година, 4Б. | https://mathnet.mit.edu/explorer.html?p=mkd_2009_e8804f | not "find all f" (prove f is periodic); also sqrt(2) coefficient |
| None 2010, Functional Equations, 13. | https://mathnet.mit.edu/explorer.html?p=mkd_2010_025fac | not "find all f" (asks for possible values of f(1)); parameter k |
| None 2010, Functional Equations, 12. | https://mathnet.mit.edu/explorer.html?p=mkd_2010_73f312 | domain not supported (f: R^2 -> R); extra hypothesis f(0,0) != 0 |
| International Mathematical Olympiad 2012, 3 | https://mathnet.mit.edu/explorer.html?p=mkd_2012_cd2a77 | not a single equation (inequality plus second condition with floor function) |
| Balkan Mathematical Olympiad (BMO) 2012, 4 | https://mathnet.mit.edu/explorer.html?p=mkd_2012_f9bf27 | domain not supported (Z+ -> Z+); factorial and divisibility conditions |
| IMO TST 2013, First day, 3 | https://mathnet.mit.edu/explorer.html?p=mkd_2013_3103d4 | domain not supported (Z* -> N0); two conditions including an inequality |
| European Mathematical Cup 2014, Junior Category, 4 | https://mathnet.mit.edu/explorer.html?p=mkd_2014_70c7ed | not a functional equation on R/Q (sequences of positive integers with extra condition) |
| European Mathematical Cup 2014, Senior Category, 4 | https://mathnet.mit.edu/explorer.html?p=mkd_2014_967fba | no complete solution: the MathNet solution stops before the answer, and the AoPS thread (https://artofproblemsolving.com/community/c6h617573) disputes the posted proofs |
| International Mathematical Olympiad (IMO) 2018, XXV Macedonian Mathematical Olympiad, 3 | https://mathnet.mit.edu/explorer.html?p=mkd_2018_1c4b6a | uses max/min (not supported operations) |
| Asia Pacific Mathematics Olympiad (APMO) 2018, 30th Asian-Pacific Mathematical Olympiad, 5 | https://mathnet.mit.edu/explorer.html?p=mkd_2018_b1584d | not a functional equation (polynomial problem) |
| IMO TST 2023, Day 1, 3 | https://mathnet.mit.edu/explorer.html?p=mkd_2023_6c8d01 | not "find all f" (smallest and largest value of f(2023)); N -> N, monotone |
| IMO TST 2023, Day 2, 4 | https://mathnet.mit.edu/explorer.html?p=mkd_2023_88c6ee | not "find all f" (prove f = 0); f: R^2 -> R |
| BMO TST 2023, 4 | https://mathnet.mit.edu/explorer.html?p=mkd_2023_e60ce8 | not "find all f" (prove statement); N -> N0 |
| Mediterranean Mathematical Olympiad, Day 2, 6 | https://mathnet.mit.edu/explorer.html?p=mkd_246e2c | domain not supported (N -> N); inequality and divisibility conditions |
| Mediterranean Mathematical Olympiad, Day 1, 2 | https://mathnet.mit.edu/explorer.html?p=mkd_83c332 | domain not supported (R+ -> R+) |
| International Mathematical Olympiad (IMO) 2007, Олон улсын математикийн 51-р олимпиад, ОУ-3 | https://mathnet.mit.edu/explorer.html?p=mng_2007_358049 | domain not supported (N -> N); perfect-square condition |
| International Mathematical Olympiad (IMO) 2007, Олон улсын математикийн 51-р олимпиад, ОУ-1 | https://mathnet.mit.edu/explorer.html?p=mng_2007_6a9a90 | floor function in equation |
| Mongolian Mathematical Olympiad 2009, 10th grade, 10.5 | https://mathnet.mit.edu/explorer.html?p=mng_2009_1086ab | domain and codomain differ (Q -> R) |
| International Mathematical Olympiad (IMO) 2012, I-сорил, I-2 | https://mathnet.mit.edu/explorer.html?p=mng_2012_359496 | not an equation (inequality; f: N -> R) |
| International Mathematical Olympiad (IMO) 2012, Бодлого 4 | https://mathnet.mit.edu/explorer.html?p=mng_2012_39d4d8 | domain not supported (Z -> Z); equation holds only on restricted values (a + b + c = 0) |
| International Mathematical Olympiad (IMO) 2012, IV-сорил, IV-2 | https://mathnet.mit.edu/explorer.html?p=mng_2012_585a2c | domain not supported (R+ -> R); square root and division |
| Mongolian Mathematical Olympiad 2013, Дундын багшийн III даваа, ДБ-В2 | https://mathnet.mit.edu/explorer.html?p=mng_2013_d1ddc2 | not a functional equation (polynomial problem: give example polynomials) |
| Mongolian Mathematical Olympiad 2014, Secondary school teachers, SST.5 | https://mathnet.mit.edu/explorer.html?p=mng_2014_721c0d | domain not supported (N -> N) |
| Mongolian Mathematical Olympiad 2014, TST 2, TST.2.1 | https://mathnet.mit.edu/explorer.html?p=mng_2014_d29d95 | extra hypothesis: continuity and f(0) = 0; inequalities, not an equation |
| IMO TST 2015, Test 1, TST-1.2 | https://mathnet.mit.edu/explorer.html?p=mng_2015_4260fb | not "find all f" (show f has a zero); continuity/boundedness hypotheses |
| Mongolian Mathematical Olympiad 2015, Grade 11, 11.3 | https://mathnet.mit.edu/explorer.html?p=mng_2015_abae02 | domain not supported (Z>=1 -> Z>=1); perfect-cube condition |
| IMO TST 2015, Test 2, TST-2.3 | https://mathnet.mit.edu/explorer.html?p=mng_2015_b1515f | not a single equation in one function (f and g); continuity hypothesis |
| Mongolian Mathematical Olympiad 2023, Round 3 F (Grades 11-12), F4 | https://mathnet.mit.edu/explorer.html?p=mng_2023_d1dc19 | not a single equation in one function (f: R -> R and h: R^2 -> R) |
| Mongolian Mathematical Olympiad 2024, T (Secondary School Teacher), T3 | https://mathnet.mit.edu/explorer.html?p=mng_2024_1f2a15 | domain not supported (R>0 -> R>0); two unknown functions and extra condition |
| Mongolian Mathematical Olympiad 2024, F (Grades 11-12), F4 | https://mathnet.mit.edu/explorer.html?p=mng_2024_8a9bc7 | not "find all f" (counting roots of good quadratic trinomials; polynomial problem) |
| Mongolian Mathematical Olympiad 2024, F (Grades 11-12), F3 | https://mathnet.mit.edu/explorer.html?p=mng_2024_ab8766 | domain not supported (R>0 -> R>0) |
| Mongolian Mathematical Olympiad 2024, T (Secondary School Teacher), T3 | https://mathnet.mit.edu/explorer.html?p=mng_2024_b28cbb | domain not supported (M_2(R) -> R) |
| Mongolian Mathematical Olympiad 2025, Category F (Grades 11-12), F3 | https://mathnet.mit.edu/explorer.html?p=mng_2025_66ba16 | not "find all f" (possible values of f(2024)); N -> N |
| Mongolian Mathematical Olympiad 2025, Category F (Grades 11-12), F6 | https://mathnet.mit.edu/explorer.html?p=mng_2025_7bd594 | domain not supported (R>0 -> R>0) |
| IMO TST 2006, Opgave 4. | https://mathnet.mit.edu/explorer.html?p=nld_2006_1c67af | domain not supported (R>0 -> R); extra hypothesis f(a) = 1; division by a variable |
| IMO TST 2008, Valkenswaard, 1. | https://mathnet.mit.edu/explorer.html?p=nld_2008_f1f591 | domain not supported (Z>0 -> Z>0) |
| IMO TST 2009, Opgave 4 | https://mathnet.mit.edu/explorer.html?p=nld_2009_bd0109 | domain not supported (Z -> Z) |
| IMO TST 2010, toets maart 2010, 2 | https://mathnet.mit.edu/explorer.html?p=nld_2010_a84c2f | duplicate of seed problem s33 |
| Dutch Mathematical Olympiad 2010, Opgave 2. | https://mathnet.mit.edu/explorer.html?p=nld_2010_cbe1d3 | uses max over y (not supported operation) |
| Netherlands IMO TST 2012, Opgave 5. | https://mathnet.mit.edu/explorer.html?p=nld_2012_9bf62c | duplicate of ukraine-2009-10-4 (Ukrainian Mathematical Olympiad 2009, Fourth Round, First Day, 10-th grade, 10.4), which is kept |
| IMO TST 2014, Opgave 2 | https://mathnet.mit.edu/explorer.html?p=nld_2014_611498 | domain not supported (R \ {0} -> R) |
| IMO TST 2014, 1 | https://mathnet.mit.edu/explorer.html?p=nld_2014_bcacea | not "find all f" (compute a value); f: Z>0 -> R |
| IMO TST 2015, Opgave 5. | https://mathnet.mit.edu/explorer.html?p=nld_2015_3130dc | domain not supported (Z>0 -> Z>0); divisibility condition, f(1) = 2 |
| IMO TST 2015, Opgave 5 | https://mathnet.mit.edu/explorer.html?p=nld_2015_d15aef | answer is not a rational polynomial (solutions include \|x\| and -\|x\|) |
| Netherlands IMO TST 2016, Opgave 4 | https://mathnet.mit.edu/explorer.html?p=nld_2016_416931 | duplicate of thailand-2014-2 (Thailand Mathematical Olympiad 2014, 2), which is kept |
| Netherlands IMO TST 2017, Opgave 4 | https://mathnet.mit.edu/explorer.html?p=nld_2017_543ee9 | duplicate of switzerland-2015-3 (Swiss Mathematical Olympiad 2015, 3.), which is kept |
| IMO TST 2017, Uitwerkingen, Opgave 2 | https://mathnet.mit.edu/explorer.html?p=nld_2017_fb271b | not "find all f" (find smallest n with f(n) = n); Z>0 -> Z |
| IMO TST 2018, Opgave 2. | https://mathnet.mit.edu/explorer.html?p=nld_2018_155add | not an equation (inequality) |
| IMO TST 2018, 4 | https://mathnet.mit.edu/explorer.html?p=nld_2018_a0afe0 | not "find all f" (prove property of a set of functions) |
| IMO TST 2019, Opgave 4. | https://mathnet.mit.edu/explorer.html?p=nld_2019_9e2fd5 | domain not supported (Z -> Z); divisibility conditions |
| IMO TST 2019, Uitwerkingen, Opgave 3. | https://mathnet.mit.edu/explorer.html?p=nld_2019_bcc966 | domain not supported (Z -> Z); inequality condition |
| IMO TST 2020, Opgave 3. | https://mathnet.mit.edu/explorer.html?p=nld_2020_202377 | domain not supported (Z -> Z) |
| IMO TST 2020, Opgave 3. | https://mathnet.mit.edu/explorer.html?p=nld_2020_6c3d8b | answer is not a rational polynomial (solutions include f(x) = 2\|x\|) |
| BxMO/EGMO TST 2020, 3 | https://mathnet.mit.edu/explorer.html?p=nld_2020_6d682b | answer is not a rational polynomial (solutions include f(x) = 2\|x\|) |
| IMO TST 2020, 3 | https://mathnet.mit.edu/explorer.html?p=nld_2020_9abdf8 | domain not supported (Z -> Z) |
| IMO TST 2020, Opgave 2. | https://mathnet.mit.edu/explorer.html?p=nld_2020_b51ecf | not a functional equation (polynomial problem) |
| IMO TST 2021, 2 | https://mathnet.mit.edu/explorer.html?p=nld_2021_38b159 | duplicate MathNet record of Dutch IMO TST 2021 (netherlands-tst-2021-3, kept); the solution attached here belongs to another problem |
| BxMO/EGMO TST 2022, 1. | https://mathnet.mit.edu/explorer.html?p=nld_2022_13f9f0 | domain not supported (Z>0 -> Z>0); divisibility condition |
| IMO TST 2022, Opgave 1. | https://mathnet.mit.edu/explorer.html?p=nld_2022_b08ef4 | domain not supported (Z>0 -> Z>0); divisibility condition |
| Dutch Junior Mathematical Olympiad 2022, Part 1, 8 | https://mathnet.mit.edu/explorer.html?p=nld_2022_f71f53 | not a functional equation (multiple-choice puzzle) |
| BxMO/EGMO TST 2023, 2 | https://mathnet.mit.edu/explorer.html?p=nld_2023_0ab3dd | not an equation (inequality); four variables |
| IMO TST 2023, 2 | https://mathnet.mit.edu/explorer.html?p=nld_2023_38e6a0 | not an equation (inequality); four variables |
| IMO TST 2023, Opgave 4. | https://mathnet.mit.edu/explorer.html?p=nld_2023_631142 | domain not supported (Q+ -> Q); division by a variable |
| IMO TST 2024, Opgave 2. | https://mathnet.mit.edu/explorer.html?p=nld_2024_0bbced | domain not supported (R>=0 -> R); inequality |
| IMO TST 2024, Opgave 2. | https://mathnet.mit.edu/explorer.html?p=nld_2024_5690fb | domain not supported (Z>0 -> Z>0); two conditions |
| IMO TST 2024, 2 | https://mathnet.mit.edu/explorer.html?p=nld_2024_8c2ba3 | domain not supported (Z>0 -> Z>0); two conditions |
| BxMO/EGMO TST 2024, 3 | https://mathnet.mit.edu/explorer.html?p=nld_2024_d7b884 | not "find all f" (find pairs (a, b) with iterated f) |
| IMO TST 2024, 2 | https://mathnet.mit.edu/explorer.html?p=nld_2024_eb3985 | domain not supported (R>=0 -> R); inequality |
| Dutch Mathematical Olympiad 2024, Opgave 3. | https://mathnet.mit.edu/explorer.html?p=nld_2024_f275aa | not "find all f" (find pairs (a, b) with iterated f) |
| IMO TST 2025, 4 | https://mathnet.mit.edu/explorer.html?p=nld_2025_951e3a | domain not supported (Z>0 -> Z>0); perfect-square condition |
| IMO TST 2025, Opgave 4. | https://mathnet.mit.edu/explorer.html?p=nld_2025_fa2053 | domain not supported (Z>0 -> Z>0); perfect-square condition |
| Nordic Mathematical Contest (NMC) 1987, 87.3. | https://mathnet.mit.edu/explorer.html?p=nmo_1987_9415bf | not "find all f" (smallest possible value of f(2)); N, increasing |
| Nordic Mathematical Contest (NMC) 1993, 93.1. | https://mathnet.mit.edu/explorer.html?p=nmo_1993_bbcc19 | not "find all f" (compute values); domain [0,1], increasing |
| Nordic Mathematical Contest (NMC) 1996, 96.4. | https://mathnet.mit.edu/explorer.html?p=nmo_1996_fff178 | not "find all f" (prove periodicity / find smallest a); positive integers |
| Nordic Mathematical Contest (NMC) 1997, 97.4. | https://mathnet.mit.edu/explorer.html?p=nmo_1997_c2becd | not "find all f" (prove injectivity); non-negative integers |
| Nordic Mathematical Contest (NMC) 1998, 98.1. | https://mathnet.mit.edu/explorer.html?p=nmo_1998_88959b | duplicate of seed problem s45 |
| Nordic Mathematical Contest (NMC) 2000, 00.4. | https://mathnet.mit.edu/explorer.html?p=nmo_2000_f05931 | not "find all f" (prove bounds); domain [0,1], inequality |
| Nordic Mathematical Contest (NMC) 2001, 01.2. | https://mathnet.mit.edu/explorer.html?p=nmo_2001_e895cd | not "find all f" (prove periodicity); boundedness hypothesis |
| Nordic Mathematical Contest (NMC) 2003, 03.4. | https://mathnet.mit.edu/explorer.html?p=nmo_2003_5f9e08 | domain not supported (R* -> R*); equation holds only on restricted values (x + y != 0) |
| Nordic Mathematical Contest (NMC) 2008, 08.1. | https://mathnet.mit.edu/explorer.html?p=nmo_2008_97e2dd | not "find all f" (determine constants A, B, C) |
| Nordic Mathematical Contest (NMC) 2010, 10.1. | https://mathnet.mit.edu/explorer.html?p=nmo_2010_80ca28 | not "find all f" (prove inequality); Z -> Z+ |
| Nordic Mathematical Contest (NMC) 2014, Problem 1 | https://mathnet.mit.edu/explorer.html?p=nmo_2014_962731 | domain not supported (N -> N); equation holds only on restricted values (x >= y) |
| Nordic Mathematical Contest (NMC) 2016, Problem 3 | https://mathnet.mit.edu/explorer.html?p=nmo_2016_d3b0bd | not "find all f" (asks for values of a; two equations) |
| Nordic Mathematical Contest (NMC) 2021, Problem 2 | https://mathnet.mit.edu/explorer.html?p=nmo_2021_677e33 | not "find all f satisfying an equation" (inequality, absolute value) |
| Nordic Mathematical Contest (NMC) 2022, Problem 1 | https://mathnet.mit.edu/explorer.html?p=nmo_2022_fee2e2 | not a single equation in one function (two equations) |
| Philippine Mathematical Olympiad (PMO), Part II, 3. | https://mathnet.mit.edu/explorer.html?p=phl_1624c2 | not "find all f" (asks for f(2011)); division by f |
| Philippine Mathematical Olympiad (PMO) 2007, Area Stage, 16. | https://mathnet.mit.edu/explorer.html?p=phl_2007_8911b7 | not a functional equation (iterate of a given function, solve for x) |
| Philippine Mathematical Olympiad (PMO) 2008, National Stage: 15-Second Round, 15.10. | https://mathnet.mit.edu/explorer.html?p=phl_2008_dcdba9 | not "find all f" (asks for f(2007)); domain not supported (positive integers); extra hypothesis: f(1)=2 |
| Philippine Mathematical Olympiad (PMO) 2009, Part I, 19. | https://mathnet.mit.edu/explorer.html?p=phl_2009_336fcc | domain not supported (positive reals); division by a variable; extra hypothesis: f(2009)=1 |
| Philippine Mathematical Olympiad (PMO) 2010, Part I, 15. | https://mathnet.mit.edu/explorer.html?p=phl_2010_ec9bd2 | not "find all f" (asks for x); domain not supported (complex numbers) |
| Philippine Mathematical Olympiad (PMO) 2011, National Stage, Oral Phase, 14. | https://mathnet.mit.edu/explorer.html?p=phl_2011_0ce09b | not "find all f" (asks for graph intersection); extra hypothesis: f(1)=-1 |
| Philippine Mathematical Olympiad (PMO) 2012, National Stage - Written Phase, 3 | https://mathnet.mit.edu/explorer.html?p=phl_2012_1fd0b8 | domain not supported (R\{1}); division by a variable |
| Philippine Mathematical Olympiad (PMO) 2012, National Stage - Oral Phase, 15.5 | https://mathnet.mit.edu/explorer.html?p=phl_2012_a64617 | not "find all f" (asks for a value); extra hypothesis: f never zero |
| Philippine Mathematical Olympiad (PMO) 2016, PART I, 2. | https://mathnet.mit.edu/explorer.html?p=phl_2016_1fe54f | not "find all f" (asks for f(2016)-f(2013)); extra hypothesis: f(0)=3 |
| Philippine Mathematical Olympiad (PMO) 2016, EASY, 2. | https://mathnet.mit.edu/explorer.html?p=phl_2016_65c19f | not "find all f" (asks for f(0)) |
| Philippine Mathematical Olympiad (PMO) 2016, PART II, 3. | https://mathnet.mit.edu/explorer.html?p=phl_2016_c8d42b | domain not supported (N); not "find all f" (least value of g(2016)); inequality condition |
| Philippine Mathematical Olympiad (PMO) 2019, EASY, 14. | https://mathnet.mit.edu/explorer.html?p=phl_2019_70f83f | not "find all f" (asks for f(4)); equation holds only on restricted values (nonzero x,y); division by a variable |
| Philippine Mathematical Olympiad (PMO) 2021, National Stage, Written Phase (Day 1), 3. | https://mathnet.mit.edu/explorer.html?p=phl_2021_fb69af | domain and codomain differ (Q+ -> Q); not "find all f" |
| Philippine Mathematical Olympiad (PMO) 2023, National Stage (Day 2), 8. | https://mathnet.mit.edu/explorer.html?p=phl_2023_f1a76f | domain not supported (points of the plane) |
| Philippine Mathematical Olympiad (PMO), PART I., 18. | https://mathnet.mit.edu/explorer.html?p=phl_50470b | not "find all f" (asks for maximum value of f) |
| Philippine Mathematical Olympiad (PMO), PART II, 8. | https://mathnet.mit.edu/explorer.html?p=phl_f98691 | not "find all f" (asks for f(1)-f(-1)); domain not supported (R\{0}); division |
| Balkan Mathematical Olympiad (BMO) 2004, 1. | https://mathnet.mit.edu/explorer.html?p=rou_2004_382714 | not a functional equation (sequence problem) |
| Romanian Mathematical Olympiad Shortlist 2010, Putnam Seniors, 20. | https://mathnet.mit.edu/explorer.html?p=rou_2010_11f74c | not "find all f" (prove differentiability); exponential |
| Romanian Mathematical Olympiad 2010, District Round, Problem 4. | https://mathnet.mit.edu/explorer.html?p=rou_2010_179ac6 | domain not supported (N*) |
| Romanian Mathematical Olympiad 2010, District Round, Problem 3. | https://mathnet.mit.edu/explorer.html?p=rou_2010_4adc43 | domain not supported (N) |
| Romanian Mathematical Olympiad Shortlist 2010, Putnam Seniors, 22. | https://mathnet.mit.edu/explorer.html?p=rou_2010_6957ae | extra hypothesis: continuity; existential parameter b |
| Romanian Mathematical Olympiad 2010, District Round, Problem 3. | https://mathnet.mit.edu/explorer.html?p=rou_2010_8d9570 | not "find all f" (prove continuity) |
| Romanian Mathematical Olympiad 2010, Final Round, Problem 4. | https://mathnet.mit.edu/explorer.html?p=rou_2010_b64dd3 | domain not supported (N) |
| Romanian Mathematical Olympiad 2010, District Round, Problem 1. | https://mathnet.mit.edu/explorer.html?p=rou_2010_dc7094 | not a functional equation (prove representation of piecewise linear function) |
| Romanian Mathematical Olympiad 2011, DISTRICT ROUND, 3 | https://mathnet.mit.edu/explorer.html?p=rou_2011_3689ee | not "find all f" (prove an inequality); floor |
| Romanian Mathematical Olympiad 2011, DISTRICT ROUND, 4 | https://mathnet.mit.edu/explorer.html?p=rou_2011_3fdd31 | domain not supported ([0,1]); inequality |
| Romanian Mathematical Olympiad Shortlist 2011, PUTNAM SENIORS, 5 | https://mathnet.mit.edu/explorer.html?p=rou_2011_4ad267 | not "find all f" (prove); inequality |
| Romanian Mathematical Olympiad Shortlist 2011, PUTNAM SENIORS, 6 | https://mathnet.mit.edu/explorer.html?p=rou_2011_604d78 | extra hypothesis: continuity; min/max not expressible |
| Clock-Tower School Competition 2011, 2 | https://mathnet.mit.edu/explorer.html?p=rou_2011_7de60f | not "find all f" (prove f is additive) |
| Romanian Mathematical Olympiad Shortlist 2011, SENIORS, 5 | https://mathnet.mit.edu/explorer.html?p=rou_2011_a8bd0a | domain and codomain differ (Z -> N); second condition (perfect square) |
| Romanian Mathematical Olympiad 2011, FINAL ROUND, 1 | https://mathnet.mit.edu/explorer.html?p=rou_2011_c50eec | not "find all f" (inequality; prove and give example) |
| Romanian Master of Mathematics (RMM) 2011, FIRST DAY, 1 | https://mathnet.mit.edu/explorer.html?p=rou_2011_e62df4 | not "find all f" (existence of two functions) |
| Romanian Mathematical Olympiad 2011, FINAL ROUND, 3 | https://mathnet.mit.edu/explorer.html?p=rou_2011_efbd80 | not "find all f" (prove nonexistence of iterative roots) |
| Romanian Mathematical Olympiad 2012, CLASA a X-a, Problema 3. | https://mathnet.mit.edu/explorer.html?p=rou_2012_8b4730 | not a functional equation (injective iff surjective for a given function) |
| Romanian Mathematical Olympiad 2013, 7th GRADE, 2 | https://mathnet.mit.edu/explorer.html?p=rou_2013_062648 | not a functional equation (find a, b; absolute values) |
| Romanian Mathematical Olympiad 2013, X. OSZTÁLY, 3. feladat | https://mathnet.mit.edu/explorer.html?p=rou_2013_0d1a13 | not a functional equation (injective iff surjective for a given function) |
| Balkan Mathematical Olympiad TST (BMO TST) 2013, First Selection Test, 3 | https://mathnet.mit.edu/explorer.html?p=rou_2013_17e728 | domain not supported (positive integers); not an equation (sum condition) |
| Romanian Mathematical Olympiad 2013, 10th GRADE, 3 | https://mathnet.mit.edu/explorer.html?p=rou_2013_2d13dc | domain not supported (Z); inequality; extra hypothesis: injective |
| Romanian Mathematical Olympiad 2013, 9th GRADE, 4 | https://mathnet.mit.edu/explorer.html?p=rou_2013_4e1c4f | not a functional equation (fixed points of a given function on N) |
| Romanian Mathematical Olympiad 2013, 12th GRADE, 1 | https://mathnet.mit.edu/explorer.html?p=rou_2013_58fc46 | extra hypothesis: continuity; integral equation |
| Romanian Mathematical Olympiad 2013, CLASA a XI-a, Problema 3 | https://mathnet.mit.edu/explorer.html?p=rou_2013_616aa9 | not "find all f" (prove); domain not supported ((0,inf)) |
| Balkan Mathematical Olympiad TST (BMO TST) 2013, Fourth Selection Test, 15 | https://mathnet.mit.edu/explorer.html?p=rou_2013_720f3d | not a functional equation (polynomial problem, complex coefficients) |
| Romanian Mathematical Olympiad 2013, CLASA a IX-a, Problema 2 | https://mathnet.mit.edu/explorer.html?p=rou_2013_b1dc94 | not "find all f" (prove f = g) |
| Balkan Mathematical Olympiad (BMO) 2013, Problem 3 | https://mathnet.mit.edu/explorer.html?p=rou_2013_b362ad | domain not supported (positive reals, function of three variables); three conditions |
| Romanian Mathematical Olympiad 2013, Problema 5 | https://mathnet.mit.edu/explorer.html?p=rou_2013_cae896 | not "find all f" (prove f(x)=x); domain and codomain differ (Q>0 -> R); inequalities |
| Romanian Mathematical Olympiad 2013, 10th GRADE, 3 | https://mathnet.mit.edu/explorer.html?p=rou_2013_ecd87e | not a functional equation (injective iff surjective for a given function) |
| Romanian Mathematical Olympiad 2014, Final Round, Problem 1. | https://mathnet.mit.edu/explorer.html?p=rou_2014_329a47 | extra hypothesis: continuity; monotonicity conditions, no equation |
| Romanian Mathematical Olympiad 2014, District Round, Problem 2. | https://mathnet.mit.edu/explorer.html?p=rou_2014_392d92 | not "find all f" (prove continuity / give example) |
| Romanian Mathematical Olympiad Shortlist 2014, Seniors, 5. | https://mathnet.mit.edu/explorer.html?p=rou_2014_6240a4 | domain and codomain differ (R -> (0,inf)); inequalities |
| Romanian Mathematical Olympiad 2014, Final Round, Problem 2. | https://mathnet.mit.edu/explorer.html?p=rou_2014_bd00d5 | extra hypothesis: differentiable |
| Romanian Mathematical Olympiad Shortlist 2014, Putnam Seniors, 4. | https://mathnet.mit.edu/explorer.html?p=rou_2014_de58f9 | extra hypothesis: differentiable, bounded derivative; derivative and max in equation |
| Romanian Mathematical Olympiad 2014, Final Round, Problem 2. | https://mathnet.mit.edu/explorer.html?p=rou_2014_efa32b | not "find all f" (prove inequality); domain not supported (N*) |
| Romanian Mathematical Olympiad 2015, DISTRICT ROUND - 10th GRADE, Problem 4 | https://mathnet.mit.edu/explorer.html?p=rou_2015_0bfeee | not "find all f" (prove); domain not supported ((0,inf)) |
| Romanian Mathematical Olympiad 2015, Etapa Judeţeană şi a Municipiului Bucureşti, Clasa a XII-a, Problem 3 | https://mathnet.mit.edu/explorer.html?p=rou_2015_12f3b2 | domain not supported ([0,inf)); extra hypothesis: continuous, increasing; integral inequality |
| Romanian Mathematical Olympiad 2015, DISTRICT ROUND - 9th GRADE, Problem 4 | https://mathnet.mit.edu/explorer.html?p=rou_2015_18009b | domain not supported (N*); gcd/lcm |
| Romanian Mathematical Olympiad 2015, DISTRICT ROUND - 12th GRADE, Problem 3 | https://mathnet.mit.edu/explorer.html?p=rou_2015_4167ef | domain not supported ([0,inf)); extra hypothesis: continuous, increasing; integrals |
| Romanian Mathematical Olympiad 2015, CLASA a X-a, Problema 4 | https://mathnet.mit.edu/explorer.html?p=rou_2015_472258 | not "find all f" (prove); domain not supported ((0,inf)) |
| Romanian Mathematical Olympiad 2015, DISTRICT ROUND - 9th GRADE, Problem 2 | https://mathnet.mit.edu/explorer.html?p=rou_2015_6a4d28 | not a functional equation (find a, b; floor) |
| Junior Balkan Mathematical Olympiad TST (JBMO TST) 2015, THIRD SELECTION TEST, Problem 11 | https://mathnet.mit.edu/explorer.html?p=rou_2015_d65487 | not a functional equation (system of equations in x, y, z) |
| Romanian Mathematical Olympiad 2015, CLASA a XI-a, Problem 1 | https://mathnet.mit.edu/explorer.html?p=rou_2015_f899e2 | not "find all f" (prove / example); domain not supported ([0,1]) |
| Romanian Mathematical Olympiad 2015, FINAL ROUND - 10th GRADE, Problem 3 | https://mathnet.mit.edu/explorer.html?p=rou_2015_fe5b4f | not a single equation in one function (two unknown functions, two equations) |
| Romanian Mathematical Olympiad 2016, District Round, 11th Grade, Problem 3. | https://mathnet.mit.edu/explorer.html?p=rou_2016_2068f0 | not "find all f satisfying an equation" (inequality); extra hypothesis: continuity |
| Romanian Mathematical Olympiad 2016, District Round, 10th Grade, Problem 4. | https://mathnet.mit.edu/explorer.html?p=rou_2016_2a27a2 | not "find all f" (prove existence / periodicity); sqrt coefficients |
| Romanian Mathematical Olympiad 2016, CLASA A X-A, 3. | https://mathnet.mit.edu/explorer.html?p=rou_2016_2bf0a4 | not "find all f" (prove); domain not supported ((0,inf)) |
| Romanian Mathematical Olympiad 2016, Etapa Judeţeană şi a Municipiului Bucureşti, CLASA a X-a, Problema 4 | https://mathnet.mit.edu/explorer.html?p=rou_2016_2f0898 | not "find all f" (prove existence / periodicity); sqrt coefficients |
| Romanian Mathematical Olympiad 2016, Etapa Locală, Clasa a -X-a, 4. | https://mathnet.mit.edu/explorer.html?p=rou_2016_354610 | not a functional equation (finite sets, injectivity) |
| IMO TST 2016, Fifth Selection Test, Problem 17. | https://mathnet.mit.edu/explorer.html?p=rou_2016_5fec63 | domain not supported (positive integers); divisibility and inequality |
| Romanian Mathematical Olympiad 2016, Final Round, 9th Grade, Problem 20. | https://mathnet.mit.edu/explorer.html?p=rou_2016_6e9f46 | not "find all f satisfying an equation" (inequality) |
| Romanian Mathematical Olympiad Shortlist 2016, Seniors, 5. | https://mathnet.mit.edu/explorer.html?p=rou_2016_a51180 | not a functional equation (prove bijectivity; floor) |
| Romanian Mathematical Olympiad 2016, CLASA A XII-A (M 4 ore) - ETAPA LOCALĂ, SUBIECTUL I | https://mathnet.mit.edu/explorer.html?p=rou_2016_bdc1ec | not a functional equation (group theory / composition law) |
| Romanian Mathematical Olympiad Shortlist 2016, Putnam Seniors, 4. | https://mathnet.mit.edu/explorer.html?p=rou_2016_bfd249 | not "find all f satisfying an equation" (inequality, absolute value) |
| Romanian Mathematical Olympiad 2016, Final Round, 11th Grade, Problem 28. | https://mathnet.mit.edu/explorer.html?p=rou_2016_d884a4 | extra hypothesis: differentiable; differential equation |
| Romanian Mathematical Olympiad 2016, Clasa a X-a, Subiectul IV. | https://mathnet.mit.edu/explorer.html?p=rou_2016_e6fcbf | extra hypothesis: bijective |
| Romanian Mathematical Olympiad Shortlist 2016, Putnam Seniors, 3. | https://mathnet.mit.edu/explorer.html?p=rou_2016_fcf4c5 | not "find all f" (inequality; example / prove convexity) |
| Romanian Mathematical Olympiad Shortlist 2017, SENIORS, 6. | https://mathnet.mit.edu/explorer.html?p=rou_2017_16cbdf | no solution: the MathNet record has none and no AoPS thread was found |
| Romanian Mathematical Olympiad 2017, Final Round - 11th Grade, Problem 1 | https://mathnet.mit.edu/explorer.html?p=rou_2017_6bacef | not "find all f" (prove continuity) |
| Romanian Mathematical Olympiad Shortlist 2017, PUTNAM SENIORS, 1. | https://mathnet.mit.edu/explorer.html?p=rou_2017_8737a8 | not "find all f" (prove); two functions; domain not supported ([0,inf)) |
| Romanian Mathematical Olympiad 2017, Final Round - 10th Grade, Problem 4 | https://mathnet.mit.edu/explorer.html?p=rou_2017_bd3f45 | not a functional equation (counting functions on finite sets) |
| Romanian Mathematical Olympiad 2017, District Round - 11th Grade, Problem 2 | https://mathnet.mit.edu/explorer.html?p=rou_2017_edf510 | not "find all f" (existence / prove); two functions |
| Romanian Mathematical Olympiad 2017, Final Round - 10th Grade, Problem 1 | https://mathnet.mit.edu/explorer.html?p=rou_2017_f719f2 | not a functional equation (equation in x) |
| Romanian Mathematical Olympiad 2018, CLASA a XI-a, Problema 3 | https://mathnet.mit.edu/explorer.html?p=rou_2018_1f749b | not "find all f" (prove continuity) |
| Romanian Mathematical Olympiad Shortlist 2018, Putnam Seniors, 6 | https://mathnet.mit.edu/explorer.html?p=rou_2018_523766 | not "find all f" (prove integral inequality); domain not supported ([0,inf)) |
| Romanian Mathematical Olympiad Shortlist 2018, Putnam Seniors, 2 | https://mathnet.mit.edu/explorer.html?p=rou_2018_75978a | not "find all f" (prove common fixed point) |
| Romanian Mathematical Olympiad 2018, 11th Grade, 3 | https://mathnet.mit.edu/explorer.html?p=rou_2018_bb955c | not "find all f" (prove continuity) |
| Romanian Mathematical Olympiad 2018, District Round - 9th Grade, 1 | https://mathnet.mit.edu/explorer.html?p=rou_2018_c37e27 | domain not supported (N); divisibility condition; extra hypothesis: increasing |
| Romanian Mathematical Olympiad 2019, FINAL ROUND - 9th GRADE, Problem 4. | https://mathnet.mit.edu/explorer.html?p=rou_2019_7c6eb0 | not "find all f satisfying an equation" (inequality) |
| Romanian Mathematical Olympiad 2019, DISTRICT ROUND - 10th GRADE, Problem 1. | https://mathnet.mit.edu/explorer.html?p=rou_2019_8853a0 | domain and codomain differ (R -> (0,inf)); inequality; division |
| Romanian Mathematical Olympiad Shortlist 2019, SENIORS, 4. | https://mathnet.mit.edu/explorer.html?p=rou_2019_8aa089 | no solution: the MathNet record has none and no AoPS thread was found |
| Romanian Mathematical Olympiad 2019, FINAL ROUND - 11th GRADE, Problem 2. | https://mathnet.mit.edu/explorer.html?p=rou_2019_93c7d9 | not "find all f" (prove f is constant) |
| Danube Mathematical Competition 2019, SENIOR LEVEL, Problem 2. | https://mathnet.mit.edu/explorer.html?p=rou_2019_aef057 | extra hypothesis: monotone (nondecreasing) |
| Romanian Mathematical Olympiad Shortlist 2019, PUTNAM SENIORS, 2. | https://mathnet.mit.edu/explorer.html?p=rou_2019_b015ab | not "find all f" (prove); domain not supported (f: (0, inf) -> R); extra hypothesis: differentiable |
| Romanian Mathematical Olympiad 2019, FINAL ROUND - 11th GRADE, Problem 3. | https://mathnet.mit.edu/explorer.html?p=rou_2019_bbf84d | not "find all f" (existence/nonexistence of differentiable f with f(f'(x)) = x) |
| IMO TST 2019, THIRD SELECTION TEST, Problem 11. | https://mathnet.mit.edu/explorer.html?p=rou_2019_bd7636 | domain not supported (non-negative integers); equation holds only on restricted values (2ab = c^2 + d^2) |
| Romanian Mathematical Olympiad 2020, 12th GRADE, Problem 2. | https://mathnet.mit.edu/explorer.html?p=rou_2020_0e26ca | equation uses an integral; extra hypothesis: integrable |
| Romanian Master of Mathematics (RMM) 2020, SECOND DAY, Problem 4. | https://mathnet.mit.edu/explorer.html?p=rou_2020_31b81f | domain not supported (N); not a functional equation (sum-free sets condition), extra hypothesis: surjective |
| Romanian Mathematical Olympiad 2020, 11th GRADE, Problem 3. | https://mathnet.mit.edu/explorer.html?p=rou_2020_7a8b8e | extra hypothesis: continuous; condition is existential in t, not an equation for all variables |
| Romanian Mathematical Olympiad 2020, 10th GRADE, Problem 2. | https://mathnet.mit.edu/explorer.html?p=rou_2020_7cb085 | not "find all f" (equation depends on parameter n; asks to show solutions exist iff n = 2) |
| Balkan Mathematical Olympiad 2020, Problem 2. | https://mathnet.mit.edu/explorer.html?p=rou_2020_ed3b79 | domain not supported (positive integers); not a functional equation (perfect square/divisibility conditions) |
| Gazeta Matematică National Olympiad 2021, Etapa a III-a - clasa a IX-a, Problema 4. | https://mathnet.mit.edu/explorer.html?p=rou_2021_647221 | domain and codomain differ (f: N -> finite set A); absolute value |
| Gazeta Matematică National Olympiad 2021, clasa a X-a, Problema 4. | https://mathnet.mit.edu/explorer.html?p=rou_2021_798924 | not a single equation in one function (two unknown functions f, g, parameter a) |
| Gazeta Matematică National Olympiad 2021, clasa a X-a, Problema 2. | https://mathnet.mit.edu/explorer.html?p=rou_2021_874d6c | not "find all f" (prove equivalence about a given floor function) |
| Romanian Mathematical Olympiad 2022, CLASA a IX-a, Problema 3 | https://mathnet.mit.edu/explorer.html?p=rou_2022_bb0b19 | not a single equation in one function (auxiliary function g); floor function |
| Romanian Mathematical Olympiad Shortlist 2023, PUTNAM SENIORS, 1 | https://mathnet.mit.edu/explorer.html?p=rou_2023_1adb85 | not "find all f" (prove); extra hypothesis: continuous |
| Romanian Mathematical Olympiad 2023, 9th GRADE, 2 | https://mathnet.mit.edu/explorer.html?p=rou_2023_244bb1 | not a functional equation (inequality) |
| Romanian Master of Mathematics (RMM) 2023, SECOND DAY, 5 | https://mathnet.mit.edu/explorer.html?p=rou_2023_494d94 | not a functional equation (polynomial problem, prove) |
| Romanian Mathematical Olympiad 2023, 12th GRADE, 3 | https://mathnet.mit.edu/explorer.html?p=rou_2023_6490ce | domain not supported ([a, b]); not "find all f" (prove uniqueness); extra hypothesis: integrable |
| Romanian Mathematical Olympiad 2023, 9th GRADE, 4 | https://mathnet.mit.edu/explorer.html?p=rou_2023_6f7bfb | domain not supported (N); divisibility condition; extra hypothesis: strictly increasing |
| Romanian Mathematical Olympiad 2023, 11th GRADE, 1 | https://mathnet.mit.edu/explorer.html?p=rou_2023_77c578 | extra hypothesis: continuous, f(1) = e; exponential in equation |
| Romanian Mathematical Olympiad 2023, 12th GRADE, 4 | https://mathnet.mit.edu/explorer.html?p=rou_2023_8c011c | domain not supported ([0, inf)); three unknown functions; absolute value |
| IMO TST 2023, 3 | https://mathnet.mit.edu/explorer.html?p=rou_2023_e36372 | not "find all f" (asks for real numbers r) |
| Romanian Mathematical Olympiad 2024, District Round, Problem 4. | https://mathnet.mit.edu/explorer.html?p=rou_2024_458879 | extra hypothesis: f(x) = 0 has a unique solution; equation depends on parameter n |
| Romanian Mathematical Olympiad 2024, Final Round, Problem 4. | https://mathnet.mit.edu/explorer.html?p=rou_2024_64d15c | not "find all f" (prove continuity / give example) |
| Romanian Mathematical Olympiad Shortlist 2024, Seniors, 6. | https://mathnet.mit.edu/explorer.html?p=rou_2024_64fc46 | not a single equation in one function (two unknown functions f, g, parameter a) |
| Romanian Mathematical Olympiad 2025, Final Round - 10th GRADE, Problem 3 | https://mathnet.mit.edu/explorer.html?p=rou_2025_4adb80 | domain not supported (Z); not a functional equation (product of injective functions) |
| Romanian Mathematical Olympiad 2025, Final Round - 11th GRADE, Problem 1 | https://mathnet.mit.edu/explorer.html?p=rou_2025_5a3274 | not a single equation in one function (two functions, derivatives); extra hypothesis: twice differentiable |
| Romanian Mathematical Olympiad 2025, District Round - 10th GRADE, Problem 3 | https://mathnet.mit.edu/explorer.html?p=rou_2025_bf76a3 | domain not supported (C); absolute value |
| Romanian Mathematical Olympiad 2025, Shortlisted Problems - PUTNAM SENIORS, 3. | https://mathnet.mit.edu/explorer.html?p=rou_2025_c55311 | extra hypothesis: continuous, surjective; not an equation (arithmetic progression condition) |
| Romanian Mathematical Olympiad 2025, Shortlisted Problems - SENIORS, 7. | https://mathnet.mit.edu/explorer.html?p=rou_2025_e3b629 | domain not supported ((0, inf)); exponentiation by f(y) |
| Romanian Master of Mathematics (RMM) 2025, SECOND DAY, Problem 4. | https://mathnet.mit.edu/explorer.html?p=rou_2025_fb3b41 | domain not supported (integers >= 10^100) and codomain differs (Z) |
| Russian Mathematical Olympiad 2014, Final round, 10 класс, 10.2 | https://mathnet.mit.edu/explorer.html?p=rus_2014_9198e0 | not a functional equation (inequality, prove) |
| Russian Mathematical Olympiad 2014, Final round, 10th grade, 10.2 | https://mathnet.mit.edu/explorer.html?p=rus_2014_e27e3e | not a functional equation (inequality, prove) |
| All-Russian Mathematical Olympiad 2025, 11 класс, 11.8 | https://mathnet.mit.edu/explorer.html?p=rus_2025_a9ef6b | not a functional equation (chords of continuous function graph) |
| Saudi Arabian Mathematical Competitions 2010, Balkan MO selection tests - Second Selection Test, 3 | https://mathnet.mit.edu/explorer.html?p=sau_2010_3cf4b3 | not a functional equation (inequality, prove) |
| Saudi Arabian Mathematical Competitions 2010, Balkan MO selection tests - Third Selection Test, 1 | https://mathnet.mit.edu/explorer.html?p=sau_2010_4ab47d | not a functional equation (sets of reals) |
| Saudi Arabian Mathematical Competitions 2010, Balkan MO selection tests - First Selection Test, 4 | https://mathnet.mit.edu/explorer.html?p=sau_2010_55abf4 | domain and codomain differ (f: N -> [0, inf)); extra hypothesis: f(4) = 2; sum/division condition |
| Saudi Arabian Mathematical Competitions 2010, IMO selection tests - Second Selection Test, 3 | https://mathnet.mit.edu/explorer.html?p=sau_2010_6a642c | not "find all f" (asks for f(2010)); domain not supported (N) |
| Saudi Arabian Mathematical Competitions 2011, Balkan MO selection tests, 1 | https://mathnet.mit.edu/explorer.html?p=sau_2011_224891 | not a functional equation (polynomial problem) |
| Saudi Arabian Mathematical Competitions 2011, IMO selection tests, 3 | https://mathnet.mit.edu/explorer.html?p=sau_2011_d2b8a7 | equation holds only on restricted values (y >= 0) |
| Saudi Arabian Mathematical Competitions 2012, 2012 Balkan MO selection tests - Test 3, 2 | https://mathnet.mit.edu/explorer.html?p=sau_2012_1ebc0e | domain not supported (positive integers); divisibility condition |
| Saudi Arabian Mathematical Competitions 2012, IMO selection tests - Test 3, 2 | https://mathnet.mit.edu/explorer.html?p=sau_2012_c18c99 | not a functional equation (polynomial problem, prove) |
| Saudi Arabian Mathematical Competitions 2012, IMO selection tests - Test 4, 4 | https://mathnet.mit.edu/explorer.html?p=sau_2012_fe539d | not "find all f" (asks for k); domain not supported (N) |
| Balkan Mathematical Olympiad TST (BMO TST) 2013, 3.3 Day III - April 14, 2013, 4 | https://mathnet.mit.edu/explorer.html?p=sau_2013_07f58b | not "find all f" (solve f(n) = 1000); domain not supported (non-negative integers) |
| Gulf Mathematical Olympiad TST (GMO TST) 2013, 2.3 Day III - January 29, 2013, 1 | https://mathnet.mit.edu/explorer.html?p=sau_2013_1ab786 | not a single equation (two equations); division by a variable; irrational constants (sqrt(3)) |
| Preselection Test 2013, 1.3 Day III - October 21, 2013, 1 | https://mathnet.mit.edu/explorer.html?p=sau_2013_87e26c | not "find all f" (prove) |
| IMO TST 2013, 4.1 Day I - May 28, 2013, 2 | https://mathnet.mit.edu/explorer.html?p=sau_2013_9353a8 | domain not supported (non-negative integers); inequality; extra hypothesis: strictly increasing |
| Saudi Arabian Mathematical Competitions 2014, Team selection tests for the Balkan Mathematical Olympiad 2014 - Day III, 4 | https://mathnet.mit.edu/explorer.html?p=sau_2014_8ae4f0 | not "find all f" (prove); domain not supported (N); extra hypothesis: injective, f(1) = 2, f(2) = 4 |
| Saudi Arabian Mathematical Competitions 2014, Team Selection tests for the International Mathematical Olympiad 2014 - Day I, 4 | https://mathnet.mit.edu/explorer.html?p=sau_2014_ab10bb | domain not supported (N); inequality |
| Saudi Arabian Mathematical Competitions 2014, Team Selection tests for the International Mathematical Olympiad 2014 - Day III, 2 | https://mathnet.mit.edu/explorer.html?p=sau_2014_b0220e | domain and codomain differ (f: [0, inf) -> R); floor; extra hypothesis: f(0) = 0 |
| Saudi Arabian Mathematical Competitions 2014, Team selection tests for the Balkan Mathematical Olympiad 2014 - Day III, 1 | https://mathnet.mit.edu/explorer.html?p=sau_2014_d856e3 | domain and codomain differ (f: N -> (0, inf)); extra hypothesis: f(4) = 4; sum/division condition |
| Saudi Arabian Mathematical Competitions 2015, Team Selection Tests for the Gulf Mathematical Olympiad 2015 - Day III - January 28, 2015, 1 | https://mathnet.mit.edu/explorer.html?p=sau_2015_32d7d6 | not a single equation (three conditions); extra hypothesis: f(1) = 1; division by a variable |
| Saudi Arabian Mathematical Competitions 2015, Team Selection Tests for the Balkan Mathematical Olympiad 2015 - Day II - April 1, 2015, 1 | https://mathnet.mit.edu/explorer.html?p=sau_2015_4aaa89 | domain and codomain differ (f: Z -> R); extra hypothesis: strictly increasing; existential condition |
| Saudi Arabian Mathematical Competitions 2015, Team Selection Tests for the Balkan Mathematical Olympiad 2015 - Day I - March 30, 2015, 1 | https://mathnet.mit.edu/explorer.html?p=sau_2015_bd8ad8 | not a functional equation (sequence) |
| Saudi Arabian Mathematical Competitions 2015, Team Selection Tests for the International Mathematical Olympiad 2015 - Day I - May 19, 2015, 1 | https://mathnet.mit.edu/explorer.html?p=sau_2015_db7d90 | domain and codomain differ (f: R>0 -> R); division by a variable |
| Saudi Arabian Mathematical Competitions 2016, Team selection tests for Gulf Mathematical Olympiad 2016 - Level 4+, day 2, 2 | https://mathnet.mit.edu/explorer.html?p=sau_2016_501a33 | not a functional equation (polynomial problem) |
| Saudi Arabian Mathematical Competitions 2016, Team selection tests for Gulf Mathematical Olympiad 2016 - Level 4, day 2, 2 | https://mathnet.mit.edu/explorer.html?p=sau_2016_57ce57 | not a functional equation (polynomial problem) |
| Saudi Arabian Mathematical Competitions 2016, Team Selection Tests for the International Mathematical Olympiad 2016 - Level 4+, day 2, 2 | https://mathnet.mit.edu/explorer.html?p=sau_2016_b50a5e | not a functional equation (inequalities) |
| Saudi Arabian Mathematical Competitions 2016, Team selection tests for Gulf Mathematical Olympiad 2016 - Level 4, day 3, 2 | https://mathnet.mit.edu/explorer.html?p=sau_2016_d9600c | domain not supported (Z) |
| Saudi Arabian Mathematical Competitions 2017, Team Selection Tests for the International Mathematical Olympiad 2017 - Day 3, Problem 1 | https://mathnet.mit.edu/explorer.html?p=sau_2017_6732d4 | not a functional equation (polynomial problem, digit sums) |
| Saudi Arabian Mathematical Competitions 2017, Mock tests for BMO 2017 - Day 1, Problem 2 | https://mathnet.mit.edu/explorer.html?p=sau_2017_6e7bdb | domain and codomain differ (f: R+ -> R); inequalities |
| Saudi Arabian Mathematical Competitions 2017, Training problem set for JBMO and IMO 2017 - Training problem for JBMO Team, Problem 1 | https://mathnet.mit.edu/explorer.html?p=sau_2017_b4a124 | not a functional equation (binary operation on positive integers; asks for values) |
| Balkan Mathematical Olympiad TST (BMO TST) 2018, The first day, Problem 2 | https://mathnet.mit.edu/explorer.html?p=sau_2018_31758c | MathNet statement and its official solution disagree (the stated answer f = 0 does not satisfy the stated equation) |
| Balkan Mathematical Olympiad TST (BMO TST) 2018, The second day, Problem 4 | https://mathnet.mit.edu/explorer.html?p=sau_2018_845fc9 | domain not supported (Z); division by a variable; equation holds only on restricted values (x != 0) |
| IMO TST 2018, The fourth day, Problem 1 | https://mathnet.mit.edu/explorer.html?p=sau_2018_c965fb | domain not supported (positive integers); divisibility with max/min; extra hypothesis: f(1) = 2, f(2) != 4 |
| Saudi Arabian Mathematical Competitions 2019, April camp - Test 2, 5 | https://mathnet.mit.edu/explorer.html?p=sau_2019_160ea4 | not a functional equation (polynomial problem) |
| Saudi Arabian Mathematical Competitions 2019, Senior level - Test 4, 11 | https://mathnet.mit.edu/explorer.html?p=sau_2019_b0b2af | domain not supported (f: R^2 -> R, function of two variables) |
| Saudi Arabian Mathematical Competitions 2019, May camp - IMO TST - Day 1, 1 | https://mathnet.mit.edu/explorer.html?p=sau_2019_c8c41b | domain not supported (positive integers); inequality |
| International Mathematical Olympiad (IMO) 2022, January camp - Test 4, 8 | https://mathnet.mit.edu/explorer.html?p=sau_2022_113471 | domain not supported (R+) |
| International Mathematical Olympiad (IMO) 2022, March camp - Test 5, 2 | https://mathnet.mit.edu/explorer.html?p=sau_2022_1d47e8 | not "find all f" (does there exist); two unknown functions |
| International Mathematical Olympiad (IMO) 2022, May camp - IMO Team Selection Test 1, 3 | https://mathnet.mit.edu/explorer.html?p=sau_2022_c1d7c2 | domain not supported (Q+); extra hypothesis: f non-constant |
| International Mathematical Olympiad (IMO) 2023, Test 4, Problem 2. | https://mathnet.mit.edu/explorer.html?p=sau_2023_1808f1 | extra hypothesis: f non-constant |
| International Mathematical Olympiad (IMO) 2023, Selected problems from training, Problem 38. | https://mathnet.mit.edu/explorer.html?p=sau_2023_afff10 | not "find all f" (prove f(2) = f(-2) = 0); extra hypothesis: f(0) = 0 |
| International Mathematical Olympiad (IMO) 2023, Selected problems from training, Problem 18. | https://mathnet.mit.edu/explorer.html?p=sau_2023_b1aea4 | domain not supported (R+); extra hypothesis: f(2x) >= 2f(x), strictly increasing |
| International Mathematical Olympiad (IMO) 2023, Selected problems from training, Problem 40. | https://mathnet.mit.edu/explorer.html?p=sau_2023_c49dde | domain not supported (R+); inequality; equation holds only on restricted values (pairwise distinct) |
| International Mathematical Olympiad (IMO) 2023, Test 1, Problem 1. | https://mathnet.mit.edu/explorer.html?p=sau_2023_e236c9 | not "find all f" (does there exist) |
| International Mathematical Olympiad (IMO) 2023, Selected problems from training, Problem 27. | https://mathnet.mit.edu/explorer.html?p=sau_2023_f5b193 | not "find all f" (inequality; asks for f(2022)) |
| Saudi Arabian Mathematical Competitions 2024, Selected problems from camps - Test 4, 14 | https://mathnet.mit.edu/explorer.html?p=sau_2024_6972c9 | not "find all f" (asks for smallest m); domain not supported (R+); division by f(x) |
| Saudi Arabian Mathematical Competitions 2025, Preselection tests - Test 4, 14 | https://mathnet.mit.edu/explorer.html?p=sau_2025_0a1e69 | domain not supported (R+) |
| Saudi Arabian Mathematical Competitions 2025, IMO Team Selection Tests - Test 3, 8 | https://mathnet.mit.edu/explorer.html?p=sau_2025_7ba562 | not "find all f" (asks for c); domain not supported ((0, inf)) |
| Saudi Arabian Mathematical Competitions 2025, EGMO Team selection tests - Test 2, 5 | https://mathnet.mit.edu/explorer.html?p=sau_2025_aef76a | extra hypothesis: at most one zero of f |
| Saudi Arabian Mathematical Competitions 2025, Preselection tests - Test 2, 6 | https://mathnet.mit.edu/explorer.html?p=sau_2025_bd978a | domain and codomain differ (f: R+ -> R) |
| Saudi Arabian Mathematical Competitions 2025, Problems without solution, 21 | https://mathnet.mit.edu/explorer.html?p=sau_2025_cb2bf4 | not a single equation (second condition with cos); extra hypothesis: f non-constant; 2025-fold iterate |
| Singapore Mathematical Olympiad (SMO) 2017, Senior Section, Round 2, 4 | https://mathnet.mit.edu/explorer.html?p=sgp_2017_7fbf79 | domain not supported (positive integers); inequality |
| Singapore Mathematical Olympiad (SMO) 2018, Senior Section, Round 2, 5 | https://mathnet.mit.edu/explorer.html?p=sgp_2018_90ba1e | not a functional equation (combinatorics on symbol tuples) |
| Singapore International Math Olympiad Challenge (SIMOC) 2018, Camp Quiz Day 1, 3 | https://mathnet.mit.edu/explorer.html?p=sgp_2018_abc010 | not "find all f" (asks whether f(n) = n + 1 must hold); domain not supported (N) |
| Singapore Mathematical Olympiad (SMO) 2023, Open Section, Round 2, 4 | https://mathnet.mit.edu/explorer.html?p=sgp_2023_4fac2a | domain not supported (Z) |
| Singapore Mathematical Olympiad (SMO) 2025, Senior Section, Round 2, 3 | https://mathnet.mit.edu/explorer.html?p=sgp_2025_c7659d | domain not supported (Z+ -> Z+, iterated f) |
| Silk Road Mathematics Competition (SRMC) 2003, II Silk Road Mathematics Competition 2003, 3 | https://mathnet.mit.edu/explorer.html?p=slk_2003_127658 | not "find all f" (prove statement about a given piecewise map) |
| Silk Road Mathematics Competition (SRMC) 2018, Problem 2 | https://mathnet.mit.edu/explorer.html?p=slk_2018_a57e89 | not a single equation in one function (two simultaneous equations) |
| Silk Road Mathematics Competition (SRMC) 2025, 1 | https://mathnet.mit.edu/explorer.html?p=slk_2025_01aa2c | not a functional equation (set problem, yes/no question) |
| Serbian Mathematical Olympiad 2007, Други дан, 4. | https://mathnet.mit.edu/explorer.html?p=srb_2007_926d54 | not "find all f" (existence question; f: N -> N) |
| Serbian Mathematical Olympiad 2012, Други дан, 6. | https://mathnet.mit.edu/explorer.html?p=srb_2012_cd7802 | not a functional equation (combinatorics: weighing coins) |
| Serbian Mathematical Olympiad 2013, Први дан, 1. | https://mathnet.mit.edu/explorer.html?p=srb_2013_2dfff8 | not "find all f" (prove; f: Z -> Z bijection) |
| Serbian Mathematical Olympiad 2014, Први дан, 1. | https://mathnet.mit.edu/explorer.html?p=srb_2014_8bf728 | answer is not a rational polynomial (official answer includes f(x) = \|x\|) |
| Serbian Mathematical Olympiad 2020, Други дан, 5. | https://mathnet.mit.edu/explorer.html?p=srb_2020_4b3837 | not "find all f" (prove; f: N -> N) |
| All-Union Mathematical Olympiad 1965, Problem 8 | https://mathnet.mit.edu/explorer.html?p=sun_1965_1d45d7 | not a functional equation (system of linear equations, prove) |
| All-Union Mathematical Olympiad 1971, 5th ASU, Problem 3 | https://mathnet.mit.edu/explorer.html?p=sun_1971_6ac3c0 | not a functional equation (array reconstruction counting) |
| All-Union Mathematical Olympiad 1974, 8th ASU, Problem 15 | https://mathnet.mit.edu/explorer.html?p=sun_1974_5ee03c | not "find all f" (inequality on [0,1], prove) |
| All-Union Mathematical Olympiad 1977, 11th ASU problems, Problem 17 | https://mathnet.mit.edu/explorer.html?p=sun_1977_bbc37a | not a functional equation (polynomial problem: commuting polynomials) |
| All-Union Mathematical Olympiad 1980, 14th ASU, Problem 11 | https://mathnet.mit.edu/explorer.html?p=sun_1980_fbe9b7 | not a functional equation (digit sums) |
| All-Union Mathematical Olympiad 1982, Problem 21 | https://mathnet.mit.edu/explorer.html?p=sun_1982_a2d544 | not a functional equation (polynomial existence problem) |
| All-Union Mathematical Olympiad 1987, Problem 20 | https://mathnet.mit.edu/explorer.html?p=sun_1987_813c0f | not "find all f" (prove / give example) |
| All-Union Mathematical Olympiad 1989, Problem 23 | https://mathnet.mit.edu/explorer.html?p=sun_1989_2f4fa1 | not "find all f" (does there exist; f: N -> N) |
| Slovenian Mathematical Olympiad 2002, 4. LETNIK, 1. | https://mathnet.mit.edu/explorer.html?p=svn_2002_df9bbb | not "find all f" (does there exist; f: N -> N) |
| IMO TST 2009, Second Selection Examination, February 2009, 3 | https://mathnet.mit.edu/explorer.html?p=svn_2009_cdbbc0 | not a single equation in one function (find g given existence of a strictly increasing f) |
| Slovenian Mathematical Olympiad 2011, Naloge za 4. letnik, 2. | https://mathnet.mit.edu/explorer.html?p=svn_2011_8f4dd8 | equation contains cos x (not built from + - * and powers) |
| Slovenian Mathematical Olympiad 2012, Final Round - Grade Four, 2 | https://mathnet.mit.edu/explorer.html?p=svn_2012_3b8957 | not "find all f" (prove no injective f exists) |
| Slovenian Mathematical Olympiad 2012, 4. letnik, 2. | https://mathnet.mit.edu/explorer.html?p=svn_2012_992bd3 | not "find all f" (prove no injective f exists) |
| Slovenian Mathematical Olympiad 2013, Naloge za 4. letnik, 1. | https://mathnet.mit.edu/explorer.html?p=svn_2013_05c3a9 | domain not supported (R \ {-1} -> R) |
| Slovenian Mathematical Olympiad 2013, Grade Three, A1. | https://mathnet.mit.edu/explorer.html?p=svn_2013_35992a | not "find all f" (multiple choice; equation contains sin, cos) |
| Slovenian Mathematical Olympiad 2013, Grade Four, 1 | https://mathnet.mit.edu/explorer.html?p=svn_2013_f12b27 | domain not supported (R \ {-1} -> R) |
| Slovenian Mathematical Olympiad 2014, Selection Examinations for the IMO 2014, 2. | https://mathnet.mit.edu/explorer.html?p=svn_2014_3aa312 | domain not supported (N -> N; conditional multiplicativity and triangle condition) |
| Slovenian Mathematical Olympiad 2014, National Math Olympiad 2014 – Final Round, 1. | https://mathnet.mit.edu/explorer.html?p=svn_2014_53677c | not a functional equation (polynomial problem) |
| Slovenian Mathematical Olympiad 2014, 3. letnik, 1. | https://mathnet.mit.edu/explorer.html?p=svn_2014_a071b6 | not a functional equation (polynomial problem) |
| IMO TST 2015, Second Selection Examination, 2. | https://mathnet.mit.edu/explorer.html?p=svn_2015_d54b78 | not "find all f" (prove; f: Z -> Z) |
| Slovenian Mathematical Olympiad 2016, Selection Examinations for the IMO 2016 - Second Selection Examination, 2 | https://mathnet.mit.edu/explorer.html?p=svn_2016_17480a | domain not supported (R+ -> R+); division by a variable |
| Slovenian Mathematical Olympiad 2019, 4. letnik, A2 | https://mathnet.mit.edu/explorer.html?p=svn_2019_117c7b | not "find all f" (multiple choice about even/odd functions) |
| Slovenian Mathematical Olympiad for Technical Schools 2022, 2. letnik, A3 | https://mathnet.mit.edu/explorer.html?p=svn_2022_311ab6 | not "find all f" (asks for the value f(-1); multiple choice) |
| Slovenian Mathematical Olympiad 2022, Državno tekmovanje, Naloge za 3. letnik, A3 | https://mathnet.mit.edu/explorer.html?p=svn_2022_8eb424 | not "find all f" (asks for the value f(-5); multiple choice) |
| Thailand Mathematical Olympiad 2007, 6 | https://mathnet.mit.edu/explorer.html?p=tha_2007_09bb65 | not "find all f" (does there exist; f: Z -> Z) |
| Thailand Mathematical Olympiad 2007, Problems, 5 | https://mathnet.mit.edu/explorer.html?p=tha_2007_6ad5b0 | not "find all f" (inequality, prove) |
| Thailand Mathematical Olympiad 2007, Problems, 12 | https://mathnet.mit.edu/explorer.html?p=tha_2007_978ba3 | not "find all f" (prove; f: R+ -> R+) |
| Thailand Mathematical Olympiad 2007, Problems, 10 | https://mathnet.mit.edu/explorer.html?p=tha_2007_f35b7b | extra hypothesis: continuous (also irrational constant (1+sqrt 5)/2) |
| Thailand Mathematical Olympiad 2011, 2011 ThMO Selected Problems, 6 | https://mathnet.mit.edu/explorer.html?p=tha_2011_341ee0 | not "find all f" (prove; domain (0, inf), division by a variable) |
| Thailand Mathematical Olympiad 2011, 2011 ThMO Selected Problems, 4 | https://mathnet.mit.edu/explorer.html?p=tha_2011_f55f34 | not "find all f" (prove; absolute value) |
| Thailand Mathematical Olympiad 2013, Day 1 Examination, 6 | https://mathnet.mit.edu/explorer.html?p=tha_2013_ccc010 | answer is not a rational polynomial (official answer includes f(x) = \|x\| and f(x) = -\|x\|) |
| Thailand Mathematical Olympiad 2016, Mathematical Competitions in Thailand 2016, 9 | https://mathnet.mit.edu/explorer.html?p=tha_2016_322970 | equation contains a real parameter a != 0 (not a rational constant); answer involves sqrt(a) |
| Thailand Third Mathematical Olympiad (T3MO) 2016, Mathematical Competitions in Thailand 2016, 2 | https://mathnet.mit.edu/explorer.html?p=tha_2016_8327bd | domain not supported (N0 -> N0, iterated f); equation holds only on restricted values (m <= n) |
| Thailand Third Mathematical Olympiad (T3MO) 2017, Problems, Problem 1 | https://mathnet.mit.edu/explorer.html?p=tha_2017_6132af | not a functional equation (polynomial problem, P in R[x,y]) |
| Thailand Third Mathematical Olympiad (T3MO) 2017, Problems, Problem 4 | https://mathnet.mit.edu/explorer.html?p=tha_2017_7373e3 | not "find all f" (does there exist; f: N -> Q) |
| Thailand Mathematical Olympiad 2017, Problems, Problem 9 | https://mathnet.mit.edu/explorer.html?p=tha_2017_ef728b | domain not supported (Q+ -> Q+) |
| Turkish Mathematical Olympiad 2000, Second day (December 9, 2000), 6 | https://mathnet.mit.edu/explorer.html?p=tur_2000_190c86 | domain not supported ([0,1] -> [0,1]); extra hypothesis: continuous; not an equation |
| IMO TST 2001, Second day (April 1, 2001), 6 | https://mathnet.mit.edu/explorer.html?p=tur_2001_8736bd | not "find all f" (prove no continuous f exists) |
| IMO TST 2009, 1 | https://mathnet.mit.edu/explorer.html?p=tur_2009_02190b | domain and codomain differ (Q+ -> Z); two equations |
| IMO TST 2011, 1 | https://mathnet.mit.edu/explorer.html?p=tur_2011_6f1e8e | domain not supported (Q+ -> Q+); two equations, division by a variable |
| IMO TST 2011, 9 | https://mathnet.mit.edu/explorer.html?p=tur_2011_f407af | domain not supported (Z_{p^n}); counts functions rather than "find all f" |
| IMO TST 2013, 8 | https://mathnet.mit.edu/explorer.html?p=tur_2013_654e62 | domain and codomain differ (R -> R+); extra hypotheses (second equation, monotonicity) |
| IMO TST 2014, for EGMO 2014, 3 | https://mathnet.mit.edu/explorer.html?p=tur_2014_7d0471 | not a functional equation (polynomial problem) |
| IMO TST 2018, for IMO 2018, 2 | https://mathnet.mit.edu/explorer.html?p=tur_2018_f9f435 | extra hypothesis: surjective |
| IMO TST 2019, 5 | https://mathnet.mit.edu/explorer.html?p=tur_2019_06b3e0 | not a functional equation (polynomial problem, prove) |
| IMO TST 2022, IMO 2022, 2 | https://mathnet.mit.edu/explorer.html?p=tur_2022_71baae | domain and codomain differ (Q+ -> Q); division by a variable |
| EGMO TST 2023, 2 | https://mathnet.mit.edu/explorer.html?p=tur_2023_6eb15a | domain not supported (Z+ -> Z+; divisibility and totient conditions) |
| Junior Balkan Mathematical Olympiad TST (JBMO TST) 2023, 3 | https://mathnet.mit.edu/explorer.html?p=tur_2023_da569a | extra hypothesis: f non-decreasing |
| Taiwan IMO Team Selection Training Camp 2011, 1 | https://mathnet.mit.edu/explorer.html?p=twn_2011_9633ec | equation contains a real parameter k (not a rational constant) |
| Taiwan IMO Team Selection Training Camp 2012, 獨立研究(三), 2 | https://mathnet.mit.edu/explorer.html?p=twn_2012_35c672 | not a functional equation (polynomial problem; pairs of polynomials f, g) |
| Taiwan IMO Team Selection Training Camp 2012, 模擬競賽(一), 3 | https://mathnet.mit.edu/explorer.html?p=twn_2012_9920bc | domain not supported (Z -> Z; divisibility condition) |
| Taiwan IMO Team Selection Training Camp 2012, 獨立研究(二), 2 | https://mathnet.mit.edu/explorer.html?p=twn_2012_9ad9f2 | domain not supported (N -> N); division by f values |
| Taiwan IMO Team Selection Training Camp 2012, 模擬競賽(二), 4 | https://mathnet.mit.edu/explorer.html?p=twn_2012_a10807 | not a functional equation (sequence problem) |
| Taiwan Mathematical Olympiad Training Camp 2012, 模擬競賽(二), 4 | https://mathnet.mit.edu/explorer.html?p=twn_2012_b04e4b | not a functional equation (sequence / number theory problem) |
| Taiwan IMO Team Selection Training Camp 2012, 模擬競賽(二), 4 | https://mathnet.mit.edu/explorer.html?p=twn_2012_b16790 | not a single equation in one function (pair f, g on positive integers) |
| Taiwan Mathematical Olympiad Training Camp 2012, 模擬競賽(二), 6 | https://mathnet.mit.edu/explorer.html?p=twn_2012_cf410c | not a single equation in one function (two unknown functions f, g) |
| Taiwan IMO Team Selection Training Camp 2013, 2 | https://mathnet.mit.edu/explorer.html?p=twn_2013_df579b | not "find all f" (prove; f: N -> N) |
| Taiwan IMO Team Selection Training Camp 2013, 模擬競賽(二), 5 | https://mathnet.mit.edu/explorer.html?p=twn_2013_f4c641 | extra hypothesis: f(-1) != 0 |
| Taiwan Mathematical Olympiad Training Camp 2014, 獨立研究(二), 1 | https://mathnet.mit.edu/explorer.html?p=twn_2014_05476e | domain not supported (N0 -> Z); extra hypothesis: increasing, f(2) = 7 |
| Taiwan IMO Team Selection Training Camp 2014, 2 | https://mathnet.mit.edu/explorer.html?p=twn_2014_80fad8 | domain and codomain differ (Q -> Z); division by integer variable b |
| Taiwan IMO Team Selection Training Camp 2014, 1 | https://mathnet.mit.edu/explorer.html?p=twn_2014_bb422f | not a functional equation (existence of sign-network coefficients) |
| Taiwan Mathematical Olympiad 2014, 2 | https://mathnet.mit.edu/explorer.html?p=twn_2014_db6ec5 | domain not supported (Z>=0 -> Z>=0) |
| Taiwan Mathematical Olympiad Training Camp 2015, 獨立研究(一), 2 | https://mathnet.mit.edu/explorer.html?p=twn_2015_39e3f4 | domain and codomain differ (Q -> R \ {0}) |
| Taiwan Mathematical Olympiad Training Camp 2015, Mock Competition (2), 5 | https://mathnet.mit.edu/explorer.html?p=twn_2015_aa5d37 | domain not supported (Z -> Z) |
| Taiwan Mathematical Olympiad Training Camp 2015, Independent Study (3), 2 | https://mathnet.mit.edu/explorer.html?p=twn_2015_bce000 | equation contains a real parameter t != -1 (not a rational constant) |
| Taiwan IMO Team Selection Training Camp 2015, 獨立研究(二), 1 | https://mathnet.mit.edu/explorer.html?p=twn_2015_da7ea8 | domain not supported (Q+ -> Q+); extra hypothesis: f(1) = 1; division by a variable |
| Taiwan Mathematical Olympiad Training Camp 2015, 模擬競賽(一), 2 | https://mathnet.mit.edu/explorer.html?p=twn_2015_f668c8 | domain not supported (R+ -> R+); too many variables (n >= 3 variables) |
| Taiwan IMO Team Selection Training Camp 2016, 模擬競賽（二）, 5 | https://mathnet.mit.edu/explorer.html?p=twn_2016_0cd184 | not a functional equation (polynomial problem, prove) |
| Taiwan IMO Team Selection Training Camp 2016, 獨立研究（三）, 2 | https://mathnet.mit.edu/explorer.html?p=twn_2016_2c3d9d | domain not supported (R+ -> R+) |
| Taiwan IMO Team Selection Training Camp 2016, 獨立研究(一), 2 | https://mathnet.mit.edu/explorer.html?p=twn_2016_39a2a5 | domain not supported (Z -> Z) |
| Taiwan Mathematical Olympiad Training Camp 2016, 模擬競賽(一), 3 | https://mathnet.mit.edu/explorer.html?p=twn_2016_49b738 | domain not supported (Z+ x Z+ -> Z+, two-argument f) |
| Taiwan Mathematical Olympiad Training Camp 2016, 獨立研究(一), 1 | https://mathnet.mit.edu/explorer.html?p=twn_2016_518ad4 | not "find all f" (inequality, prove) |
| Taiwan Mathematical Olympiad Training Camp 2016, 模擬競賽(二), 4 | https://mathnet.mit.edu/explorer.html?p=twn_2016_f8e06d | domain not supported (Z -> Z) |
| Taiwan Mathematical Olympiad Training Camp 2017, 模擬競賽(一), 3 | https://mathnet.mit.edu/explorer.html?p=twn_2017_1033cf | domain not supported (N -> N); extra hypothesis: injective |
| Taiwan IMO Team Selection Training Camp 2017, 模擬競賽(二), 4 | https://mathnet.mit.edu/explorer.html?p=twn_2017_257b60 | not "find all f" (counting periodic functions Z -> {0..2016}) |
| Taiwan IMO Team Selection Training Camp 2017, 獨立研究（三）, 1 | https://mathnet.mit.edu/explorer.html?p=twn_2017_46c415 | domain not supported (Z -> Z); extra hypothesis: surjective |
| Taiwan IMO Team Selection Training Camp 2017, 模擬競賽(一), 3 | https://mathnet.mit.edu/explorer.html?p=twn_2017_51818c | domain not supported (N -> N; divisibility condition) |
| Taiwan IMO Team Selection Training Camp 2017, 獨立研究（二）, 1 | https://mathnet.mit.edu/explorer.html?p=twn_2017_56d601 | not a functional equation (polynomial problem with digit sums) |
| Taiwan Mathematical Olympiad Training Camp 2017, 獨立研究(三), 1 | https://mathnet.mit.edu/explorer.html?p=twn_2017_897e93 | not a functional equation (polynomial problem) |
| Taiwan IMO Team Selection Training Camp 2018, 2 | https://mathnet.mit.edu/explorer.html?p=twn_2018_0737a3 | domain not supported (f: Z -> Z); also extra hypothesis f(0) = 0 |
| Taiwan IMO Team Selection Training Camp 2018, 模擬競賽(二), 6 | https://mathnet.mit.edu/explorer.html?p=twn_2018_6d56b2 | not a functional equation (combinatorics on finite sets; prove) |
| Taiwan IMO Team Selection Training Camp 2018, 模擬競賽(二), 5 | https://mathnet.mit.edu/explorer.html?p=twn_2018_d47233 | domain not supported (f: N -> N) |
| Taiwan Mathematical Olympiad Training Camp 2018, 模擬競賽(二), 5 | https://mathnet.mit.edu/explorer.html?p=twn_2018_e8e7cf | domain not supported (f: N -> Z; divisibility condition) |
| Taiwan IMO Team Selection Training Camp 2019, 1 | https://mathnet.mit.edu/explorer.html?p=twn_2019_4e6b06 | domain not supported (f: Q>0 -> Q>0) |
| Taiwan IMO Team Selection Training Camp 2019, 模擬競賽(一), 2 | https://mathnet.mit.edu/explorer.html?p=twn_2019_8afd91 | domain not supported (f: (0, inf) -> R); division by a variable |
| IMO TST 2020, Independent Study 2, 2 | https://mathnet.mit.edu/explorer.html?p=twn_2020_750536 | not "find all f" (existence proof) |
| IMO TST 2020, Independent Study 1, 1 | https://mathnet.mit.edu/explorer.html?p=twn_2020_919bff | not "find all f" (prove; f on positive integers, divisibility) |
| Taiwan IMO Team Selection Training Camp 2021, 5 | https://mathnet.mit.edu/explorer.html?p=twn_2021_eb3af7 | domain not supported (f: N -> N) |
| Taiwan IMO Team Selection Training Camp 2022, 4. | https://mathnet.mit.edu/explorer.html?p=twn_2022_7c634b | domain not supported (f on sets of positive integers -> R+); inequalities |
| Taiwan IMO Team Selection Training Camp 2022, II-A. | https://mathnet.mit.edu/explorer.html?p=twn_2022_995110 | domain not supported (f: R+ -> R+) |
| Taiwan Mathematical Olympiad Training Camp 2022, 1. | https://mathnet.mit.edu/explorer.html?p=twn_2022_9a3c0d | equation contains a general parameter n (exponent n for arbitrary positive integer n); not expressible |
| Taiwan IMO Team Selection Training Camp 2022, II-A. | https://mathnet.mit.edu/explorer.html?p=twn_2022_9afb5b | extra hypothesis: f injective |
| Taiwan IMO Team Selection Training Camp 2022, 6. | https://mathnet.mit.edu/explorer.html?p=twn_2022_c18cd6 | domain not supported (f: R\{-1} -> R); division by a variable; equation holds only on restricted values |
| Taiwan IMO Team Selection Training Camp 2022, 獨力研究(三)試題, 1. | https://mathnet.mit.edu/explorer.html?p=twn_2022_cdbe46 | not a functional equation (polynomial problem) |
| Taiwan Mathematical Olympiad Training Camp 2023, 獨立研究(一), I-A | https://mathnet.mit.edu/explorer.html?p=twn_2023_0602fd | not "find all f" (prove; f: N -> R>0) |
| Taiwan IMO Team Selection Training Camp 2023, 國際競賽實作(一), 2 | https://mathnet.mit.edu/explorer.html?p=twn_2023_11be87 | not "find all f" (asks for rational q) |
| Taiwan Mathematical Olympiad Training Camp 2023, 獨立研究(二), II-A | https://mathnet.mit.edu/explorer.html?p=twn_2023_27e0b7 | not a functional equation (polynomial problem; prove) |
| Taiwan Mathematical Olympiad Training Camp 2023, 國際競賽實作(一), 1 | https://mathnet.mit.edu/explorer.html?p=twn_2023_89bb20 | not "find all f" (prove; f: Q>1 -> Z) |
| Taiwan Mathematical Olympiad Training Camp 2023, 國際競賽實作(二), 5 | https://mathnet.mit.edu/explorer.html?p=twn_2023_b874cb | domain not supported (f: N -> N; divisibility) |
| IMO TST 2024, II-N | https://mathnet.mit.edu/explorer.html?p=twn_2024_313bc0 | not "find all f" (prove; f: N -> N) |
| IMO TST 2024, II-A | https://mathnet.mit.edu/explorer.html?p=twn_2024_449a92 | domain not supported (f: R+ -> R+) |
| IMO TST 2024, I-C | https://mathnet.mit.edu/explorer.html?p=twn_2024_6a611a | domain not supported (f: N -> N; set condition) |
| IMO TST 2024, 2 | https://mathnet.mit.edu/explorer.html?p=twn_2024_74ba45 | domain not supported (f: R>0 -> R>0); inequality |
| IMO TST 2024, 3 | https://mathnet.mit.edu/explorer.html?p=twn_2024_a1a569 | domain not supported (f: N -> N; divisibility) |
| IMO TST 2024, 6 | https://mathnet.mit.edu/explorer.html?p=twn_2024_a426c8 | not a functional equation (polynomial/integer sequence problem) |
| IMO TST 2024, I-N | https://mathnet.mit.edu/explorer.html?p=twn_2024_af3097 | domain not supported (f: Z -> Z) |
| Ukrainian Mathematical Olympiad 2005, 11TH FORM, 4 | https://mathnet.mit.edu/explorer.html?p=ukr_2005_c98a91 | domain not supported (f: [0, inf) -> R); extra hypothesis: monotone, f(3) + 3f(1) = 3f(2) + f(0) |
| Ukrainian Mathematical Olympiad 2005, 10TH FORM, 5 | https://mathnet.mit.edu/explorer.html?p=ukr_2005_d75082 | domain not supported (f: (0, inf) -> R); division by a variable |
| Ukrainian Mathematical Olympiad 2006, 11TH FORM, 3 | https://mathnet.mit.edu/explorer.html?p=ukr_2006_6a93cd | not a functional equation (floor/fractional part equation) |
| Ukrainian Mathematical Olympiad 2009, 3 | https://mathnet.mit.edu/explorer.html?p=ukr_2009_09230f | not a functional equation (polynomial problem) |
| Ukrainian Mathematical Olympiad 2009, Fourth Round, First Day, 11-th grade, 11.4 | https://mathnet.mit.edu/explorer.html?p=ukr_2009_8b8901 | not a functional equation (polynomial problem) |
| Ukrainian Mathematical Olympiad 2009, Fourth Round, Second Day, 11 grade, 11.6 | https://mathnet.mit.edu/explorer.html?p=ukr_2009_a33566 | domain not supported (f: Z -> Z); absolute value |
| Ukrainian Mathematical Olympiad 2010, 11-th grade, 7 | https://mathnet.mit.edu/explorer.html?p=ukr_2010_a93cb0 | domain not supported (f: Z -> Z); extra hypothesis: f(0) = 2 |
| Ukrainian Mathematical Olympiad 2010, 9-th grade, 2 | https://mathnet.mit.edu/explorer.html?p=ukr_2010_cc8b9c | not a functional equation (polynomial problem) |
| Ukrainian National Mathematical Olympiad 2011, First Tour, 11-th grade, 6 | https://mathnet.mit.edu/explorer.html?p=ukr_2011_5b69f0 | extra hypothesis: f(x) >= 0 |
| Ukrainian National Mathematical Olympiad 2011, Second Day, 11th grade, 11-6 | https://mathnet.mit.edu/explorer.html?p=ukr_2011_ae6875 | not "find all f" (existence proof) |
| Ukrainian Mathematical Olympiad 2012, Final round, First day, 2 | https://mathnet.mit.edu/explorer.html?p=ukr_2012_427487 | not "find all f satisfying an equation" (inequality) |
| Ukrainian Mathematical Olympiad 2012, Final round, First day, 2 | https://mathnet.mit.edu/explorer.html?p=ukr_2012_975882 | not "find all f" (asks for f(2012); given value f(2011) = 2012) |
| Ukrainian National Mathematical Olympiad 2013, Grade 11, 4 | https://mathnet.mit.edu/explorer.html?p=ukr_2013_7f5d49 | no solution: the MathNet solution stops before stating the answer and no AoPS thread was found |
| Ukrainian National Mathematical Olympiad 2015, 10th grade, 10.8 | https://mathnet.mit.edu/explorer.html?p=ukr_2015_8611f6 | the official solution contradicts itself about the answer |
| Ukrainian Mathematical Olympiad 2016, 56th Ukrainian National Mathematical Olympiad, Fourth Round, March 2016, Second day, Grade 8, 8.7 | https://mathnet.mit.edu/explorer.html?p=ukr_2016_0336d7 | not "find all f" (binary operation on integers; compute values) |
| Ukrainian Mathematical Olympiad 2016, 56th Ukrainian National Mathematical Olympiad, Third Round, January 2016, Second Tour, Grade 7, 3 | https://mathnet.mit.edu/explorer.html?p=ukr_2016_27113c | not a functional equation (iterated given map) |
| Ukrainian Mathematical Olympiad 2016, 56th Ukrainian National Mathematical Olympiad, Third Round, January 2016, Second Tour, Grade 11, 3 | https://mathnet.mit.edu/explorer.html?p=ukr_2016_942db3 | extra hypothesis: strictly increasing, y^2 + f(y) surjective |
| Ukrainian Mathematical Olympiad 2016, 56th Ukrainian National Mathematical Olympiad, Third Round, January 2016, Second Tour, Grade 9, 3 | https://mathnet.mit.edu/explorer.html?p=ukr_2016_cad5a6 | domain not supported (f: N -> Z); asks for values of f(1000) |
| Ukrainian Mathematical Olympiad 2016, 56th Ukrainian National Mathematical Olympiad, Fourth Round, March 2016, First Day, Grade 10, 10.4 | https://mathnet.mit.edu/explorer.html?p=ukr_2016_daf745 | not "find all f" (existence; inequality) |
| Ukrainian National Mathematical Olympiad 2018, Fourth Round, First Day, 10 grade, 10-4. | https://mathnet.mit.edu/explorer.html?p=ukr_2018_353033 | domain not supported (f: [0, inf) -> [0, inf)) |
| Ukrainian National Mathematical Olympiad 2018, Third Round, Tour 2, Grade 10, 1. | https://mathnet.mit.edu/explorer.html?p=ukr_2018_6cab40 | not "find all f" (existence; f: (0,1) -> (2018, inf)) |
| Ukrainian National Mathematical Olympiad 2019, Fourth Round, Second Day, 11th Grade, 11-7 | https://mathnet.mit.edu/explorer.html?p=ukr_2019_9c3db7 | domain not supported (f: R+ -> R+) |
| Ukrainian Mathematical Olympiad 2021, 3 | https://mathnet.mit.edu/explorer.html?p=ukr_2021_49f61a | domain not supported (f: R+ -> R+); extra hypothesis: bijective |
| Berkeley Math Circle, 5. | https://mathnet.mit.edu/explorer.html?p=usa_177173 | not "find all f" (prove; binary operation) |
| Harvard-MIT Mathematics Tournament (HMMT) 1998, Advanced Topics, 8. | https://mathnet.mit.edu/explorer.html?p=usa_1998_16ef01 | not "find all f" (compute a value; binary operation on R+) |
| Harvard-MIT Mathematics Tournament (HMMT) 1998, Algebra Solutions, 9. | https://mathnet.mit.edu/explorer.html?p=usa_1998_d72315 | not "find all f" (compute f(-2)); division by a variable |
| Harvard-MIT Mathematics Tournament (HMMT) 1999, Calculus Solutions, Problem C4 | https://mathnet.mit.edu/explorer.html?p=usa_1999_93034c | not "find all f" (compute f(5)); extra hypothesis: continuous, f(2) = 5 |
| Bay Area Mathematical Olympiad (BAMO) 2001, 3. | https://mathnet.mit.edu/explorer.html?p=usa_2001_9b70bd | domain not supported (f on positive integers); asks for f(2001) |
| Harvard-MIT Mathematics Tournament (HMMT) 2002, Guts Round, 47. | https://mathnet.mit.edu/explorer.html?p=usa_2002_feafc2 | not "find all f" (compute f(2002)); equation holds only on restricted values |
| Harvard-MIT Mathematics Tournament (HMMT) 2003, Guts Round, 9. | https://mathnet.mit.edu/explorer.html?p=usa_2003_79e807 | not a functional equation (count solutions for a given f) |
| International Mathematical Olympiad (IMO) 2003, Team Selection Test, 4 | https://mathnet.mit.edu/explorer.html?p=usa_2003_893a66 | domain not supported (f: N -> N) |
| Harvard-MIT Mathematics Tournament (HMMT) 2004, Individual Round: General Test, Part 1, 3. | https://mathnet.mit.edu/explorer.html?p=usa_2004_aafe5a | not "find all f" (compute f(0)); too many variables (5) |
| IMO TST 2004, Team Selection Test, 6 | https://mathnet.mit.edu/explorer.html?p=usa_2004_e0c776 | not "find all f" (given recursive f: N0 -> Q; prove injective, find range) |
| Harvard-MIT Mathematics Tournament (HMMT) 2005, Individual Round: Calculus Subject Test, 8. | https://mathnet.mit.edu/explorer.html?p=usa_2005_4501cd | not "find all f" (inequality; integral minimum; continuity) |
| Harvard-MIT Mathematics Tournament (HMMT) 2006, What do the following problems have in common?, 15. | https://mathnet.mit.edu/explorer.html?p=usa_2006_2ae03d | not a functional equation (Mobius transformation problem) |
| Harvard-MIT Mathematics Tournament (HMMT) 2006, Calculus Test, 10. | https://mathnet.mit.edu/explorer.html?p=usa_2006_4a227a | not a functional equation (differential/integral conditions, two functions) |
| Harvard-MIT Mathematics Tournament (HMMT) 2007, Grab Bag - Miscellaneous Problems, 13. | https://mathnet.mit.edu/explorer.html?p=usa_2007_154019 | not a functional equation (polynomial problem) |
| Harvard-MIT Mathematics Tournament (HMMT) 2007, Individual Round: Algebra Test, 8. | https://mathnet.mit.edu/explorer.html?p=usa_2007_4290d4 | not "find all f" (compute f(2007)); f: Q\{0,1} -> R, log |
| Harvard-MIT Mathematics Tournament (HMMT) 2007, Individual Round: Calculus Test, 5. | https://mathnet.mit.edu/explorer.html?p=usa_2007_b99b73 | not a functional equation (differential equation; compute value) |
| Harvard-MIT Mathematics Tournament (HMMT) 2008, Individual Round: General Test, Part 1, 5. | https://mathnet.mit.edu/explorer.html?p=usa_2008_36d70c | not "find all f" (asks for f(10)) |
| Harvard-MIT Mathematics Tournament (HMMT) 2008, Individual Round: Algebra Test, 4. | https://mathnet.mit.edu/explorer.html?p=usa_2008_68946c | not "find all f" (asks for f(10)) |
| International Mathematical Olympiad (IMO) 2008, 5.1 IMO 2008 Problems, 4 | https://mathnet.mit.edu/explorer.html?p=usa_2008_b4961a | domain not supported (f: R+ -> R+); division; equation holds only on restricted values (pq = rs); too many variables |
| Harvard-MIT Mathematics Tournament (HMMT) 2008, Guts Round, 24. | https://mathnet.mit.edu/explorer.html?p=usa_2008_e6a63b | not a functional equation (iterate a given function) |
| International Mathematical Olympiad (IMO) 2009, 6.1 IMO 2009 Problems, 5 | https://mathnet.mit.edu/explorer.html?p=usa_2009_ed888c | domain not supported (f on positive integers; triangle condition) |
| Harvard-MIT Mathematics Tournament (HMMT) 2010, Linear? What's The Problem?, 8. | https://mathnet.mit.edu/explorer.html?p=usa_2010_18a217 | not a functional equation (bilinear interpolation) |
| Harvard-MIT Mathematics Tournament (HMMT) 2010, Linear? What's The Problem?, 9. | https://mathnet.mit.edu/explorer.html?p=usa_2010_d028e9 | not a functional equation (multilinear interpolation) |
| Harvard-MIT Mathematics Tournament (HMMT) 2010, Team Round A, 8. | https://mathnet.mit.edu/explorer.html?p=usa_2010_d9db3d | not a functional equation (combinatorics) |
| Harvard-MIT Mathematics Tournament (HMMT) 2010, Algebra Subject Test, 10. | https://mathnet.mit.edu/explorer.html?p=usa_2010_fbcc70 | not a functional equation (polynomial problem) |
| Harvard-MIT Mathematics Tournament (HMMT) 2011, Algebra & Calculus Individual Test, 10. | https://mathnet.mit.edu/explorer.html?p=usa_2011_5f2646 | not a functional equation (iterate a given function) |
| Harvard-MIT Mathematics Tournament (HMMT) 2011, Algebra & Calculus Individual Test, 15. | https://mathnet.mit.edu/explorer.html?p=usa_2011_7d45d5 | not "find all f" (integral values; continuous f on [0,1]) |
| Harvard-MIT Mathematics Tournament (HMMT) 2011, Calculus & Geometry Individual Test, 17. | https://mathnet.mit.edu/explorer.html?p=usa_2011_cbd549 | not "find all f" (derivative values; f on (0,1)) |
| Berkeley Math Circle 2012, 7. | https://mathnet.mit.edu/explorer.html?p=usa_2012_34476f | not a functional equation (prove rationality for a given f) |
| Harvard-MIT Mathematics Tournament (HMMT) 2012, Algebra Test, 7. | https://mathnet.mit.edu/explorer.html?p=usa_2012_3719c2 | not "find all f" (binary operation on R+; continuity) |
| IMO TST 2012, TSTST 2012 Problems, 1 | https://mathnet.mit.edu/explorer.html?p=usa_2012_5176bd | not a single equation in one function of one variable (f of two variables; median condition) |
| Harvard-MIT Mathematics Tournament (HMMT) 2012, Guts, 10. | https://mathnet.mit.edu/explorer.html?p=usa_2012_a70d80 | not a functional equation (polynomial problem) |
| Berkeley Math Circle 2013, 6. | https://mathnet.mit.edu/explorer.html?p=usa_2013_3c3573 | not "find all f" (counting question); domain not supported (Z -> R) |
| IMO TST 2013, TSTST 2013 Problems, 3. | https://mathnet.mit.edu/explorer.html?p=usa_2013_539a5e | not "find all f" (prove that); domain not supported (N) |
| Romanian Master of Mathematics (RMM) 2013, RMM 2013 Problems, 2. | https://mathnet.mit.edu/explorer.html?p=usa_2013_74c50e | not "find all f" (does there exist) |
| Berkeley Math Circle 2013, 5. | https://mathnet.mit.edu/explorer.html?p=usa_2013_db7a06 | not a functional equation (polynomial evaluation problem) |
| IMO TST 2014, TSTST 2014 Problems, 6. | https://mathnet.mit.edu/explorer.html?p=usa_2014_19553f | domain not supported (N); iterates of variable order |
| Harvard-MIT Mathematics Tournament (HMMT) 2014, Guts Round, 9. | https://mathnet.mit.edu/explorer.html?p=usa_2014_1e3bf2 | not "find all f" (asks for a value); domain not supported (nonnegative integers) |
| Harvard-MIT Mathematics Tournament (HMMT) 2014, Guts, 17. | https://mathnet.mit.edu/explorer.html?p=usa_2014_aeace0 | not "find all f" (counting question); domain not supported (N) |
| Harvard-MIT Mathematics Tournament (HMMT) 2015, Guts, 18. | https://mathnet.mit.edu/explorer.html?p=usa_2015_0050c9 | not "find all f" (asks for a value); domain not supported (Z) |
| Harvard-MIT Mathematics Tournament (HMMT) 2015, Guts round, 18. | https://mathnet.mit.edu/explorer.html?p=usa_2015_145df2 | not "find all f" (asks for a maximum value); domain not supported (two-variable function on nonnegative integers) |
| Harvard-MIT Mathematics Tournament (HMMT) 2015, Guts round, 26. | https://mathnet.mit.edu/explorer.html?p=usa_2015_271e26 | not "find all f" (asks for a value); domain not supported (R+); extra hypothesis: continuity, f(2) = 0 |
| Harvard-MIT Mathematics Tournament (HMMT) 2015, Individual, 6. | https://mathnet.mit.edu/explorer.html?p=usa_2015_672ba2 | not "find all f" (asks for a sum of integers); domain not supported (Z) |
| Berkeley Math Circle 2016, 7. | https://mathnet.mit.edu/explorer.html?p=usa_2016_8d69f5 | extra hypothesis: twice differentiable |
| Harvard-MIT Mathematics Tournament (HMMT) 2016, 3. | https://mathnet.mit.edu/explorer.html?p=usa_2016_97d7ae | not "find all f" (prove that); domain not supported (N); too many variables |
| Berkeley Math Circle 2016, 4. | https://mathnet.mit.edu/explorer.html?p=usa_2016_b1d462 | not a single equation in one function (three unknown functions); extra hypothesis: continuity |
| Harvard-MIT Mathematics Tournament (HMMT) 2016, Guts, 22. | https://mathnet.mit.edu/explorer.html?p=usa_2016_c1264f | not "find all f" (asks for a value); domain not supported (Z) |
| American Mathematics Competitions 10 (AMC 10) 2017, Guts, 25. | https://mathnet.mit.edu/explorer.html?p=usa_2017_1e1ecd | not a functional equation (solve a real equation) |
| American Mathematics Competitions 10 (AMC 10) 2017, Algebra and Number Theory, 3. | https://mathnet.mit.edu/explorer.html?p=usa_2017_32e6ec | not "find all f" (asks for possible values of f(2017)) |
| Harvard-MIT Mathematics Tournament (HMMT) 2017, Guts Round, 28. | https://mathnet.mit.edu/explorer.html?p=usa_2017_abef79 | not "find all f" (counting question); domain not supported (finite set) |
| IMO TST 2018, Day 1, TSTST 1 | https://mathnet.mit.edu/explorer.html?p=usa_2018_1d04a5 | domain not supported (Z[x] -> Z); divisibility condition |
| Harvard-MIT Mathematics Tournament (HMMT) 2018, 4. | https://mathnet.mit.edu/explorer.html?p=usa_2018_63f491 | domain not supported (R+) |
| Harvard-MIT Mathematics Tournament (HMMT) 2019, Guts Round, 16. | https://mathnet.mit.edu/explorer.html?p=usa_2019_5817da | not "find all f" (asks for number of possible values of a sum) |
| Harvard-MIT Mathematics Tournament (HMMT) 2019, Algebra and Number Theory, 4. | https://mathnet.mit.edu/explorer.html?p=usa_2019_81b414 | not "find all f" (asks for a sum); domain not supported (N) |
| Berkeley Math Circle 2019, 5. | https://mathnet.mit.edu/explorer.html?p=usa_2019_b1597c | equation uses max and min |
| Bay Area Mathematical Olympiad (BAMO) 2019, Problem 6 | https://mathnet.mit.edu/explorer.html?p=usa_2019_b28219 | not "find all f" (prove that); domain not supported (finite set) |
| Harvard-MIT Mathematics Tournament (HMMT) 2019, Guts Round, 11. | https://mathnet.mit.edu/explorer.html?p=usa_2019_c1a12a | not a functional equation (identity with absolute value, find constants) |
| Harvard-MIT Mathematics Tournament (HMMT) 2019, Combinatorics, 5. | https://mathnet.mit.edu/explorer.html?p=usa_2019_d69ce9 | not a functional equation (probability problem) |
| IMO TST 2019, Day 1, TSTST 1 | https://mathnet.mit.edu/explorer.html?p=usa_2019_f27ccd | domain not supported (binary operation on R+); extra hypothesis: inequality |
| Berkeley Math Circle 2020, 6. | https://mathnet.mit.edu/explorer.html?p=usa_2020_a15b1b | division by a variable; equation holds only on restricted values (x != 0) |
| Harvard-MIT Mathematics Tournament (HMMT) 2020, Team Round, 7. | https://mathnet.mit.edu/explorer.html?p=usa_2020_a63e76 | not a functional equation (absolute value equation) |
| United States of America Junior Mathematical Olympiad (USAJMO) 2021, Day I Problems, USAJMO 1 | https://mathnet.mit.edu/explorer.html?p=usa_2021_1e2e48 | domain not supported (N); two equations |
| Harvard-MIT Mathematics Tournament (HMMT) 2021, General Round, 7. | https://mathnet.mit.edu/explorer.html?p=usa_2021_9213d1 | not a functional equation (given function, solve iterate equation) |
| Harvard-MIT Mathematics Tournament (HMMT) 2021, 23. | https://mathnet.mit.edu/explorer.html?p=usa_2021_c653e6 | not "find all f" (asks for a value); domain not supported (N); extra hypothesis: strictly increasing, f(1) = 1 |
| Harvard-MIT Mathematics Tournament (HMMT) 2022, Guts Round, 31. | https://mathnet.mit.edu/explorer.html?p=usa_2022_05d396 | not a functional equation (integer sequence problem) |
| Berkeley Math Circle 2022, Monthly Contest 1, 4. | https://mathnet.mit.edu/explorer.html?p=usa_2022_4db103 | domain not supported (Z) |
| Harvard-MIT Mathematics Tournament (HMMT) 2022, Team Round, 7. | https://mathnet.mit.edu/explorer.html?p=usa_2022_62ba9b | domain not supported (R\{0} -> R); equation holds only on restricted values (xyz = 1) |
| Harvard-MIT Mathematics Tournament (HMMT) 2022, Team Round, 1. | https://mathnet.mit.edu/explorer.html?p=usa_2022_9cdc63 | not "find all f" (asks for a value); two unknown linear functions |
| Harvard-MIT Mathematics Tournament (HMMT) 2023, 5. | https://mathnet.mit.edu/explorer.html?p=usa_2023_628e08 | not a functional equation (sequence, prove that) |
| Harvard-MIT Mathematics Tournament (HMMT) 2023, 1. | https://mathnet.mit.edu/explorer.html?p=usa_2023_697f93 | domain not supported (Q+) |
| Harvard-MIT Mathematics Tournament (HMMT) 2023, Team Round, 8. | https://mathnet.mit.edu/explorer.html?p=usa_2023_6aee54 | not a functional equation (polynomial problem); division by a variable |
| Harvard-MIT Mathematics Tournament (HMMT) 2023, Algebra and Number Theory Round, 4. | https://mathnet.mit.edu/explorer.html?p=usa_2023_889163 | not a functional equation (polynomial problem, asks for a value) |
| IMO TST 2023, §2.3 USA TST 2023/6, USA TST 2023/6 | https://mathnet.mit.edu/explorer.html?p=usa_2023_de1495 | not "find all f" (prove that); domain not supported (N) |
| Bay Area Mathematical Olympiad (BAMO) 2024, BAMO-12, 4 | https://mathnet.mit.edu/explorer.html?p=usa_2024_552e91 | not a functional equation (polynomial problem); division by a variable |
| Harvard-MIT Mathematics Tournament (HMMT) 2024, Team Round, 6. | https://mathnet.mit.edu/explorer.html?p=usa_2024_6a5aa1 | equation contains a parameter a (rational a != 0), not a fixed rational constant |
| Harvard-MIT Mathematics Tournament (HMMT) 2024, General Round, 5. | https://mathnet.mit.edu/explorer.html?p=usa_2024_926fb4 | not "find all f" (asks for a sum); domain not supported (nonnegative integers) |
| Harvard-MIT Mathematics Tournament (HMMT) 2024, Combinatorics Round, 9. | https://mathnet.mit.edu/explorer.html?p=usa_2024_abc7e4 | not "find all f" (counting permutation triples); domain not supported (finite set) |
| United States of America Junior Mathematical Olympiad (USAJMO) 2025, Day I, JMO 1 | https://mathnet.mit.edu/explorer.html?p=usa_2025_412144 | not "find all f" (prove that); domain not supported (Z) |
| Harvard-MIT Mathematics Tournament (HMMT) 2025, Team Round, 9. | https://mathnet.mit.edu/explorer.html?p=usa_2025_80886b | not "find all f" (find primes p for which f exists); domain not supported (Z) |
| IMO TST 2025, Day I, Problem 2 | https://mathnet.mit.edu/explorer.html?p=usa_2025_990fe9 | not "find all f" (inequality, asks for possible ranges); domain and codomain differ (R -> Z) |
| IMO TST 2025, Solutions to Day 1, TSTST 2 | https://mathnet.mit.edu/explorer.html?p=usa_2025_a11fb3 | not "find all f" (inequality, asks for possible ranges); domain and codomain differ (R -> Z) |
| Berkeley Math Circle, 5. | https://mathnet.mit.edu/explorer.html?p=usa_21e509 | not a functional equation (given piecewise function, solve iterate equation) |
| Berkeley Math Circle, Monthly Contest 7, 5. | https://mathnet.mit.edu/explorer.html?p=usa_22f86a | not "find all f" (prove two equations equivalent) |
| Berkeley Math Circle, 2. | https://mathnet.mit.edu/explorer.html?p=usa_6876f0 | not a functional equation (continued fraction) |
| Berkeley Math Circle, Monthly Contest 2, 4. | https://mathnet.mit.edu/explorer.html?p=usa_6b6ccd | not a functional equation (polynomial problem); division by a variable |
| Berkeley Math Circle, 6. | https://mathnet.mit.edu/explorer.html?p=usa_7f77fd | domain and codomain differ (Q -> R) |
| Berkeley Math Circle, 6. | https://mathnet.mit.edu/explorer.html?p=usa_bbec04 | not "find all f" (prove that); domain not supported (Z) |
| Berkeley Math Circle, Monthly Contest 7, 3. | https://mathnet.mit.edu/explorer.html?p=usa_ce6cf1 | duplicate of seed s14 |
| Berkeley Math Circle, 5. | https://mathnet.mit.edu/explorer.html?p=usa_d057fa | domain not supported (Z) |
| Berkeley Math Circle, 5. | https://mathnet.mit.edu/explorer.html?p=usa_dc7e6a | not "find all f" (does there exist); not a functional equation |
| Berkeley Math Circle, Take-Home Contest #3, 1. | https://mathnet.mit.edu/explorer.html?p=usa_e365a8 | division by expressions in f; extra hypothesis: f(x) + f(y) != 0 |
| Vietnamese Mathematical Olympiad 2001, Second Day, 5 | https://mathnet.mit.edu/explorer.html?p=vnm_2001_45a2d4 | domain not supported (interval (-1, 1)); extra hypothesis: continuity; division by a variable |
| Vietnamese Mathematical Olympiad 2003, Part 1: PROBLEMS, 3 | https://mathnet.mit.edu/explorer.html?p=vnm_2003_16d22f | not a functional equation (polynomial problem) |
| Vietnamese Mathematical Olympiad 2003, Part 1: PROBLEMS, 8 | https://mathnet.mit.edu/explorer.html?p=vnm_2003_98ada4 | not "find all f" (inequality, find greatest constant); domain not supported (R+) |
| Vietnamese Mathematical Olympiad 2006, Second day, Problem 5 | https://mathnet.mit.edu/explorer.html?p=vnm_2006_e20b07 | not a functional equation (polynomial problem) |
| Vietnamese Mathematical Olympiad 2007, 5 | https://mathnet.mit.edu/explorer.html?p=vnm_2007_42542b | equation contains exponentials, a parameter b and f(y)^(-1) |
| Vietnamese Mathematical Olympiad 2008, Contest for Selecting Vietnamese Team to IMO2008, 4 | https://mathnet.mit.edu/explorer.html?p=vnm_2008_b8743b | not a functional equation (polynomial problem) |
| Vietnamese Mathematical Olympiad 2012, 7 | https://mathnet.mit.edu/explorer.html?p=vnm_2012_960dde | extra hypothesis: bijective, increasing |
| Vietnamese Mathematical Olympiad 2013, IMO SELECTION FINAL TEST, Problem 1. | https://mathnet.mit.edu/explorer.html?p=vnm_2013_1c4ab0 | extra hypothesis: limit at 0, f(0) = 0 |
| Vietnamese Mathematical Olympiad 2013, TEAM SELECTION TEST, Problem 3. | https://mathnet.mit.edu/explorer.html?p=vnm_2013_6fb2bd | domain not supported (Z x S_n -> [0,1]); not "find all f" |
| Vietnamese Mathematical Olympiad 2013, Southern Spring School MOCK TEST FOR TST PREPARATION 2013, Problem 3. | https://mathnet.mit.edu/explorer.html?p=vnm_2013_938f45 | domain not supported (Z\{0} -> N*); not a functional equation |
| Vietnamese Mathematical Olympiad 2013, Day 2, 5 | https://mathnet.mit.edu/explorer.html?p=vnm_2013_f0a024 | extra hypothesis: f(0) = 0, f(1) = 2013 |
| Vietnamese Mathematical Olympiad 2016, Day 2, 5 | https://mathnet.mit.edu/explorer.html?p=vnm_2016_d8c35c | not "find all f" (find parameter a); extra hypothesis: f(1) = 2016 |
| Vietnamese Mathematical Olympiad 2022, Day 1, 2 | https://mathnet.mit.edu/explorer.html?p=vnm_2022_22ba21 | domain not supported (R+); division by a variable |
| IMO TST 2022, Day 1, 1 | https://mathnet.mit.edu/explorer.html?p=vnm_2022_b974b3 | equation contains exponential x^2 e^(alpha x) and parameter alpha |
| Vietnamese Mathematical Olympiad 2023, Day 2 (February 25th, 2023), 5 | https://mathnet.mit.edu/explorer.html?p=vnm_2023_9ad037 | not a single equation in one function (two unknown functions f, g); extra hypothesis: f(0) = 2022 |
| IMO TST 2024, Day 1, 1 | https://mathnet.mit.edu/explorer.html?p=vnm_2024_1d7fff | extra hypothesis: continuity; equation contains an arbitrary polynomial parameter P |
| Vietnamese Mathematical Olympiad 2024, Day 1, 2 | https://mathnet.mit.edu/explorer.html?p=vnm_2024_58d02f | not a functional equation (polynomial problem) |
| South African Mathematical Olympiad (SAMO) 2011, University of Stellenbosch Senior Camp December 2011: Test 5, 1 | https://mathnet.mit.edu/explorer.html?p=zaf_2011_69a07e | domain not supported (N) |
| South African Mathematical Olympiad (SAMO) 2012, The Monthly Problem Sets, 11 | https://mathnet.mit.edu/explorer.html?p=zaf_2012_18463b | not "find all f" (prove that); domain not supported (N) |
| South African Mathematical Olympiad (SAMO) 2012, The Monthly Problem Sets, 9 | https://mathnet.mit.edu/explorer.html?p=zaf_2012_23f986 | domain and codomain differ (Q+ -> R+); square root; equation holds only on restricted values (0 < y < x) |
| South African Mathematical Olympiad (SAMO) 2012, Senior Division (Grades 10 to 12), 6 | https://mathnet.mit.edu/explorer.html?p=zaf_2012_72f0ab | inequality, not an equation; domain and codomain differ (N -> R) |
| International Mathematical Olympiad (IMO) 2012, IMO in Mar Del Plata, Argentina 2012: Day 2, 4 | https://mathnet.mit.edu/explorer.html?p=zaf_2012_f15929 | domain not supported (Z); equation holds only on restricted values (a + b + c = 0) |
| South African Mathematical Olympiad (SAMO) 2012, Rhodes University Camp April 2012: Test 3, 3 | https://mathnet.mit.edu/explorer.html?p=zaf_2012_f7ece2 | domain not supported (R+) |
| South African Mathematical Olympiad (SAMO) 2015, Second Round: Senior Section: Grade 10-12, 17 | https://mathnet.mit.edu/explorer.html?p=zaf_2015_d74141 | not "find all f" (asks for a value); domain not supported (R+); division by a variable |
| South African Mathematical Olympiad (SAMO) 2016, Senior Division (Grades 10 to 12), 6 | https://mathnet.mit.edu/explorer.html?p=zaf_2016_39e520 | not a functional equation (polynomial problem) |
| South African Mathematical Olympiad (SAMO) 2019, Senior Division (Grades 10 to 12), 5 | https://mathnet.mit.edu/explorer.html?p=zaf_2019_749c3b | domain not supported (Z) |
| South African Mathematical Olympiad (SAMO) 2022, Senior Division, 6 | https://mathnet.mit.edu/explorer.html?p=zaf_2022_208a50 | not a functional equation (polynomial problem, show infinitely many) |
| South African Mathematical Olympiad (SAMO) 2024, Senior Division (Grades 10 to 12), 6 | https://mathnet.mit.edu/explorer.html?p=zaf_2024_7bd6b6 | not "find all f" (prove that); domain and codomain differ (N -> N0) |
| South African Mathematical Olympiad (SAMO) 2024, Senior Division (Grades 10 to 12), 4 | https://mathnet.mit.edu/explorer.html?p=zaf_2024_b569f7 | domain not supported (Z) |
| International Zhautykov Olympiad (IZhO) 2014, First Day, Problem 2 | https://mathnet.mit.edu/explorer.html?p=zhk_2014_96a9ab | not "find all f" (does there exist); extra hypothesis: surjective |
| International Zhautykov Olympiad (IZhO) 2018, 1-st round, 5. | https://mathnet.mit.edu/explorer.html?p=zhk_2018_bc1dee | not "find all f" (find all a); equation uses floor [y] |
| International Zhautykov Olympiad (IZhO), Second day, №5. | https://mathnet.mit.edu/explorer.html?p=zhk_f9d334 | domain not supported (Z) |
| Asia Pacific Mathematics Olympiad (APMO) 1993, 2 | https://mathnet.mit.edu/explorer.html?p=apm_1993_5590e4 | not a functional equation (counting values of a floor-sum function) |
| Asia Pacific Mathematics Olympiad (APMO) 2008, Problem 4 | https://mathnet.mit.edu/explorer.html?p=apm_2008_ec38c0 | not a functional equation (recursively defined function on N0); domain not supported |
| Bulgarian Mathematical Olympiad 2003, Spring Mathematical Competition, Problem 12.1 | https://mathnet.mit.edu/explorer.html?p=bgr_2003_71574e | not a functional equation (calculus) |
| Bulgarian Mathematical Olympiad 2004, Regional round, Problem 12.2. | https://mathnet.mit.edu/explorer.html?p=bgr_2004_a2d4bb | not a functional equation (calculus: maximum of a given function) |
| Bulgarian Mathematical Olympiad 2004, Regional round, Problem 10.4. | https://mathnet.mit.edu/explorer.html?p=bgr_2004_c2a9fd | not a functional equation (polynomial roots with parameter) |
| Bulgarian Mathematical Olympiad 2004, Team selection test for 21. BMO, Problem 3. | https://mathnet.mit.edu/explorer.html?p=bgr_2004_e21482 | not a functional equation (combinatorics: counting functions on a finite set) |
| Bulgarian Mathematical Olympiad 2004, Team selection test for 21. BMO, Problem 5. | https://mathnet.mit.edu/explorer.html?p=bgr_2004_e37987 | not a functional equation (polynomial problem) |
| Bulgarian Mathematical Olympiad 2005, Winter Mathematical Competition, 12.3 | https://mathnet.mit.edu/explorer.html?p=bgr_2005_426424 | not a functional equation (image of a given function, parameter) |
| Bulgarian Mathematical Olympiad 2006, Winter Mathematical Competition, 12.1 | https://mathnet.mit.edu/explorer.html?p=bgr_2006_8c6c5b | not a functional equation (calculus) |
| Bulgarian Mathematical Olympiad 2006, 10, Problem 10.2. | https://mathnet.mit.edu/explorer.html?p=bgr_2006_d830e7 | not a functional equation (maximum of a given function) |
| IMO TST 2007, 6 | https://mathnet.mit.edu/explorer.html?p=bgr_2007_7a83f0 | not "find all f" (largest number of values); domain not supported (subsets of a finite set) |
| Bulgarian Winter Tournament 2007, 10.1 | https://mathnet.mit.edu/explorer.html?p=bgr_2007_c04ae4 | not a functional equation (equations/inequalities in x for given functions) |
| Bulgarian Spring Tournament 2007, 12.2 | https://mathnet.mit.edu/explorer.html?p=bgr_2007_f6bbb4 | not a functional equation (trigonometric equation roots with parameter) |
| Bulgarian Autumn Tournament 2008, 9, 9.1 | https://mathnet.mit.edu/explorer.html?p=bgr_2008_167a2c | not a functional equation (graphs and area) |
| Bulgarian Mathematical Olympiad 2010, 59. National Mathematical Olympiad Final round, Problem 2. | https://mathnet.mit.edu/explorer.html?p=bgr_2010_d68d44 | not a functional equation (geometry of a cubic graph; proof) |
| Bulgarian Mathematical Olympiad 2011, National Mathematical Olympiad, Final round, 3 | https://mathnet.mit.edu/explorer.html?p=bgr_2011_a70d59 | not "find all f" (prove an inequality); domain not supported (R+) |
| Bulgarian Mathematical Olympiad 2022, Winter Mathematical Competitions, 10.4 | https://mathnet.mit.edu/explorer.html?p=bgr_2022_ae0a6d | not a functional equation (combinatorics: counting injections) |
| Bulgarian Autumn Tournament 2023, 9.1, 1.5 | https://mathnet.mit.edu/explorer.html?p=bgr_2023_35921b | not a functional equation (graphs and area) |
| Bulgarian Autumn Tournament 2023, 12.4, 1.20 | https://mathnet.mit.edu/explorer.html?p=bgr_2023_725427 | not a functional equation (combinatorial geometry) |
| Bulgarian Winter Tournament 2023, 12, 2.19 | https://mathnet.mit.edu/explorer.html?p=bgr_2023_c4adaa | not a functional equation (combinatorics/calculus; prove monotonicity) |
| Belarusian Mathematical Olympiad 2012, FINAL ROUND - Category D, 5 | https://mathnet.mit.edu/explorer.html?p=blr_2012_9176e7 | not a functional equation (intersections of graphs; find parameters) |
| Belarusian Mathematical Olympiad 2019, FINAL ROUND, 3 | https://mathnet.mit.edu/explorer.html?p=blr_2019_efe8a5 | not a functional equation (polynomial problem; prove inequality) |
| IMO TST 2024, Fourth Selection Test, 14 | https://mathnet.mit.edu/explorer.html?p=blr_2024_548b33 | not a functional equation (set partition under a quadratic map) |
| Balkan Mathematical Olympiad Shortlist (BMO Shortlist) 2012, Algebra, A4 | https://mathnet.mit.edu/explorer.html?p=bmo_2012_0ec531 | not a functional equation (geometric extremum) |
| Balkan Mathematical Olympiad Shortlist (BMO Shortlist) 2012, Algebra, A5 | https://mathnet.mit.edu/explorer.html?p=bmo_2012_f7e2ed | not a functional equation (inequality) |
| Balkan Mathematical Olympiad Shortlist (BMO Shortlist) 2020, Number Theory, N3 | https://mathnet.mit.edu/explorer.html?p=bmo_2020_e0be37 | domain not supported (positive integers); divisibility condition, not an equation; k variables |
| Balkan Mathematical Olympiad (BMO) 2021, ALGEBRA, A4 | https://mathnet.mit.edu/explorer.html?p=bmo_2021_2fdefd | not a functional equation (combinatorics of lattice jumps) |
| Balkan Mathematical Olympiad (BMO) 2024, Combinatorics, C2. | https://mathnet.mit.edu/explorer.html?p=bmo_2024_4b7efa | not a functional equation (combinatorics on functions of a finite set) |
| Balkan Mathematical Olympiad (BMO) 2024, Geometry, G7. | https://mathnet.mit.edu/explorer.html?p=bmo_2024_e13d37 | not "find all f" (prove f constant); domain not supported (plane points, geometric condition) |
| Brazilian Mathematical Olympiad (OBM) 2000, 5 | https://mathnet.mit.edu/explorer.html?p=bra_2000_75b48f | not a functional equation (combinatorics: counting isometries) |
| Brazilian Mathematical Olympiad (OBM) 2000, 3 | https://mathnet.mit.edu/explorer.html?p=bra_2000_f14c8f | not a functional equation (number theory sum of a given function) |
| Brazilian Mathematical Olympiad (OBM) 2006, Problem Set 6, 7 | https://mathnet.mit.edu/explorer.html?p=bra_2006_10d6b2 | not a functional equation (iterating a given table function) |
| Brazilian Mathematical Olympiad (OBM) 2009, Undergraduates, Problem 1 | https://mathnet.mit.edu/explorer.html?p=bra_2009_c707da | not a functional equation (calculus) |
| Brazilian Mathematical Olympiad (OBM) 2011, Aritmética e Álgebra, 83 | https://mathnet.mit.edu/explorer.html?p=bra_2011_7d3d0a | not a functional equation (evaluate a sum) |
| Brazilian Mathematical Olympiad (OBM) 2012, Undergraduates, Problem 5 | https://mathnet.mit.edu/explorer.html?p=bra_2012_9d39ab | not a functional equation (calculus/differential equation); domain not supported (R+) |
| Brazilian Mathematical Olympiad (OBM), Lista 3, 1. Carro flex | https://mathnet.mit.edu/explorer.html?p=bra_b582f9 | not a functional equation (word problem) |
| Baltic Way 1996, 14. | https://mathnet.mit.edu/explorer.html?p=btw_1996_795c30 | not a functional equation (polynomial graph geometry) |
| Baltic Way 2010, ALGEBRA, LAT2 | https://mathnet.mit.edu/explorer.html?p=btw_2010_dd2184 | not a functional equation (sequence recurrence; proof) |
| Baltic Way 2014, Algebra, A-11 | https://mathnet.mit.edu/explorer.html?p=btw_2014_b14134 | not a functional equation (functional inequality; yes/no question) |
| Baltic Way 2019, Combinatorics, C13 | https://mathnet.mit.edu/explorer.html?p=btw_2019_bea5f3 | not a functional equation (combinatorics: counting functions) |
| Baltic Way 2020, Geometry, G-8. | https://mathnet.mit.edu/explorer.html?p=btw_2020_25872d | domain not supported (half-strip of the plane); geometric conditions, not a single equation |
| Canadian Mathematical Olympiad (CMO) 1975, Problem 7 | https://mathnet.mit.edu/explorer.html?p=can_1975_b5a06d | not a functional equation (periodicity of sin(x^2)) |
| Canadian Mathematical Olympiad (CMO) 1990, Problem 5 | https://mathnet.mit.edu/explorer.html?p=can_1990_541caa | not a functional equation (recursively defined sequence) |
| Canadian Mathematical Olympiad (CMO) 1996, Problem 5 | https://mathnet.mit.edu/explorer.html?p=can_1996_66183b | not a functional equation (extremes of a floor-sum function) |
| Canadian Mathematical Olympiad (CMO) 2008, 4. | https://mathnet.mit.edu/explorer.html?p=can_2008_79e03b | domain not supported (natural numbers); congruence condition |
| Canadian Mathematical Olympiad (CMO) 2017, Problem Set, 2 | https://mathnet.mit.edu/explorer.html?p=can_2017_f44777 | not "find all f" (prove f(p) prime); domain not supported (positive integers) |
| IMO TST 2005, 6. | https://mathnet.mit.edu/explorer.html?p=che_2005_f66679 | domain not supported (triples of non-negative integers); domain and codomain differ |
| IMO TST 2023, Fourth Exam, 12. | https://mathnet.mit.edu/explorer.html?p=che_2023_d46f87 | not a functional equation (combinatorics) |
| China Mathematical Competition 2002, Part I Multiple-choice Questions, 1 | https://mathnet.mit.edu/explorer.html?p=chn_2002_2ca662 | not a functional equation (monotonicity of a given function) |
| China Mathematical Competition 2002, Part III Word Problems, 15 | https://mathnet.mit.edu/explorer.html?p=chn_2002_59ddeb | not a functional equation (quadratic with conditions; find maximal m) |
| China Mathematical Competition 2002, Part I Multiple-choice Questions, 3 | https://mathnet.mit.edu/explorer.html?p=chn_2002_b1a220 | not a functional equation (parity of a given function) |
| China Mathematical Competition 2004, Part II Short-answer Questions, 7 | https://mathnet.mit.edu/explorer.html?p=chn_2004_2cb376 | not a functional equation (area between graphs) |
| China Mathematical Competition 2004, Part III Word Problems, 15 | https://mathnet.mit.edu/explorer.html?p=chn_2004_f2ce96 | not a functional equation (extrema and inequality) |
| China Mathematical Competition 2005, Part II Short-answer Questions, 8 | https://mathnet.mit.edu/explorer.html?p=chn_2005_434d09 | not a functional equation (inequality via monotonicity) |
| China Mathematical Competition 2005, First Day, 3 | https://mathnet.mit.edu/explorer.html?p=chn_2005_792f2b | not a functional equation (evaluate a sum) |
| China Mathematical Competition 2005, First Day, 2 | https://mathnet.mit.edu/explorer.html?p=chn_2005_d660ee | not a functional equation (minimum of a given function) |
| China Mathematical Competition 2010, Part I Short-Answer Questions, 5 | https://mathnet.mit.edu/explorer.html?p=chn_2010_c3b298 | not a functional equation (extrema of a given function) |
| China Mathematical Olympiad (CMO) 2013, Second Day, 5 | https://mathnet.mit.edu/explorer.html?p=chn_2013_895030 | not a functional equation (combinatorics) |
| China Mathematical Competition 2020, First Round, Test Paper A, 3 | https://mathnet.mit.edu/explorer.html?p=chn_2020_ce83b8 | not a functional equation (minima of a given function) |
| China Mathematical Competition 2021, First Round, Test Paper B, 4 | https://mathnet.mit.edu/explorer.html?p=chn_2021_0e568a | not "find all f" (sum of zeros); domain not supported (R\{0}); division by a variable |
| China Mathematical Competition 2021, First Round, Test Paper A1, 9 | https://mathnet.mit.edu/explorer.html?p=chn_2021_248190 | not a functional equation (given function, find a value) |
| China Mathematical Competition 2021, First Round, Test Paper B1, 10 | https://mathnet.mit.edu/explorer.html?p=chn_2021_4a44dc | not a functional equation (given function, find a minimum) |
| China Mathematical Competition 2021, First Round, Test Paper A2, 11 | https://mathnet.mit.edu/explorer.html?p=chn_2021_bd790a | not a functional equation (polynomial problem) |
| China Mathematical Competition 2021, First Round, Test Paper B1, 1 | https://mathnet.mit.edu/explorer.html?p=chn_2021_f08ba9 | not "find all f" (value of f(f(-1)) for an odd function) |
| IMO TST 2022, Test 2 Day 2, 5 | https://mathnet.mit.edu/explorer.html?p=chn_2022_5a13de | not a functional equation (number theory; prove equivalence) |
| European Girls' Mathematical Olympiad (EGMO) 2024, Problem 5 | https://mathnet.mit.edu/explorer.html?p=egm_2024_efd366 | domain not supported (positive integers); divisor/gcd conditions, not an equation |
| Spanish Mathematical Olympiad 1963, Primera sesión, 1/2. | https://mathnet.mit.edu/explorer.html?p=esp_1963_78ee68 | not a functional equation (piecewise linear word problem) |
| Spanish Mathematical Olympiad 1986, Segunda sesión, 22/4 | https://mathnet.mit.edu/explorer.html?p=esp_1986_180079 | not a functional equation (comparison of means; convexity) |
| Spanish Mathematical Olympiad 1996, Primera sesión, 32/3 | https://mathnet.mit.edu/explorer.html?p=esp_1996_804e11 | not a functional equation (polynomial inequality) |
| Spanish Mathematical Olympiad 2002, Primera sesión, 38/3 | https://mathnet.mit.edu/explorer.html?p=esp_2002_1a1ff5 | not a functional equation (recursively defined function on naturals) |
| Spanish Mathematical Olympiad 2010, Problema 2 | https://mathnet.mit.edu/explorer.html?p=esp_2010_6cee4b | not a functional equation (recursively defined function on N0) |
| Iberoamerican Mathematical Olympiad (OIM) 2014, 5 | https://mathnet.mit.edu/explorer.html?p=esp_2014_e47faf | not a functional equation (combinatorics on a finite set; proof) |
| BarcelonaTech Mathcontest 2014, 4 | https://mathnet.mit.edu/explorer.html?p=esp_2014_f61bcb | not a functional equation (permutations; proof) |
| None, Problema 3 | https://mathnet.mit.edu/explorer.html?p=esp_7a737a | not a functional equation (recursively defined function on naturals) |
| Spanish Mathematical Olympiad, Primera sesión, 12/2 | https://mathnet.mit.edu/explorer.html?p=esp_a449aa | not a functional equation (calculus: study and graph a function) |
| French Mathematical Olympiad 2017, Exercices communs, Exercice 6. | https://mathnet.mit.edu/explorer.html?p=fra_2017_b06dd9 | not a functional equation (combinatorics: counting functions) |
| French Mathematical Olympiad Preparation 2019, Exercices du groupe Junior, Exercice 4 | https://mathnet.mit.edu/explorer.html?p=fra_2019_1a5273 | not "find all f" (prove f constant); domain and codomain differ (Z -> R); extra hypothesis: bounded |
| French Mathematical Olympiad Preparation 2021, Test du 17 Novembre 2021, Exercice 4 | https://mathnet.mit.edu/explorer.html?p=fra_2021_516414 | not a functional equation (sequence convergence) |
| French Mathematical Olympiad Preparation 2022, Exercices Seniors, Exercice 13 | https://mathnet.mit.edu/explorer.html?p=fra_2022_6a321b | not "find all f" (prove f(p) prime); domain not supported (positive integers) |
| IMO TST 2019, Test 1, 1 | https://mathnet.mit.edu/explorer.html?p=hkg_2019_ce479d | not a functional equation (calculus: maximum of a given function) |
| Croatia National Mathematical Competition (Final Round) 2012, Second round – County competition, 4.3. | https://mathnet.mit.edu/explorer.html?p=hrv_2012_6347d3 | not a functional equation (geometry of a parabola) |
| Croatia National Mathematical Competition (Final Round) 2012, Final round – National competition, 3.1. | https://mathnet.mit.edu/explorer.html?p=hrv_2012_953fee | not a functional equation (periodicity of a given function) |
| Croatia National Mathematical Competition (Final Round) 2014, First round – City competition, 2.3 | https://mathnet.mit.edu/explorer.html?p=hrv_2014_49c4cd | not a functional equation (discriminant of a quadratic) |
| Croatia National Mathematical Competition (Final Round) 2014, First round – City competition, 3.1 | https://mathnet.mit.edu/explorer.html?p=hrv_2014_d2ba71 | not a functional equation (extrema of a given function) |
| Croatia National Mathematical Competition (Final Round) 2015, First round – City competition, 4.1 | https://mathnet.mit.edu/explorer.html?p=hrv_2015_bbb454 | not a functional equation (evaluate a given function) |
| Ibero-American Mathematical Olympiad (OIM) 1989, 4th Iberoamerican, B2 | https://mathnet.mit.edu/explorer.html?p=ibe_1989_3ae839 | not a functional equation (recursively defined function on positive integers; find its range) |
| Ibero-American Mathematical Olympiad (OIM) 1990, 5th Iberoamerican, A1 | https://mathnet.mit.edu/explorer.html?p=ibe_1990_245211 | not a functional equation (recursively defined function on non-negative integers) |
| International Mathematical Olympiad (IMO) 2008, Number Theory, N5 | https://mathnet.mit.edu/explorer.html?p=imo_2008_40ef71 | domain not supported (natural numbers); divisor-count and divisibility conditions |
| IMO Shortlist 2012, Algebra, A7 | https://mathnet.mit.edu/explorer.html?p=imo_2012_6a3ef7 | not a functional equation (metapolynomials; proof) |
| IMO Shortlist 2015, Number Theory, N7 | https://mathnet.mit.edu/explorer.html?p=imo_2015_b5a2eb | not a functional equation (number theory: find k for which a k-good f: Z>0 -> Z>0 exists) |
| International Mathematical Olympiad (IMO) 2017, Number Theory, N8 | https://mathnet.mit.edu/explorer.html?p=imo_2017_4a4305 | not "find all f" (prove an inequality; f: Z>0 x Z>0 -> {0,1}) |
| IMO Shortlist 2019, Geometry, G8 | https://mathnet.mit.edu/explorer.html?p=imo_2019_7bd8a9 | not a functional equation (geometry: f on lines of the plane) |
| Indian National Mathematical Olympiad (INMO) 2006, 3. | https://mathnet.mit.edu/explorer.html?p=ind_2006_16deec | not a functional equation (find integer triples fixed by f o f) |
| Indian National Mathematical Olympiad (INMO) 2007, 6 | https://mathnet.mit.edu/explorer.html?p=ind_2007_9757d0 | not a functional equation (combinatorics: counting over permutations) |
| Indian National Mathematical Olympiad (INMO) 2024, Indian National Mathematical Olympiad, 4. | https://mathnet.mit.edu/explorer.html?p=ind_2024_29557d | not a functional equation (combinatorics on sets; asks for values of f(2024), domain N) |
| Irish Mathematical Olympiad 2017, 16 | https://mathnet.mit.edu/explorer.html?p=irl_2017_54189d | not "find all f" (existence question; f: Z -> Z with congruence conditions) |
| Irish Mathematical Olympiad 2024, Problems, 20 | https://mathnet.mit.edu/explorer.html?p=irl_2024_3316c9 | not a functional equation (polynomial roots) |
| Irish Mathematical Olympiad 2024, Problems, 4 | https://mathnet.mit.edu/explorer.html?p=irl_2024_36c8f5 | not a functional equation (polynomial roots) |
| Iranian Mathematical Olympiad 2010, Third Round, 11 | https://mathnet.mit.edu/explorer.html?p=irn_2010_2002e3 | not "find all f" (prove a statement; f: N -> N increasing) |
| Iranian Mathematical Olympiad 2010, Third Round, 8 | https://mathnet.mit.edu/explorer.html?p=irn_2010_5f459a | not a functional equation (graph theory) |
| Iranian Mathematical Olympiad 2010, Second Round, 4 | https://mathnet.mit.edu/explorer.html?p=irn_2010_c2ad22 | not "find all f" (existence question; inequality in two functions) |
| Iranian Mathematical Olympiad 2012, Second Round, 7 | https://mathnet.mit.edu/explorer.html?p=irn_2012_1b5675 | not a functional equation (set theory/combinatorics) |
| Iranian Mathematical Olympiad 2021, Team Selection Test, 3 | https://mathnet.mit.edu/explorer.html?p=irn_2021_a0eca0 | not "find all f" (prove a statement; multiplicative f, g: N -> {0,1}) |
| Iranian Mathematical Olympiad 2025, Third Round - Algebra, 3 | https://mathnet.mit.edu/explorer.html?p=irn_2025_255e36 | not a functional equation (analysis inequality on an explicit function) |
| Iranian Mathematical Olympiad 2025, Team Selection Test - Second Exam, 2 | https://mathnet.mit.edu/explorer.html?p=irn_2025_664197 | not a functional equation (number theory/polynomials) |
| Junior Balkan Mathematical Olympiad (JBMO) 2003, Grade 12, 12.7 | https://mathnet.mit.edu/explorer.html?p=jbm_2003_9d702c | not a functional equation (analytic geometry) |
| Junior Balkan Mathematical Olympiad (JBMO) 2003, Grade 12, 12.6 | https://mathnet.mit.edu/explorer.html?p=jbm_2003_ec611d | not a functional equation (calculus: antiderivatives) |
| JBMO Shortlist 2007, Number Theory, NT4 | https://mathnet.mit.edu/explorer.html?p=jbm_2007_505f4f | not a functional equation (number theory) |
| Moldova Mathematical Olympiad 2018, clasa a XI - a, 11.8. | https://mathnet.mit.edu/explorer.html?p=mda_2018_200a89 | not a functional equation (prove a fixed point exists) |
| Moldova Mathematical Olympiad 2018, clasa a XI - a, 11.1. | https://mathnet.mit.edu/explorer.html?p=mda_2018_b3f1d3 | not a functional equation (calculus: range of an explicit function) |
| Moldova Mathematical Olympiad 2018, Clasa a X-a, ziua întâi, 10.1. | https://mathnet.mit.edu/explorer.html?p=mda_2018_efe906 | not a functional equation (inequality) |
| Moldova Mathematical Olympiad 2019, Prima zi, 11.1. | https://mathnet.mit.edu/explorer.html?p=mda_2019_436650 | not a functional equation (calculus: extrema) |
| Moldova Mathematical Olympiad 2020, Ziua a doua, Clasa a XII-a, 12.5 | https://mathnet.mit.edu/explorer.html?p=mda_2020_207dbe | not a functional equation (calculus: antiderivatives) |
| Moldova Mathematical Olympiad 2020, Ziua a doua, Clasa a XII-a, 12.8 | https://mathnet.mit.edu/explorer.html?p=mda_2020_710a6a | not a functional equation (integral equation for continuous f on an interval) |
| Moldova Mathematical Olympiad 2022, Clasa a XI-a, 11.2 | https://mathnet.mit.edu/explorer.html?p=mda_2022_6df63a | not a functional equation (differential equation) |
| Moldova Mathematical Olympiad 2022, Clasa a XII-a, 12.1. | https://mathnet.mit.edu/explorer.html?p=mda_2022_9cf75a | not a functional equation (calculus: antiderivative) |
| Moldova Mathematical Olympiad 2023, Clasa a XI-a Prima zi, 11.4. | https://mathnet.mit.edu/explorer.html?p=mda_2023_a250cf | not a functional equation (calculus: limit of a sequence) |
| None 2010, Number Theory, 8. | https://mathnet.mit.edu/explorer.html?p=mkd_2010_bc2848 | not "find all f" (compute a value; f: N -> R) |
| International Mathematical Olympiad (IMO) 2017, 24-th Macedonian mathematical olympiad, 5 | https://mathnet.mit.edu/explorer.html?p=mkd_2017_e39b7f | not a functional equation (sequences/combinatorics) |
| IMO TST 2019, Opgave 2. | https://mathnet.mit.edu/explorer.html?p=nld_2019_8f5e59 | not a functional equation (combinatorics: find n for which f, g on a finite set exist) |
| Nordic Mathematical Contest (NMC) 1999, 99.1. | https://mathnet.mit.edu/explorer.html?p=nmo_1999_b96235 | not "find all f" (recursively defined f on non-negative integers; solve f(n) = 1999) |
| Philippine Mathematical Olympiad (PMO), PART I, 6. | https://mathnet.mit.edu/explorer.html?p=phl_1eba6f | not a functional equation (multiple-choice algebra) |
| Philippine Mathematical Olympiad (PMO) 2010, Part I, 9. | https://mathnet.mit.edu/explorer.html?p=phl_2010_fc6e04 | not a functional equation (range of an explicit function) |
| Philippine Mathematical Olympiad (PMO) 2011, National Stage, Oral Phase, 19. | https://mathnet.mit.edu/explorer.html?p=phl_2011_c472b4 | not a functional equation (domain of an explicit function) |
| Philippine Mathematical Olympiad (PMO) 2014, PART I, 12. | https://mathnet.mit.edu/explorer.html?p=phl_2014_dc6cd4 | not a functional equation (algebra on an explicit function) |
| Philippine Mathematical Olympiad (PMO) 2016, AVERAGE, 7. | https://mathnet.mit.edu/explorer.html?p=phl_2016_89393f | not "find all f" (recurrence with given values; compute f(2016)) |
| Philippine Mathematical Olympiad (PMO) 2016, AVERAGE, 4. | https://mathnet.mit.edu/explorer.html?p=phl_2016_94b502 | not a functional equation (polynomial problem) |
| Philippine Mathematical Olympiad (PMO) 2018, EASY, 4. | https://mathnet.mit.edu/explorer.html?p=phl_2018_3dfad6 | not a functional equation (algebra: fixed points of explicit quadratics) |
| Philippine Mathematical Olympiad (PMO) 2018, Part II, 3. | https://mathnet.mit.edu/explorer.html?p=phl_2018_96fcdc | not a functional equation (sequence sum; f: N -> Z) |
| Philippine Mathematical Olympiad (PMO) 2020, DIFFICULT, 4. | https://mathnet.mit.edu/explorer.html?p=phl_2020_201344 | not a functional equation (polynomial problem: fixed points) |
| Philippine Mathematical Olympiad (PMO) 2020, EASY, 15. | https://mathnet.mit.edu/explorer.html?p=phl_2020_f860f6 | not a functional equation (trivia question on the Collatz conjecture) |
| Philippine Mathematical Olympiad (PMO) 2021, PART I, 2. | https://mathnet.mit.edu/explorer.html?p=phl_2021_83cbe1 | not a functional equation (quadratic inequality) |
| Philippine Mathematical Olympiad (PMO) 2021, PART II, 24. | https://mathnet.mit.edu/explorer.html?p=phl_2021_c82f45 | not a functional equation (combinatorics: counting functions on a finite set) |
| Philippine Mathematical Olympiad (PMO) 2022, PART II., 25. | https://mathnet.mit.edu/explorer.html?p=phl_2022_29836b | not a functional equation (geometry: area of a region) |
| Philippine Mathematical Olympiad (PMO), PART I., 4. | https://mathnet.mit.edu/explorer.html?p=phl_6f15b7 | not a functional equation (logarithms) |
| Philippine Mathematical Olympiad (PMO), Part I, 11. | https://mathnet.mit.edu/explorer.html?p=phl_85e783 | not a functional equation (polynomial problem: find roots) |
| Philippine Mathematical Olympiad (PMO), Part I, 5. | https://mathnet.mit.edu/explorer.html?p=phl_9299f3 | not a functional equation (quadratic function) |
| Philippine Mathematical Olympiad (PMO), Part I, 2. | https://mathnet.mit.edu/explorer.html?p=phl_c864a8 | not a functional equation (quadratic function) |
| Philippine Mathematical Olympiad (PMO), PART II, 6. | https://mathnet.mit.edu/explorer.html?p=phl_e6ed27 | not a functional equation (range of an explicit function) |
| Polish Mathematical Olympiad, Rozwiązania zadań konkursowych zawodów stopnia pierwszego, 8. | https://mathnet.mit.edu/explorer.html?p=pol_11891f | not a functional equation (combinatorics: permutations) |
| Polish Mathematical Olympiad, zawodów stopnia trzeciego, 6. | https://mathnet.mit.edu/explorer.html?p=pol_22a76b | not a functional equation (sequences) |
| Polish Mathematical Olympiad, Rozwiązania zadań konkursowych zawodów stopnia trzeciego, 6. | https://mathnet.mit.edu/explorer.html?p=pol_682c82 | not a functional equation (sequences) |
| Polish Mathematical Olympiad, zawodów stopnia pierwszego, 1. | https://mathnet.mit.edu/explorer.html?p=pol_d936df | not a functional equation (quadratic inequality) |
| Olympic Revenge 2016, 5. | https://mathnet.mit.edu/explorer.html?p=prt_2016_25e13d | not "find all f" (prove f = 0; f on integer sequences) |
| Romanian Mathematical Olympiad 2009, The Danube Mathematical Competition, Problem 5. | https://mathnet.mit.edu/explorer.html?p=rou_2009_5b16c1 | not a functional equation (combinatorics) |
| Romanian Mathematical Olympiad Shortlist 2010, Putnam Seniors, 24. | https://mathnet.mit.edu/explorer.html?p=rou_2010_17ec11 | not a functional equation (calculus) |
| Romanian Mathematical Olympiad 2010, Final Round, Problem 4. | https://mathnet.mit.edu/explorer.html?p=rou_2010_1d1ed7 | not a functional equation (calculus) |
| Romanian Mathematical Olympiad 2010, District Round, Problem 3. | https://mathnet.mit.edu/explorer.html?p=rou_2010_4cdedb | not a functional equation (calculus) |
| Romanian Mathematical Olympiad Shortlist 2010, Putnam Seniors, 23. | https://mathnet.mit.edu/explorer.html?p=rou_2010_56be71 | not a functional equation (calculus) |
| Romanian Mathematical Olympiad 2010, District Round, Problem 4. | https://mathnet.mit.edu/explorer.html?p=rou_2010_69bc80 | not a functional equation (calculus) |
| Romanian Mathematical Olympiad 2010, Final Round, Problem 3. | https://mathnet.mit.edu/explorer.html?p=rou_2010_c4709f | not "find all f" (prove an equivalence; functional inequality, f: R -> [0, inf)) |
| Romanian Mathematical Olympiad Shortlist 2010, Putnam Seniors, 25. | https://mathnet.mit.edu/explorer.html?p=rou_2010_dbc3be | not a functional equation (calculus: integral inequality) |
| Romanian Mathematical Olympiad Shortlist 2010, Putnam Seniors, 19. | https://mathnet.mit.edu/explorer.html?p=rou_2010_dc1d85 | not a functional equation (real analysis) |
| Balkan Mathematical Olympiad TST (BMO TST) 2010, First Selection Test, Problem 2. | https://mathnet.mit.edu/explorer.html?p=rou_2010_f6c5ca | not a functional equation (monotonicity of an explicit function) |
| Romanian Mathematical Olympiad Shortlist 2011, PUTNAM SENIORS, 10 | https://mathnet.mit.edu/explorer.html?p=rou_2011_3ac425 | not a functional equation (calculus: differential inequality on an interval) |
| Romanian Mathematical Olympiad Shortlist 2011, PUTNAM SENIORS, 4 | https://mathnet.mit.edu/explorer.html?p=rou_2011_46ebb5 | not a functional equation (real analysis) |
| Romanian Mathematical Olympiad Shortlist 2011, PUTNAM SENIORS, 9 | https://mathnet.mit.edu/explorer.html?p=rou_2011_6762ec | not a functional equation (calculus) |
| IMO TST 2011, SIXTH SELECTION TEST, 15 | https://mathnet.mit.edu/explorer.html?p=rou_2011_85273b | not a functional equation (recursive sequence on positive integers) |
| Romanian Mathematical Olympiad 2011, FINAL ROUND, 3 | https://mathnet.mit.edu/explorer.html?p=rou_2011_abee56 | not a functional equation (calculus) |
| Romanian Mathematical Olympiad 2011, FINAL ROUND, 4 | https://mathnet.mit.edu/explorer.html?p=rou_2011_b4942e | not a functional equation (calculus) |
| Romanian Mathematical Olympiad 2011, FINAL ROUND, 3 | https://mathnet.mit.edu/explorer.html?p=rou_2011_d8a213 | not a functional equation (monotonicity of an explicit function) |
| Romanian Mathematical Olympiad 2011, DISTRICT ROUND, 3 | https://mathnet.mit.edu/explorer.html?p=rou_2011_dfb416 | not a functional equation (calculus) |
| Romanian Mathematical Olympiad Shortlist 2011, PUTNAM SENIORS, 8 | https://mathnet.mit.edu/explorer.html?p=rou_2011_f4a583 | not a functional equation (calculus) |
| Romanian Mathematical Olympiad 2012, Etapa Judeţeană şi a Municipiului Bucureşti, CLASA a XI-a, Problema 4. | https://mathnet.mit.edu/explorer.html?p=rou_2012_42dda9 | not a functional equation (real analysis) |
| Romanian Mathematical Olympiad Shortlist 2013, Seniors, 4 | https://mathnet.mit.edu/explorer.html?p=rou_2013_09b66d | domain not supported (f: N* -> N*, increasing, number-theoretic condition) |
| Romanian Mathematical Olympiad 2013, 11th GRADE, 4 | https://mathnet.mit.edu/explorer.html?p=rou_2013_1181b6 | not a functional equation (real analysis) |
| Romanian Mathematical Olympiad 2013, 11th GRADE, 4 | https://mathnet.mit.edu/explorer.html?p=rou_2013_2e28ae | not a functional equation (calculus: differential equation on [0, inf)) |
| Romanian Mathematical Olympiad 2013, XI. OSZTÁLY, 4. feladat | https://mathnet.mit.edu/explorer.html?p=rou_2013_34c676 | not a functional equation (real analysis) |
| Romanian Mathematical Olympiad 2013, CLASA a XI-a, Problema 4 | https://mathnet.mit.edu/explorer.html?p=rou_2013_36b8f9 | not a functional equation (calculus: differential equation on [0, inf)) |
| Romanian Mathematical Olympiad 2013, 11th GRADE, 3 | https://mathnet.mit.edu/explorer.html?p=rou_2013_437231 | not a functional equation (real analysis) |
| Romanian Mathematical Olympiad Shortlist 2013, Putnam Seniors, 3 | https://mathnet.mit.edu/explorer.html?p=rou_2013_4c60c2 | not a functional equation (real analysis) |
| Romanian Mathematical Olympiad 2013, 9th GRADE, 2 | https://mathnet.mit.edu/explorer.html?p=rou_2013_5bf470 | not "find all f" (prove f = g) |
| Romanian Mathematical Olympiad 2013, XII. OSZTÁLY, 3. feladat | https://mathnet.mit.edu/explorer.html?p=rou_2013_751217 | not a functional equation (calculus) |
| Romanian Mathematical Olympiad Shortlist 2013, Putnam Seniors, 4 | https://mathnet.mit.edu/explorer.html?p=rou_2013_7b91e1 | not a functional equation (real analysis) |
| Romanian Mathematical Olympiad 2013, 12th GRADE, 3 | https://mathnet.mit.edu/explorer.html?p=rou_2013_94509c | not a functional equation (calculus: optimization over functions) |
| Romanian Mathematical Olympiad Shortlist 2013, Putnam Seniors, 8 | https://mathnet.mit.edu/explorer.html?p=rou_2013_951cf8 | not a functional equation (calculus) |
| Romanian Mathematical Olympiad 2013, Clasa a XII-a, Problema 3 | https://mathnet.mit.edu/explorer.html?p=rou_2013_a85d75 | not a functional equation (calculus: optimization over functions) |
| Romanian Mathematical Olympiad 2013, 12th GRADE, 3 | https://mathnet.mit.edu/explorer.html?p=rou_2013_cf030c | not a functional equation (calculus) |
| Romanian Mathematical Olympiad Shortlist 2013, Putnam Seniors, 5 | https://mathnet.mit.edu/explorer.html?p=rou_2013_d2ba6d | not a functional equation (calculus: differentiability, integral inequality; domain [0,inf)) |
| Romanian Mathematical Olympiad 2013, CLASA a XII-a, Problema 3. | https://mathnet.mit.edu/explorer.html?p=rou_2013_fb046a | not a functional equation (integral inequality) |
| Romanian Mathematical Olympiad Shortlist 2014, Putnam Seniors, 1. | https://mathnet.mit.edu/explorer.html?p=rou_2014_194984 | not a functional equation (sequence convergence) |
| Romanian Mathematical Olympiad Shortlist 2014, Putnam Seniors, 8. | https://mathnet.mit.edu/explorer.html?p=rou_2014_2e7f27 | not a functional equation (calculus/inequality equivalence) |
| Romanian Mathematical Olympiad 2014, District Round, Problem 2. | https://mathnet.mit.edu/explorer.html?p=rou_2014_32db76 | not a functional equation (sequence limit, calculus) |
| Romanian Mathematical Olympiad Shortlist 2014, Putnam Seniors, 10. | https://mathnet.mit.edu/explorer.html?p=rou_2014_4c1a3d | not a functional equation (sequence convergence) |
| Romanian Mathematical Olympiad 2014, Final Round, Problem 3. | https://mathnet.mit.edu/explorer.html?p=rou_2014_4fcc26 | not a functional equation (calculus limits) |
| Romanian Mathematical Olympiad 2014, Final Round, Problem 3. | https://mathnet.mit.edu/explorer.html?p=rou_2014_620d29 | not a functional equation (combinatorics: counting functions) |
| Romanian Mathematical Olympiad 2014, District Round, Problem 1. | https://mathnet.mit.edu/explorer.html?p=rou_2014_694f23 | not a functional equation (calculus: integral limit) |
| Romanian Mathematical Olympiad 2014, Final Round, Problem 2. | https://mathnet.mit.edu/explorer.html?p=rou_2014_975414 | not a functional equation (differential equation proof) |
| Romanian Mathematical Olympiad 2014, District Round, Problem 4. | https://mathnet.mit.edu/explorer.html?p=rou_2014_a41f92 | not a functional equation (sequences) |
| Romanian Mathematical Olympiad 2015, DISTRICT ROUND - 11th GRADE, Problem 1 | https://mathnet.mit.edu/explorer.html?p=rou_2015_3657e4 | not a functional equation (real analysis) |
| Romanian Mathematical Olympiad 2015, FINAL ROUND - 12th GRADE, Problem 3 | https://mathnet.mit.edu/explorer.html?p=rou_2015_4ff71a | not a functional equation (calculus: integral maximization) |
| Romanian Mathematical Olympiad 2015, CLASA a XII-a, Problema 4 | https://mathnet.mit.edu/explorer.html?p=rou_2015_5dc1b0 | not a functional equation (calculus: polynomial/integral problem) |
| Romanian Mathematical Olympiad Shortlist 2015, PUTNAM SENIORS, 8 | https://mathnet.mit.edu/explorer.html?p=rou_2015_5fc9b4 | not a functional equation (integral equation on [0,1]) |
| Romanian Mathematical Olympiad 2015, FINAL ROUND - 11th GRADE, Problem 1 | https://mathnet.mit.edu/explorer.html?p=rou_2015_717c04 | not a functional equation (calculus: derivative conditions) |
| Romanian Mathematical Olympiad 2015, CLASA a IX-a, Problema 2 | https://mathnet.mit.edu/explorer.html?p=rou_2015_71ba6a | not a functional equation (quadratic function interval lengths, proof) |
| Romanian Mathematical Olympiad 2015, CLASA a XII-a, Problema 3 | https://mathnet.mit.edu/explorer.html?p=rou_2015_85d164 | not a functional equation (calculus: integral maximization) |
| Romanian Mathematical Olympiad 2015, CLASA a XI-a, Problema 1 | https://mathnet.mit.edu/explorer.html?p=rou_2015_8ba85a | not a functional equation (calculus: derivative conditions) |
| Romanian Mathematical Olympiad 2015, FINAL ROUND - 9th GRADE, Problem 2 | https://mathnet.mit.edu/explorer.html?p=rou_2015_ba5f97 | not a functional equation (quadratic function interval lengths, proof) |
| Romanian Mathematical Olympiad 2015, FINAL ROUND - 10th GRADE, Problem 2 | https://mathnet.mit.edu/explorer.html?p=rou_2015_baf4c9 | not a functional equation (combinatorics: counting functions) |
| Romanian Mathematical Olympiad Shortlist 2015, PUTNAM SENIORS, 7 | https://mathnet.mit.edu/explorer.html?p=rou_2015_c393ea | not a functional equation (calculus: primitives) |
| IMAR Mathematical Competition 2015, Problem 4. | https://mathnet.mit.edu/explorer.html?p=rou_2015_e2ed1c | not a functional equation (polynomial approximation, proof) |
| Romanian Mathematical Olympiad 2015, FINAL ROUND - 12th GRADE, Problem 4 | https://mathnet.mit.edu/explorer.html?p=rou_2015_fe9716 | not a functional equation (calculus: polynomial/integral problem) |
| Romanian Mathematical Olympiad 2016, Clasa a XII-a, Subiectul I. | https://mathnet.mit.edu/explorer.html?p=rou_2016_110ffd | not a functional equation (calculus: primitive, involves \|x-1\|) |
| Romanian Mathematical Olympiad 2016, Etapa Judeţeană şi a Municipiului Bucureşti, CLASA a XII-a, Problema 2 | https://mathnet.mit.edu/explorer.html?p=rou_2016_12b288 | not a functional equation (integral inequality) |
| Romanian Mathematical Olympiad 2016, District Round, 12th Grade, Problem 4. | https://mathnet.mit.edu/explorer.html?p=rou_2016_2a90d6 | not a functional equation (calculus: sequence of integrals) |
| Romanian Mathematical Olympiad 2016, Etapa Locală, Clasa a XII-a, 2. | https://mathnet.mit.edu/explorer.html?p=rou_2016_4299f3 | not a functional equation (calculus: improper integrals) |
| Romanian Mathematical Olympiad 2016, Final Round, 12th Grade, Problem 31. | https://mathnet.mit.edu/explorer.html?p=rou_2016_4889ac | not a functional equation (calculus: continuity criterion) |
| Romanian Mathematical Olympiad Shortlist 2016, Putnam Seniors, 6. | https://mathnet.mit.edu/explorer.html?p=rou_2016_4c4563 | not a functional equation (calculus: limit) |
| IMO TST 2016, Third Selection Test, Problem 9. | https://mathnet.mit.edu/explorer.html?p=rou_2016_5a3051 | not a functional equation (combinatorics on finite sets; domain not supported) |
| Romanian Mathematical Olympiad Shortlist 2016, Putnam Seniors, 7. | https://mathnet.mit.edu/explorer.html?p=rou_2016_6de781 | not a functional equation (calculus: mean value) |
| Romanian Mathematical Olympiad 2016, Etapa Judeţeană şi a Municipiului Bucureşti, CLASA a XII-a, Problema 4 | https://mathnet.mit.edu/explorer.html?p=rou_2016_7a942f | not a functional equation (calculus: sequence of integrals) |
| Romanian Mathematical Olympiad 2016, Final Round, 10th Grade, Problem 21. | https://mathnet.mit.edu/explorer.html?p=rou_2016_81755c | not a functional equation (monotonicity proof) |
| Romanian Mathematical Olympiad 2016, Final Round, 10th Grade, Problem 22. | https://mathnet.mit.edu/explorer.html?p=rou_2016_c3acf9 | not a functional equation (functional inequalities, proof) |
| Romanian Mathematical Olympiad 2016, District Round, 11th Grade, Problem 4. | https://mathnet.mit.edu/explorer.html?p=rou_2016_db8d25 | not a functional equation (inequality in two functions, division by x-y) |
| Romanian Mathematical Olympiad 2016, District Round, 12th Grade, Problem 2. | https://mathnet.mit.edu/explorer.html?p=rou_2016_edfe95 | not a functional equation (integral inequality) |
| Romanian Mathematical Olympiad 2017, Final Round - 11th Grade, Problem 4 | https://mathnet.mit.edu/explorer.html?p=rou_2017_2f9867 | not a functional equation (calculus: mean value theorem) |
| Romanian Mathematical Olympiad Shortlist 2017, PUTNAM SENIORS, 5. | https://mathnet.mit.edu/explorer.html?p=rou_2017_469209 | not a functional equation (calculus: derivatives/Darboux) |
| Romanian Mathematical Olympiad 2017, District Round - 12th Grade, Problem 2 | https://mathnet.mit.edu/explorer.html?p=rou_2017_4bc0e3 | not a functional equation (group theory) |
| Romanian Mathematical Olympiad Shortlist 2017, PUTNAM SENIORS, 7. | https://mathnet.mit.edu/explorer.html?p=rou_2017_6fad7a | not a functional equation (calculus: integral limit) |
| Romanian Mathematical Olympiad 2017, Final Round - 12th Grade, Problem 4 | https://mathnet.mit.edu/explorer.html?p=rou_2017_80ce1c | not a functional equation (calculus: limits) |
| Romanian Mathematical Olympiad Shortlist 2017, PUTNAM SENIORS, 8. | https://mathnet.mit.edu/explorer.html?p=rou_2017_bef254 | not a functional equation (quasiconvexity inequality, proof) |
| Romanian Mathematical Olympiad 2017, Final Round - 12th Grade, Problem 1 | https://mathnet.mit.edu/explorer.html?p=rou_2017_c540a0 | not a functional equation (calculus: sequence limit) |
| Romanian Mathematical Olympiad Shortlist 2017, PUTNAM SENIORS, 9. | https://mathnet.mit.edu/explorer.html?p=rou_2017_c912b2 | not a functional equation (integral inequality, convex functions) |
| Romanian Mathematical Olympiad 2017, District Round - 12th Grade, Problem 1 | https://mathnet.mit.edu/explorer.html?p=rou_2017_e1388d | not a functional equation (integral inequality) |
| Romanian Mathematical Olympiad Shortlist 2017, PUTNAM SENIORS, 6. | https://mathnet.mit.edu/explorer.html?p=rou_2017_ea4b95 | not a functional equation (calculus: integral maximization) |
| Romanian Mathematical Olympiad 2018, District Round - 11th Grade, 4 | https://mathnet.mit.edu/explorer.html?p=rou_2018_0318f8 | not a functional equation (real analysis: continuity proof) |
| Romanian Mathematical Olympiad 2018, 12th Grade, 3 | https://mathnet.mit.edu/explorer.html?p=rou_2018_046bda | not a functional equation (calculus: integral inequality) |
| Romanian Mathematical Olympiad 2018, District Round - 12th Grade, 1 | https://mathnet.mit.edu/explorer.html?p=rou_2018_0611c5 | not a functional equation (calculus: integral functional extremum) |
| Romanian Mathematical Olympiad 2018, District Round - 12th Grade, 3 | https://mathnet.mit.edu/explorer.html?p=rou_2018_444b9b | not a functional equation (integral inequality criterion) |
| Romanian Mathematical Olympiad 2018, CLASA a XII-a, Problema 3 | https://mathnet.mit.edu/explorer.html?p=rou_2018_728717 | not a functional equation (integral inequality criterion) |
| Romanian Mathematical Olympiad 2018, Etapa Judeteana si a Municipiului Bucuresti, CLASA a XI-a, varianta 2, Problema 4 | https://mathnet.mit.edu/explorer.html?p=rou_2018_76ba8d | not a functional equation (real analysis: continuity proof) |
| Romanian Mathematical Olympiad 2018, Clasa a X-a, Problema 1 | https://mathnet.mit.edu/explorer.html?p=rou_2018_83cdc7 | not a functional equation (monotonicity proof) |
| Romanian Mathematical Olympiad 2018, District Round - 9th Grade, 4 | https://mathnet.mit.edu/explorer.html?p=rou_2018_a9adf5 | not a functional equation (monotonicity proof) |
| Romanian Mathematical Olympiad 2018, 12th Grade, 2 | https://mathnet.mit.edu/explorer.html?p=rou_2018_c41631 | not a functional equation (calculus: integral minimization) |
| Romanian Mathematical Olympiad 2018, 10th Grade, 1 | https://mathnet.mit.edu/explorer.html?p=rou_2018_d457d3 | not a functional equation (monotonicity proof) |
| Romanian Mathematical Olympiad 2018, CLASA a XII-a, 3. | https://mathnet.mit.edu/explorer.html?p=rou_2018_e1844e | not a functional equation (calculus: integral inequality) |
| Romanian Mathematical Olympiad 2018, 9th Grade, 3 | https://mathnet.mit.edu/explorer.html?p=rou_2018_e98188 | not a functional equation (quadratic functions, integer values proof) |
| Romanian Mathematical Olympiad Shortlist 2018, Putnam Seniors, 5 | https://mathnet.mit.edu/explorer.html?p=rou_2018_f4ca4c | not a functional equation (calculus: integral limit) |
| Romanian Mathematical Olympiad 2018, CLASA a XII-a, Problema 1 | https://mathnet.mit.edu/explorer.html?p=rou_2018_f7c764 | not a functional equation (calculus: integral functional extremum) |
| Romanian Mathematical Olympiad Shortlist 2019, PUTNAM SENIORS, 3. | https://mathnet.mit.edu/explorer.html?p=rou_2019_69548e | not a functional equation (calculus: mean value theorem) |
| Romanian Mathematical Olympiad 2019, FINAL ROUND - 12th GRADE, Problem 1. | https://mathnet.mit.edu/explorer.html?p=rou_2019_81db82 | not a functional equation (calculus: integral minimization) |
| Romanian Mathematical Olympiad Shortlist 2019, PUTNAM SENIORS, 8. | https://mathnet.mit.edu/explorer.html?p=rou_2019_a783e0 | not a functional equation (integral equation with differentiability hypotheses; domain [0,inf)) |
| Romanian Mathematical Olympiad 2019, DISTRICT ROUND - 12th GRADE, Problem 2. | https://mathnet.mit.edu/explorer.html?p=rou_2019_a81975 | not a functional equation (calculus: integrals) |
| Romanian Mathematical Olympiad 2019, FINAL ROUND - 10th GRADE, Problem 4. | https://mathnet.mit.edu/explorer.html?p=rou_2019_ab0820 | not a functional equation (combinatorics: counting functions on subsets) |
| Romanian Mathematical Olympiad 2019, DISTRICT ROUND - 11th GRADE, Problem 4. | https://mathnet.mit.edu/explorer.html?p=rou_2019_bb3a17 | not a functional equation (real analysis: fixed points, sequences) |
| Romanian Mathematical Olympiad 2019, DISTRICT ROUND - 12th GRADE, Problem 1. | https://mathnet.mit.edu/explorer.html?p=rou_2019_d12564 | not a functional equation (group theory; domain is a finite group) |
| Romanian Mathematical Olympiad Shortlist 2019, PUTNAM SENIORS, 7. | https://mathnet.mit.edu/explorer.html?p=rou_2019_f1edde | not a functional equation (calculus: Riemann sums) |
| Romanian Mathematical Olympiad 2020, 12th GRADE, Problem 4. | https://mathnet.mit.edu/explorer.html?p=rou_2020_4bf972 | not a functional equation (calculus: integral mean value) |
| Gazeta Matematică National Olympiad 2021, Etapa a 3 -a - clasa a XII-a, Problema 1. | https://mathnet.mit.edu/explorer.html?p=rou_2021_691011 | not a functional equation (integral equation) |
| Gazeta Matematică National Olympiad 2021, Etapa a 3 -a - clasa a XII-a, Problema 4. | https://mathnet.mit.edu/explorer.html?p=rou_2021_806bea | not a functional equation (integral inequality) |
| Gazeta Matematică National Olympiad 2021, Etapa III - clasa a XI-a, Problema 3. | https://mathnet.mit.edu/explorer.html?p=rou_2021_a7847e | not a functional equation (calculus: limits of derivatives) |
| Gazeta Matematică National Olympiad 2021, Etapa III - clasa a XI-a, Problema 1. | https://mathnet.mit.edu/explorer.html?p=rou_2021_d71056 | not a functional equation (Darboux property, existence proof) |
| Romanian Mathematical Olympiad 2023, 12th GRADE, 1 | https://mathnet.mit.edu/explorer.html?p=rou_2023_04086d | not a functional equation (differential/integral inequality) |
| Romanian Mathematical Olympiad 2023, 11th GRADE, 4 | https://mathnet.mit.edu/explorer.html?p=rou_2023_62c1db | not a functional equation (calculus: differentiability) |
| Romanian Mathematical Olympiad 2023, 12th GRADE, 3 | https://mathnet.mit.edu/explorer.html?p=rou_2023_70dc4f | not a functional equation (calculus: integral limits) |
| Romanian Mathematical Olympiad Shortlist 2023, PUTNAM SENIORS, 7 | https://mathnet.mit.edu/explorer.html?p=rou_2023_79649c | not a functional equation (group theory of homeomorphisms) |
| Romanian Mathematical Olympiad 2023, 11th GRADE, 1 | https://mathnet.mit.edu/explorer.html?p=rou_2023_925b1f | not a functional equation (differential inequality) |
| Romanian Mathematical Olympiad 2023, 12th GRADE, 4 | https://mathnet.mit.edu/explorer.html?p=rou_2023_ab99e3 | not a functional equation (calculus: integrals) |
| Romanian Mathematical Olympiad Shortlist 2023, PUTNAM SENIORS, 2 | https://mathnet.mit.edu/explorer.html?p=rou_2023_ecacb0 | not a functional equation (differential inequality) |
| Romanian Mathematical Olympiad Shortlist 2023, PUTNAM SENIORS, 8 | https://mathnet.mit.edu/explorer.html?p=rou_2023_fc5500 | not a functional equation (Jensen-type integral inequality, convexity proof) |
| Romanian Mathematical Olympiad 2024, District Round, Problem 4. | https://mathnet.mit.edu/explorer.html?p=rou_2024_0d5708 | not a functional equation (real analysis: limits, monotone functions) |
| Romanian Mathematical Olympiad 2024, Final Round, Problem 3. | https://mathnet.mit.edu/explorer.html?p=rou_2024_34676d | not a functional equation (linear algebra: matrices) |
| Romanian Mathematical Olympiad 2024, Final Round, Problem 1. | https://mathnet.mit.edu/explorer.html?p=rou_2024_4b698f | not a functional equation (integral inequality) |
| Romanian Mathematical Olympiad 2024, Final Round, Problem 3. | https://mathnet.mit.edu/explorer.html?p=rou_2024_648842 | not a functional equation (calculus: limit) |
| Romanian Mathematical Olympiad Shortlist 2024, Putnam Seniors, 6. | https://mathnet.mit.edu/explorer.html?p=rou_2024_677b09 | not a functional equation (integral inequality, convex functions) |
| Romanian Mathematical Olympiad 2024, District Round, Problem 4. | https://mathnet.mit.edu/explorer.html?p=rou_2024_9400e7 | not a functional equation (integral inequality) |
| Romanian Mathematical Olympiad 2024, District Round, Problem 2. | https://mathnet.mit.edu/explorer.html?p=rou_2024_962f3f | not a functional equation (calculus: inverse functions, integrals) |
| Romanian Mathematical Olympiad 2024, Final Round, Problem 1. | https://mathnet.mit.edu/explorer.html?p=rou_2024_9d06f5 | not a functional equation (calculus) |
| Romanian Mathematical Olympiad Shortlist 2024, Putnam Seniors, 7. | https://mathnet.mit.edu/explorer.html?p=rou_2024_e615d9 | not a functional equation (calculus: integrals) |
| Romanian Mathematical Olympiad 2024, Final Round, Problem 3. | https://mathnet.mit.edu/explorer.html?p=rou_2024_ec339c | not a functional equation (combinatorics: counting functions on a finite set) |
| Romanian Mathematical Olympiad 2024, Final Round, Problem 2. | https://mathnet.mit.edu/explorer.html?p=rou_2024_ff44b1 | not a functional equation (affine functions with inequalities) |
| Romanian Mathematical Olympiad 2025, Shortlisted Problems - PUTNAM SENIORS, 7. | https://mathnet.mit.edu/explorer.html?p=rou_2025_37154a | not a functional equation (calculus: integrals) |
| Romanian Mathematical Olympiad 2025, District Round - 12th GRADE, Problem 4 | https://mathnet.mit.edu/explorer.html?p=rou_2025_4ffbdb | not a functional equation (calculus) |
| Romanian Mathematical Olympiad 2025, Final Round - 11th GRADE, Problem 3 | https://mathnet.mit.edu/explorer.html?p=rou_2025_61ff37 | not a functional equation (calculus: differentiability) |
| Romanian Mathematical Olympiad 2025, District Round - 12th GRADE, Problem 3 | https://mathnet.mit.edu/explorer.html?p=rou_2025_65fab9 | not a functional equation (calculus: integrals) |
| Romanian Mathematical Olympiad 2025, Shortlisted Problems - PUTNAM SENIORS, 8. | https://mathnet.mit.edu/explorer.html?p=rou_2025_7ea59a | not a functional equation (calculus: limits) |
| Romanian Mathematical Olympiad 2025, District Round - 11th GRADE, Problem 3 | https://mathnet.mit.edu/explorer.html?p=rou_2025_94e841 | not a functional equation (calculus: limits) |
| Romanian Mathematical Olympiad 2025, Final Round - 12th GRADE, Problem 3 | https://mathnet.mit.edu/explorer.html?p=rou_2025_be14df | not a functional equation (calculus: inequality) |
| Romanian Mathematical Olympiad 2025, Shortlisted Problems - SENIORS, 3. | https://mathnet.mit.edu/explorer.html?p=rou_2025_de5ac8 | domain not supported (f: N* -> N; cube and monotonicity conditions, no equation) |
| Romanian Mathematical Olympiad 2025, Final Round - 12th GRADE, Problem 2 | https://mathnet.mit.edu/explorer.html?p=rou_2025_e13840 | not a functional equation (integral inequality) |
| Russian Mathematical Olympiad 2009, Final round, 10 grade, 10.3 | https://mathnet.mit.edu/explorer.html?p=rus_2009_ad6a4c | not a functional equation (trigonometry: sign changes) |
| All-Russian Mathematical Olympiad 2025, 9 класс, 9.5 | https://mathnet.mit.edu/explorer.html?p=rus_2025_21b815 | not a functional equation (quadratic polynomials) |
| Saudi Arabian Mathematical Competitions 2012, January-February tests - Test 2, 4 | https://mathnet.mit.edu/explorer.html?p=sau_2012_65cf6f | not a functional equation (counting quadratics) |
| Saudi Arabian Mathematical Competitions 2014, Team selection tests for the Balkan Mathematical Olympiad 2014 - Day II, 2 | https://mathnet.mit.edu/explorer.html?p=sau_2014_6519ef | not a functional equation (combinatorics: coloring of integers) |
| Saudi Arabian Mathematical Competitions 2016, Team selection tests for Gulf Mathematical Olympiad 2016 - Level 4, day 1, 1 | https://mathnet.mit.edu/explorer.html?p=sau_2016_d535a4 | not a functional equation (quadratic polynomial inequality) |
| IMO TST 2018, The third day, Problem 3 | https://mathnet.mit.edu/explorer.html?p=sau_2018_d16fcb | not a functional equation (polynomial problem) |
| International Mathematical Olympiad (IMO) 2022, November camp - Test 1, 2 | https://mathnet.mit.edu/explorer.html?p=sau_2022_a8aef3 | not a functional equation (polynomial iteration) |
| International Mathematical Olympiad (IMO) 2022, March camp - Test 5, 3 | https://mathnet.mit.edu/explorer.html?p=sau_2022_f9e7bb | not a functional equation (combinatorics: partitions) |
| International Mathematical Olympiad (IMO) 2023, Test 2, Problem 2. | https://mathnet.mit.edu/explorer.html?p=sau_2023_5615e7 | domain not supported (f: N -> N; divisibility condition) |
| Singapore International Math Olympiad Challenge (SIMOC) 2018, Camp Quiz Day 2, 4 | https://mathnet.mit.edu/explorer.html?p=sgp_2018_06a70a | domain not supported (f: N\{1} -> N; gcd/lcm condition) |
| Silk Road Mathematics Competition (SRMC) 2016, 3 | https://mathnet.mit.edu/explorer.html?p=slk_2016_a66067 | not "find all f" (prove statement; f: N -> N divisibility) |
| All-Union Mathematical Olympiad 1976, 10th ASU problems, Problem 15 | https://mathnet.mit.edu/explorer.html?p=sun_1976_18fb14 | not a functional equation (geometry on a sphere) |
| Slovenian Mathematical Olympiad for Technical Schools 2002, 3. LETNIK, 2. | https://mathnet.mit.edu/explorer.html?p=svn_2002_16c150 | not a functional equation (trigonometric equation) |
| Slovenian Mathematical Olympiad for Technical Schools 2002, 1. LETNIK, 5. | https://mathnet.mit.edu/explorer.html?p=svn_2002_8fcd8f | not a functional equation (graph and area) |
| Slovenian Mathematical Olympiad for Technical Schools 2002, 2. LETNIK, 3. | https://mathnet.mit.edu/explorer.html?p=svn_2002_95a47f | not a functional equation (determine a quadratic from values) |
| Slovenian Mathematical Olympiad for Technical Schools 2002, 4. LETNIK, 1. | https://mathnet.mit.edu/explorer.html?p=svn_2002_b8335e | not a functional equation (rational inequality) |
| Slovenian Mathematical Olympiad for Technical Schools 2004, NALOGE ZA 4. LETNIK, 4. | https://mathnet.mit.edu/explorer.html?p=svn_2004_1f8b6b | not a functional equation (determine parameters from values) |
| Slovenian Mathematical Olympiad for Technical Schools 2006, 3. LETNIK, 1. | https://mathnet.mit.edu/explorer.html?p=svn_2006_40105e | not a functional equation (exponential functions) |
| Slovenian Mathematical Olympiad for Technical Schools 2006, 2. LETNIK, 2. | https://mathnet.mit.edu/explorer.html?p=svn_2006_cc0132 | not a functional equation (linear function graph) |
| Slovenian Mathematical Olympiad 2008, 2. letnik, 1. | https://mathnet.mit.edu/explorer.html?p=svn_2008_02b3a8 | not a functional equation (linear function parameters) |
| Slovenian Mathematical Olympiad 2008, 3. letnik, 4. | https://mathnet.mit.edu/explorer.html?p=svn_2008_af9996 | not a functional equation (exponential function parameters) |
| Slovenian Mathematical Olympiad 2008, 4. letnik, 3. | https://mathnet.mit.edu/explorer.html?p=svn_2008_ea002f | not a functional equation (rational function parameters) |
| Slovenian Mathematical Olympiad for Technical Schools 2010, Naloge za 4. letnik, 2. | https://mathnet.mit.edu/explorer.html?p=svn_2010_6a479d | not a functional equation (domain of a logarithmic function) |
| Slovenian Mathematical Olympiad 2012, First Round - Grade Three, A2 | https://mathnet.mit.edu/explorer.html?p=svn_2012_7e872b | not a functional equation (zeros of given functions) |
| Slovenian Mathematical Olympiad 2013, Grade Four, A2. | https://mathnet.mit.edu/explorer.html?p=svn_2013_45fafc | not a functional equation (evaluate expression for given f) |
| Slovenian Mathematical Olympiad 2013, Naloge za 3. letnik, 1. | https://mathnet.mit.edu/explorer.html?p=svn_2013_b62bb9 | not a functional equation (logarithmic function graph) |
| Slovenian Mathematical Olympiad 2013, Naloge za 3. letnik, 4. | https://mathnet.mit.edu/explorer.html?p=svn_2013_d34c04 | not a functional equation (quadratic functions and inequality) |
| Slovenian Mathematical Olympiad for Technical Schools 2014, 3. letnik, 3. | https://mathnet.mit.edu/explorer.html?p=svn_2014_3eb6dc | not a functional equation (quadratic function parameter) |
| Slovenian Mathematical Olympiad for Technical Schools 2014, 2. letnik, 1. | https://mathnet.mit.edu/explorer.html?p=svn_2014_858c3f | not a functional equation (linear function and area) |
| Slovenian Mathematical Olympiad for Technical Schools 2014, 4. letnik, 3. | https://mathnet.mit.edu/explorer.html?p=svn_2014_b9009d | not a functional equation (rational function graph) |
| Slovenian Mathematical Olympiad for Technical Schools 2015, 3. | https://mathnet.mit.edu/explorer.html?p=svn_2015_1280ff | not a functional equation (linear function parameter) |
| Slovenian Mathematical Olympiad for Technical Schools 2015, Naloge za 4. letnik, 2. | https://mathnet.mit.edu/explorer.html?p=svn_2015_b03a77 | not a functional equation (trigonometric function) |
| Slovenian Mathematical Olympiad for Technical Schools 2015, Naloge za 3. letnik, 2. | https://mathnet.mit.edu/explorer.html?p=svn_2015_d7c096 | not a functional equation (quadratic function minimum) |
| Slovenian Mathematical Olympiad for Technical Schools 2016, 4. letnik, A3 | https://mathnet.mit.edu/explorer.html?p=svn_2016_77a1c0 | not a functional equation (trigonometric function properties) |
| Slovenian Mathematical Olympiad for Technical Schools 2016, 4. letnik, B2 | https://mathnet.mit.edu/explorer.html?p=svn_2016_abeca7 | not a functional equation (calculus: tangents) |
| Slovenian Mathematical Olympiad for Technical Schools 2016, 3. letnik, B2 | https://mathnet.mit.edu/explorer.html?p=svn_2016_de2fd9 | not a functional equation (quadratic function parameter) |
| Slovenian Mathematical Olympiad for Technical Schools 2016, 2. letnik, B2 | https://mathnet.mit.edu/explorer.html?p=svn_2016_f72339 | not a functional equation (piecewise function graph, inverse) |
| Slovenian Mathematical Olympiad for Technical Schools 2017, Naloge za 3. letnik, B1. | https://mathnet.mit.edu/explorer.html?p=svn_2017_019d31 | not a functional equation (calculus: tangent) |
| Slovenian Mathematical Olympiad for Technical Schools 2017, Naloge za 3. letnik, A1. | https://mathnet.mit.edu/explorer.html?p=svn_2017_4935a3 | not a functional equation (quadratic from table of values) |
| Slovenian Mathematical Olympiad for Technical Schools 2017, Naloge za 2. letnik, A2. | https://mathnet.mit.edu/explorer.html?p=svn_2017_6bde85 | not a functional equation (linear function from values) |
| Slovenian Mathematical Olympiad for Technical Schools 2017, Naloge za 4. letnik, A3. | https://mathnet.mit.edu/explorer.html?p=svn_2017_dee5db | not a functional equation (domain of a function) |
| Slovenian Mathematical Olympiad for Technical Schools 2017, Naloge za 4. letnik, B2. | https://mathnet.mit.edu/explorer.html?p=svn_2017_fdd540 | not a functional equation (calculus: tangent) |
| Slovenian Mathematical Olympiad for Technical Schools 2018, 3. letnik, A2 | https://mathnet.mit.edu/explorer.html?p=svn_2018_0ffd1e | not a functional equation (logarithmic function zero) |
| Slovenian Mathematical Olympiad for Technical Schools 2018, 4. letnik, A3 | https://mathnet.mit.edu/explorer.html?p=svn_2018_1da2cb | not a functional equation (calculus: derivative) |
| Slovenian Mathematical Olympiad for Technical Schools 2018, 4. letnik, 2. | https://mathnet.mit.edu/explorer.html?p=svn_2018_3d177d | not a functional equation (rational function graph) |
| Slovenian Mathematical Olympiad for Technical Schools 2018, 4. letnik, A1 | https://mathnet.mit.edu/explorer.html?p=svn_2018_553ddf | not a functional equation (evaluate a given function) |
| Slovenian Mathematical Olympiad for Technical Schools 2018, 3. letnik, 2. | https://mathnet.mit.edu/explorer.html?p=svn_2018_c1428a | not a functional equation (quadratic function parameter) |
| Slovenian Mathematical Olympiad for Technical Schools 2019, Naloge za 4. letnik, A2. | https://mathnet.mit.edu/explorer.html?p=svn_2019_12ebfc | not a functional equation (range of a trigonometric function) |
| Slovenian Mathematical Olympiad for Technical Schools 2019, 3. letnik, 2. | https://mathnet.mit.edu/explorer.html?p=svn_2019_8979e1 | not a functional equation (logarithmic functions) |
| Slovenian Mathematical Olympiad for Technical Schools 2019, Naloge za 4. letnik, B3. | https://mathnet.mit.edu/explorer.html?p=svn_2019_cb1053 | not a functional equation (calculus: stationary points) |
| Slovenian Mathematical Olympiad for Technical Schools 2021, Naloge za 3. letnik, A2. | https://mathnet.mit.edu/explorer.html?p=svn_2021_ac0bea | not a functional equation (domain of a logarithmic function) |
| Slovenian Mathematical Olympiad for Technical Schools 2022, 4. letnik, B3 | https://mathnet.mit.edu/explorer.html?p=svn_2022_db745e | not a functional equation (calculus: curves and monotonicity) |
| Slovenian Mathematical Olympiad for Technical Schools 2023, Naloge za 4. letnik, B1 | https://mathnet.mit.edu/explorer.html?p=svn_2023_9af862 | not a functional equation (polynomial graph intersections) |
| Turkish Mathematical Olympiad 2000, First day (December 8, 2000), 3 | https://mathnet.mit.edu/explorer.html?p=tur_2000_31ba9e | not a functional equation (combinatorics) |
| Turkish Mathematical Olympiad 2008, 4 | https://mathnet.mit.edu/explorer.html?p=tur_2008_cb6d61 | not a functional equation (recurrence / combinatorics) |
| IMO TST 2010, 6 | https://mathnet.mit.edu/explorer.html?p=tur_2010_33fb1c | not a functional equation (combinatorics on lattice points) |
| IMO TST 2011, for IMO 2012, 1 | https://mathnet.mit.edu/explorer.html?p=tur_2011_bc9c8e | not a functional equation (combinatorics: counting functions on subsets) |
| IMO TST 2011, 3 | https://mathnet.mit.edu/explorer.html?p=tur_2011_cff8d2 | not a functional equation (combinatorics) |
| IMO TST 2022, JBMO 2022, 6 | https://mathnet.mit.edu/explorer.html?p=tur_2022_6c14d1 | not a functional equation (quadratic inequality) |
| IMO TST 2023, 7 | https://mathnet.mit.edu/explorer.html?p=tur_2023_70479d | not a functional equation (number theory: sequences) |
| Taiwan IMO Team Selection Training Camp 2012, 獨立研究(二), 1 | https://mathnet.mit.edu/explorer.html?p=twn_2012_2863b3 | not a functional equation (combinatorics: counting permutations) |
| Taiwan Mathematical Olympiad Training Camp 2015, 模擬競賽(二), 5 | https://mathnet.mit.edu/explorer.html?p=twn_2015_92d57f | not a functional equation (iterated piecewise map / sequences) |
| Taiwan IMO Team Selection Training Camp 2018, 獨立研究(二), 2 | https://mathnet.mit.edu/explorer.html?p=twn_2018_0aed17 | not a functional equation (combinatorics: maps on a finite set) |
| IMO TST 2020, Independent Study 1, 1 | https://mathnet.mit.edu/explorer.html?p=twn_2020_8cf0f7 | not a functional equation (number theory) |
| Taiwan IMO Team Selection Training Camp 2021, 國際競賽實作(一), 1 | https://mathnet.mit.edu/explorer.html?p=twn_2021_530498 | domain not supported (f: positive integers -> non-negative integers); extra hypothesis: conditions (1) and (3) |
| Taiwan IMO Team Selection Training Camp 2022, I-N. | https://mathnet.mit.edu/explorer.html?p=twn_2022_be06cf | not a functional equation (number theory: gcd expressions) |
| Taiwan Mathematical Olympiad Training Camp 2022, 1. | https://mathnet.mit.edu/explorer.html?p=twn_2022_f963bb | not a functional equation (inequality) |
| Taiwan IMO Team Selection Training Camp 2023, 獨立研究(二), II-C | https://mathnet.mit.edu/explorer.html?p=twn_2023_af7b8e | not a functional equation (combinatorics) |
| Taiwan Mathematical Olympiad Training Camp 2023, 國際競賽實作(二), 4 | https://mathnet.mit.edu/explorer.html?p=twn_2023_b6c08d | not a functional equation (combinatorics: permutations) |
| Ukrainian Mathematical Olympiad 2006, 11TH FORM, 1 | https://mathnet.mit.edu/explorer.html?p=ukr_2006_a03919 | not a functional equation (polynomial problem) |
| Ukrainian Mathematical Olympiad 2009, Third Round, 11-th grade, 2 | https://mathnet.mit.edu/explorer.html?p=ukr_2009_afe4de | not a functional equation (trigonometry: periodicity) |
| Ukrainian National Mathematical Olympiad 2011, First Tour, 10-th grade, 2 | https://mathnet.mit.edu/explorer.html?p=ukr_2011_60a333 | not a functional equation (quadratic polynomials) |
| Ukrainian Mathematical Olympiad 2012, Regional round, First day, 2 | https://mathnet.mit.edu/explorer.html?p=ukr_2012_85bbcf | not a functional equation (solve equation for a given f) |
| Ukrainian Mathematical Olympiad 2019, The Problems of Ukrainian Authors, 4 | https://mathnet.mit.edu/explorer.html?p=ukr_2019_76bed9 | not "find all f" (existence question; inequality condition, f: A -> (0, +inf)) |
| Ukrainian National Mathematical Olympiad 2020, Third Round, Second Tour, Grade 8, 1 | https://mathnet.mit.edu/explorer.html?p=ukr_2020_e86009 | not a functional equation (polynomial divisibility) |
| Harvard-MIT Mathematics Tournament (HMMT) 1999, Calculus Solutions, Problem C1 | https://mathnet.mit.edu/explorer.html?p=usa_1999_40610b | not a functional equation (calculus: differential equation with given values) |
| Berkeley Math Circle 2000, Monthly Contest #2 - Solutions, 4. | https://mathnet.mit.edu/explorer.html?p=usa_2000_54b4cf | not a functional equation (combinatorics: counting functions on subsets) |
| Berkeley Math Circle 2000, Take-Home Contest #7, 4. | https://mathnet.mit.edu/explorer.html?p=usa_2000_c579f2 | not a functional equation (minimize a given function) |
| Berkeley Math Circle 2000, Monthly Contest #3, 4. | https://mathnet.mit.edu/explorer.html?p=usa_2000_f274f0 | not a functional equation (prove a statement about two functions with f < g) |
| Harvard-MIT Mathematics Tournament (HMMT) 2002, Individual Subject Test: Calculus, 9. | https://mathnet.mit.edu/explorer.html?p=usa_2002_7521be | not a functional equation (calculus: differential inequality) |
| Harvard-MIT Mathematics Tournament (HMMT) 2002, Individual Subject Test: Calculus, 3. | https://mathnet.mit.edu/explorer.html?p=usa_2002_91152d | not a functional equation (calculus: derivatives of products) |
| Harvard-MIT Mathematics Tournament (HMMT) 2002, Individual Subject Test: Calculus, 10. | https://mathnet.mit.edu/explorer.html?p=usa_2002_c047d3 | not "find all f" (asks for an integral value; also continuity hypothesis) |
| Harvard-MIT Mathematics Tournament (HMMT) 2003, Individual Round: Calculus Subject Test, 9. | https://mathnet.mit.edu/explorer.html?p=usa_2003_a50293 | not a functional equation (calculus: differential equation, two functions) |
| Harvard-MIT Mathematics Tournament (HMMT) 2004, Individual Round: Calculus Subject Test, 2. | https://mathnet.mit.edu/explorer.html?p=usa_2004_0a397e | not a functional equation (calculus: derivative value) |
| Harvard-MIT Mathematics Tournament (HMMT) 2005, Individual Round: Calculus Subject Test, 3. | https://mathnet.mit.edu/explorer.html?p=usa_2005_441aeb | not a functional equation (calculus: integrals) |
| Harvard-MIT Mathematics Tournament (HMMT) 2005, Individual Round: Calculus Subject Test, 4. | https://mathnet.mit.edu/explorer.html?p=usa_2005_b24dae | not a functional equation (calculus: differential equation) |
| Harvard-MIT Mathematics Tournament (HMMT) 2005, Individual Round: Calculus Subject Test, 10. | https://mathnet.mit.edu/explorer.html?p=usa_2005_bd7f52 | not a functional equation (calculus: functional-differential equation, asks f(1)) |
| Harvard-MIT Mathematics Tournament (HMMT) 2007, Individual Round: Calculus Test, 9. | https://mathnet.mit.edu/explorer.html?p=usa_2007_ecc0f5 | not a functional equation (calculus: differential equation) |
| Berkeley Math Circle 2008, 4. | https://mathnet.mit.edu/explorer.html?p=usa_2008_9abdf9 | not a functional equation (iterates of a given function on a finite set; prove) |
| Harvard-MIT Mathematics Tournament (HMMT) 2009, General Test, 3. | https://mathnet.mit.edu/explorer.html?p=usa_2009_0d7926 | not a functional equation (period of a given function) |
| Harvard-MIT Mathematics Tournament (HMMT) 2009, Guts Round, 29. | https://mathnet.mit.edu/explorer.html?p=usa_2009_4771ab | not a functional equation (polynomial problem) |
| Harvard-MIT Mathematics Tournament (HMMT) 2009, Guts Round, 18. | https://mathnet.mit.edu/explorer.html?p=usa_2009_5e6aa7 | not "find all f" (counting determining values of f on integer triples; domain not supported) |
| Harvard-MIT Mathematics Tournament (HMMT) 2009, Individual Round: Combinatorics Test, 4. | https://mathnet.mit.edu/explorer.html?p=usa_2009_940966 | not a functional equation (combinatorics: counting functions on a finite set) |
| Harvard-MIT Mathematics Tournament (HMMT) 2009, Individual Round: General Test, Part 1, 9. | https://mathnet.mit.edu/explorer.html?p=usa_2009_cbf864 | not a functional equation (combinatorics: counting functions on a finite set) |
| Harvard-MIT Mathematics Tournament (HMMT) 2009, Individual Round: Calculus Test Solutions, 1. | https://mathnet.mit.edu/explorer.html?p=usa_2009_f1bf3e | not a functional equation (calculus: tangent lines, differential equation) |
| Harvard-MIT Mathematics Tournament (HMMT) 2010, Guts Round, 9. | https://mathnet.mit.edu/explorer.html?p=usa_2010_19eb3e | not a functional equation (combinatorics: counting functions on a finite set) |
| Harvard-MIT Mathematics Tournament (HMMT) 2010, Calculus Subject Test, 2. | https://mathnet.mit.edu/explorer.html?p=usa_2010_6c716f | not a functional equation (calculus: differential equation) |
| Harvard-MIT Mathematics Tournament (HMMT) 2010, Guts Round, 25. | https://mathnet.mit.edu/explorer.html?p=usa_2010_7a9517 | not a functional equation (combinatorics: counting functions on a finite set) |
| Harvard-MIT Mathematics Tournament (HMMT) 2010, Combinatorics Subject Test, 3. | https://mathnet.mit.edu/explorer.html?p=usa_2010_7f5cf7 | not a functional equation (combinatorics: counting function compositions) |
| Harvard-MIT Mathematics Tournament (HMMT) 2010, Calculus Subject Test, 5. | https://mathnet.mit.edu/explorer.html?p=usa_2010_afef21 | not a functional equation (calculus: derivatives) |
| Harvard-MIT Mathematics Tournament (HMMT) 2010, Linear? What's The Problem?, 10. | https://mathnet.mit.edu/explorer.html?p=usa_2010_cdeae5 | not a functional equation (multilinear interpolation, compute a value) |
| Harvard-MIT Mathematics Tournament (HMMT) 2010, Combinatorics Subject Test, 8. | https://mathnet.mit.edu/explorer.html?p=usa_2010_ee4111 | not a functional equation (combinatorics: counting increasing functions) |
| Harvard-MIT Mathematics Tournament (HMMT) 2011, Guts Round, 31. | https://mathnet.mit.edu/explorer.html?p=usa_2011_119699 | not a functional equation (combinatorics: counting permutations) |
| Harvard-MIT Mathematics Tournament (HMMT) 2011, Calculus & Geometry Individual Test, 14. | https://mathnet.mit.edu/explorer.html?p=usa_2011_3bc4da | not a functional equation (calculus: possible integral values; f on [0,1], continuous) |
| Harvard-MIT Mathematics Tournament (HMMT) 2011, Algebra & Calculus Individual Test, 16. | https://mathnet.mit.edu/explorer.html?p=usa_2011_738d72 | not a functional equation (sequence from iterating a quadratic) |
| Harvard-MIT Mathematics Tournament (HMMT) 2011, Algebra & Calculus Individual Test, 7. | https://mathnet.mit.edu/explorer.html?p=usa_2011_9b6c1c | not a functional equation (calculus: derivative of a given function) |
| Harvard-MIT Mathematics Tournament (HMMT) 2011, Calculus & Geometry Individual Test, 3. | https://mathnet.mit.edu/explorer.html?p=usa_2011_d145b9 | not a functional equation (calculus: range of integral values) |
| Harvard-MIT Mathematics Tournament (HMMT) 2011, Combinatorics & Geometry Individual Test, 14. | https://mathnet.mit.edu/explorer.html?p=usa_2011_ffb5af | not a functional equation (combinatorics: counting functions on a finite set) |
| Harvard-MIT Mathematics Tournament (HMMT) 2012, Team A, 2. | https://mathnet.mit.edu/explorer.html?p=usa_2012_1651e8 | not a functional equation (combinatorics: existence of functions on a finite set) |
| Harvard-MIT Mathematics Tournament (HMMT) 2012, Algebra Test, 1. | https://mathnet.mit.edu/explorer.html?p=usa_2012_25bf2a | not a functional equation (graph length of iterates of a given function) |
| Harvard-MIT Mathematics Tournament (HMMT) 2012, Team A, 8. | https://mathnet.mit.edu/explorer.html?p=usa_2012_7a7c30 | not a functional equation (combinatorics: bijective counting proof) |
| Harvard-MIT Mathematics Tournament (HMMT) 2012, Guts, 27. | https://mathnet.mit.edu/explorer.html?p=usa_2012_a9bf72 | not a functional equation (combinatorics: counting commuting permutations) |
| Harvard-MIT Mathematics Tournament (HMMT) 2013, 4. | https://mathnet.mit.edu/explorer.html?p=usa_2013_5e4d69 | not a functional equation (real analysis/topology proof) |
| Harvard-MIT Mathematics Tournament (HMMT) 2013, General Test, 10. | https://mathnet.mit.edu/explorer.html?p=usa_2013_84175d | not a functional equation (combinatorics: counting functions on a finite set) |
| Harvard-MIT Mathematics Tournament (HMMT) 2014, Guts Round, 32. | https://mathnet.mit.edu/explorer.html?p=usa_2014_b651c9 | not a functional equation (number theory: iterates of a given polynomial mod 89) |
| IMO TST 2014, TSTST 2014 Problems, 8. | https://mathnet.mit.edu/explorer.html?p=usa_2014_f1b5d5 | not a functional equation (number theory: recursively defined sequence) |
| Harvard-MIT Mathematics Tournament (HMMT) 2015, Combinatorics, 6. | https://mathnet.mit.edu/explorer.html?p=usa_2015_13d503 | not a functional equation (combinatorics: counting colorings) |
| Harvard-MIT Mathematics Tournament (HMMT) 2015, Team, 7. | https://mathnet.mit.edu/explorer.html?p=usa_2015_1f3697 | not a functional equation (complex analysis: polynomial approximation) |
| Berkeley Math Circle 2015, 6. | https://mathnet.mit.edu/explorer.html?p=usa_2015_50e1eb | not a functional equation (combinatorics: counting functions on a finite set) |
| Harvard-MIT Mathematics Tournament (HMMT) 2015, Guts, 3. | https://mathnet.mit.edu/explorer.html?p=usa_2015_7c1e58 | not a functional equation (set images under functions) |
| Harvard-MIT Mathematics Tournament (HMMT) 2015, Theme round, 7. | https://mathnet.mit.edu/explorer.html?p=usa_2015_9896b0 | not a functional equation (combinatorics: counting functions by cycle structure) |
| Harvard-MIT Mathematics Tournament (HMMT) 2016, Combinatorics, 8. | https://mathnet.mit.edu/explorer.html?p=usa_2016_63f338 | not a functional equation (combinatorics: counting functions on a finite set) |
| Harvard-MIT Mathematics Tournament (HMMT) 2016, Guts, 13. | https://mathnet.mit.edu/explorer.html?p=usa_2016_9cf8bc | not a functional equation (combinatorics: counting monotone Boolean functions) |
| American Mathematics Competitions 10 (AMC 10) 2017, Guts, 33. | https://mathnet.mit.edu/explorer.html?p=usa_2017_48ebb4 | not a functional equation (collection of yes/no existence questions) |
| American Mathematics Competitions 10 (AMC 10) 2017, Algebra and Number Theory, 10. | https://mathnet.mit.edu/explorer.html?p=usa_2017_b8fdc5 | not "find all f" (counting functions N -> {0,...,16} with congruences; domain not supported) |
| Harvard-MIT Mathematics Tournament (HMMT) 2017, 5. | https://mathnet.mit.edu/explorer.html?p=usa_2017_e92b83 | not a functional equation (combinatorics: approximate homomorphisms on {-1,1}^n, prove) |
| Harvard-MIT Mathematics Tournament (HMMT) 2018, Team Round, 7. | https://mathnet.mit.edu/explorer.html?p=usa_2018_382040 | not a functional equation (probability on random functions) |
| Harvard-MIT Mathematics Tournament (HMMT) 2018, Guts Round, 21. | https://mathnet.mit.edu/explorer.html?p=usa_2018_553354 | not a functional equation (combinatorics: counting functions on a finite set) |
| Berkeley Math Circle 2018, Monthly Contest 4, 4. | https://mathnet.mit.edu/explorer.html?p=usa_2018_c3efca | not "find all f" (asks for an example; inequality, codomain [0,1]) |
| IMO TST 2019, Solutions to Day 2, TST 4 | https://mathnet.mit.edu/explorer.html?p=usa_2019_272f92 | not "find all f" (prove; f on Z>=0 x Z>=0) |
| IMO TST 2019, Solutions to Day 1, TST 2 | https://mathnet.mit.edu/explorer.html?p=usa_2019_377e55 | not a functional equation (number theory: bijections on Z/nZ) |
| IMO TST 2019, Day 3, TSTST 7 | https://mathnet.mit.edu/explorer.html?p=usa_2019_412886 | not "find all f" (prove; gcd equation on integers) |
| Harvard-MIT Mathematics Tournament (HMMT) 2019, Algebra and Number Theory, 8. | https://mathnet.mit.edu/explorer.html?p=usa_2019_4f6b06 | not "find all f" (asks a value; divisor-sum equation on N) |
| Harvard-MIT Mathematics Tournament (HMMT) 2019, 5. | https://mathnet.mit.edu/explorer.html?p=usa_2019_af7053 | not "find all f" (counting functions Z -> F_p; domain not supported) |
| Harvard-MIT Mathematics Tournament (HMMT) 2019, Guts Round, 30. | https://mathnet.mit.edu/explorer.html?p=usa_2019_c6e3f2 | not "find all f" (inequality on Z, asks maximum value) |
| Harvard-MIT Mathematics Tournament (HMMT) 2020, Guts Round, 17. | https://mathnet.mit.edu/explorer.html?p=usa_2020_93dddf | not "find all f" (counts possible values; domain not supported: integers > 1) |
| Harvard-MIT Mathematics Tournament (HMMT) 2021, Combinatorics Round, 7. | https://mathnet.mit.edu/explorer.html?p=usa_2021_116c1e | not a functional equation (combinatorics: sum over functions on a finite set) |
| Harvard-MIT Mathematics Tournament (HMMT) 2021, Combinatorics Round, 4. | https://mathnet.mit.edu/explorer.html?p=usa_2021_56f25d | not a functional equation (combinatorics: counting permutations) |
| Harvard-MIT Mathematics Tournament (HMMT) 2021, 16. | https://mathnet.mit.edu/explorer.html?p=usa_2021_e04e2c | not a functional equation (recursively defined function, compute a value) |
| Harvard-MIT Mathematics Tournament (HMMT) 2021, Guts Round, 30. | https://mathnet.mit.edu/explorer.html?p=usa_2021_e73174 | not a functional equation (recursion on integer grid, compute a value) |
| Harvard-MIT Mathematics Tournament (HMMT) 2022, 5. | https://mathnet.mit.edu/explorer.html?p=usa_2022_1d0d9f | not a functional equation (counting functions over F_p^2) |
| Harvard-MIT Mathematics Tournament (HMMT) 2022, Algebra and Number Theory Round, 6. | https://mathnet.mit.edu/explorer.html?p=usa_2022_55d17a | not a functional equation (number theory: divisibility on a finite set) |
| Harvard-MIT Mathematics Tournament (HMMT) 2022, Guts Round, 22. | https://mathnet.mit.edu/explorer.html?p=usa_2022_9baa34 | not a functional equation (polynomial problem) |
| IMO TST 2023, §1.3 USA TST 2023/3, USA TST 2023/3 | https://mathnet.mit.edu/explorer.html?p=usa_2023_4eb572 | not a functional equation (optimization with inequalities on nonnegative integers) |
| Harvard-MIT Mathematics Tournament (HMMT) 2023, Theme Round, 6. | https://mathnet.mit.edu/explorer.html?p=usa_2023_978a59 | not a functional equation (quadratic inequality optimization) |
| IMO TST 2023, Solutions to Day 3, 9 | https://mathnet.mit.edu/explorer.html?p=usa_2023_cb6858 | not a functional equation (counting functions Z/aZ -> Z/p^eZ via finite differences) |
| Harvard-MIT Mathematics Tournament (HMMT) 2024, 4. | https://mathnet.mit.edu/explorer.html?p=usa_2024_1992ab | not a functional equation (combinatorics: bijective counting proof) |
| American Mathematics Competitions 12 (AMC 12) 2024, 20 | https://mathnet.mit.edu/explorer.html?p=usa_2024_f8a0b9 | not a functional equation (geometry) |
| American Invitational Mathematics Examination (AIME) 2025, 15 | https://mathnet.mit.edu/explorer.html?p=usa_2025_5e6994 | not a functional equation (calculus: minima of a given rational function) |
| American Invitational Mathematics Examination (AIME) 2025, Problem 11 | https://mathnet.mit.edu/explorer.html?p=usa_2025_84eb2f | not a functional equation (intersection of a given periodic function with a parabola) |
| Harvard-MIT Mathematics Tournament (HMMT) 2025, Guts Round, 28. | https://mathnet.mit.edu/explorer.html?p=usa_2025_a3a2c2 | not a functional equation (recursively defined function on integers, compute a sum) |
| IMO TST 2025, Day I, 1 | https://mathnet.mit.edu/explorer.html?p=usa_2025_c87ac0 | not a functional equation (combinatorial game with periodic functions) |
| IMO TST 2025, Solutions to Day 1, TST 1 | https://mathnet.mit.edu/explorer.html?p=usa_2025_d1cd24 | not a functional equation (combinatorial game with periodic functions) |
| Berkeley Math Circle, Monthly Contest 6 Solutions, 5. | https://mathnet.mit.edu/explorer.html?p=usa_5c9efa | not "find all f" (existence question; number theory on positive integers) |
| IMO TST 2003, 3 | https://mathnet.mit.edu/explorer.html?p=vnm_2003_23ab5b | not a functional equation (recursively defined function on N x Z, prove) |
| Vietnamese Mathematical Olympiad 2003, Part 1: PROBLEMS, 6 | https://mathnet.mit.edu/explorer.html?p=vnm_2003_d83cc0 | not "find all f" (asks extrema of f(x)f(1-x); trigonometric expressions) |
| Vietnamese Mathematical Olympiad 2006, Second day, Problem 4 | https://mathnet.mit.edu/explorer.html?p=vnm_2006_6a3ccf | not a functional equation (analysis of a given function, prove) |
| Vietnamese Mathematical Olympiad 2013, IMO SELECTION FINAL TEST, Problem 3. | https://mathnet.mit.edu/explorer.html?p=vnm_2013_4017e2 | not a functional equation (combinatorics on words) |
| Vietnamese Mathematical Olympiad 2019, Day 1, 1 | https://mathnet.mit.edu/explorer.html?p=vnm_2019_8cd945 | not a functional equation (real analysis: continuous function limits, prove) |
| South African Mathematical Olympiad (SAMO) 2012, The Monthly Problem Sets, 10 | https://mathnet.mit.edu/explorer.html?p=zaf_2012_a2002b | not "find all f" (prove an inequality; trigonometric expressions) |
| International Zhautykov Olympiad (IZhO) 2019, Second day, №5 | https://mathnet.mit.edu/explorer.html?p=zhk_2019_8141d2 | not a functional equation (number theory: periods of functions on integers, prove) |
| EGMO 2012, Problem 3 | https://web.evanchen.cc/exams/EGMO-2012-notes.pdf | duplicate of egmo-2012-3 (European Girls' Mathematical Olympiad (EGMO) 2012, Problema 3), which is kept |
| EGMO 2014, Problem 6 | https://web.evanchen.cc/exams/EGMO-2014-notes.pdf | duplicate of egmo-2014-6 (rule 1, MathNet record), which is kept with its official answer; the notes here do not state the final answer |
| EGMO 2017, Problem 2 | https://web.evanchen.cc/exams/EGMO-2017-notes.pdf | not "find all f" (find smallest k; f: Z>0 -> Z>0, domain not supported) |
| EGMO 2021, Problem 6 | https://web.evanchen.cc/exams/EGMO-2021-notes.pdf | not a functional equation (number theory with floor sums) |
| ELMO 2014 (official solutions, problem list only) | https://web.evanchen.cc/exams/ELMO-2014-sols.pdf | problem list with no in-scope functional equation (Problem 1: triple of injective functions f, g, h with three equations; not a single equation in one function, extra hypothesis: injective) |
| ELMO 2014 (problem list only) | https://web.evanchen.cc/exams/ELMO-2014.pdf | problem list with no in-scope functional equation (Problem 1: triple of injective functions f, g, h with three equations; not a single equation in one function, extra hypothesis: injective) |
| ELMO 2020 (problem list only) | https://web.evanchen.cc/exams/ELMO-2020.pdf | problem list with no in-scope functional equation (Problem 1: f: N -> N with iterates, domain not supported) |
| ELSMO 2020 (problem list only) | https://web.evanchen.cc/exams/ELSMO-2020.pdf | problem list with no in-scope functional equation (redacted copy of ELMO 2020; Problem 1: f: N -> N, domain not supported) |
| IMO 1998, Problem 6 | https://web.evanchen.cc/exams/IMO-1998-notes.pdf | domain not supported (f: N -> N) |
| IMO 2002, Problem 5 | https://web.evanchen.cc/exams/IMO-2002-notes.pdf | too many variables (x, y, z, t) |
| IMO 2008, Problem 4 | https://web.evanchen.cc/exams/IMO-2008-notes.pdf | domain not supported (positive reals); equation holds only on restricted values (wx = yz); division |
| IMO 2009, Problem 5 | https://web.evanchen.cc/exams/IMO-2009-notes.pdf | domain not supported (Z>0); not an equation (triangle condition) |
| IMO 2010, Problem 1 | https://web.evanchen.cc/exams/IMO-2010-notes.pdf | floor function in equation; answer has restricted parameter (f = c, 1 <= c < 2) |
| IMO 2010, Problem 3 | https://web.evanchen.cc/exams/IMO-2010-notes.pdf | domain not supported (Z>0); not an equation (perfect square condition) |
| IMO 2011, Problem 3 | https://web.evanchen.cc/exams/IMO-2011-notes.pdf | not "find all f" (inequality; prove f(x) = 0 for x <= 0) |
| IMO 2011, Problem 5 | https://web.evanchen.cc/exams/IMO-2011-notes.pdf | not "find all f" (prove; divisibility, f: Z -> Z>0) |
| IMO 2012, Problem 4 | https://web.evanchen.cc/exams/IMO-2012-notes.pdf | domain not supported (Z); equation holds only on restricted values (a + b + c = 0) |
| IMO 2013, Problem 5 | https://web.evanchen.cc/exams/IMO-2013-notes.pdf | not "find all f" satisfying an equation (inequalities, given value; f: Q>0 -> R) |
| USA TST 2016 (problem list only) | https://web.evanchen.cc/exams/IMO-2016-TST.pdf | problem list with no in-scope functional equation (TST 5: W: {1,...,n}^2 -> R, domain not supported) |
| USA TST 2018 (problem list only) | https://web.evanchen.cc/exams/IMO-2018-TST.pdf | problem list with no in-scope functional equation (TST 2: f: Z^2 -> [0,1], domain not supported) |
| USA TST 2019 (problem list only) | https://web.evanchen.cc/exams/IMO-2019-TST.pdf | problem list with no in-scope functional equation (TST 4: f: Z>=0 x Z>=0 -> Z, not "find all f") |
| IMO 2019, Problem 1 | https://web.evanchen.cc/exams/IMO-2019-notes.pdf | domain not supported (Z) |
| USA TST 2021 (problem list only) | https://web.evanchen.cc/exams/IMO-2021-TST.pdf | problem list with no in-scope functional equation (TST 3: functional inequality, not "find all f" satisfying an equation) |
| IMO 2021, Problem 2 | https://web.evanchen.cc/exams/IMO-2021-notes.pdf | not a functional equation (inequality) |
| IMO 2022, Problem 2 | https://web.evanchen.cc/exams/IMO-2022-notes.pdf | domain not supported (R+); not an equation (inequality condition) |
| IMO 2022, Problem 6 | https://web.evanchen.cc/exams/IMO-2022-notes.pdf | not a functional equation (combinatorics) |
| USA TST 2023 (problem list only) | https://web.evanchen.cc/exams/IMO-2023-TST.pdf | problem list with no in-scope functional equation (TST 3: pair of functions on nonnegative integers with inequalities) |
| USA TST 2024, Problem 6 | https://web.evanchen.cc/exams/IMO-2024-TST.pdf | USA TST 2024 problem list without solutions; its in-scope problem 6 is covered by the solutions file (usa-tst-2024-6), which is kept |
| IMO 2024, Problem 6 | https://web.evanchen.cc/exams/IMO-2024-notes.pdf | not "find all f" (find smallest c; disjunctive condition on f: Q -> Q) |
| USA TST 2025 (problem list only) | https://web.evanchen.cc/exams/IMO-2025-TST.pdf | problem list with no in-scope functional equation (Problem 1: game with periodic f: Z -> Z, not a functional equation) |
| IMO 2025, Problem 3 | https://web.evanchen.cc/exams/IMO-2025-notes.pdf | domain not supported (f: N -> N); not an equation (divisibility) |
| IMO 2026, Problem 5 | https://web.evanchen.cc/exams/IMO-2026-notes.pdf | domain not supported (R>0); not an equation (inequalities with square roots) |
| USAJMO 2014, Problem 3 | https://web.evanchen.cc/exams/JMO-2014-notes.pdf | domain not supported (Z); division by a variable; equation holds only on restricted values (x != 0) |
| USAJMO 2015, Problem 4 | https://web.evanchen.cc/exams/JMO-2015-notes.pdf | equation holds only on restricted values (x < y < z < t in arithmetic progression) |
| USAJMO 2019, Problem 2 | https://web.evanchen.cc/exams/JMO-2019-notes.pdf | not a single equation in one function (f, g: Z -> Z, two equations; asks for pairs (a, b)) |
| USAJMO 2021, Problem 1 | https://web.evanchen.cc/exams/JMO-2021-notes.pdf | domain not supported (f: N -> N); two equations |
| USAJMO 2021, Problem 4 | https://web.evanchen.cc/exams/JMO-2021-notes.pdf | not a functional equation (combinatorics) |
| USAJMO 2023, Problem 1 | https://web.evanchen.cc/exams/JMO-2023-notes.pdf | not a functional equation (Diophantine equation) |
| USAJMO 2023, Problem 3 | https://web.evanchen.cc/exams/JMO-2023-notes.pdf | not a functional equation (combinatorics) |
| USAJMO 2025, Problem 1 | https://web.evanchen.cc/exams/JMO-2025-notes.pdf | not "find all f" (prove; f: Z -> Z) |
| USAJMO 2026, Problem 1 | https://web.evanchen.cc/exams/JMO-2026-notes.pdf | not a functional equation (number theory inequality) |
| USA TST 2012 (problem list only) | https://web.evanchen.cc/exams/TST-IMO-2012.pdf | problem list with no in-scope functional equation (Problem 2: f(x + y^2) = f(x) + \|yf(y)\|, absolute value) |
| USA TST 2013 (problem list only) | https://web.evanchen.cc/exams/TST-IMO-2013.pdf | problem list with no in-scope functional equation (Problem 4: f on positive integers, prove) |
| USA TSTST 2011 (problem list only) | https://web.evanchen.cc/exams/TSTST-2011.pdf | problem list with no in-scope functional equation (Problem 1: f on pairs of reals with median condition) |
| USA TSTST 2012 (problem list only) | https://web.evanchen.cc/exams/TSTST-2012.pdf | problem list with no in-scope functional equation (Problem 3: f: N -> N, prove) |
| USA TSTST 2014 (problem list only) | https://web.evanchen.cc/exams/TSTST-2014.pdf | problem list with no in-scope functional equation (Problem 3: not a functional equation (polynomial problem), with square roots and \|x\| <= 1) |
| USA TSTST 2018 (problem list only) | https://web.evanchen.cc/exams/TSTST-2018.pdf | problem list with no in-scope functional equation (theta: Z[x] -> Z, domain not supported) |
| Taiwan TST 2014, Round 1 (problem list only) | https://web.evanchen.cc/exams/TaiwanTST-2014-1.pdf | problem list with no in-scope functional equation (Problem 1: f: N0 -> Z with given value f(2) = 7, domain not supported) |
| USAMO 1996, Problem 6 | https://web.evanchen.cc/exams/USAMO-1996-notes.pdf | not a functional equation (existence of a subset of Z) |
| USAMO 1998, Problem 6 | https://web.evanchen.cc/exams/USAMO-1998-notes.pdf | not a functional equation (geometry) |
| USAMO 2000, Problem 1 | https://web.evanchen.cc/exams/USAMO-2000-notes.pdf | not "find all f" (prove nonexistence; inequality with absolute value) |
| USAMO 2000, Problem 3 | https://web.evanchen.cc/exams/USAMO-2000-notes.pdf | not a functional equation (combinatorics) |
| USAMO 2001, Problem 6 | https://web.evanchen.cc/exams/USAMO-2001-notes.pdf | not "find all f" (prove; function on points of the plane) |
| USAMO 2002, Problem 4 | https://web.evanchen.cc/exams/USAMO-2002-notes.pdf | solver was run on this problem during development (issue #2), before the rule selected it |
| USAMO 2012, Problem 4 | https://web.evanchen.cc/exams/USAMO-2012-notes.pdf | domain not supported (N); also divisibility condition |
| USAMO 2014, Problem 2 | https://web.evanchen.cc/exams/USAMO-2014-notes.pdf | domain not supported (Z); also division by x, holds only for x != 0 |
| USAMO 2016, Problem 4 | https://web.evanchen.cc/exams/USAMO-2016-notes.pdf | duplicate of usajmo-2016-6 (USAJMO 2016, Problem 6), which is kept |
| USAMO 2017, Problem 2 | https://web.evanchen.cc/exams/USAMO-2017-notes.pdf | not a functional equation (combinatorics) |
| USAMO 2018, Problem 2 | https://web.evanchen.cc/exams/USAMO-2018-notes.pdf | domain not supported (R+); also division by a variable |
| USAMO 2019, Problem 1 | https://web.evanchen.cc/exams/USAMO-2019-notes.pdf | domain not supported (N); asks for values of f(1000) |
| USAMO 2019, Problem 6 | https://web.evanchen.cc/exams/USAMO-2019-notes.pdf | not a functional equation (polynomial problem) |
| USAMO 2022, Problem 3 | https://web.evanchen.cc/exams/USAMO-2022-notes.pdf | domain not supported (R+) |
| USAMO 2022, Problem 5 | https://web.evanchen.cc/exams/USAMO-2022-notes.pdf | not a functional equation (combinatorics) |
| USAMO 2023, Problem 2 | https://web.evanchen.cc/exams/USAMO-2023-notes.pdf | domain not supported (R+) |
| USAMO 2023, Problem 3 | https://web.evanchen.cc/exams/USAMO-2023-notes.pdf | not a functional equation (combinatorics) |
| USAMO 2024, Problem 6 | https://web.evanchen.cc/exams/USAMO-2024-notes.pdf | not a functional equation (inequality) |
| USAMO 2026, Problem 1 | https://web.evanchen.cc/exams/USAMO-2026-notes.pdf | not a functional equation (floor-function sum) |
| USEMO 2019 (problem list only) | https://web.evanchen.cc/exams/USEMO-2019.pdf | problem list with no in-scope functional equation (Problem 2: theta: Z[x] -> Z[x], domain not supported) |
| USEMO 2022 (problem list only) | https://web.evanchen.cc/exams/USEMO-2022.pdf | problem list with no in-scope functional equation (Problems 2 and 6: f: Z -> Z, domain not supported; Problem 6 asks for k) |
| USA TST 2015, Problem 4 | https://web.evanchen.cc/exams/sols-TST-IMO-2015.pdf | not "find all f" (decide whether a constant must exist; integrality condition) |
| USA TST 2016, Problem 1 | https://web.evanchen.cc/exams/sols-TST-IMO-2016.pdf | not a functional equation (combinatorics of bijections) |
| USA TST 2016, Problem 5 | https://web.evanchen.cc/exams/sols-TST-IMO-2016.pdf | domain not supported ({1,...,n}^2); sum condition over partitions |
| USA TST 2018, Problem 2 | https://web.evanchen.cc/exams/sols-TST-IMO-2018.pdf | domain not supported (Z^2 -> [0,1]) |
| USA TST 2018, Problem 4 | https://web.evanchen.cc/exams/sols-TST-IMO-2018.pdf | not a functional equation (combinatorics) |
| USA TST 2019, Problem 2 | https://web.evanchen.cc/exams/sols-TST-IMO-2019.pdf | not "find all f" (find n; bijections on Z/nZ) |
| USA TST 2019, Problem 4 | https://web.evanchen.cc/exams/sols-TST-IMO-2019.pdf | domain not supported (Z>=0 x Z>=0); not "find all f" |
| USA TST 2021, Problem 3 | https://web.evanchen.cc/exams/sols-TST-IMO-2021.pdf | not "find all f satisfying an equation" (inequality) |
| USA TST 2023, Problem 3 | https://web.evanchen.cc/exams/sols-TST-IMO-2023.pdf | not a functional equation (combinatorics/optimization) |
| USA TST 2023, Problem 4 | https://web.evanchen.cc/exams/sols-TST-IMO-2023.pdf | not a functional equation (number theory, bitwise xor) |
| USA TST 2023, Problem 6 | https://web.evanchen.cc/exams/sols-TST-IMO-2023.pdf | not "find all f" (prove); domain not supported (N) |
| USA TST 2024, Problem 3 | https://web.evanchen.cc/exams/sols-TST-IMO-2024.pdf | not a functional equation (combinatorics) |
| USA TST 2025, Problem 1 (Solution to TST 1, by Anthony Wang) | https://web.evanchen.cc/exams/sols-TST-IMO-2025.pdf | not a functional equation (combinatorial game) |
| USA TSTST 2011, Problem 1 | https://web.evanchen.cc/exams/sols-TSTST-2011.pdf | domain not supported (function of pairs of reals); median condition, not an equation |
| USA TSTST 2012, Problem 3 | https://web.evanchen.cc/exams/sols-TSTST-2012.pdf | not "find all f" (prove); domain not supported (N) |
| USA TSTST 2013, Problem 6 | https://web.evanchen.cc/exams/sols-TSTST-2013.pdf | domain not supported (N) |
| USA TSTST 2013, Problem 8 | https://web.evanchen.cc/exams/sols-TSTST-2013.pdf | not a functional equation (sequence, prove) |
| USA TSTST 2014, Problem 3 | https://web.evanchen.cc/exams/sols-TSTST-2014.pdf | not a functional equation (polynomial problem) |
| USA TSTST 2016, Problem 1 | https://web.evanchen.cc/exams/sols-TSTST-2016.pdf | not a functional equation (polynomial problem, prove) |
| USA TSTST 2016, Problem 4 | https://web.evanchen.cc/exams/sols-TSTST-2016.pdf | not a functional equation (number theory, Euler phi) |
| USA TSTST 2018, Problem 1 | https://web.evanchen.cc/exams/sols-TSTST-2018.pdf | domain not supported (Z[x] -> Z) |
| USA TSTST 2018, Problem 6 | https://web.evanchen.cc/exams/sols-TSTST-2018.pdf | not a functional equation (combinatorics) |
| USA TSTST 2019, Problem 1 | https://web.evanchen.cc/exams/sols-TSTST-2019.pdf | domain not supported (binary operation on R>0); extra hypothesis: inequality condition |
| USA TSTST 2019, Problem 7 | https://web.evanchen.cc/exams/sols-TSTST-2019.pdf | not "find all f" (prove); domain not supported (Z) |
| USA TSTST 2022, Problem 4 | https://web.evanchen.cc/exams/sols-TSTST-2022.pdf | not "find all f" (prove); domain not supported (N) |
| USA TSTST 2022, Problem 8 | https://web.evanchen.cc/exams/sols-TSTST-2022.pdf | domain and codomain differ (N -> Z); floor function |
| USA TSTST 2023, Problem 9 | https://web.evanchen.cc/exams/sols-TSTST-2023.pdf | not a functional equation (finite differences on Z/aZ) |
| USA TSTST 2024, Problem 2 | https://web.evanchen.cc/exams/sols-TSTST-2024.pdf | not a functional equation (polynomial/number theory) |
| USA TSTST 2024, Problem 5 | https://web.evanchen.cc/exams/sols-TSTST-2024.pdf | not a functional equation (inequality on binary digit sums) |
| USA TSTST 2024, Problem 6 | https://web.evanchen.cc/exams/sols-TSTST-2024.pdf | not "find all f" (does there exist); domain not supported (Z>0) |
| USA TST 2002, Problem 4 (problem list only) | https://web.evanchen.cc/exams/tse02.pdf | not a functional equation (combinatorics, prove) |

# Counts

| | covered | in scope | skipped |
|---|---|---|---|
| rule 1 (MathNet, tagged) | 1164 | 130 | 1034 |
| rule 2a (MathNet, text search) | 441 | 0 | 441 |
| rule 2b (Evan Chen's notes) | 107 | 7 | 100 |
| **total** | 1712 | 137 | 1575 |

Two rule 1 problems, China TST 2021 Test III problem 5 and Korean MO 2015
problem 1, were first listed above as skipped. They are in scope, and were
left out only because `scripts/validate_bench.py` did not finish on their
exponents (2021 and 2015). They were moved to `real.jsonl` once the validator
gained an exponent limit. No search had been run on the benchmark at that
point. The checker refuses to load either equation ("identity too large"),
so both count as unsolved for version 1.
