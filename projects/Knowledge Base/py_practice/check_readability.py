import matplotlib.pyplot as plt
import numpy as np
import re
from pathlib import Path

def strip_yaml_frontmatter(text):
    """Remove YAML frontmatter from beginning of text."""
    # Check if text starts with ---
    text = text.lstrip()
    if text.startswith('---'):
        # Find the closing ---
        parts = text.split('---', 2)
        if len(parts) >= 3:
            # Return text after second ---
            return parts[2]
    return text

def extract_sentences(text):
    """Extract sentences from text using basic sentence boundary detection.
    Treats markdown headings as sentences."""
    # Strip YAML frontmatter first
    text = strip_yaml_frontmatter(text)

    # Convert markdown headings to sentences by adding periods after them
    # This handles # Heading, ## Heading, etc.
    text = re.sub(r'^(#{1,6}\s+.+)$', r'\1.', text, flags=re.MULTILINE)

    # Split on sentence endings (., !, ?) followed by space or end of string
    sentences = re.split(r'[.!?]+\s+', text)
    # Filter out empty strings and strip whitespace
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def get_char_counts(filepath):
    """Read file and return character counts per sentence."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    sentences = extract_sentences(text)
    char_counts = [len(s) for s in sentences]
    return char_counts

def create_distribution_plot(char_counts, label, color, ax, bins):
    """Create a histogram for character count distribution."""
    counts, _ = np.histogram(char_counts, bins=bins)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    bin_width = bins[1] - bins[0]

    ax.bar(bin_centers, counts, width=bin_width*0.9, alpha=0.8, color=color,
           edgecolor='black', linewidth=0.8)
    ax.set_xlabel('Characters per Sentence', fontsize=11, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
    ax.set_title(f'{label} Text Distribution\n(n={len(char_counts)} sentences, '
                 f'mean={np.mean(char_counts):.1f}, median={np.median(char_counts):.1f})',
                 fontsize=12, fontweight='bold', pad=10)
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlim(bins[0], bins[-1])

def create_difference_plot(older_counts, newer_counts, ax, bins):
    """Create a difference visualization (newer - older)."""
    # Create histograms with the same bins
    older_hist, _ = np.histogram(older_counts, bins=bins)
    newer_hist, _ = np.histogram(newer_counts, bins=bins)

    difference = newer_hist - older_hist
    bin_centers = (bins[:-1] + bins[1:]) / 2
    bin_width = bins[1] - bins[0]

    # Create bar plot with color coding
    colors = ['#d62728' if d < 0 else '#2ca02c' for d in difference]
    ax.bar(bin_centers, difference, width=bin_width*0.9, color=colors,
           alpha=0.8, edgecolor='black', linewidth=0.8)

    ax.axhline(y=0, color='black', linestyle='-', linewidth=1.5)
    ax.set_xlabel('Characters per Sentence', fontsize=11, fontweight='bold')
    ax.set_ylabel('Frequency Difference\n(Newer - Older)', fontsize=11, fontweight='bold')
    ax.set_title('Distribution Change: Newer - Older\n(Green: More in newer, Red: Less in newer)',
                 fontsize=12, fontweight='bold', pad=10)
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlim(bins[0], bins[-1])

def main(older_filepath, newer_filepath, num_bins=25):
    """Main function to analyze and visualize sentence character distributions.

    Args:
        older_filepath: Path to older text file
        newer_filepath: Path to newer text file
        num_bins: Number of bins/buckets to use (default: 25)
    """

    # Extract character counts
    print(f"Reading older text from: {older_filepath}")
    older_counts = get_char_counts(older_filepath)

    print(f"Reading newer text from: {newer_filepath}")
    newer_counts = get_char_counts(newer_filepath)

    # Create consistent bins for bucketing
    all_counts = older_counts + newer_counts
    min_chars = 0
    max_chars = max(all_counts)

    # Create bins with specified number of bins
    bins = np.linspace(min_chars, max_chars, num_bins + 1)
    bucket_size = bins[1] - bins[0]

    print(f"\nUsing {num_bins} bins of size {bucket_size:.1f} characters")
    print(f"Range: {min_chars} to {max_chars} characters")

    # Create figure with grid layout: 2x2 with merged right column
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1], hspace=0.3, wspace=0.3,
                          left=0.08, right=0.96, top=0.93, bottom=0.08)

    ax_older = fig.add_subplot(gs[0, 0])
    ax_newer = fig.add_subplot(gs[1, 0])
    ax_diff = fig.add_subplot(gs[:, 1])  # Spans both rows

    fig.suptitle('Sentence Length Distribution Analysis',
                 fontsize=18, fontweight='bold', y=0.98)

    # Plot 1: Older text (top left)
    create_distribution_plot(older_counts, 'Older', '#1f77b4', ax_older, bins)

    # Plot 2: Newer text (bottom left)
    create_distribution_plot(newer_counts, 'Newer', '#ff7f0e', ax_newer, bins)

    # Plot 3: Difference (right side, full height)
    create_difference_plot(older_counts, newer_counts, ax_diff, bins)

    # Save the figure (no tight_layout here since we handled margins in gridspec)
    output_path = 'sentence_distribution_analysis.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.2)
    print(f"\nVisualization saved to: {output_path}")

    plt.show()

    # Print statistics
    print("\n" + "="*60)
    print("STATISTICS SUMMARY")
    print("="*60)
    print(f"\nOlder Text:")
    print(f"  Sentences: {len(older_counts)}")
    print(f"  Mean chars/sentence: {np.mean(older_counts):.2f}")
    print(f"  Median chars/sentence: {np.median(older_counts):.2f}")
    print(f"  Std dev: {np.std(older_counts):.2f}")

    print(f"\nNewer Text:")
    print(f"  Sentences: {len(newer_counts)}")
    print(f"  Mean chars/sentence: {np.mean(newer_counts):.2f}")
    print(f"  Median chars/sentence: {np.median(newer_counts):.2f}")
    print(f"  Std dev: {np.std(newer_counts):.2f}")

    print(f"\nChange (Newer - Older):")
    print(f"  Mean difference: {np.mean(newer_counts) - np.mean(older_counts):.2f} chars")
    print(f"  Median difference: {np.median(newer_counts) - np.median(older_counts):.2f} chars")
    print("="*60)

if __name__ == "__main__":
    # File paths
    older_file = "/home/ansarimn/Downloads/temp old.md"
    newer_file = "/home/ansarimn/Downloads/temp new.md"

    # Adjust num_bins as needed (default: 25)
    # Fewer bins = broader patterns, More bins = finer granularity
    main(older_file, newer_file, num_bins=25)
