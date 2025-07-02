# Dataset Description

The dataset contains 155M records (with 23 columns) sampled at 1 Hz for 10 different rigs, simulating continuous drilling operations over a 6-month period.

| Feature Name         | Dtype           | Description                                               | Has_Nulls |
|----------------------|------------------|-----------------------------------------------------------|-----------|
| Timestamp            | datetime64[ns]   | Timestamp of the record (1-second interval)               | False     |
| Rig_ID               | str              | Identifier for the rig (e.g., RIG_01)                     | False     |
| Depth                | float64          | Cumulative drilled depth (in meters or feet)              | True      |
| WOB                  | float64          | Weight on Bit – Downward force on the bit                | True      |
| RPM                  | float64          | Rotations per minute of the drill bit                    | True      |
| Torque               | float64          | Rotational force applied to the drill                    | True      |
| ROP                  | float64          | Rate of Penetration – Drill speed                        | True      |
| Mud_Flow_Rate        | float64          | Flow rate of drilling mud                                | True      |
| Mud_Pressure         | float64          | Pressure in the mud system                               | True      |
| Mud_Temperature      | float64          | Temperature of the drilling mud                          | True      |
| Mud_Density          | float64          | Density of drilling fluid                                | True      |
| Mud_Viscosity        | float64          | Viscosity of drilling mud                                | True      |
| Mud_PH               | float64          | pH value of drilling mud                                 | True      |
| Gamma_Ray            | float64          | Gamma ray readings from rock formation                   | True      |
| Resistivity          | float64          | Electrical resistivity of the formation                  | True      |
| Pump_Status          | int64            | 0 or 1 indicating pump on/off                            | True      |
| Compressor_Status    | int64            | 0 or 1 indicating compressor on/off                      | True      |
| Power_Consumption    | float64          | Power usage of the rig system                            | True      |
| Vibration_Level      | float64          | Vibration intensity of equipment                         | True      |
| Bit_Temperature      | float64          | Temperature at the drill bit                             | True      |
| Motor_Temperature    | float64          | Temperature of the motor                                 | True      |
| Maintenance_Flag     | int64            | 1 if maintenance is needed, else 0                       | True      |
| Failure_Type         | str              | Type of failure, or "None" if no failure                 | False     |


### Additional Information
* Sensor values were simulated using domain-informed normal distributions to resemble real-world drilling operations.
* Maintenance events were injected at a rate of 5% per device, with randomized failure types simulating diverse equipment issues.
* 5% of the dataset was randomly masked to simulate sensor dropout or communication loss. Critical identifiers and failure labels were left intact.
* 3% of numeric values were corrupted with random noise (±10%) to reflect sensor drift or calibration errors.

