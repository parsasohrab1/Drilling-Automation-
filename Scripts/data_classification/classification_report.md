# Operational vs Non-operational Data Classification Report

**Total rows processed:** 155,520,000

**Total non-operational rows:** 7,702,781

**Percentage of non-operational data:** 4.95%

## Applied Rules

| Rule Key | Description | Violating Rows | Percentage of Total Rows |
|----------|-------------|----------------|--------------------------|
| low_rpm | RPM less than 10 (likely drilling stopped) | 0 | 0.00% |
| no_force | WOB and Torque equal zero (no physical activity) | 0 | 0.00% |
| pump_off | Pump is off | 1,480,935 | 0.95% |
| compressor_off | Compressor is off | 2,956,797 | 1.90% |
| low_power | Power consumption below normal threshold | 36 | 0.00% |
| too_many_nans | More than 3 missing values in the row | 2,273,478 | 1.46% |
| cold_bit | Bit temperature below normal (likely idle) | 0 | 0.00% |
| high_vibration | Vibration level unusually high, possible abnormal condition | 4,962 | 0.00% |
| high_temp_motor | Motor temperature exceeds safe limit | 34 | 0.00% |
| low_mud_flow | Mud flow rate below operational minimum | 5,257 | 0.00% |
| high_resistivity | High resistivity may indicate sensor issues or abnormal formation | 0 | 0.00% |
| bit_wear_flag | Recorded bit wear failure event | 1,111,064 | 0.71% |
| stalled_rig | RPM very low but weight on bit high, indicating stall | 0 | 0.00% |