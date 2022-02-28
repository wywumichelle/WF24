# Task3 data deliverables


Wen-Ying Wu 2022.02.17
This is the technical note for the WF24 Task3 data deliverbles.

## File Name
T3_Quad_${variable}_${frequency}_${model}_${scenario}.csv
e.g., T3_Quad_tasmin_mon_UKESM1-0-LL_ssp585.csv

T3: Task3
Quad: 27 TWDB quadrangle
${variable}: The standard name used in CMIP6 archeive. 
             pr- precipitation; 
             tas- air temperature;
             tasmin - Daily minimum near-surface air temperature;
             tasmax- Daily maximum near-surface air temperature.
${freqency}: mon-monthly data; day-daily data

${model}: CMIP6 model name


${scenario}: historifcal- 1850-2014; ssp- 2015-2100

## Calendar
There is no standard calendar used in the CMIP6 models.


## Unit
precipitation: inch; inch/day for daily fields, inch/month for monthly fields.
temperature: K (Kelvin)
Monthly/daily fields are downloaded from CMIP6 archeive. We did not mannualy average the daily fields to monthly fields.
Original unit for precipitation is kg/m2/s. We used 0.0393700787 inch =1 mm; 1 day= 86400 seconds 
Number of day in year depends on each GCM calendar (gregorian or 360 days). 

## Downscale/regrid
Model resolutions range from 0.7-1.88 degree. All model fields are regrid to a common 1 degree. Nearest interpolation is used for precipiation, and bilinear interpolation is used for all other variables.

