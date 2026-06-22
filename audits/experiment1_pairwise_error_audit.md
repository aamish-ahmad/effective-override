# Experiment 1 Pairwise Error Audit

| Pair | Positive ID | Control ID | Ground truth | Trajectory decisions | Snapshot decisions | Snapshot error status | Trajectory correct | Crossing-step difference |
|---|---|---|---|---|---|---|---|---|
| E1P01 | E1T01 | E1T02 | positive=yes; control=no | positive=yes; control=no | positive=uncertain; control=no | positive uncertain | yes | N/A |
| E1P02 | E1T03 | E1T04 | positive=yes; control=no | positive=yes; control=no | positive=no; control=no | positive missed | yes | N/A |
| E1P03 | E1T05 | E1T06 | positive=yes; control=no | positive=yes; control=no | positive=yes; control=no | none | yes | 1 |
| E1P04 | E1T07 | E1T08 | positive=yes; control=no | positive=yes; control=no | positive=yes; control=no | none | yes | 1 |
| E1P05 | E1T09 | E1T10 | positive=yes; control=no | positive=yes; control=no | positive=yes; control=yes | control false-positive | yes | 1 |
| E1P06 | E1T11 | E1T12 | positive=yes; control=no | positive=yes; control=no | positive=no; control=no | positive missed | yes | N/A |
| E1P07 | E1T13 | E1T14 | positive=yes; control=no | positive=yes; control=no | positive=uncertain; control=no | positive uncertain | yes | N/A |
| E1P08 | E1T15 | E1T16 | positive=yes; control=no | positive=yes; control=no | positive=no; control=no | positive missed | yes | N/A |
| E1P09 | E1T17 | E1T18 | positive=yes; control=no | positive=yes; control=no | positive=yes; control=no | none | yes | 1 |
| E1P10 | E1T19 | E1T20 | positive=yes; control=no | positive=yes; control=no | positive=no; control=no | positive missed | yes | N/A |
| E1P11 | E1T21 | E1T22 | positive=yes; control=no | positive=yes; control=no | positive=uncertain; control=no | positive uncertain | yes | N/A |
| E1P12 | E1T23 | E1T24 | positive=yes; control=no | positive=yes; control=no | positive=yes; control=no | none | yes | 1 |
| E1P13 | E1T25 | E1T26 | positive=yes; control=no | positive=yes; control=no | positive=no; control=no | positive missed | yes | N/A |
| E1P14 | E1T27 | E1T28 | positive=yes; control=no | positive=yes; control=no | positive=uncertain; control=no | positive uncertain | yes | N/A |
| E1P15 | E1T29 | E1T30 | positive=yes; control=no | positive=yes; control=no | positive=uncertain; control=no | positive uncertain | yes | N/A |

Crossing-step difference is snapshot detection step minus trajectory detection step on positive rows where both detected a crossing.
