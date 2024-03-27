#!/bin/bash

for folder in 10m_u_component_of_wind 10m_v_component_of_wind 2m_dewpoint_temperature 2m_temperature cloud_base_height convective_available_potential_energy convective_inhibition convective_precipitation convective_rain_rate convective_snowfall high_cloud_cover instantaneous_10m_wind_gust k_index land_sea_mask large_scale_precipitation large_scale_snowfall mean_large_scale_precipitation_rate mean_top_net_long_wave_radiation_flux mean_top_net_short_wave_radiation_flux mean_total_precipitation_rate mean_sea_level_pressure mean_surface_latent_heat_flux mean_surface_net_long_wave_radiation_flux mean_surface_net_short_wave_radiation_flux mean_vertically_integrated_moisture_divergence surface_pressure total_precipitation total_totals_index
do
	for year in $(seq 1990 1 2021)
	do
		sbatch --mail-type FAIL --mail-user fabien.augsburger@unil.ch --chdir /work/FAC/FGSE/IDYST/tbeucler/default/raw_data/ECMWF/WS_fabien/case_study --job-name stats_6 --output /work/FAC/FGSE/IDYST/tbeucler/default/raw_data/ECMWF/WS_fabien/case_study/log/con-%j.out --error /work/FAC/FGSE/IDYST/tbeucler/default/raw_data/ECMWF/WS_fabien/case_study/log/err-%j.err --partition cpu --nodes 1 --ntasks 1 --cpus-per-task 1 --mem 64G --time 04:30:00 --wrap "module purge; module load gcc; source ~/.bashrc; conda activate kera_lgbm; python3 /work/FAC/FGSE/IDYST/tbeucler/default/raw_data/ECMWF/WS_fabien/tc_irad_multi_cleaned_SL.py $folder $year"
	done
done
