#### seed (51 problems)

| solver | solved | rate | mean checker calls (solved) | median calls (solved) | mean time per problem |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 48/51 | 94.1% | 1.1 | 0 | 0.046s |
| network, search (128 calls) | 45/51 | 88.2% | 2.8 | 0 | 0.084s |
| network, search (2000 calls) | 51/51 | 100.0% | 39.3 | 0 | 0.223s |
| untrained network, no backtracking (32 calls) | 45/51 | 88.2% | 0.3 | 0 | 0.028s |
| untrained network, search (128 calls) | 47/51 | 92.2% | 3.2 | 0 | 0.073s |
| untrained network, search (2000 calls) | 49/51 | 96.1% | 23.3 | 0 | 0.652s |
| uniform policy, no backtracking (32 calls) | 45/51 | 88.2% | 0.4 | 0 | 0.006s |
| uniform policy, search (128 calls) | 45/51 | 88.2% | 1.3 | 0 | 0.023s |
| brute force (128 calls) | 47/51 | 92.2% | 6.4 | 0 | 0.021s |
| brute force (2000 calls) | 50/51 | 98.0% | 64.5 | 0 | 0.067s |

Solved per sampling seed: network, no backtracking (32 calls): [48, 45, 46]; network, search (128 calls): [45, 45, 46]; network, search (2000 calls): [51, 51, 51]

Mean checker calls on commonly solved problems: network, no backtracking (32 calls): 0.1 calls vs brute force 2.1 on the 44 problems both solve; network, search (128 calls): 0.2 calls vs brute force 2.1 on the 44 problems both solve; network, search (2000 calls): 34.4 calls vs brute force 64.5 on the 50 problems both solve.

| solver | 0M | 5M | 10M | 15M | 20M |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 22/22 | 15/15 | 9/12 | 1/1 | 1/1 |
| network, search (128 calls) | 22/22 | 15/15 | 7/12 | 1/1 | 0/1 |
| network, search (2000 calls) | 22/22 | 15/15 | 12/12 | 1/1 | 1/1 |
| untrained network, no backtracking (32 calls) | 22/22 | 15/15 | 7/12 | 1/1 | 0/1 |
| untrained network, search (128 calls) | 22/22 | 15/15 | 9/12 | 1/1 | 0/1 |
| untrained network, search (2000 calls) | 22/22 | 15/15 | 11/12 | 1/1 | 0/1 |
| uniform policy, no backtracking (32 calls) | 22/22 | 15/15 | 7/12 | 1/1 | 0/1 |
| uniform policy, search (128 calls) | 22/22 | 15/15 | 7/12 | 1/1 | 0/1 |
| brute force (128 calls) | 22/22 | 15/15 | 9/12 | 1/1 | 0/1 |
| brute force (2000 calls) | 22/22 | 15/15 | 12/12 | 1/1 | 0/1 |

#### dev (32 problems)

| solver | solved | rate | mean checker calls (solved) | median calls (solved) | mean time per problem |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 21/32 | 65.6% | 1.4 | 0 | 0.113s |
| network, search (128 calls) | 22/32 | 68.8% | 8.4 | 0 | 0.428s |
| network, search (2000 calls) | 23/32 | 71.9% | 23.0 | 0 | 5.488s |
| untrained network, no backtracking (32 calls) | 20/32 | 62.5% | 1.6 | 0 | 0.074s |
| untrained network, search (128 calls) | 21/32 | 65.6% | 9.5 | 0 | 0.367s |
| untrained network, search (2000 calls) | 24/32 | 75.0% | 33.2 | 0 | 4.369s |
| uniform policy, no backtracking (32 calls) | 23/32 | 71.9% | 2.8 | 0 | 0.023s |
| uniform policy, search (128 calls) | 23/32 | 71.9% | 5.9 | 0 | 0.191s |
| brute force (128 calls) | 18/32 | 56.2% | 0.1 | 0 | 0.168s |
| brute force (2000 calls) | 23/32 | 71.9% | 51.2 | 0 | 1.038s |

Solved per sampling seed: network, no backtracking (32 calls): [21, 22, 19]; network, search (128 calls): [22, 23, 20]; network, search (2000 calls): [23, 24, 23]

Mean checker calls on commonly solved problems: network, no backtracking (32 calls): 0.2 calls vs brute force 0.1 on the 18 problems both solve; network, search (128 calls): 1.1 calls vs brute force 0.1 on the 18 problems both solve; network, search (2000 calls): 23.3 calls vs brute force 51.5 on the 22 problems both solve.

| solver | 0M | 5M | 10M | 15M | 20M | 25M | 35M | 40M |
|---|---|---|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 3/3 | 5/7 | 3/6 | 7/9 | 1/3 | 1/1 | 1/2 | 0/1 |
| network, search (128 calls) | 3/3 | 5/7 | 3/6 | 8/9 | 1/3 | 1/1 | 1/2 | 0/1 |
| network, search (2000 calls) | 3/3 | 6/7 | 3/6 | 8/9 | 1/3 | 1/1 | 1/2 | 0/1 |
| untrained network, no backtracking (32 calls) | 3/3 | 5/7 | 3/6 | 7/9 | 1/3 | 1/1 | 0/2 | 0/1 |
| untrained network, search (128 calls) | 3/3 | 5/7 | 3/6 | 8/9 | 1/3 | 1/1 | 0/2 | 0/1 |
| untrained network, search (2000 calls) | 3/3 | 6/7 | 4/6 | 8/9 | 1/3 | 1/1 | 1/2 | 0/1 |
| uniform policy, no backtracking (32 calls) | 3/3 | 6/7 | 4/6 | 8/9 | 1/3 | 1/1 | 0/2 | 0/1 |
| uniform policy, search (128 calls) | 3/3 | 6/7 | 4/6 | 8/9 | 1/3 | 1/1 | 0/2 | 0/1 |
| brute force (128 calls) | 3/3 | 5/7 | 2/6 | 7/9 | 1/3 | 0/1 | 0/2 | 0/1 |
| brute force (2000 calls) | 3/3 | 6/7 | 4/6 | 8/9 | 1/3 | 1/1 | 0/2 | 0/1 |

