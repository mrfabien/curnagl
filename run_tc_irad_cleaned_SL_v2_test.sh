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
nom_var=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $2}' $config)

# Extract the Annee for the current $SLURM_ARRAY_TASK_ID
annee=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $3}' $config)

echo "Variable name: $nom_var, Year: $annee"

# Execute the python script
python3 /work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/tc_irad_multi_cleaned_SL.py "$nom_var" "$annee"

# Print to a file a message that includes the current $SLURM_ARRAY_TASK_ID, the same variable, and the year of the sample
echo "This is array task ${SLURM_ARRAY_TASK_ID}, the variable name is ${nom_var} and the year is ${annee}." >> /work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/case_study/output.txt