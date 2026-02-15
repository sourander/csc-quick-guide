# Preparing Data

Even though the `home`, `project`, and `scratch` directories feel like they are typical HDD's, they are actually networked storage called [Lustre](https://docs.csc.fi/computing/lustre/). This kind of networked drives tend to perform poorly when accessing many small files, which is the case with datasets that follow the Torchvision [ImageFolder](https://docs.pytorch.org/vision/main/generated/torchvision.datasets.ImageFolder.html) structure. There are multiple ways to mitigate this issue, but a simple and effective way with small-ish datasets is:

1. Zip the dataset on your local machine.
2. Upload the zip file to your project directory on CSC.
3. In the `squeue` slurm script, unzip the dataset to the `$LOCAL_SCRATCH` directory, which is a local SSD drive on the compute node.

Note that the `$LOCAL_SCRATCH` directory is not shared between nodes and you cannot access it from the login node beforehands. Why? Because you have no idea which compute node your job will run on. Also, the data will NOT be persistent. The unzipping will be done every time you run the job.

For benchmark on how much faster the local scratch is compared to the project directory, see CSC's [Which directory should I use to analyze many small files?](https://docs.csc.fi/support/faq/local_scratch_for_data_processing/).

!!! note

    In order to be able to use the `$LOCAL_SCRATCH` variable, you need to request the `nvme` resource in your slurm script. For example: `#SBATCH --gres=gpu:v100:1,nvme:32G`.

## Practical Example

Let's assume we have a directory where running `tree` gives us the following output:

```
images/
├── class1
│   ├── img1.jpg
│   ├── img2.jpg
│   └── ...
├── class2
│   ├── img1.jpg
│   ├── img2.jpg
│   └── ...
└── ...
```

Now we can zip or tarball the `images` directory and upload the zip/tar file to our project directory on CSC. Steps are below.

### Option A: Zip and Unzip

```bash title="On your local machine"
zip -r images.zip images/
scp images.zip puhti:/$PROJECTPATH/data/
```

Now the files are on CSC Lustre storage. In the slurm script, you can unzip the files to the local scratch and run your training script from there:

```bash title="slurm_script_should_contain.sh"
unzip -q $PROJECTPATH/data/images.zip -d $LOCAL_SCRATCH
srun python your_script.py --data_path $LOCAL_SCRATCH/images
```

### Option B: Tar and Untar

```bash title="On your local machine"
tar -czf images.tar.gz images/
scp images.tar.gz puhti:/$PROJECTPATH/data/
```

Now the files are on CSC Lustre storage. In the slurm script, you can untar the files to the local scratch and run your training script from there:

```bash title="slurm_script_should_contain.sh"
tar -xf $PROJECTPATH/data/images.tar -C $LOCAL_SCRATCH
srun python your_script.py --data_path $LOCAL_SCRATCH/images
```



