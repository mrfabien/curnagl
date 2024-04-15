#!/bin/bash

#SBATCH --mail-type ALL
#SBATCH --mail-user fabien.augsburger@unil.ch
#SBATCH --chdir /work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/case_study
#SBATCH --job-name stats_test
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
#SBATCH --array=0-2%2  # Change this to match the number of folders you have and the desired stride

# Define your folders array
folders=(
    "10m_u_component_of_wind"
    "10m_v_component_of_wind"
)

# Get the folder for this task
folder="${folders[$SLURM_ARRAY_TASK_ID]}"

# Loop over years
for year in {1990..1993}
do
    python3 /work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/tc_irad_multi_cleaned_SL.py "$folder" "$year"
done
