def run_statistical_checks(data):
    """
    Perform a basic statistical check.
    Check if 'value' exists and is between 0 and 100.
    """
    value = data.get("value")
    if value is None:
        raise ValueError("'value' is missing from the data.")
    if not (0 <= value <= 100):
        raise ValueError(f"Value {value} is out of the valid range (0–100).")
