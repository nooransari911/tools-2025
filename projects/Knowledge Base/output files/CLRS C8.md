# Chapter 8: Sorting in Linear Time  

Sorting algorithms like merge sort and heap sort impose limits on runtime, bounded below by $\Omega(n \log n)$ complexity for comparison-based sorting. The reasoning—and limitation—stems from the decision-tree model: any deterministic sorting algorithm using comparisons as its only operation on data must make at least enough decisions to differentiate all $ n! $ input permutations, requiring **at least $\log_2(n!) \approx n \log n$ decisions per input permutation**. This lower bound makes traditional sorting models inefficient for non-comparison-based data that may possess structural assumptions enabling faster processing.

This analysis sets the stage for algorithms introduced in this chapter, which relax the assumption that **all sorting algorithms must be comparison-based**. It details three algorithms—**counting sort**, **radix sort**, and **bucket sort**—that produce a **linear-time sorting**, bypassing $\Omega(n \log n)$ lower bounds using problem-specific constraints: counting sort exploits bounded integer keys; radix sort breaks keys into subvalues and uses stability; bucket sort assumes uniform distributions over input probabilities. This makes Chapter 8 a pivotal bridge from standard sorting to more **model-aware**, performance-optimized techniques.

---

## **8.1 Lower Bounds for Comparison Sorts**

### **The Decision-Tree Model**

In the decision-tree model of comparison sorting, an algorithm is represented as a **binary tree where internal nodes represent comparisons between pairs of elements** in the input array, and each **leaf node represents a final, unique permutation of the array**. The **depth** of this binary tree—i.e., its longest path from root to a leaf—represents the **maximum number of comparisons required** for sorting in that algorithm.

The minimum number of comparisons made on any array of size $ n $ can be rigorously defined as the **height $ h $** of the decision tree: every permutation must correspond to **at least one leaf node**, and the total number of leaves must be $ \geq n! $ for the full spread of permutations. For a binary decision tree, a height $ h $ implies a maximum number of leaves of $ l \leq 2^h $, thus:
$$
n! \leq 2^h \Rightarrow h \geq \log_2(n!) = \Omega(n \log n).
$$
This proves that **any comparison-based sorting algorithm takes at least $\Omega(n \log n)$ time** in the **worst-case** scenario.

### **Implications for Sorting Complexity**
These theoretical limits suggest that comparison-based sorting methods, which involve pairwise comparisons between elements (e.g., merge sort, quicksort, or heap sort), regardless of their implementation logic, cannot escape a **hard complexity floor of $ \Omega(n \log n) $**. The decision-tree model proves this applies universally under the assumption that no knowledge beyond pairwise comparisons exists and that the structure of the array before sorting is arbitrary.

This limitation makes **alternative sorting algorithms necessary when sorting guarantees exceed expected-case assumptions and model dependencies**. If a specific attribute of the input data—such as bounded key values, specific digit hierarchy, or uniformity—can be identified, sorting strategies like **non-comparison sorting algorithms** become applicable. This sets the groundwork for Chapter 8’s shift away from comparison-based paradigms, into algorithms which break the known barriers through specialized use cases.

This section also draws directly from **Chapter 3** and **Chapter 5**, specifically reinforcing asymptotic behavior through **big-O and $\Omega$ notations** and probabilistic reasoning applied to algorithmic analysis. It also **builds upon Chapter 6**, verifying that algorithms like **heapsort remain bounded within known lower complexity thresholds** while acknowledging scenarios where they **must lose optimization to comparison-based assumptions.** This theoretical barrier is directly confronted in the next section.

---

## **8.2 Counting Sort: Sorting Through Frequency Counts**

### **Assumptions and Performance Conditions**
Counting sort diverges from decision-tree assumptions through a **key constraint**: it applies to **input arrays** of $ n $ elements drawn **from a known finite range of integers**, usually from $ 0 $ to $ k $, where $ k $ is small relative to $ n $. If $ k = O(n) $, the algorithm guarantees a linear runtime $ \Theta(n) $. Its fundamental idea is to **count frequencies** and use those to map elements to specific indices in an **output array**.

