#### seed (50 problems)

| solver | solved | rate | mean checker calls (solved) | median calls (solved) | mean time per problem |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 34/50 | 68.0% | 3.3 | 1 | 0.04s |
| network, search (128 calls) | 40/50 | 80.0% | 16.3 | 1 | 0.08s |
| network, search (2000 calls) | 42/50 | 84.0% | 57.7 | 1 | 0.965s |
| untrained network, no backtracking (32 calls) | 25/50 | 50.0% | 9.6 | 9 | 0.104s |
| untrained network, search (128 calls) | 32/50 | 64.0% | 19.6 | 6 | 0.104s |
| uniform policy, no backtracking (32 calls) | 14/50 | 28.0% | 5.4 | 5 | 0.005s |
| uniform policy, search (128 calls) | 29/50 | 58.0% | 23.3 | 7 | 0.011s |
| brute force (128 calls) | 32/50 | 64.0% | 9.0 | 1 | 0.018s |
| brute force (2000 calls) | 39/50 | 78.0% | 123.8 | 4 | 0.166s |

Solved per sampling seed: network, no backtracking (32 calls): [34, 34, 33]; network, search (128 calls): [40, 37, 36]; network, search (2000 calls): [42, 41, 45]

Mean checker calls on commonly solved problems: network, no backtracking (32 calls): 1.7 calls vs brute force 6.4 on the 30 problems both solve; network, search (128 calls): 5.5 calls vs brute force 9.1 on the 31 problems both solve; network, search (2000 calls): 34.9 calls vs brute force 91.1 on the 37 problems both solve.

| solver | 0M | 5M | 10M | 15M | 20M |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 21/22 | 11/15 | 1/11 | 1/1 | 0/1 |
| network, search (128 calls) | 21/22 | 15/15 | 3/11 | 1/1 | 0/1 |
| network, search (2000 calls) | 22/22 | 15/15 | 4/11 | 1/1 | 0/1 |
| untrained network, no backtracking (32 calls) | 16/22 | 7/15 | 1/11 | 1/1 | 0/1 |
| untrained network, search (128 calls) | 21/22 | 9/15 | 1/11 | 1/1 | 0/1 |
| uniform policy, no backtracking (32 calls) | 8/22 | 4/15 | 1/11 | 1/1 | 0/1 |
| uniform policy, search (128 calls) | 19/22 | 8/15 | 1/11 | 1/1 | 0/1 |
| brute force (128 calls) | 22/22 | 7/15 | 2/11 | 1/1 | 0/1 |
| brute force (2000 calls) | 22/22 | 12/15 | 4/11 | 1/1 | 0/1 |

#### synthetic-tier1 (200 problems)

| solver | solved | rate | mean checker calls (solved) | median calls (solved) | mean time per problem |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 179/200 | 89.5% | 1.9 | 1 | 0.016s |
| network, search (128 calls) | 186/200 | 93.0% | 3.2 | 1 | 0.023s |
| untrained network, no backtracking (32 calls) | 148/200 | 74.0% | 6.2 | 3 | 0.055s |
| untrained network, search (128 calls) | 169/200 | 84.5% | 13.0 | 4 | 0.049s |
| uniform policy, no backtracking (32 calls) | 112/200 | 56.0% | 8.9 | 6 | 0.003s |
| uniform policy, search (128 calls) | 162/200 | 81.0% | 13.6 | 5 | 0.006s |
| brute force (128 calls) | 173/200 | 86.5% | 4.3 | 1 | 0.007s |
| brute force (2000 calls) | 177/200 | 88.5% | 36.2 | 1 | 0.07s |

Solved per sampling seed: network, no backtracking (32 calls): [179, 178, 179]; network, search (128 calls): [186, 186, 186]

Mean checker calls on commonly solved problems: network, no backtracking (32 calls): 1.4 calls vs brute force 3.9 on the 168 problems both solve; network, search (128 calls): 2.2 calls vs brute force 4.3 on the 173 problems both solve.

#### synthetic-tier2 (200 problems)

