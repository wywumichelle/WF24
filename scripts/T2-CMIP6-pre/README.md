
# Download and post-procssesing CMIP6 data
## 1. Download CMIP6
### Generate the wget scripts from one of the below portal.

- USA, PCMDI/LLNL (California) - https://esgf-node.llnl.gov/search/cmip6/
- France, IPSL - https://esgf-node.ipsl.upmc.fr/search/cmip6-ipsl/
- Germany, DKRZ - https://esgf-data.dkrz.de/search/cmip6-dkrz/
- UK, CEDA - https://esgf-index1.ceda.ac.uk/search/cmip6-ceda/

### Change the permission of the script
```
chmod 750 wget-*.sh
```
### Download in background
```
nohup ./wget-*.sh -s > *.log &
```

Ref:
https://esgf.github.io/esgf-user-support/user_guide.html

## 2. Combine different time slices into one
./scripts/combine.sh

It could be done easily using CDO (mergetime) or NCO (e.g., ncrcat).
For example,
```
cdo mergetime pr_Amon_UKESM1-0-LL_historical_r1i1p1f2_gn_185001-194912.nc \
              pr_Amon_UKESM1-0-LL_historical_r1i1p1f2_gn_195001-201412.nc \
              pr_Amon_UKESM1-0-LL_historical_r1i1p1f2_gn_185001-201412.nc

```

## 3. Regrid to common coordinate

To regrid different resolution in to 1x1 degree resolution, here I use two-step cdo commands:

###1. Generate weighting files by assign the regrid method and the resolution
./scripts/genwgt.sh

I use nearest interpolation for precipitation, bi-linear for other  variables
```
cdo -O -L gennn,global_1 $infile ${vars}_${model}_weights.nc
cdo -O -L genbil,global_1 $infile $outweightfile
```
###2. Regrid the files according to the weight files, and select the timeframe
./scripts/seldate_remap.sh
```
cdo -O -L remap,global_1,./${vars}_${model}_weights.nc -seldate,18500101,20141231 $infile $outfile
```

## 4. Ensemble average
./scripts/ensmean.sh
Some models have multiple ensemble members (r*i*p*f*). Here I average all the ensemble member into one ensemble average.
```
cdo ensmean $infiles $outfile
```
### Masking the State
Input: one of any netCDF generated in above proccess(1-degree coordinate)
Input: Polygon of Texas State
Output: 1-degree 0-1 mask (if the center of gridcell is inside the polygon)

Scripts: ./mask/mask_Texas_global-1.ncl
Ouput:./mask/StateTexas_global-1.nc
Figure: ./mask/mask_StateTexas_global-1.png

