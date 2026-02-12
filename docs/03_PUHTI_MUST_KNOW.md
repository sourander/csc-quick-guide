# Puhti Must Know

Some basic stuff you need to know before using Puhti.

## Storage and Login Node

* The node you log into is called the login node. It is shared by all users. **Do not run heavy calculations here!**
* There are three disk areas: home, project and scratch. 
    * **home** is for small personal files (helper scripts etc.)
    * **projappl** is for files related to your project. 
    * **scratch** is for temporary files that can be deleted at any time. Move the dataset to scratch and read/write from there during training. After the training is done, store the permanent files to project dir.

Quotas are:

| Storage Path          | Files | Size  |
| --------------------- | ----- | ----- |
| /users/yourname/      | 100k  | 10 GB |
| /projappl/project_123 | 100k  | 50 GB |
| /scratch/project_123  | 1M    | 1 TB  |

Read more: [Data storage for machine learning](https://docs.csc.fi/support/tutorials/ml-data/)

## Running Code

* Puhti uses the module system to manage software. You need to load the appropriate modules to use the software you need. For example, to use Python, you need to load the Python module.
* You can see the available modules with `module avail` command. Currently loaded modules can be seen with `module list` command.
* Puhti uses Apptainer (ex. Singularity) containers to run software. You can either use the pre-built containers provided by CSC or build your own container with the software you need.
* You do not run your training script directly on the login node. Instead, you submit a batch job to the Slurm scheduler. It is a TODO queueing system that manages the resources of the cluster and runs your job when the resources are available. If your job is tiny, it will likely find free resources quickly and start immediately. If your job is huge, requiring many GPUs, it may take a while before it starts. You can check the status of your job with `squeue` command.

## One Tutorial to Rule Them All

The [CSC Computing Environment](https://csc-training.github.io/csc-env-eff/) in CSC Training site is highly recommended. It covers all you probably need to know right now.