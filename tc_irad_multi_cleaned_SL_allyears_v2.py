import xarray as xr
import numpy as np
import pandas as pd
import sys
from datetime import datetime

# Define a function to open datasets and concatenate them
def open_and_concatenate(year, variable, months, way):
    datasets = [xr.open_dataset(f'{way}{variable}/ERA5_{year}-{month}_{variable}.nc') for month in months]
    return xr.concat(datasets, dim='time')

# Define a function to calculate statistics
def calculate_statistics(data_array):
    return {
        'mean': np.mean(data_array),
        'min': np.min(data_array),
        'max': np.max(data_array),
        'std': np.std(data_array),
        #'skew': pd.Series(data_array.reshape(-1)).skew(),
        #'kurtosis': pd.Series(data_array.reshape(-1)).kurtosis()
    }

# Function to log processing details
def log_processing(variable, year, storm_number):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f'Processed variable: {variable}, Year: {year}, Timestamp: {timestamp}, Storm number:{storm_number}'
    with open(f'/work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/datasets/processing_log.txt', 'a') as log_file:
        log_file.write(log_message + '\n')

# Main function to process data
def process_data(variable, year):
    year = int(year)
    year_next = year + 1
    month_act = [10, 11, 12]
    month_next = [1, 2, 3]
    if variable == 'geopential':
        way = '/work/FAC/FGSE/IDYST/tbeucler/default/raw_data/ECMWF/ERA5/PL/'
    else:
        way = '/work/FAC/FGSE/IDYST/tbeucler/default/raw_data/ECMWF/ERA5/SL/'

    # Open and concatenate datasets
    if year == 1990:
        dataset_act = open_and_concatenate(str(year), variable, month_next, way)
        dataset_next = open_and_concatenate(str(year_next), variable, month_next, way)
        dataset = xr.concat([dataset_act, dataset_next], dim='time')
    elif year == 2021:
        dataset = open_and_concatenate(str(year), variable, month_next, way)
    else:
        dataset_act = open_and_concatenate(str(year), variable, month_act, way)
        dataset_next = open_and_concatenate(str(year_next), variable, month_next, way)
        dataset = xr.concat([dataset_act, dataset_next], dim='time')

    # Determine the specific variable to extract
    specific_var = next(var for var in dataset.variables if var not in ['longitude', 'latitude', 'time'])

    # Import all tracks and convert dates
    dates = pd.read_csv(f'/work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/storms_start_end.csv', parse_dates=['start_date', 'end_date'])
    dates['year'] = dates['start_date'].dt.year

    # Find the indices for storms within the specified timeframe
    if year == 1990:
        index_start_october = dates[(dates['start_date'].dt.month <= 3) & (dates['start_date'].dt.year == year)].index[0]
        index_end_march = dates[(dates['end_date'].dt.month <= 3) & (dates['end_date'].dt.year == year_next)].index[0]
    elif year == 2021:
        index_start_october = dates[(dates['start_date'].dt.month <= 3) & (dates['start_date'].dt.year == year)].index[0]
        index_end_march = dates[(dates['end_date'].dt.year == 2021)].index[0]
    else:
        index_start_october = dates[(dates['start_date'].dt.month >= 10) & (dates['start_date'].dt.year == year)].index[0]
        index_end_march = dates[(dates['end_date'].dt.month <= 3) & (dates['end_date'].dt.year == year_next)].index[0]

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
            pd.DataFrame(stats[key]).to_csv(f'/work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/datasets/{variable}/storm_{i+1}/{key}_{i+1}.csv')

    # Log the processing details
    log_processing(variable, year, i)

if __name__ == '__main__':
    variable = sys.argv[1]
    year = sys.argv[2]
    process_data(variable, year)