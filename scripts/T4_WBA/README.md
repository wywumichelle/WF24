# Task4: Predict Naturalized Flow

## Proposed method:
Level1: water balance approach
Level2: Level1 + bias correction

## Level1
In a given gauge, the flows is caculated from the summation of the runoff in its contributed area.
Q = sum(runoff *Area)

Negative runoff is mannualy replace by zero firstly.

Output: ./data/output/T4_NCP_Flows_L1_mon_ACCESS-CM2_historical.csv

![plot](./fig/T4_L1_Compare_K1.pdf)


![plot](./fig/T4_L1_NF_K1.pdf)

## Level2
Here I tried to applied a CDF matching. I borrowed the code from 
https://soilwater.github.io/pynotes-agriscience/notebooks/cdf_matching.html

But I found it is not that good for streamflow correction.
Becuase streamflow has very large variance.
It sometime results in very high bias corrected flow.
I still share the figure/output here, but not the code.

Output: ./data/output/T4_NCP_Flow_L2_mon_ACCESS-CM2_historical.csv

![plot](./fig/T4_L2_NF_K1_ACCESS-CM2.pdf)
