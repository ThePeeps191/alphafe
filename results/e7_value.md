#### seed (50 problems)

| solver | solved | rate | mean checker calls (solved) | median calls (solved) | mean time per problem |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 34/50 | 68.0% | 3.3 | 1 | 0.041s |
| network, search (128 calls) | 37/50 | 74.0% | 10.1 | 1 | 0.129s |
| network, search (2000 calls) | 42/50 | 84.0% | 47.9 | 1 | 1.5s |
| untrained network, no backtracking (32 calls) | 25/50 | 50.0% | 9.6 | 9 | 0.103s |
| untrained network, search (128 calls) | 32/50 | 64.0% | 19.6 | 6 | 0.104s |
| uniform policy, no backtracking (32 calls) | 14/50 | 28.0% | 5.4 | 5 | 0.005s |
| uniform policy, search (128 calls) | 29/50 | 58.0% | 23.3 | 7 | 0.011s |
| brute force (128 calls) | 32/50 | 64.0% | 9.0 | 1 | 0.018s |
| brute force (2000 calls) | 39/50 | 78.0% | 123.8 | 4 | 0.163s |

Solved per sampling seed: network, no backtracking (32 calls): [34, 34, 33]; network, search (128 calls): [37, 40, 35]; network, search (2000 calls): [42, 42, 43]

Mean checker calls on commonly solved problems: network, no backtracking (32 calls): 1.7 calls vs brute force 6.4 on the 30 problems both solve; network, search (128 calls): 5.2 calls vs brute force 9.1 on the 31 problems both solve; network, search (2000 calls): 12.9 calls vs brute force 91.1 on the 37 problems both solve.

| solver | 0M | 5M | 10M | 15M | 20M |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 21/22 | 11/15 | 1/11 | 1/1 | 0/1 |
| network, search (128 calls) | 21/22 | 13/15 | 2/11 | 1/1 | 0/1 |
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
| network, search (128 calls) | 185/200 | 92.5% | 3.1 | 1 | 0.027s |
| untrained network, no backtracking (32 calls) | 148/200 | 74.0% | 6.2 | 3 | 0.057s |
| untrained network, search (128 calls) | 169/200 | 84.5% | 13.0 | 4 | 0.049s |
| uniform policy, no backtracking (32 calls) | 112/200 | 56.0% | 8.9 | 6 | 0.003s |
| uniform policy, search (128 calls) | 162/200 | 81.0% | 13.6 | 5 | 0.005s |
| brute force (128 calls) | 173/200 | 86.5% | 4.3 | 1 | 0.007s |
| brute force (2000 calls) | 177/200 | 88.5% | 36.2 | 1 | 0.07s |

Solved per sampling seed: network, no backtracking (32 calls): [179, 178, 179]; network, search (128 calls): [185, 187, 185]

Mean checker calls on commonly solved problems: network, no backtracking (32 calls): 1.4 calls vs brute force 3.9 on the 168 problems both solve; network, search (128 calls): 1.8 calls vs brute force 4.3 on the 172 problems both solve.

#### synthetic-tier2 (200 problems)

| solver | solved | rate | mean checker calls (solved) | median calls (solved) | mean time per problem |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 167/200 | 83.5% | 3.1 | 1 | 0.039s |
| network, search (128 calls) | 169/200 | 84.5% | 9.0 | 1 | 0.092s |
| untrained network, no backtracking (32 calls) | 102/200 | 51.0% | 6.8 | 4 | 0.121s |
| untrained network, search (128 calls) | 129/200 | 64.5% | 16.0 | 5 | 0.13s |
| uniform policy, no backtracking (32 calls) | 74/200 | 37.0% | 10.9 | 9 | 0.005s |
| uniform policy, search (128 calls) | 128/200 | 64.0% | 20.8 | 9 | 0.012s |
| brute force (128 calls) | 132/200 | 66.0% | 4.0 | 1 | 0.018s |
| brute force (2000 calls) | 144/200 | 72.0% | 51.0 | 1 | 0.238s |

Solved per sampling seed: network, no backtracking (32 calls): [167, 164, 160]; network, search (128 calls): [169, 167, 169]

Mean checker calls on commonly solved problems: network, no backtracking (32 calls): 1.9 calls vs brute force 4.0 on the 130 problems both solve; network, search (128 calls): 2.7 calls vs brute force 4.0 on the 131 problems both solve.

#### synthetic-tier3 (200 problems)

| solver | solved | rate | mean checker calls (solved) | median calls (solved) | mean time per problem |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 79/200 | 39.5% | 3.7 | 1 | 0.092s |
| network, search (128 calls) | 87/200 | 43.5% | 11.1 | 2 | 0.205s |
| untrained network, no backtracking (32 calls) | 42/200 | 21.0% | 7.2 | 4 | 0.151s |
| untrained network, search (128 calls) | 65/200 | 32.5% | 23.8 | 8 | 0.21s |
| uniform policy, no backtracking (32 calls) | 25/200 | 12.5% | 12.0 | 10 | 0.008s |
| uniform policy, search (128 calls) | 57/200 | 28.5% | 28.9 | 10 | 0.024s |
| brute force (128 calls) | 60/200 | 30.0% | 7.3 | 2 | 0.043s |
| brute force (2000 calls) | 81/200 | 40.5% | 82.6 | 5 | 0.625s |

Solved per sampling seed: network, no backtracking (32 calls): [79, 78, 79]; network, search (128 calls): [87, 86, 89]

Mean checker calls on commonly solved problems: network, no backtracking (32 calls): 2.0 calls vs brute force 6.6 on the 58 problems both solve; network, search (128 calls): 2.1 calls vs brute force 6.6 on the 59 problems both solve.

#### synthetic-tier4 (200 problems)

| solver | solved | rate | mean checker calls (solved) | median calls (solved) | mean time per problem |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 52/200 | 26.0% | 4.0 | 2 | 0.156s |
| network, search (128 calls) | 57/200 | 28.5% | 12.2 | 3 | 0.428s |
| untrained network, no backtracking (32 calls) | 27/200 | 13.5% | 4.3 | 3 | 0.233s |
| untrained network, search (128 calls) | 41/200 | 20.5% | 22.7 | 10 | 0.28s |
| uniform policy, no backtracking (32 calls) | 18/200 | 9.0% | 9.1 | 4 | 0.011s |
| uniform policy, search (128 calls) | 37/200 | 18.5% | 33.6 | 11 | 0.031s |
| brute force (128 calls) | 46/200 | 23.0% | 13.3 | 5 | 0.051s |
| brute force (2000 calls) | 52/200 | 26.0% | 37.3 | 5 | 0.815s |

Solved per sampling seed: network, no backtracking (32 calls): [52, 51, 49]; network, search (128 calls): [57, 57, 57]

Mean checker calls on commonly solved problems: network, no backtracking (32 calls): 3.0 calls vs brute force 13.8 on the 43 problems both solve; network, search (128 calls): 3.6 calls vs brute force 13.6 on the 44 problems both solve.
