# Chapter 12: Binary Search Trees  

This chapter bridges the gap between elementary data structures and balanced trees by presenting the **binary search tree (BST)**, a dynamically modifiable structure supporting basic operations—insertion, deletion, and search—in $O(n)$ worst-case time but $O(\log n)$ on average. BSTs allow for keys to be arranged such that for any node $x$, all keys in the left subtree ≤ $x.key$ and all keys in the right subtree ≥ $x.key$, enabling sorting via traversal and efficient range queries. This chapter explores the mechanisms by which this structure supports **dynamic set operations** and sets the stage for more sophisticated variations—for example, red-black trees in Chapter 13.

---

## Binary Search Tree Properties and In-Order Traversal

Each node in a binary search tree contains a key, a reference to the left and right subtrees, and—if part of a deletion algorithm—its parent. These trees allow **comparison-based operations**, where keys dictate both placement and retrieval. A binary search tree preserves the **symmetric order** property: an **in-order traversal** results in a monotonically non-decreasing sequence of keys. The recursive `INORDER-TREE-WALK` pseudocode for non-empty trees begins in the leftmost subtree and ends in the rightmost subtree:

```plaintext
INORDER-TREE-WALK(x)
    if x ≠ NIL
        INORDER-TREE-WALK(x.left)
        print x.key
        INORDER-TREE-WALK(x.right)
```

Each subtree’s local in-order traversal ensures that the accumulated sequence of keys forms a sorted output of size $n$ in $O(n)$ time. This traversal is the bedrock upon which augmented operations rest, including augmented trees used in range queries and augmented priority queues, aligning with the broader theme of efficiency through ordered decomposition.

---

## Tree Search: Navigating Within the Structure

Two principal algorithms for iterating within the structure are provided—`TREE-SEARCH` for recursive descent through a binary search tree and `ITERATIVE-TREE-SEARCH`, which performs the same task iteratively. Both operate on a key and node with expected $O(h)$ worst-case time complexity, where h is the height of the tree—a critical determinant in per-operation cost. The recurrence is straightforward; when the key at node $x$ does not match the target, the structure necessitates descending into one of two branches:

```plaintext
TREE-SEARCH(x, k)
    if x == NIL or k == x.key
        return x
    if k < x.key
        return TREE-SEARCH(x.left, k)
    else
        return TREE-SEARCH(x.right, k)
```

The recursive solution serves as the conceptual basis for traversing binary search trees and will be foundational in analyzing the expected complexity of the more intrusive operations like insertions and deletions that augment the tree’s state.

```plaintext
ITERATIVE-TREE-SEARCH(x, k)
    while x ≠ NIL and k ≠ x.key
        if k < x.key
            x = x.left
        else x = x.right
    return x
```

Both recursion and iteration demonstrate the essence of the comparison model applied to dynamic sets, with nontrivial implications for worst-case performance, particularly in imbalanced configurations. The iterative version is commonly favored in environments where recursion depth is constrained—such as in hardware with shallow call stacks or in embedded system implementations.

---

## Insertion into Binary Search Trees: Adding Nodes With Precision

New nodes are inscribed within the BST's structure through `TREE-INSERT`, which ensures the comparability property dictates placement. Atypical of balanced tree implementations, `TREE-INSERT` traverses from the root downward, tracking the current subtree's parent $y$ as it descends to position $x$ in the appropriate spot. The algorithm is outlined as follows:

```plaintext
TREE-INSERT(T, z)
    y = NIL
    x = T.root
    while x ≠ NIL
        y = x
        if z.key < x.key
            x = x.left
        else x = x.right
    z.p = y
    if y == NIL
        T.root = z
    else
        if z.key < y.key
            y.left = z
        else y.right = z
```

