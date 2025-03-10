#!/bin/bash
#SBATCH -J CaPTk_registration
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 128
#SBATCH --time=1-00:00:00
#SBATCH -p batch
#SBATCH --qos=normal

singularity exec  --no-home \
                  --bind datasets/:/datasets \
                  --bind output_registration/:/output_registration \
                  --bind src/:/src \
                  --bind scripts:/scripts \
                  --bind atlases/:/atlases \
                  --bind logs/:/logs \
                  captk_latest.sif \
                  bash scripts/registration/intermediate_registration.sh "$1" "$2" "$3" "$4" "$5"