| solver | solved | rate | mean checker calls (solved) | median calls (solved) | mean time per problem |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 167/200 | 83.5% | 3.1 | 1 | 0.038s |
| network, search (128 calls) | 171/200 | 85.5% | 9.6 | 1 | 0.079s |
| untrained network, no backtracking (32 calls) | 102/200 | 51.0% | 6.8 | 4 | 0.122s |
| untrained network, search (128 calls) | 129/200 | 64.5% | 16.0 | 5 | 0.129s |
| uniform policy, no backtracking (32 calls) | 74/200 | 37.0% | 10.9 | 9 | 0.005s |
| uniform policy, search (128 calls) | 128/200 | 64.0% | 20.8 | 9 | 0.012s |
| brute force (128 calls) | 132/200 | 66.0% | 4.0 | 1 | 0.018s |
| brute force (2000 calls) | 144/200 | 72.0% | 51.0 | 1 | 0.235s |

Solved per sampling seed: network, no backtracking (32 calls): [167, 164, 160]; network, search (128 calls): [171, 170, 176]

Mean checker calls on commonly solved problems: network, no backtracking (32 calls): 1.9 calls vs brute force 4.0 on the 130 problems both solve; network, search (128 calls): 3.5 calls vs brute force 4.0 on the 132 problems both solve.

#### synthetic-tier3 (200 problems)

| solver | solved | rate | mean checker calls (solved) | median calls (solved) | mean time per problem |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 79/200 | 39.5% | 3.7 | 1 | 0.093s |
| network, search (128 calls) | 89/200 | 44.5% | 12.7 | 2 | 0.183s |
| untrained network, no backtracking (32 calls) | 42/200 | 21.0% | 7.2 | 4 | 0.151s |
| untrained network, search (128 calls) | 65/200 | 32.5% | 23.8 | 8 | 0.209s |
| uniform policy, no backtracking (32 calls) | 25/200 | 12.5% | 12.0 | 10 | 0.008s |
| uniform policy, search (128 calls) | 57/200 | 28.5% | 28.9 | 10 | 0.023s |
| brute force (128 calls) | 60/200 | 30.0% | 7.3 | 2 | 0.042s |
| brute force (2000 calls) | 81/200 | 40.5% | 82.6 | 5 | 0.606s |

Solved per sampling seed: network, no backtracking (32 calls): [79, 78, 79]; network, search (128 calls): [89, 88, 91]

Mean checker calls on commonly solved problems: network, no backtracking (32 calls): 2.0 calls vs brute force 6.6 on the 58 problems both solve; network, search (128 calls): 4.2 calls vs brute force 7.3 on the 60 problems both solve.

#### synthetic-tier4 (200 problems)

| solver | solved | rate | mean checker calls (solved) | median calls (solved) | mean time per problem |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 52/200 | 26.0% | 4.0 | 2 | 0.164s |
| network, search (128 calls) | 57/200 | 28.5% | 12.1 | 3 | 0.39s |
| untrained network, no backtracking (32 calls) | 27/200 | 13.5% | 4.3 | 3 | 0.221s |
| untrained network, search (128 calls) | 41/200 | 20.5% | 22.7 | 10 | 0.282s |
| uniform policy, no backtracking (32 calls) | 18/200 | 9.0% | 9.1 | 4 | 0.011s |
| uniform policy, search (128 calls) | 37/200 | 18.5% | 33.6 | 11 | 0.032s |
| brute force (128 calls) | 46/200 | 23.0% | 13.3 | 5 | 0.052s |
| brute force (2000 calls) | 52/200 | 26.0% | 37.3 | 5 | 0.817s |

Solved per sampling seed: network, no backtracking (32 calls): [52, 51, 49]; network, search (128 calls): [57, 57, 53]

Mean checker calls on commonly solved problems: network, no backtracking (32 calls): 3.0 calls vs brute force 13.8 on the 43 problems both solve; network, search (128 calls): 6.2 calls vs brute force 13.4 on the 45 problems both solve.