Notably, **stability** is a hallmark of counting sort. Equal values are placed in arrays while **retaining relative order**, especially important when **used as an internal subroutine in more advanced stable algorithms such as Radix Sort.**

### **Algorithm Logic and Implementation**

Counting sort operates by:
1. **Initializing a count array $ C $** of size $ k+1 $, initialized with zero values to prepare for frequency tracking.
    ```python
    def COUNTING_SORT(A, B, C, k):
        for i in range(0, k+1):
            C[i] = 0
    ```
2. **Increment frequency counts** to correlate with keys found in the array:
    ```python
        for j in range(1, len(A)+1):
            C[A[j]] += 1
    ```
3. **Compute cumulative frequency** to reflect values less than or equal to a certain index in $ C $, producing the position of the last element of a specific integer in $ A $, **which is essential for stable sorting**:
    ```python
        for i in range(1, k+1):
            C[i] += C[i - 1]
    ```
4. **Populate the output array $ B $** by placing each element $ A[j] $ into its correct position in $ B $, decrementing its count each time to **maintain positional order between duplicates**.
    ```python
        for j in range(len(A), 0, -1):
            B[C[A[j]]] = A[j]
            C[A[j]] -= 1
    ```
This mechanism results in $ \Theta(n + k) $ time complexity:
- Two $ O(n) $ loops initially populate $ C $ and output $ B $.
- One $ O(k) $ loop calculates the prefix sum to ensure proper placement.
- A **final $ O(n) $ pass** is made to sort the arrays correctly.

### **Practical Advantages and Applicability**
Although counting sort guarantees **linear complexity under bounded integer input models**, it is inherently tied to the **limitations of constant $ k $**, prohibiting its use in more complex numeric domains. Despite these, the ability to **simultaneously sort and count element frequencies efficiently**, and maintain **stability under dynamic updates**, makes it a **vital tool for numerical algorithms where $ k $ matches the problem space—especially in combinatorial counting and dynamic programming.**

---

## **8.3 Radix Sort: Sorting by Digits**

### **The Advantage of Multi-Digit Stability**

Radix sort is another linear-time sorting algorithm with guaranteed linearity under a different operational assumption: keys are **sorted based on individual digit values**. By leveraging a stable sort, such as counting sort, radix sort sorts $ n $ $ d $-digit numbers through a series of $ d $ **digit-by-digit sorts**. Each sort, stable and incremental, preserves order previously learned by prior digit positions, guaranteeing final sort correctness.

### **Algorithm Logic and Properties**
Two implementation details underpin the Radix Sort pseudo:
1. **In successive passes**, iterate through **each digit from least significant to most significant.**
2. **Maintain stability** in order preservation using **Counting Sort**, guaranteeing relative order remains uncorrupted through digit passes.

```python
def RADIX_SORT(A, d):
    for i in range(1, d + 1):
        use a stable sort (COUNTING_SORT) to sort A on digit i
```

Performance hinges heavily on the stability of the sorting subroutine and the digit-by-digit implementation. **For d-digit numbers sorted with stable selection, the complexity is $\Theta(d(n + k))$, where $ k $ is the range of digits (often assumed $ k = O(n) $)**. When $ d $ is a constant and $ k $ is small, $ d(n + k) $ simplifies to $ O(n) $, marking notable speedups over comparison-based methods.

**Practical applications reinforce mathematical bounds**, as radix sort excels in sorting large sets of uniformly distributed integers efficiently in parallel and hybrid computing architectures. It works across scenarios like:
- Sorting of strings using character-by-character operations over fixed-length words.
- High-precision arithmetic, **especially in cryptographic logic requiring low-computation, high-order digit manipulations** for large floating-point values.

---

## **8.4 Bucket Sort: Probabilistic Distribution Sorting**

### **Uniform Distributions and Bucketing**

Bucket sort exploits a distinct advantage: that the input distribution **follows a uniform and bounded probability** over a range, particularly $[0,1)$ in most formal models.

