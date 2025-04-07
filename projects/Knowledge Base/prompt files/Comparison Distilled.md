# Prompt: Processing Comparative Text into Structured Thematic Tables

Your primary goal is to process the provided source text, which compares multiple items, and present the information **ONLY** in structured **thematic** table formats. Accuracy in categorization based on the explicit meaning of the text and consistent presentation are paramount.

*(Guidance: If the source text compares many items, focus on the most common or representative ones, potentially grouping very similar items with explicit notation if it aids clarity.)*

# 1. Generate Thematic Sub-Tables with Accurate and Comprehensive Grouping

Analyze the source text to identify comparison criteria and organize them directly into logically themed tables.

## 1.1 Identify All Comparison Criteria and Representative Items
-   Analyze the source text thoroughly to identify **all** key parameters, features, or criteria used for comparison. Maintain a comprehensive internal list of these identified criteria for later verification.
-   Identify the distinct items being compared. If numerous, select the most representative items for comparison, potentially grouping similar ones if appropriate and noted.
-   Capture both explicitly stated comparison points and details strongly implied by the descriptions.

## 1.2 Define Thematic Structure & Content Based Primarily on Explicit Meaning
-   **Meaning-First Grouping:** Review the comprehensive list of identified criteria. Group these criteria into logical, distinct themes. **Crucially, the primary basis for grouping must be the direct meaning and functional relevance of the explicitly stated criteria.** Ask: "What aspect of the item does this criterion fundamentally describe according to the text?"
-   **Conceptual Coherence:** Aim for themes that represent significant conceptual categories discussed in the text. If a primary theme covers a broad conceptual area with distinct sub-aspects clearly delineated in the text, create relevant sub-themes under it (using H2 Markdown headings for sub-themes if needed).
-   **Ensure Correct Placement:** Assign each criterion to the single theme (or sub-theme) that best reflects its fundamental purpose based on its explicit description in the source material. Resolve potential overlaps by choosing the theme that most accurately represents the criterion's core implication in context.

## 1.3 Define Table Layout & Standards
-   **Structure:** For each identified theme (and sub-theme, if used):
    -   Create a separate table.
    -   Use a clear **Title** reflecting the theme/sub-theme (Use **H1** Markdown heading for primary themes, **H2** for sub-themes).
    -   *(Optional but Recommended):* Write a brief **Overview** paragraph summarizing the conceptual focus of that section's parameters.
    -   Construct tables with an initial column listing only the relevant comparison criteria assigned to that specific theme/sub-theme.
    -   Include subsequent columns for each selected/grouped item being compared.
-   **Column Sorting:** Consistently order the item columns from highest performance (leftmost) to lowest performance (rightmost) across all tables, based on an overall assessment derived from the source data. If overall performance is highly variable or difficult to rank definitively, group columns by logical item types (e.g., premium vs. standard, category A vs. category B) and state the grouping logic. Maintain this order consistently.
-   **Standardized Terminology:** Use a consistent lexicon for qualitative assessments across all tables where applicable, especially when comparing performance levels directly. Define or use a standard scale if appropriate, for example:
    *   **Exceptional:** Top-tier performance.
    *   **Excellent:** Very high performance.
    *   **Very Good:** High performance, reliably above average.
    *   **Good:** Meets standard requirements effectively.
    *   **Fair:** Adequate, potential limitations.
    *   **Poor:** Significant limitations.
    *   **N/A:** Not Applicable or Not Specified/Relevant.
    *   *(Retain specific numerical data (e.g., temperature ranges, measurements) and unique descriptive terms (e.g., 'Cost-effective', 'Lightweight') where standardization is not suitable or loses meaning).*

## 1.4 Accurately Populate Table Data
-   Fill the table cells accurately for each item against each assigned criterion within its theme/sub-theme.
-   **Ensure fidelity to the original text:** The data placed in each cell must directly correspond to the specific information provided for that item and criterion in the source text.

# 2. Verify Completeness and Accuracy
-   **Cross-Reference Criteria:** Before finalizing, explicitly verify that **all** comparison criteria identified in step 1.1 have been placed into one (and only one) appropriate thematic table. Ensure no criteria are missed or duplicated across themes.
-   **Verify Data Accuracy:** Quickly check the populated data within the thematic tables against the source text information to confirm accurate placement and transcription.

# 3. Final Review
-   Briefly review the generated thematic tables for:
    -   Accuracy: Data matches source text (as confirmed in step 2).
    -   Completeness: All criteria included (as confirmed in step 2).
    -   Logical Grouping: Themes (and sub-themes) are distinct, logical, and based primarily on the explicit meaning of the criteria.
    -   Consistency: Standardized terminology and column order applied uniformly.
