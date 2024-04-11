#!/bin/bash

#SBATCH --mail-type FAIL
#SBATCH --mail-user fabien.augsburger@unil.ch
#SBATCH --chdir /work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/case_study
#SBATCH --job-name stats_8
#SBATCH --output /work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/case_study/log/con/con-%A_%a.out
#SBATCH --error /work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/case_study/log/error/err-%A_%a.err
#SBATCH --partition cpu
#SBATCH --nodes 1
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 1
#SBATCH --mem 64G
#SBATCH --time 00:30:00

# Set your environment
module purge
module load gcc
source ~/.bashrc
conda activate kera_lgbm

# Define your array
#SBATCH --array=0-30%5  # Change this to match the number of folders you have and the desired stride

# Define your folders array
folders=(
    "10m_u_component_of_wind"
    "10m_v_component_of_wind"
    "2m_dewpoint_temperature"
    "2m_temperature"
    "cloud_base_height"
    "convective_available_potential_energy"
    "convective_inhibition"
    "convective_precipitation"
    "convective_rain_rate"
    "convective_snowfall"
    "high_cloud_cover"
    "instantaneous_10m_wind_gust"
    "k_index"
    "land_sea_mask"
    "large_scale_precipitation"
    "large_scale_snowfall"
    "mean_large_scale_precipitation_rate"
    "mean_top_net_long_wave_radiation_flux"
    "mean_top_net_short_wave_radiation_flux"
    "mean_total_precipitation_rate"
    "mean_sea_level_pressure"
    "mean_surface_latent_heat_flux"
    "mean_surface_net_long_wave_radiation_flux"
    "mean_surface_net_short_wave_radiation_flux"
    "mean_vertically_integrated_moisture_divergence"
    "surface_pressure"
    "total_precipitation"
    "total_totals_index"
)

# Get the folder for this task
folder="${folders[$SLURM_ARRAY_TASK_ID]}"

# Loop over years
for year in {1990..2021}
do
    python3 /work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/tc_irad_multi_cleaned_SL.py "$folder" "$year"
done
