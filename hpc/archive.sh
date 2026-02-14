#!/bin/bash
#SBATCH --job-name=ks-arxv
#SBATCH --time=36:00:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1
#SBATCH --output=logs/archive_%j.out
#SBATCH --error=logs/archive_%j.err

# Get the current username
USERNAME=$(whoami)

LOCAL="/mnt/parscratch/users/$USERNAME/data/iBEAt_Build"
REMOTE="login1:/shared/abdominal_imaging/Archive/iBEAt_Build"

rsync -av --no-group --no-perms --delete "$LOCAL/kidney_shape" "$REMOTE"
