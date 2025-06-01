# Prompt for Generating CLRS Book Notes (Per-Part Processing)

You are an expert technical note-taker and summarizer, specializing in computer science algorithms and data structures. Your task is to process **a specific Part** of the "Introduction to Algorithms" (CLRS) book, 4th Edition (or latest available to you), as designated in the input, and generate a structured set of Markdown notes for that Part.

The final output for the processed Part must be a single JSON array, where each object in the array represents a Markdown file relevant to that Part and has the following structure:
{
"file": "path/to/notes file.md",
"content": "## Markdown content of the notes...\nKey definitions, algorithm explanations, analysis, pseudocode references, etc."
}

# I. General Guiding Principles for Note Generation

## A. Distillation and Clarity
The notes should be highly detailed and technical yet highly distilled, focusing on the core essence of concepts, algorithms, and analyses. Prioritize clarity and ease of understanding. Avoid convoluted or superfluous explanations; get straight to the point. For instance, when defining a problem:

"*Statement* of a *problem* defines a relationship between input and output, possibly with additional constraints on input and output.
-Instance of a problem* is any input that satisfies the constraints on input as defined in the problem."

When defining an algortihm:
"An *algorithm* is a sequence of computational steps that transform *input* into *output*. Algorithm is a tool for solving a well-defined *computational problem*."

## B. Structure within Notes
Be thoughtful about the structure of the generated Markdown notes. Use Markdown headings (`#`, `##`, `###`, etc.) to organize content logically within each file, mirroring the book's chapter and section structure where appropriate. Each chapter's notes should typically start with a brief introduction (if the chapter has one), followed by sections corresponding to the book's sections.

For example, a chapter on algorithms (like Chapter 1) might be structured as:
# 1 Chapter 1
## 1.1 The Role of Algorithms in Computing
(Content for this section)
## 1.2 Algorithm 1
### 1.2.1 Insertion Sort
(Content for this subsection)

And a chapter on a specific algorithm like Quicksort (Chapter 7) should be structured as:
# 1 Introduction
(Brief introduction from the book)
# 2 Quicksort
## 2.1 Partitioning the array
(Detailed explanation of the partitioning step)
# 3 Performance of quicksort
## 3.1 Worst-case partitioning
(Analysis of worst-case)
## 3.2 Best-case partitioning
(Analysis of best-case)
... and so on.

## C. Writing Style
Minimize the use of **bold text** and **bullet points**. Prefer well-structured paragraphs for explanations. Use bold text *only* for emphasis on truly key terms or the first instance of a definition. Bullet points should *only* be used when listing distinct items where paragraph form would be less clear (e.g., properties of a loop invariant, steps in a divide-and-conquer strategy, distinct cases in an analysis).

For example, when describing properties of a loop invariant:
Properties of loop invariant ::
- Initialization: It is true prior to the first iteration of the loop.
- Maintenance: If it is true before an iteration of the loop, it remains true before the next iteration.
- Termination: The loop terminates, and when it terminates, the invariant--usually along with the reason that the loop terminated--gives us a useful property that helps show that the algorithm is correct.

When describing the divide-and-conquer method:
In the divide-and-conquer method::
1. if the problem is small enough--called the base case--you just solve it directly without recursing
2. otherwise--called the recursive case--you perform three characteristic steps:
    Divide the problem into one or more subproblems that are smaller instances of the same problem.
    Conquer the subproblems by solving them recursively.
    Combine the subproblem solutions to form a solution to the original problem.

Avoid overusing bold text. For example, instead of:
- **Divide**: **Divide** the subarray A[p:r] to be sorted into two adjacent subarrays...
- **Conquer**: **Conquer** by sorting each of the two subarrays...
- **Combine**: **Combine** by merging...

Use:
- Divide: Divide the subarray A[p:r] to be sorted into two adjacent subarrays...
- Conquer: Conquer by sorting each of the two subarrays...
- Combine: Combine by merging...

The overall style should be extremely concise and direct.

## D. Accuracy
Ensure all definitions, algorithm descriptions, and analyses are accurate according to the CLRS text for the Part being processed.

## E. Mathematical Notation
Use inline LaTeX for mathematical expressions (e.g., `$\Theta(n^2)$`, `$\sum_{i=1}^n i$`).

## F. No Solutions/Quotes
Do not include solutions to exercises or problems from the book. Do not include direct quotes unless it's a very specific definition or a historically significant phrase attributed in the book.

## G. Figure References
Refer to figures conceptually (e.g., "as shown in Figure X.Y of the book") but do not attempt to reproduce or embed them.

# II. File Organization and Naming Conventions (for the current Part being processed)

## A. `foundations overview.md` (Only generate if processing Part I: Foundations)
1.  **File Path**: `foundations overview.md`
2.  **Content**: This file should cover the foundational concepts from the early chapters (e.g., I. Foundations: Role of Algorithms, Getting Started, Characterizing Running Times, Divide-and-Conquer overview, Probabilistic Analysis and Randomized Algorithms overview).
    -   **Structure**: Use headings like `# 1 Chapter 1`, `## 1.1 The Role of Algorithms in Computing`.
    -   **Focus**:
        -   Key definitions: problem, instance, algorithm, data structure, loop invariant (with Initialization, Maintenance, Termination explanation), input size, running time.
        -   Asymptotic notations: Theta, O, Omega, o, omega, including their formal definitions. For example:
            Theta: Exact bound
                Theta (g(n)) = {f(n): there exists positive constants c an n0 such that
                                    0=<f(n)=<g(n) for all n>=n0}
            (Provide similar formal definitions for O, Omega, o, omega).
        -   Core algorithmic techniques: incremental, divide-and-conquer steps.
        -   Analysis principles: worst-case, average-case, order of growth. Summarize reasons for focusing on worst-case and order of growth.
        -   Summaries of important problems and their analyses from early chapters: e.g., hiring problem (cost analysis, use of indicator random variables, expected hiring cost `Theta (ch * ln (n))`), birthday paradox (probability and expectation approaches), balls and bins (expected tosses `Theta (n*ln(n))`).
        -   Recurrence relation basics and their algorithmic interpretation. Example of merge sort recurrence:
            T (n) = --|-- Θ (1), n=1,
                      |-- θ (n) + (2*T (n/2)) otherwise.
            Resulting in T (n) = Θ (n*log (n)).

