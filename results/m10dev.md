#### seed (51 problems)

| solver | solved | rate | mean checker calls (solved) | median calls (solved) | mean time per problem |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 46/51 | 90.2% | 0.2 | 0 | 0.066s |
| network, search (128 calls) | 48/51 | 94.1% | 4.1 | 0 | 0.098s |
| network, search (2000 calls) | 49/51 | 96.1% | 25.1 | 0 | 1.066s |
| untrained network, no backtracking (32 calls) | 45/51 | 88.2% | 0.7 | 0 | 0.106s |
| untrained network, search (128 calls) | 45/51 | 88.2% | 1.2 | 0 | 0.256s |
| untrained network, search (2000 calls) | 48/51 | 94.1% | 42.6 | 0 | 2.526s |
| uniform policy, no backtracking (32 calls) | 45/51 | 88.2% | 0.2 | 0 | 0.016s |
| uniform policy, search (128 calls) | 46/51 | 90.2% | 1.3 | 0 | 0.212s |
| brute force (128 calls) | 47/51 | 92.2% | 6.4 | 0 | 0.051s |
| brute force (2000 calls) | 50/51 | 98.0% | 64.5 | 0 | 0.166s |

Solved per sampling seed: network, no backtracking (32 calls): [46, 49, 47]; network, search (128 calls): [48, 48, 49]; network, search (2000 calls): [49, 50, 50]

Mean checker calls on commonly solved problems: network, no backtracking (32 calls): 0.1 calls vs brute force 2.1 on the 44 problems both solve; network, search (128 calls): 4.1 calls vs brute force 4.6 on the 46 problems both solve; network, search (2000 calls): 25.1 calls vs brute force 42.8 on the 49 problems both solve.

| solver | 0M | 5M | 10M | 15M | 20M |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 22/22 | 15/15 | 8/12 | 1/1 | 0/1 |
| network, search (128 calls) | 22/22 | 15/15 | 10/12 | 1/1 | 0/1 |
| network, search (2000 calls) | 22/22 | 15/15 | 11/12 | 1/1 | 0/1 |
| untrained network, no backtracking (32 calls) | 22/22 | 15/15 | 7/12 | 1/1 | 0/1 |
| untrained network, search (128 calls) | 22/22 | 15/15 | 7/12 | 1/1 | 0/1 |
| untrained network, search (2000 calls) | 22/22 | 15/15 | 10/12 | 1/1 | 0/1 |
| uniform policy, no backtracking (32 calls) | 22/22 | 15/15 | 7/12 | 1/1 | 0/1 |
| uniform policy, search (128 calls) | 22/22 | 15/15 | 8/12 | 1/1 | 0/1 |
| brute force (128 calls) | 22/22 | 15/15 | 9/12 | 1/1 | 0/1 |
| brute force (2000 calls) | 22/22 | 15/15 | 12/12 | 1/1 | 0/1 |

#### dev (32 problems)

| solver | solved | rate | mean checker calls (solved) | median calls (solved) | mean time per problem |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 20/32 | 62.5% | 1.1 | 0 | 0.88s |
| network, search (128 calls) | 21/32 | 65.6% | 9.7 | 0 | 2.57s |
| network, search (2000 calls) | 24/32 | 75.0% | 30.4 | 0 | 14.684s |
| untrained network, no backtracking (32 calls) | 20/32 | 62.5% | 1.6 | 0 | 0.444s |
| untrained network, search (128 calls) | 23/32 | 71.9% | 6.2 | 0 | 1.714s |
| untrained network, search (2000 calls) | 23/32 | 71.9% | 97.0 | 0 | 23.673s |
| uniform policy, no backtracking (32 calls) | 22/32 | 68.8% | 1.3 | 0 | 0.071s |
| uniform policy, search (128 calls) | 23/32 | 71.9% | 6.6 | 0 | 0.499s |
| brute force (128 calls) | 18/32 | 56.2% | 0.1 | 0 | 0.303s |
| brute force (2000 calls) | 23/32 | 71.9% | 51.2 | 0 | 1.642s |

Solved per sampling seed: network, no backtracking (32 calls): [20, 19, 21]; network, search (128 calls): [21, 23, 21]; network, search (2000 calls): [24, 24, 25]

Mean checker calls on commonly solved problems: network, no backtracking (32 calls): 0.3 calls vs brute force 0.1 on the 18 problems both solve; network, search (128 calls): 1.2 calls vs brute force 0.1 on the 18 problems both solve; network, search (2000 calls): 27.9 calls vs brute force 51.2 on the 23 problems both solve.

| solver | 0M | 5M | 10M | 15M | 20M | 25M | 35M | 40M |
|---|---|---|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 3/3 | 5/7 | 3/6 | 7/9 | 1/3 | 1/1 | 0/2 | 0/1 |
| network, search (128 calls) | 3/3 | 6/7 | 3/6 | 7/9 | 1/3 | 0/1 | 1/2 | 0/1 |
| network, search (2000 calls) | 3/3 | 6/7 | 4/6 | 8/9 | 1/3 | 1/1 | 1/2 | 0/1 |
| untrained network, no backtracking (32 calls) | 3/3 | 6/7 | 2/6 | 7/9 | 1/3 | 1/1 | 0/2 | 0/1 |
| untrained network, search (128 calls) | 3/3 | 6/7 | 4/6 | 7/9 | 1/3 | 1/1 | 1/2 | 0/1 |
| untrained network, search (2000 calls) | 3/3 | 6/7 | 4/6 | 7/9 | 1/3 | 1/1 | 1/2 | 0/1 |
| uniform policy, no backtracking (32 calls) | 3/3 | 6/7 | 4/6 | 7/9 | 1/3 | 1/1 | 0/2 | 0/1 |
| uniform policy, search (128 calls) | 3/3 | 6/7 | 4/6 | 8/9 | 1/3 | 1/1 | 0/2 | 0/1 |
| brute force (128 calls) | 3/3 | 5/7 | 2/6 | 7/9 | 1/3 | 0/1 | 0/2 | 0/1 |
| brute force (2000 calls) | 3/3 | 6/7 | 4/6 | 8/9 | 1/3 | 1/1 | 0/2 | 0/1 |
