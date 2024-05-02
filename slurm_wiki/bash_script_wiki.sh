#!/bin/bash -l

#SBATCH --account project_id 
#SBATCH --mail-type ALL 
#SBATCH --mail-user firstname.surname@unil.ch

#SBATCH --chdir /scratch/<your_username>/
#SBATCH --job-name my_code 
#SBATCH --output my_code.out

#SBATCH --partition cpu

#SBATCH --nodes 1 
#SBATCH --ntasks 1 
#SBATCH --cpus-per-task 8 
#SBATCH --mem 10G 
#SBATCH --time 00:30:00 
#SBATCH --export NONE

module load gcc/10.4.0 python/3.9.13

python3 /PATH_TO_YOUR_CODE/my_code.py