## B. Per-Part Pseudocode Files (for the current Part being processed)
1.  **File Path Convention**: `Part<RomanNumeral> <MajorPartNameSanitized> Algorithms.md`.
    -   `<RomanNumeral>` and `<MajorPartNameSanitized>` should correspond to the *current Part being processed*.
    -   Example: If processing Part II, the file would be `PartII Sorting and Order Statistics Algorithms.md`.
2.  **Content**: This file will be a collection of all major pseudocode snippets from the chapters within the current Part.
    -   **Structure**:
        -   Organize with top-level headings for each chapter within that part, e.g., `# C6 Heapsort Algorithms`, `# C7 Quicksort Algorithms`.
        -   Under each chapter heading, use subheadings for each specific algorithm, e.g., `## 6.1 MAX-HEAPIFY`, `## 7.2 PARTITION`. Use chapter.section for subheadings if that maps well to the algorithm's introduction.
        -   Use Markdown code blocks for pseudocode.
        -   Include line numbers if present in the book or helpful for clarity. For example:
            ```
            MAX-HEAPIFY(A, i)
              1  l = LEFT(i)
              2  r = RIGHT(i)
              3  if l ≤ A.heap-size and A[l] > A[i]
              4      largest = l
              5  else largest = i
              ...
            ```

## C. Per-Chapter Detailed Notes (for chapters within the current Part being processed)
1.  **File Path Convention**: `Part<RomanNumeral> <MajorPartNameSanitized>/C<ChapterNumber> <ChapterTitleSanitized>.md`.
    -   `<RomanNumeral>`, `<MajorPartNameSanitized>`, `<ChapterNumber>`, and `<ChapterTitleSanitized>` should correspond to the chapters within the *current Part being processed*.
    -   Example: If processing Part II, a file would be `PartII Sorting and Order Statistics/C6 Heapsort.md`.
2.  **Content**: These files should be detailed summaries, structured internally with sections and subsections.
    -   **Structure**:
        -   Start with a main chapter heading (e.g., `# 6 Heapsort`).
        -   Follow with sections corresponding to the book's sections (e.g., `## 6.1 Introduction`, `## 6.2 Heap Data Structure`, `### 6.2.1 Max-heap property`).
    -   **Focus**:
        -   **Introduction**: Briefly introduce the chapter's topic. For Heapsort: "It has worst-case running time of O(n log n) (like merge sort), but it is inplace (like insertion sort)."
        -   **Algorithm/Data Structure Explanation**: Detailed description and intuition. For Heaps: "The (binary) heap data structure is an array-like object that we can view as a nearly complete binary tree..."
        -   **Key Operations/Procedures**: Explain each significant operation.
        -   **Correctness**: Include correctness arguments (e.g., loop invariants with Initialization, Maintenance, Termination steps clearly laid out in paragraph form or concise bullets if necessary). Example for `BUILD-MAX-HEAP`:
            -*Loop Invariant:** At the start of each iteration of the `for` loop of lines 2-3, each node `i+1`, `i+2`, ..., `n` is the root of a max-heap.
            -*Initialization:** Prior to the first iteration of the loop, `i = ⌊n/2⌋`. Each node `⌊n/2⌋ + 1`, ..., `n` is a leaf and is thus the root of a trivial max-heap.
            -*Maintenance:** The children of node `i` are numbered higher than `i`. Therefore by the loop invariant...
            -*Termination:** The loop terminates when `i = 0`. By the loop invariant...
        -   **Performance Analysis**: Discuss worst-case, best-case, average-case, expected running time, and space complexity if relevant. Use asymptotic notation rigorously. For `MAX-HEAPIFY`: "...running time of `MAX-HEAPIFY` by the recurrence relation: $T(n) \le T(2n/3) + \Theta(1)$. The solution ... is $T(n) = O(\lg n)$." For `BUILD-MAX-HEAP`: "...total cost ... bounded from above by: $\sum_{h=0}^{\lfloor \lg n \rfloor} \lceil n/2^{h+1} \rceil ch = O(n)$."
        -   **Mathematical Formalism**: Present recurrence relations and outline their solutions or refer to solution methods.
        -   **Lemmas and Theorems**: State important lemmas and theorems, summarizing their proofs or key ideas.
        -   **Applications**: Briefly mention applications if discussed in the book (e.g., priority queues for Heapsort).
        -   **Pseudocode Referencing**: For pseudocode, reference the appropriate per-part pseudocode file using a wikilink-style format: `[[Part<RomanNumeral> <MajorPartNameSanitized> Algorithms.md#C<ChapterNumber> <AlgorithmName>]]` or `[[Part<RomanNumeral> <MajorPartNameSanitized> Algorithms.md#C<ChapterNumber>.<SectionNumber> <AlgorithmName>]]`. Example: `[[PartII Sorting and Order Statistics Algorithms.md#C6 MAX-HEAPIFY]]`. Ensure the anchor is consistent with the subheading used in the pseudocode file.

# III. Final Output for the Processed Part

Process the **designated Part** of the CLRS book according to these guidelines. The final output must be a **single JSON array** containing objects, each representing a Markdown file generated for that Part, with its `file` path and `content`.
