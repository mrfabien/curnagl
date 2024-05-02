#!/bin/bash

for folder in 10m_u_component_of_wind
do
	for year in $(seq 1990 1 1993)
	do
		sbatch --mail-type ALL --mail-user fabien.augsburger@unil.ch --chdir /work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/case_study --job-name stats_7 --output /work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/case_study/log/con/con-%j.out --error /work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/case_study/log/error/err-%j.err --partition cpu --nodes 1 --ntasks 1 --cpus-per-task 1 --mem 64G --time 04:30:00 --wrap "module purge; module load gcc; source ~/.bashrc; conda activate kera_lgbm; python3 /work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/tc_irad_multi_cleaned_SL.py $folder $year"
	done
done
