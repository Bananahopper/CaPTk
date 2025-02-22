#!/bin/bash
#SBATCH -J CaPTk_Brain_Extraction
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 128
#SBATCH --time=1-00:00:00
#SBATCH -p batch
#SBATCH --qos=normal


module load tools/Singularity
source activate CaPTk

singularity exec  --no-home \
                  --bind datasets/:/datasets \
                  --bind output_registration/:/output_registration \
                  --bind src/:/src \
                  --bind scripts:/scripts \
                  --bind atlases/:/atlases \
                  --bind logs/:/logs \
                  captk_latest.sif \
                  bash scripts/segmentation/intermediary_brain_extraction.sh "$1"