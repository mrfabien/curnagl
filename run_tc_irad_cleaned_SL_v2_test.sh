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
#SBATCH --array=1-10  # Change this to match the number of folders you have and the desired stride

# Specify the path to the config file
config=/work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/config_test.txt
#echo "${SLURM_ARRAY_TASK_ID}"

# Extract the Nom_dossier for the current $SLURM_ARRAY_TASK_ID
Nom_dossier=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $2}' $config)

# Extract the Annee for the current $SLURM_ARRAY_TASK_ID
Annee=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $3}' $config)

# Execute the python script
python3 /work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/tc_irad_multi_cleaned_SL.py "$Nom_dossier" "$Annee"