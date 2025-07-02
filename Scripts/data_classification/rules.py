# Rules for separating operational and non-operational data

rules = {
    "low_rpm": {
        "func": lambda df: df["RPM"] < 10,
        "description": "RPM less than 10 (likely drilling stopped)"
    },
    "no_force": {
        "func": lambda df: (df["WOB"] == 0) & (df["Torque"] == 0),
        "description": "WOB and Torque equal zero (no physical activity)"
    },
    "pump_off": {
        "func": lambda df: df["Pump_Status"] == 0,
        "description": "Pump is off"
    },
    "compressor_off": {
        "func": lambda df: df["Compressor_Status"] == 0,
        "description": "Compressor is off"
    },
    "low_power": {
        "func": lambda df: df["Power_Consumption"] < 100,
        "description": "Power consumption below normal threshold"
    },
    "too_many_nans": {
        "func": lambda df: df.isnull().sum(axis=1) > 3,
        "description": "More than 3 missing values in the row"
    },
    "cold_bit": {
        "func": lambda df: df["Bit_Temperature"] < 50,
        "description": "Bit temperature below normal (likely idle)"
    },
    "high_vibration": {
        "func": lambda df: df["Vibration_Level"] > 2,
        "description": "Vibration level unusually high, possible abnormal condition"
    },
    "high_temp_motor": {
        "func": lambda df: df["Motor_Temperature"] > 100,
        "description": "Motor temperature exceeds safe limit"
    },
    "low_mud_flow": {
        "func": lambda df: df["Mud_Flow_Rate"] < 800,
        "description": "Mud flow rate below operational minimum"
    },
    "high_resistivity": {
        "func": lambda df: df["Resistivity"] > 100,
        "description": "High resistivity may indicate sensor issues or abnormal formation"
    },
    "bit_wear_flag": {
        "func": lambda df: df["Failure_Type"] == 'Bit_Wear',
        "description": "Recorded bit wear failure event"
    },
    "stalled_rig": {
        "func": lambda df: (df["RPM"] < 5) & (df["WOB"] > 0),
        "description": "RPM very low but weight on bit high, indicating stall"
    }
}

def add_rule(rule_key, func, description):
    """
    Adds a new rule to the rules dictionary for identifying non-operational records.

    Each rule is defined by:
    - A unique rule key (string identifier)
    - A function (usually a lambda) that takes a DataFrame and returns a Boolean Series
    - A description explaining what the rule does

    Example usage:
    >>> add_rule(
    ...     rule_key="low_rop",
    ...     func=lambda df: df["ROP"] < 5,
    ...     description="Rate of penetration is below acceptable range"
    ... )

    :param rule_key: str
        A unique string name for the rule (e.g. "low_rop").
        Must not duplicate an existing rule key.

    :param func: function
        A function that takes a pandas DataFrame and returns a boolean Series.
        This boolean mask determines which rows violate the rule.

    :param description: str
        A short explanation of what the rule does and why it's considered non-operational.

    :raises ValueError: if the rule_key already exists in the rules dictionary.
    """
    if rule_key in rules:
        raise ValueError(f"Rule '{rule_key}' already exists.")
    rules[rule_key] = {
        "func": func,
        "description": description
    }
