#!/bin/bash

for folder in geopotential
do
	for year in $(seq 1990 1 2021)
	do
		sbatch --mail-type FAIL --mail-user fabien.augsburger@unil.ch --chdir /work/FAC/FGSE/IDYST/tbeucler/default/raw_data/ECMWF/WS_fabien/case_study --job-name stats_6 --output /work/FAC/FGSE/IDYST/tbeucler/default/raw_data/ECMWF/WS_fabien/case_study/log/con-%j.out --error /work/FAC/FGSE/IDYST/tbeucler/default/raw_data/ECMWF/WS_fabien/case_study/log/err-%j.err --partition cpu --nodes 1 --ntasks 1 --cpus-per-task 1 --mem 32G --time 04:30:00 --wrap "module purge; module load gcc; source ~/.bashrc; conda activate kera_lgbm; python3 /work/FAC/FGSE/IDYST/tbeucler/default/raw_data/ECMWF/WS_fabien/tc_irad_multi_cleaned_PL.py $folder $year"
	done
done
