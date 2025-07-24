from dvr_stats import run_statistical_checks
from dvr_reconciliation import reconcile_data

def process_data(record):
    # Step 1: Statistical check
    run_statistical_checks(record)

    # Step 2: Reconciliation
    reconciled_record = reconcile_data(record)

    # Save the reconciliation report and print confirmation
    report = f"Sensor {reconciled_record['sensor_id']} reconciliation status: {reconciled_record['status']}"
    save_reconciliation_report(report)
    print("Report saved:", report)

    return reconciled_record

def save_reconciliation_report(report, filename="reconciliation_reports.log"):
    with open(filename, "a") as f:  # Open file in append mode
        f.write(report + "\n")      # Write report and newline
