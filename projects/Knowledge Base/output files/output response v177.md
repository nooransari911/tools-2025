# Question, briefly
MAX Array problem: Minimum operations to make maximum elements unique or adjacent.

# Question
Given an array `a` of `N` non-negative integers, determine the minimum number of operations required to modify the array such that it satisfies one of the following conditions:
1. There is exactly one maximum element in the array.
2. If there is more than one maximum element, all such maximum elements are adjacent to each other.

An operation consists of choosing an element of the array and decreasing its value by one.

# Answer
```python
import math

class Solution:
    def minOperations(self, a, N):
        if N == 0:
            return 0

        # Step 1: Find the maximum element (M) in the array.
        # Initialize M. Since a[i] >= 0, -1 is a safe starting point.
        # Or, if N >= 1, M = a[0] and iterate from a[1].
        M = -1 
        if N > 0:
            M = a[0] # Handles N=1 case correctly for loop starting at 1
            for i in range(1, N):
                if a[i] > M:
                    M = a[i]
        else: # N = 0, though problem constraint says N >= 1
            return 0
            
        # If M is still -1 (e.g. if array could be empty and N was misleading)
        # or if N=0 was passed (already handled), this means no elements or no positive max.
        # However, for N>=1 and a[i]>=0, M will be >=0.

        # Step 2: Count total occurrences (k) of M and 
        # find the length of the longest contiguous subsegment (L) of elements equal to M.
        k = 0
        max_L = 0
        current_L = 0
        
        for i in range(N):
            if a[i] == M:
                k += 1
                current_L += 1
            else:
                # If a run of M's just ended, update max_L
                if current_L > 0:
                    max_L = max(max_L, current_L)
                current_L = 0  # Reset current run length
        
        # After the loop, account for a run of M's at the very end of the array.
        max_L = max(max_L, current_L)
        L = max_L
        
        # Step 3: Calculate the minimum operations.
        # If k=0 (e.g. empty array, though N>=1) or k=1 (already one max), ops = 0.
        # The formula k-L covers these:
        # If k=0, L=0, then k-L = 0.
        # If k=1, M occurs once. This single M forms a run of length 1. So L=1. Then k-L = 1-1 = 0.
        # If all elements are M (e.g., {5,5,5}), then k=N, L=N. k-L = N-N = 0.
        
        return k - L

```

# Explanation

The problem asks for the minimum number of operations to either make the maximum element unique (Condition 1) or to make all maximum elements adjacent (Condition 2). An operation consists of decreasing an element's value by 1, costing 1 unit per decrease.

Let the original maximum value in the array `a` be `M_orig`.
Operations only allow decreasing values. This means any element `x < M_orig` can never become `M_orig`. Thus, the maximum value in the modified array will be at most `M_orig`.

Consider two scenarios for the final maximum value `M_final` in the modified array:

1.  `M_final = M_orig`:
    We aim to satisfy one of the conditions while keeping `M_orig` as the maximum value.
    Let `k` be the total number of elements equal to `M_orig` in the original array.
    Let `L` be the length of the longest contiguous subsegment of elements equal to `M_orig`. For example, in `{M, x, M, M, y, M}`, if `x,y < M`, then `k=4` and the runs of `M` are of length 1, 2, and 1. So, `L=2`.
    -   To satisfy Condition 1 (exactly one maximum): We need to keep one occurrence of `M_orig` and change the other `k-1` occurrences. The cheapest way to change an `M_orig` so it's no longer the maximum is to decrease it to `M_orig - 1`, costing 1 operation. So, this strategy costs `(k-1) * 1 = k-1` operations.
    -   To satisfy Condition 2 (all maximums `M_orig` are adjacent): We should aim to preserve an existing run of `M_orig`s. To minimize operations, we preserve the longest such run, which has length `L`. We need to change the other `k-L` occurrences of `M_orig` (those not part of this chosen longest run) to `M_orig-1`. This costs `(k-L) * 1 = k-L` operations.

    Comparing these two options, since `L >= 1` (if `k >= 1`, there's at least one `M_orig`, forming a run of length at least 1), `k-L` will always be less than or equal to `k-1`. Thus, the minimum cost if `M_final = M_orig` is `k-L`.
    If `L=1` (meaning all `M_orig`s are isolated, or there's only one `M_orig`), then `k-L = k-1`. This correctly means we keep one `M_orig`, and the result satisfies Condition 1.
    If `L > 1`, `k-L` operations result in `L` adjacent maximums, satisfying Condition 2.
    If `k=0` (empty array, not per constraints) or `k=1` (already one max), then `L` would be `k`. So `k-L = 0` operations, which is correct.

2.  `M_final < M_orig`:
    Suppose we decide the final maximum should be `M_new = M_orig - 1` (or any value less than `M_orig`).
    To achieve this, all `k` elements that were originally `M_orig` must be reduced to `M_new` or less. Reducing each of these `k` elements to `M_orig-1` (the minimum change to make them not `M_orig`) alone would cost `k * 1 = k` operations.
    This cost `k` is generally greater than `k-L` (since `L >= 1 \implies k-L \le k-1 < k`, for `k>0`).
    Even if reducing all `M_orig`s fortuitously creates a valid configuration of `M_new`s from elements that were already `M_new`, the initial cost of `k` operations to deal with the original `M_orig`s makes this strategy likely more expensive than the `k-L` cost. For example, in `{10, 9, 9, 9, 10}`, `M_orig=10, k=2, L=1`. `k-L=1` (e.g. modify to `{9,9,9,9,10}`). If we change both 10s to 9s, it costs 2 operations (result `{9,9,9,9,9}`), which is worse.

Therefore, the optimal strategy is to ensure `M_orig` remains the maximum value. The minimum operations needed is `k-L`.

The algorithm is:
1.  Find the maximum value `M` in the array `a`. If `N=0`, operations are 0.
2.  Count the total occurrences `k` of `M`.
3.  Find the length `L` of the longest contiguous subsegment of elements equal to `M`.
    - Iterate through the array, keeping track of the `current_L` (length of current run of `M`s).
    - If an element is not `M`, the run breaks; compare `current_L` with `max_L` found so far and reset `current_L`.
    - After the loop, ensure the last run is also considered for `max_L`.
4.  The result is `k - L`. This formula correctly handles cases where `k=0, k=1`, or all `M`s are already adjacent (`L=k`), resulting in 0 operations.

This approach has a time complexity of `O(N)` because finding `M`, `k`, and `L` each takes a pass through the array. Space complexity is `O(1)`. These are well within typical limits for `N` up to `10^6`.
