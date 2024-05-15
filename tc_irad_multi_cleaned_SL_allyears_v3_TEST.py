import xarray as xr
import numpy as np
import pandas as pd
import sys
from datetime import datetime
from guppy import hpy

# Créer une instance de heapy
hp = hpy()
# might be a problem for ML data, since the data is quite large in size
# Define a function to open datasets and concatenate them
def open_and_concatenate(year, variable, months, way, level=0):
    datasets = [xr.open_dataset(f'{way}{variable}/ERA5_{year}-{month}_{variable}.nc') for month in months]
    if variable == 'geopential' and level != 0:
        datasets = [dataset.sel(level=level) for dataset in datasets]
    return xr.concat(datasets, dim='time')

# Define a function to calculate statistics
def calculate_statistics(data_array):
    return {
        'mean': np.mean(data_array),
        'min': np.min(data_array),
        'max': np.max(data_array),
        'std': np.std(data_array),
    }

# Function to log processing details
def log_processing(variable, year, level, storm_number):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f'Processed variable: {variable}, Year: {year}, Level: {level}, Timestamp: {timestamp}, Storm number:{storm_number}'
    with open(f'/work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/datasets/processing_log.txt', 'a') as log_file:
        log_file.write(log_message + '\n')

# Créer une instance de heapy
hp = hpy()

# Main function to process data
def process_data(variable, year, level=0):
    year = int(year)
    year_next = year + 1
    month_act = [10, 11, 12]
    month_next = [1, 2, 3]
    if variable == 'geopotential':
        way = '/work/FAC/FGSE/IDYST/tbeucler/default/raw_data/ECMWF/ERA5_hourly_PL/'
    else:
        way = '/work/FAC/FGSE/IDYST/tbeucler/default/raw_data/ECMWF/ERA5/SL/'

    # Open and concatenate datasets
    if year == 1990:
        dataset_act = open_and_concatenate(str(year), variable, month_next, way, level)
        dataset_next = open_and_concatenate(str(year_next), variable, month_next, way, level)
        dataset = xr.concat([dataset_act, dataset_next], dim='time')
        dataset = dataset.chunk({'time': 10})
    elif year == 2021:
        dataset = open_and_concatenate(str(year), variable, month_next, way, level)
    else:
        dataset_act = open_and_concatenate(str(year), variable, month_act, way, level)
        dataset_next = open_and_concatenate(str(year_next), variable, month_next, way, level)
        dataset = xr.concat([dataset_act, dataset_next], dim='time')
        dataset = dataset.chunk({'time': 10})

    # Determine the specific variable to extract
    specific_var = next(var for var in dataset.variables if var not in ['longitude', 'latitude', 'time', 'level'])

    # Import all tracks and convert dates
    dates = pd.read_csv(f'/work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/storms_start_end.csv', parse_dates=['start_date', 'end_date'])
    dates['year'] = dates['start_date'].dt.year

    # Find the indices for storms within the specified timeframe
    if year == 1990:
        index_start_october = dates[(dates['start_date'].dt.month <= 3) & (dates['start_date'].dt.year == year)].index[0]
        index_end_march = dates[(dates['end_date'].dt.month <= 3) & (dates['end_date'].dt.year == year_next)].index[0]
        print(index_start_october, index_end_march, '1st condition of 1990')
    elif year == 2021:
        index_start_october = dates[(dates['start_date'].dt.month <= 3) & (dates['start_date'].dt.year == year)].index[0]
        index_end_march = dates[(dates['end_date'].dt.year == 2021)].index[0]
        print(index_start_october, index_end_march, '2021 condition')
    else:
        #index_start_october = dates[((dates['start_date'].dt.month >= 10) & (dates['start_date'].dt.year == year)) | ((dates['start_date'].dt.year == year_next) & (dates['start_date'].dt.month <= 3))].index[0]
        # Chercher start_october dans year, sinon chercher dès janvier de year_next
        index_start_october = dates[((dates['start_date'].dt.month >= 10) & (dates['start_date'].dt.year == year)) | ((dates['start_date'].dt.year == year_next) & (dates['start_date'].dt.month >= 1))].index[0]
        index_end_march_first = dates[((dates['end_date'].dt.month <= 3) & (dates['end_date'].dt.year == year_next))].index
        print(index_start_october, index_end_march_first, '3rd condition start_october + index_end_march_first')
        if len(index_end_march_first) > 0:
            index_end_march = index_end_march_first[-1]
            print(index_end_march, 'index_end_march 1st condition of 2nd condition')
        else:
            #year_next += 2
            #index_end_march_second = dates[((dates['end_date'].dt.year == year_next) & (dates['end_date'].dt.month <= 3))].index
            #print(index_end_march_second, 'index_end_march_second 2nd condition of 2nd condition, +2 years')
            # Si year_next ne renvoie rien, chercher la dernière instance de tempête dans year
            index_end_march = dates[((dates['end_date'].dt.year == year) & (dates['end_date'].dt.month <= 12))].index[-1]
            print(index_end_march, 'index_end_march 2nd condition of 2nd condition')
            #if len(index_end_march_second) > 0:
            #    index_end_march = index_end_march_second[-1]
            #    print(index_end_march, 'index_end_march 1st condition of 3rd condition')
            #else:
            #    index_end_march = dates[((dates['end_date'].dt.year == year) & (dates['end_date'].dt.month == 12))].index[-1]
            #    print(index_end_march, 'index_end_march 2nd condition of 3rd condition')

    # Process each storm
    for i in range(index_start_october, index_end_march + 1):
        track = pd.read_csv(f'/work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/tc_irad_tracks/tc_1_hour/tc_irad_{i+1}_interp.txt')
        start_date = dates.at[i, 'start_date']
        end_date = dates.at[i, 'end_date']
        storm_data = dataset[specific_var].sel(time=slice(start_date, end_date))

        # Initialize lists to store statistics
        stats = {'mean': [], 'min': [], 'max': [], 'std': []}
        #, 'skewness': [], 'kurtosis': []

        # Calculate statistics for each time step
        for time_step in storm_data.time:
            data_slice = storm_data.sel(time=time_step).values
            step_stats = calculate_statistics(data_slice)
            for key in stats:
                stats[key].append(step_stats[key])

        # Save statistics to CSV files
        for key in stats:
            pd.DataFrame(stats[key]).to_csv(f'/work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/datasets/{variable}/storm_{i+1}/{key}_{i+1}_{level}.csv')

    # Log the processing details
    log_processing(variable, year, level, i+1)


variable = '2m_temperature'
year = sys.argv[2]
level = sys.argv[3]
process_data(variable, year, level)

# Obtenir un instantané de l'utilisation de la mémoire
h = hp.heap()

# Imprimer l'information d'utilisation de la mémoire
print(h)