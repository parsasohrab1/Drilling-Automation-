import os
import pandas as pd
from fastparquet import ParquetFile, write
from rules import rules
from generate_report import generate_report

# Global counters
violation_counts = {key: 0 for key in rules}
total_rows = 0
non_operational_row_count = 0

# Directories
INPUT_DIR = "../output_fastparquet"
OP_PATH = "output_operational.parquet"
NON_OP_PATH = "output_non_operational.parquet"


def process_chunk(df):
    """
    Processes a chunk of data by applying predefined operational rules to classify records as operational or non-operational.

    This function performs the following steps:
    1. Updates the global count of total processed rows.
    2. Applies each rule's function to the DataFrame to generate boolean masks indicating which rows violate each rule.
       - Handles exceptions by logging errors and treating those rows as not violating the rule.
    3. Combines all rule masks to identify rows violating at least one rule (non-operational rows).
    4. Updates global counts for the number of violations per rule and the total count of non-operational rows.
    5. Splits the DataFrame into two subsets:
       - `df_op`: operational rows (no rule violations)
       - `df_non_op`: non-operational rows (violate one or more rules)

    Parameters
    df : pandas.DataFrame
        Input data chunk to classify.

    Returns
    tuple of pandas.DataFrame
        - df_op: DataFrame containing operational records.
        - df_non_op: DataFrame containing non-operational records.
    """
    global total_rows, non_operational_row_count
    total_rows += len(df)

    # Create rule masks
    rule_masks = {}
    for key, rule in rules.items():
        try:
            rule_masks[key] = rule["func"](df)
        except Exception as e:
            print(f"Error applying rule {key}: {e}")
            rule_masks[key] = pd.Series(False, index=df.index)

    # Combine all rule violations
    combined_mask = pd.DataFrame(rule_masks).any(axis=1)

    # Count per-rule violations
    for key in rule_masks:
        violation_counts[key] += rule_masks[key].sum()

    # Count total non-operational rows
    non_operational_row_count += combined_mask.sum()

    # Split data
    df_non_op = df[combined_mask].copy()
    df_op = df[~combined_mask].copy()
    return df_op, df_non_op


def process_all_files():
    """
    Processes all Parquet files in the input directory by chunk, classifying each record as operational or non-operational.

    Workflow:
    1. Iterates over all Parquet files in the `INPUT_DIR` directory, sorted alphabetically.
    2. For each file:
        - Reads the data in chunks (row groups).
        - Applies `process_chunk` to separate operational and non-operational records.
        - Writes the operational records to a cumulative Parquet file (`OP_PATH`).
        - Writes the non-operational records to a separate cumulative Parquet file (`NON_OP_PATH`).
        - Uses a flag (`first_op` and `first_non_op`) to handle initial write vs append mode.
        - Prints progress logs for each file and chunk processed.
    3. After processing all files and chunks, prints a completion message.
    4. Optionally generates a classification report summarizing the results using `generate_report`.

    Returns:
    - None
    """
    first_op, first_non_op = True, True
    for file in sorted(os.listdir(INPUT_DIR)):
        if not file.endswith(".parquet"):
            continue

        path = os.path.join(INPUT_DIR, file)
        print(f"Processing file {file} started")
        pf = ParquetFile(path)

        for i, df in enumerate(pf.iter_row_groups()):
            df_op, df_non_op = process_chunk(df)

            if not df_op.empty:
                if first_op:
                    write(OP_PATH, df_op, compression='snappy')
                    first_op = False
                else:
                    write(OP_PATH, df_op, compression='snappy', append=True)

            if not df_non_op.empty:
                if first_non_op:
                    write(NON_OP_PATH, df_non_op, compression='snappy')
                    first_non_op = False
                else:
                    write(NON_OP_PATH, df_non_op, compression='snappy', append=True)

            print(f"File {file} chunk {i} was processed")

    print("All files processed.")

    # Generate report (Optional)
    generate_report(
        total_rows=total_rows,
        violation_counts=violation_counts,
        total_non_operational=non_operational_row_count,
        output_path="classification_report.md"
    )


if __name__ == "__main__":
    process_all_files()
