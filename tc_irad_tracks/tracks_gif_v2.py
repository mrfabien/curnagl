# %%
import xarray as xr
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import math
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import imageio

# %%
# convert the longitudes from 0-360 to -180-180
def convert_lon(lon):
    if lon > 180:
        return lon - 360
    else:
        return lon

# %%

# Function to plot storm for a specific timestep
def plot_storm(ax, lon_east, lon_west, lat_south, lat_north):
    lon_east = convert_lon((lon_east))
    lon_west = convert_lon(lon_west)
    lat_south = np.asarray(lat_south)
    lat_north = np.asarray(lat_north)
    ax.add_patch(patches.Rectangle((lon_west, lat_south), lon_east - lon_west, lat_north - lat_south, linewidth=1, edgecolor='r', facecolor='none'))

# Read storm start and end dates
storm_dates = pd.read_csv("/Users/fabienaugsburger/Documents/GitHub/master-project/tracks_square_storm/storms_start_end.csv", parse_dates=['start_date', 'end_date'])

# Loop through each storm file
for i in range(1, 97):
    storm_data = pd.read_csv(f"/Users/fabienaugsburger/Documents/GitHub/master-project/tracks_square_storm/tc_irad_tracks/tc_1_hour/tc_irad_{i}_interp.txt")

    # Create a list of storm frames
    storm_frames = []

    # Loop through each timestep of the storm
    for index, row in storm_data.iterrows():
        fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
        
        # Add basemap features
        ax.coastlines()
        ax.add_feature(cfeature.BORDERS)
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.OCEAN)
        
        # Plot storm rectangle
        plot_storm(ax, row['lon_east'], row['lon_west'], row['lat_south'], row['lat_north'])
        
        # Get the corresponding storm start and end date
        storm_start_date = storm_dates.iloc[i-1]['start_date']
        storm_end_date = storm_dates.iloc[i-1]['end_date']
        
        # Set title with storm start and end dates
        ax.set_title(f"Storm {i} - {storm_start_date} to {storm_end_date}")
        
        # Set x and y limits
        ax.set_xlim(-100, 150)
        ax.set_ylim(0, 90)
        
        # Set labels
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        
        # Save the plot as an image
        plt.savefig(f"/Users/fabienaugsburger/Documents/GitHub/master-project/tracks_square_storm/all_frames/storm_{i}_frame_{index}.png")
        plt.close()
        
        # Append the image to the list of frames
        storm_frames.append(f"/Users/fabienaugsburger/Documents/GitHub/master-project/tracks_square_storm/all_frames/storm_{i}_frame_{index}.png")
    
    # Create gif from frames
    with imageio.get_writer(f"/Users/fabienaugsburger/Documents/GitHub/master-project/tracks_square_storm/test_gif/storm_{i}_animation.gif", mode='I') as writer:
        for frame in storm_frames:
            image = imageio.imread(frame)
            writer.append_data(image)


# %%
# check if the coordinates are separated by 8 degrees at each timestep

# Loop through each storm file

for i in range(1, 97):
    storm_data = pd.read_csv(f"/Users/fabienaugsburger/Documents/GitHub/master-project/tracks_square_storm/tc_irad_tracks/tc_1_hour/tc_irad_{i}_interp.txt")
    print(f"Storm {i}")
    for index, row in storm_data.iterrows():
        if index == 0:
            continue
        lon_diff = abs(row['lon_east'] - row['lon_west'])
        lat_diff = abs(row['lat_north'] - row['lat_south'])
        print(f"Time {index} - Lon diff: {lon_diff}, Lat diff: {lat_diff}")