It works by:
1. Creating $ n $ **almost-equal-sized buckets** to fragment a uniform distribution across an arbitrary input.
2. **Distributing $ n $ elements** across these buckets using these partitions—every element $ x $ in $ A[i] $ is placed in bucket $ \lfloor n \times A[i] \rfloor $, **ensuring average-case distribution to $ O(1) $ elements per bucket**.
3. **Sorting each bucket internally** using insertion sort (linear in $ n $ per bucket due to the small expected constituent size when uniformly distributed).
4. **Concatenating and returning all buckets** to reconstruct a sorted array.

This gives an efficient, expected **linear complexity $\Theta(n)$** for inputs uniformly distributed in $[0, 1)$, as shown in the pseudocode:
```python
def BUCKET_SORT(A):
    n = len(A)
    B = [[] for _ in range(n)]
    for i in range(n):
        B[floor(n * A[i])].append(A[i])
    for i in range(n):
        insertion_sort(B[i])
    output = []
    for i in range(n):
        output.extend(B[i])
    return output
```
Each bucket insertion involves $ O(1) $ time, and since buckets take constant time, **each bucket sort contributes $ \Theta(1) $—totaling linear.** Although individual bucket sorting at most takes $ O(n^2) $ time **in the event that a substantial number of elements fall into the same bin (making worst-case runtime $\Theta(n^2)$)**, such outlier scenarios are atypical for uniform input models.

### **Variance and Efficiency Under Uniform Conditions**

The expectation of **linearity and performance guarantees** hinges on **the assumption that the input follows a uniform distribution**. Under more generalized distributions—discrete or continuous—the decision to apply bucket sort for large-scale datasets may entail preprocessing input data **to approximate uniform distribution characteristics using hashing or transformations.** When dealing with large dynamic datasets where expected input conditions are unknown, bucket sort may be an unreliable method unless measures are in place to estimate and stabilize such probabilistic behavior effectively.

Where bucket sort excels is its use of probability theory in sorting. It exploits prior knowledge about **input distributions** to bypass the limitations of guaranteed $ \Omega(n \log n) $ sorting paradigms, **leveraging probabilistic guarantees rather than deterministic ones**. This shifts the focus from traditional worst-case guarantees toward a **better understanding of probabilistic bounds on sorting correctness**—a theme explored in **Chapter 5’s probabilistic analysis**.

It bridges **decision theory and sorting efficiency**, particularly **mapping directly to hashing**. Bucket sort resembles a hash-based partitioning mechanism, **distributing keys randomly into buckets (like hash chains) across a known domain**, then relying on known patterns in sorting hash buckets, extending further into **Part III's structures like hash tables**. This links directly to **Chapter 7 on quicksort** and **Chapter 5 on randomized algorithms**, using **uniform data assumptions** to guarantee **expected $ O(n) $ runtimes**.

---

## **Conclusion to Chapter 8: Linear Time Sorting**

This chapter charts a path from limiting assumptions of traditional comparison-based sorts to a trio of non-comparison, linear-time sorting algorithms. It establishes that **sorting faster than $ \Theta(n \log n) $**, at least expected or amortized across algorithm-specific domains and data models, is possible when strong structural or probabilistic attributes are exploited:
- **Counting sort relies on bounded integers within a tightly defined range**.
- **Radix sort assumes a digit-based decomposition of key values** and stability for preserved ordering.
- **Bucket sort assumes input uniformity across a known interval**, ensuring even bucket distribution and quick intra-bucket sorting.

These algorithms **allow sorting to transcend theoretical constraints within known domains**, revealing the wide trade-off between generality of use and performance efficiency. Understanding where these assumptions apply is crucial for **applying these high-efficiency methods intelligently in real-world problems where tight complexity bounds matter**.

This concludes Chapter 8, leaving a strong foundation in linear sorting techniques for advancing into **Chapter 9 on Order Statistics**, where average-case lower complexity is extended in selection-based operations like selecting the **median or $ i $-th smallest element**.
