# Training CNN

## LeNet-5 on MNIST

This practical example is based on the [LeNet-5 architecture](https://en.wikipedia.org/wiki/LeNet) and the [MNIST dataset](https://en.wikipedia.org/wiki/MNIST_database). Note that **we do not use** the torchvision's `ImageFolder` dataset class and we **do not** move any files from local PC to Puhti like shown in the [Preparing Data for Training](training_cnn/01-intro.md) section. Why? To make sure that the example script doesn't show 99 % correct answer to University course project. You need to implement that portion yourself. :nerd:

### Accessing the example files

The example files are located in the `scripts` directory of this repository. You can find a link to the Github repository in the top right corner of the page. Look for :simple-github: icon. Either clone the repository or download the specific files you need. The example files are:

```
scripts/
├── lenet.py
└── lenet.sh
```

### Copying files to Puhti

```bash title="On your local machine"
cd scripts
scp ./lenet.* puhti:/$PROJECTPATH/lenet/
```

!!! note

    The latter command assumes you have configured your `.ssh/config` file to have an alias for Puhti. If you haven't, you can use the full command:

    ```bash
    scp ./lenet.* <your_username>@puhti.csc.fi:/project_123456/lenet/
    ```

### Using LOCAL_SCRATCH in Python

Whether you use MNIST downloader or `ImageFolder`, how you use the `LOCAL_SCRATCH` environment variable is the same. The `os` module in Python can be used to read environment variables. This is implemented in the `lenet.py` script, but is also demonstrated below for quick reference:

```python title="lenet.py"
import os

# ...
DATA_PATH = os.environ.get("LOCAL_SCRATCH", "./data")
DATA_PATH = os.path.expandvars(DATA_PATH)
print(f"Using data path: {DATA_PATH}")

# ...
trainset = datasets.MNIST(
    DATA_PATH, download=True, train=True, transform=train_transform
)
```

### Running the job

This should start to feel familiar by now. Instead of running anything in the login node, you add the script to the chosen partition's queue. The choices are made in the Slurm script, which is `lenet.sh` in this case.

```bash title="On Puhti"
# ssh puhti 
cd $PROJECTPATH/lenet

sbatch lenet.sh
```

The `lenet.sh` script can be found in the repo, as mentioned above, but it's contents are shown below for quick reference. You will need to change the `--account` flag to match your project ID.

```bash title="lenet.sh"
#!/bin/bash
#SBATCH --job-name=lenet_mnist_v001
#SBATCH --account=project_CHANGE_ME
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
```

### Using the Model

The `lenet.py` script trains a simple LeNet-5 model on the MNIST dataset and stores it to `models/MNIST_make_your_own_versioning_stragegy.pth`. Now you can either:

1. Implement an inference script and run it on Puhti, or
2. Download the model to your local machine and run inference there.

The option 2 is easy and, assuming that you own a GPU-enabled machine (like Nvidia RTX 3060 or similar), typical assignment-scale models should run fine on your local machine. Training requires more resources than inference. To copy the model to your local machine, you can use `scp` again:

```bash title="On your local machine"
# A variable is created here to keep code lines shorter
MODELNAME=MNIST_make_your_own_versioning_stragegy.pth
MODELPATH=$PROJECTPATH/lenet/models/$MODELNAME

# Copy the model to local machine
scp puhti:$MODELPATH ./models/
```

!!! info "Why the funky file name?"

    The file name is intentionally verbose to encourage you to implement your own versioning strategy for your models. You **need** to know what was the learning rate, batch size, and other hyperparameters for the model you are using. This is especially important when you start to experiment with different architectures and hyperparameters. You can use tools like MLflow or Weights & Biases to track your experiments, or simply maintain a well-structured directory and file naming convention plus potentially an Excel sheet to track your experiments.

![Stupid meme concluding the section](https://i.imgflip.com/ak710f.jpg)

## Extra Tips and Resources

### How to Handle Python Packages

#### What packages are in the module?

The `pytorch` module on Puhti contains **a lot** more than just PyTorch. It also contains many common dependencies, such as `torchvision`, `torchaudio`, and `torchtext`. You can check the exact content of the module by running:

```bash title="On Puhti"
module load pytorch
pip list
```

#### Installing a new package

In case you need additional packages, you need some extra steps. A recommended method here is a virtual environment. Check the [Using Python on CSC supercomputers](https://docs.csc.fi/support/tutorials/python-usage-guide/#using-venv). How will you know if you need additional packages? You will find out when you run the script and it throws an error about a missing package. Read the `slurm-[jobid].out` file to see the error message.

```bash title="On Puhti"
module load pytorch
which python
# Out:  /appl/soft/ai/wrap/pytorch-2.9/bin/python3
python -m venv --system-site-packages .venv
source .venv/bin/activate
pip install cowsay
cowsay -t "Miau"
```

This will print out:

```
  ____
| Miau |
  ====
    \
     \
       ^__^
       (oo)\_______
       (__)\       )\/\
           ||----w |
           ||     ||
```

!!! warning

    Your `pip` cache dir is located in your home directory, which has a very limited quota. If you install new packages, you may want to look into guide: [How to avoid Python pip cache filling up my home directory](https://docs.csc.fi/support/faq/python-pip-cache/)

Now, in order to use this in your Slurm job, you will need to call to correct Python executable in your Slurm script:

```bash title="lenet.sh"
# ... rest of the Slurm script ...
PYTHON=./.venv/bin/python
srun $PYTHON lenet.py
```

!!! info

    If you have a lot of dependencies, especially some that contains large files, you may want to look into using a container instead. Guide at CSC's [Apptainer containers](https://docs.csc.fi/computing/containers/overview/) is a good starting point.
    
    You don't need to build everything from scratch. Running `module show pytorch` reveals that `pytorch` module on Puhti is e.g. `/appl/soft/ai/wrap/pytorch-2.9/container.sif` image. You can follow CSC's [Example: Extending a local image](https://docs.csc.fi/computing/containers/examples/#example-extending-a-local-image) to build your own image on top of that, adding only the packages you need as layer on top of the existing image. This will save you a lot of time and effort, while also giving you the flexibility to add whatever packages you need.



### How to Monitor GPU Usage

#### After the Job

Use `seff <jobid>` to check CPU and GPU usage stats after the job completes.

#### During the Job

A quick and dirty way to monitor GPU usage during a job is to run `nvidia-smi` in a loop on the compute node. You can do this by adding the following line to your slurm script:

```bash
# Find nodename
squeue -u $USER

# One-time SSH into the node to check GPU status
ssh <nodename> nvidia-smi
```

This tiny LeNet-5 model consumes very little GPU memory:

```
Sun Feb 15 10:55:22 2026       
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.288.01             Driver Version: 535.288.01   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  Tesla V100-SXM2-32GB           On  | 00000000:89:00.0 Off |                    0 |
| N/A   35C    P0              79W / 300W |    597MiB / 32768MiB |     32%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
                                                                                         
+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|    0   N/A  N/A   1149299      C   ...soft/ai/wrap/pytorch-2.9/bin/python      594MiB |
+---------------------------------------------------------------------------------------+
```

!!! tip

    A better option would be to use e.g. `torch.profiler` to log GPU usage stats during the job. This is a bit more work to set up, so we won't cover it in this guide. You could even place these to MLflow, if you want true visibility into your training runs.



### Further Reading

Note that the guide below will most likely 100% match your use case. You will need to adapt the code and commands to your needs. The guide is meant to be a starting point and a reference for you to build on top of. Check the CSC documentation for more details and examples:

* You will find example `.py` files at [gh:CSCfi/machine-learning-scripts/tree/master/examples](https://github.com/CSCfi/machine-learning-scripts/tree/master/examples)
* And Slurm files at [gh:CSCfi/machine-learning-scripts/tree/master/slurm](https://github.com/CSCfi/machine-learning-scripts/tree/master/slurm)

CSC has a very through documentation. Use it. They have also very helpful staff that can be contacted via email or by attending their Zoom sessions: [CSC Research Support Coffee – Every Wednesday at 14:00 Finnish time](https://csc.fi/en/training-calendar/csc-research-support-coffee-every-wednesday-at-1400-finnish-time-2-2/)


