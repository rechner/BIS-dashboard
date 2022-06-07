# BIS ASCII serial format

|          | BIS field | Field                   | Type                   | Ex                  | ex 2                |
|----------|-----------|-------------------------|------------------------|---------------------|---------------------|
| S_HDR3   | TIME      | Datetime                | str datetime           | 10/22/2021 22:44:00 | 05/29/2022 23:42:43 |
| SYS 3.30 | DSC       | Smoothing Rate?         |                        | 10                  | 10                  |
|          | PIC       | PIC Version             |                        | 27                  | 57                  |
|          | Filters   | Filters                 | bool "On" or "Off"     | On                  | On                  |
|          | Alarm     | Alarms                  | str "High" or "Low"    | None                | None                |
|          | Lo-Limit  | Low Limit               | int or "Off"           | Off                 | Off                 |
|          | Hi-Limit  | High Limit              | int or "Off"           | Off                 | Off                 |
|          | Silence   | Silence Alarms          | bool "Yes" or "No"     | No                  | No                  |
| Ch. 1    | SR        | Suppression Ratio       |                        | 0                   | 0                   |
|          | SEF       | Spectral edge frequency | float                  | 21.3                | 20.5                |
|          | BISBIT    | Hex BIS bitmap value    | hexadecimal            | 20b2                | 601                 |
|          | BIS       | BIS number              | float                  | 65.2                | 63.6                |
|          | TOTPOW    | Total Power             | float                  | 67.7                | 57                  |
|          | EMGLOW    | EMG                     | float                  | 49.1                | 29.3                |
|          | SQI       | Signal Quality Index    | float                  | 50.6                | 97.4                |
|          | IMPEDNCE  | Sensor Impedance        | int                    | 12                  | 3277                |
|          | ARTF2     |                         | int                    | 0                   | 20000000            |
| Ch. 2    | SR        |                         |                        | 0                   | 0                   |
|          | SEF       |                         |                        | 0                   | 20.5                |
|          | BISBIT    |                         |                        | 8000                | 601                 |
|          | BIS       |                         |                        | 0                   | 63.6                |
|          | TOTPOW    |                         |                        | 0                   | 57                  |
|          | EMGLOW    |                         |                        | 0                   | 29.3                |
|          | SQI       |                         |                        | 100                 | 100                 |
|          | IMPEDNCE  |                         |                        | 13                  | 3277                |
|          | ARTF2     |                         |                        | 0                   | 20000000            |
| Ch. 12   | SR        |                         |                        | 0                   | 0                   |
|          | SEF       |                         |                        | 21.3                | 20.7                |
|          | BISBIT    |                         |                        | 20b2                | 601                 |
|          | BIS       |                         |                        | 97.7                | 63                  |
|          | TOTPOW    |                         |                        | 67.7                | 57.1                |
|          | EMGLOW    |                         |                        | 49.1                | 22.7                |
|          | SQI       |                         |                        | 50.6                | 100                 |
|          | IMPEDNCE  |                         |                        | 0                   | 0                   |
|          | ARTF2     |                         |                        | 0                   | 20000000            |

