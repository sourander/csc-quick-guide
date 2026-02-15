# Preparing Data for Training

Now that you have verified your access and GPU capabilities, the next step is to prepare your data for efficient training. In the [Training CNN](training_cnn/01-intro.md) section, we will use a torchvision MNIST downloader. This section explains how to handle datasets that consist of many small files, which is a common scenario in deep learning. With MNIST, this is handled for you, but with custom datasets (read: the one in your assignment), you will need to do this yourself. This guide will prepare you for that.

!!! abstract "Why does this matter?"
    Deep Learning training often involves reading thousands of small image files repeatedly. On a supercomputer with a shared filesystem, doing this inefficiently can make your training very slow—or even crash the file system for everyone else!

## The `LOCAL_SCRATCH` Advantage

Even though the `home`, `project`, and `scratch` directories feel like typical hard drives, they are actually networked storage called [Lustre](https://docs.csc.fi/computing/lustre/). This kind of networked storage tends to perform poorly when accessing many small files randomly, which is exactly what happens when training a CNN with a dataset like ImageNet or CIFAR.

To solve this, Puhti compute nodes have a fast, temporary local SSD drive called `LOCAL_SCRATCH`.

**The Strategy:**
1. **Compress:** Zip your dataset into a single file on your local machine.
2. **Transfer:** Upload only that single zip file to your project directory on CSC.
3. **Unzip on Node:** In your `sbatch` job script, unzip the dataset directly to `$LOCAL_SCRATCH` at the *start* of the job.

This ensures data is read from the ultra-fast local SSD during training.

!!! warning "Temporary Storage"

    The `$LOCAL_SCRATCH` directory is **temporary** and **node-specific**.
    
    * It is wiped clean as soon as your job finishes.
    * You cannot access it from the login node.
    * You must unzip your data there *every time* you run a job.

For benchmarks, see CSC's [Which directory should I use to analyze many small files?](https://docs.csc.fi/support/faq/local_scratch_for_data_processing/).

!!! tip "Requesting NVMe"

    To use `$LOCAL_SCRATCH`, you must request NVMe space in your Slurm script, e.g., `#SBATCH --gres=gpu:v100:1,nvme:32`. This requests 32 GB of local SSD space.

## Practical Example

Let's assume we have a directory structure locally:


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



