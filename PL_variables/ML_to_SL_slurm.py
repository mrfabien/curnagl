import xarray as xr
import numpy as np
import os
import sys

variable = sys.argv[1]
year = sys.argv[2]

path_to_ML = f'/work/FAC/FGSE/IDYST/tbeucler/default/raw_data/ECMWF/ERA5/PL/{variable}/'
path_to_scratch = f'/scratch/faugsbur/{variable}/'

full_pressure = [
    "10",
    "20",
    "30",
    "50",
    "70",
    "100",
    "150",
    "200",
    "250",
    "300",
    "400",
    "500",
    "600",
    "700",
    "800",
    "850",
    "900",
    "925",
    "950",
    "975",
    "1000",
]

#years = range(1992,2022)
months = range(1,13)

# open each file in the path_to_ML directory and select one level at a time and then register it in the path_to_scratch directory

for i in range(len(full_pressure)):
    print('Processing level ',full_pressure[i])
    #for year in years:
        #print('Processing year ',year)
    for month in months:
        file_path = f'{path_to_scratch}ERA5_{str(year)}-{month}_{variable}_{full_pressure[i]}.nc'
        if os.path.exists(file_path):
            print('Month ',month,' of year', year, 'and level', full_pressure[i],' already processed')
        else:
            ds = xr.open_dataset(f'{path_to_ML}ERA5_{str(year)}-{month}_{variable}.nc')
            ds = ds.sel(level=int(full_pressure[i]))
            #ds = ds.rename({'r':'r'+full_pressure[i]})
            #ds = ds.drop(['latitude','longitude'])
            ds.to_netcdf(path_to_scratch+'ERA5_'+str(year)+'-'+str(month)+'_'+variable+'_'+str(full_pressure[i])+'.nc')
            ds.close()