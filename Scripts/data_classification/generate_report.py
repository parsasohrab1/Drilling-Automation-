from rules import rules

def generate_report(total_rows, violation_counts, total_non_operational, output_path="classification_report.md"):
    """
    Generates a markdown report summarizing the classification of operational and non-operational data.
    The report includes:
    - Total number of rows processed.
    - Total number and percentage of non-operational rows.
    - Detailed statistics for each rule applied, including description,
      count of rows violating the rule, and the violation percentage.

    Parameters
    total_rows : int
        The total number of data rows processed across all datasets.
    violation_counts : dict
        A dictionary mapping rule keys (str) to the count (int) of rows violating each rule.
    total_non_operational : int
        The total number of rows classified as non-operational.
    output_path : str, optional
        File path where the markdown report will be saved. Default is "classification_report.md".
    """
    lines = [
        "# Operational vs Non-operational Data Classification Report\n",
        f"**Total rows processed:** {total_rows:,}\n",
        f"**Total non-operational rows:** {total_non_operational:,}\n",
        f"**Percentage of non-operational data:** {(total_non_operational / total_rows * 100) if total_rows else 0:.2f}%\n",
        "## Applied Rules\n",
        "| Rule Key | Description | Violating Rows | Percentage of Total Rows |",
        "|----------|-------------|----------------|--------------------------|"
    ]

    for rule_key, info in rules.items():
        count = violation_counts.get(rule_key, 0)
        percent = (count / total_rows * 100) if total_rows else 0
        lines.append(f"| {rule_key} | {info['description']} | {count:,} | {percent:.2f}% |")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Report saved to: {output_path}")