This algorithm introduces two variables: $x$ represents the current node traversed, and $y$ acts as its predecessor to aid in reference establishment. Starting with the root, the algorithm descends while comparing keys—moving left or right depending on whether the new key is smaller or larger. Once the traversal terminates, reconfiguration of the tree’s properties ensures the node $z$ is placed properly, maintaining in-order comparability. Insertion time is bounded by traversal depth; however, without balancing mechanisms, worst-case performance on sorted input degrades to $O(n)$ as the tree becomes a linked list.  

---

## Deletion in Binary Search Trees: Structural Integrity Amid Change

Preserving the BST invariant during deletions requires a **multifaceted approach**, encapsulated in `TREE-DELETE`, which is conditional upon the number and structure of a node’s children. The algorithm relies on replacement strategies that guarantee **subtree structure**—specifically, how to handle cases where deletion causes structural changes:

```plaintext
TRANSPLANT(T, u, v)
    if u.p == NIL
        T.root = v
    else if u == u.p.left
        u.p.left = v
    else u.p.right = v
    if v ≠ NIL
        v.p = u.p
```

This `TRANSPLANT` function is used by `TREE-DELETE` to simplify pointer updates when replacing nodes. While preserving order properties, `TREE-DELETE` manages three deletion scenarios within the tree:

1.  **Node has no left child**: Can transplant the entire right subtree.
2.  **Node has a left child, but no right child**: The left subtree of the node being deleted takes its place; reformation of parent links follows.
3.  **Node has two children**: The node must find a surrogate—an in-order successor—to replace it, and this surrogate is subject to its own deletion, typically with fewer children. `TREE-MINIMUM` locates the successor. 

```plaintext
TREE-DELETE(T, z)
    if z.left == NIL
        TRANSPLANT(T, z, z.right)
    else if z.right == NIL
        TRANSPLANT(T, z, z.left)
    else
        y = TREE-MINIMUM(z.right)
        if y.p != z
            TRANSPLANT(T, y, y.right)
            y.right = z.right
            y.right.p = y
        TRANSPLANT(T, z, y)
        y.left = z.left
        y.left.p = y
```

The process demonstrates the nuanced interplay between tree reorganization and algorithm design, where each case must respect parent and sibling references while ensuring the original binary search property is upheld. Because this can involve up to three traversals (for locating the minimum and restructuring), complexity increases with the tree's depth $h$, which remains a hidden variable in BST performance profiles absent augmenting structural constraints.

---

### Time Complexity and Binary Tree Analysis Throughout Chapter 12

Under the best-case scenario of a perfectly balanced tree, operations in Chapter 12 illustrate $O(\log n)$ complexity. However, in the worst-case of a completely **unbalanced** tree, which, for example, occurs when elements are inserted in **ascending order**, leading to a tree resembling a singly-linked list, complexity degrades to **O(n)**. The average-case performance aligns with the balanced expectations, provided keys are randomly inserted. Insertion and deletion use multiple iterations—traversals—through the tree before modifying links or rebalancing. These iterations ensure correctness but highlight the necessity of self-balancing constructs like **red-black trees (Chapter 13)** and **AVL trees**, which maintain optimal height and performance regardless of insertion order.

Binary search tree searches perform comparably to many array-based and linked list operations; however, without balancing, operations do not maintain consistent efficiency. The algorithms detailed here lack mechanisms to guarantee persistent balance but focus correctly on mechanisms that maintain the binary search property while enforcing structured node movement within a dynamically changing set.

The algorithms address multiple variations, from tree walks (in-order, pre-order, and post-order), tree searches that match either of a given recursive or iterative nature, insert, and delete, each requiring **seamless transition** between parent and child links. Each of these operations is bound by tree height—a metric that fluctuates with data order and structure. As Chapter 13 delves into modifications that guarantee balanced performance, the focus here remains on operations that expose vulnerabilities of naively constructed binary trees—particularly in time complexity sensitivity to node disposition.

Ultimately, this chapter systematically **defines the BST as a prototypical hierarchical structure** and serves as the groundwork for complex extensions in an ever-evolving algorithm landscape, particularly those that address and correct for skew present in unchecked binary tree operations.
