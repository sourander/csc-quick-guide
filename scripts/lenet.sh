#!/bin/bash
#SBATCH --job-name=lenet_mnist_v001
#SBATCH --account=project_2017744
#SBATCH --partition=gputest
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=10
#SBATCH --mem=64G
#SBATCH --time=00:14:59
#SBATCH --gres=gpu:v100:1,nvme:32

module purge
module load pytorch

# If you would be using ImageFolder, you would have to:
#   unzip -q $PROJECTPATH/data/mnist.zip -d $LOCAL_SCRATCH

srun python lenet.py