#### synthetic-tier1 (200 problems)

| solver | solved | rate | mean checker calls (solved) | median calls (solved) | mean time per problem |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 188/200 | 94.0% | 0.2 | 0 | 0.012s |
| network, search (128 calls) | 189/200 | 94.5% | 0.6 | 0 | 0.038s |
| untrained network, no backtracking (32 calls) | 183/200 | 91.5% | 0.1 | 0 | 0.008s |
| untrained network, search (128 calls) | 186/200 | 93.0% | 1.2 | 0 | 0.035s |
| uniform policy, no backtracking (32 calls) | 182/200 | 91.0% | 0.0 | 0 | 0.002s |
| uniform policy, search (128 calls) | 186/200 | 93.0% | 0.5 | 0 | 0.011s |
| brute force (128 calls) | 188/200 | 94.0% | 2.1 | 0 | 0.016s |
| brute force (2000 calls) | 190/200 | 95.0% | 15.7 | 0 | 0.124s |

Solved per sampling seed: network, no backtracking (32 calls): [188, 189, 188]; network, search (128 calls): [189, 189, 190]

Mean checker calls on commonly solved problems: network, no backtracking (32 calls): 0.2 calls vs brute force 1.9 on the 187 problems both solve; network, search (128 calls): 0.6 calls vs brute force 2.1 on the 188 problems both solve.

#### synthetic-tier2 (200 problems)

| solver | solved | rate | mean checker calls (solved) | median calls (solved) | mean time per problem |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 193/200 | 96.5% | 0.1 | 0 | 0.012s |
| network, search (128 calls) | 194/200 | 97.0% | 0.7 | 0 | 0.023s |
| untrained network, no backtracking (32 calls) | 185/200 | 92.5% | 0.1 | 0 | 0.01s |
| untrained network, search (128 calls) | 188/200 | 94.0% | 0.4 | 0 | 0.023s |
| uniform policy, no backtracking (32 calls) | 187/200 | 93.5% | 0.2 | 0 | 0.002s |
| uniform policy, search (128 calls) | 190/200 | 95.0% | 0.7 | 0 | 0.021s |
| brute force (128 calls) | 191/200 | 95.5% | 2.4 | 0 | 0.02s |
| brute force (2000 calls) | 194/200 | 97.0% | 18.6 | 0 | 0.062s |

Solved per sampling seed: network, no backtracking (32 calls): [193, 193, 193]; network, search (128 calls): [194, 194, 193]

Mean checker calls on commonly solved problems: network, no backtracking (32 calls): 0.1 calls vs brute force 2.4 on the 191 problems both solve; network, search (128 calls): 0.2 calls vs brute force 2.4 on the 191 problems both solve.

#### synthetic-tier3 (200 problems)

| solver | solved | rate | mean checker calls (solved) | median calls (solved) | mean time per problem |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 139/200 | 69.5% | 0.5 | 0 | 0.11s |
| network, search (128 calls) | 141/200 | 70.5% | 1.4 | 0 | 0.5s |
| untrained network, no backtracking (32 calls) | 133/200 | 66.5% | 0.9 | 0 | 0.096s |
| untrained network, search (128 calls) | 140/200 | 70.0% | 3.0 | 0 | 0.334s |
| uniform policy, no backtracking (32 calls) | 134/200 | 67.0% | 0.7 | 0 | 0.058s |
| uniform policy, search (128 calls) | 135/200 | 67.5% | 1.7 | 0 | 0.23s |
| brute force (128 calls) | 138/200 | 69.0% | 5.6 | 0 | 0.139s |
| brute force (2000 calls) | 144/200 | 72.0% | 53.6 | 0 | 1.319s |

Solved per sampling seed: network, no backtracking (32 calls): [139, 139, 140]; network, search (128 calls): [141, 139, 140]

Mean checker calls on commonly solved problems: network, no backtracking (32 calls): 0.5 calls vs brute force 4.5 on the 135 problems both solve; network, search (128 calls): 1.2 calls vs brute force 5.2 on the 137 problems both solve.

#### synthetic-tier4 (200 problems)

| solver | solved | rate | mean checker calls (solved) | median calls (solved) | mean time per problem |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 105/200 | 52.5% | 0.8 | 0 | 0.256s |
| network, search (128 calls) | 109/200 | 54.5% | 6.4 | 0 | 1.682s |
| untrained network, no backtracking (32 calls) | 96/200 | 48.0% | 1.2 | 0 | 0.213s |
| untrained network, search (128 calls) | 104/200 | 52.0% | 7.0 | 0 | 1.165s |
| uniform policy, no backtracking (32 calls) | 102/200 | 51.0% | 1.8 | 0 | 0.192s |
| uniform policy, search (128 calls) | 105/200 | 52.5% | 6.3 | 0 | 0.883s |
| brute force (128 calls) | 97/200 | 48.5% | 3.8 | 0 | 0.435s |
| brute force (2000 calls) | 114/200 | 57.0% | 90.2 | 0 | 3.813s |

Solved per sampling seed: network, no backtracking (32 calls): [105, 103, 104]; network, search (128 calls): [109, 107, 107]

Mean checker calls on commonly solved problems: network, no backtracking (32 calls): 0.4 calls vs brute force 2.8 on the 95 problems both solve; network, search (128 calls): 1.5 calls vs brute force 2.9 on the 96 problems both solve.
