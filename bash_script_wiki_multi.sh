#!/bin/bash -l

#SBATCH --account project_id 
#SBATCH --mail-type ALL 
#SBATCH --mail-user firstname.surname@unil.ch 

#SBATCH --chdir /scratch/<your_username>/
#SBATCH --job-name my_code 
#SBATCH --output=my_code_%A_%a.out

#SBATCH --partition cpu 
#SBATCH --ntasks 1

#SBATCH --cpus-per-task 8 
#SBATCH --mem 10G 
#SBATCH --time 00:30:00 
#SBATCH --export NONE

#SBATCH --array=0-13

module load gcc/10.4.0 python/3.9.13

ARGS=(0.1 2.2 3.5 14 51 64 79.5 80 99 104 118 125 130 100)

python3 /PATH_TO_YOUR_CODE/my_code.py ${ARGS[$SLURM_ARRAY_TASK_ID]}