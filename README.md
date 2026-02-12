# CSC Quick Guide: Training CNN on GPU

This guide provides a quick overview of how to train a Convolutional Neural Network (CNN) on a GPU using the CSC (Center for Scientific Computing) resources. It covers the necessary steps to set up your environment, prepare your data, and execute your training script efficiently.

**Prerequisites:**

- Haka (or Virtu) account. You need to be a Uni student in Finland.

---

## Getting CSC Access

1. If you do not have a CSC account, read [How to create new CSC user account > Getting an account with Haka or Virtu](https://docs.csc.fi/accounts/how-to-create-new-user-account/#getting-an-account-with-haka-or-virtu). Remember to check the terms and conditions.
2. Follow the instructions on [Getting started with CSC services for students](https://docs.csc.fi/support/tutorials/student_quick/) to set up your student project. Remember to check the terms and conditions.

The MEMO of what buttons I needed to press in order to create mine can be found in [docs/01_CSC_PROJECT.md](docs/01_CSC_PROJECT.md) file.

---

## Accessing Puhti

<div style="background-color: #54c7ec; color: #fff; font-weight: 700; padding-left: 10px; padding-top: 5px; padding-bottom: 5px"><strong>NOTE:</strong></div>

<div style="background-color: #f3f4f7; padding-left: 10px; padding-top: 10px; padding-bottom: 10px; padding-right: 10px">

<p>It may take on hour or so before you can continue logging into Puhti. Things are being set up in the background.</p>

<p>While waiting, look into Puhti documentation. Add <a href="https://docs.csc.fi/support/tutorials/hpc-quick/">Getting started with supercomputing at CSC</a> documentation site to your bookmarks. You may need that site often.</p>

<p>Check also the <a href="https://docs.csc.fi/support/tutorials/">Tutorials</a>. If you are not accustomed to Linux Command line or Slurm, there is a <b>Linux basics for CSC</b> cheat sheet with most common commands you will need.</p>

</div>

Further MEMO of what button I need to press to access Puhti can be found at [docs/02_PUHTI.md](docs/02_PUHTI.md)

---

## Puhti Stuff You Must Know

Read the [docs/03_PUHTI_MUST_KNOW.md](docs/03_PUHTI_MUST_KNOW.md) if you are completely new to supercomputing environment. Do not treat a supercomputer like a virtual machine. It is not.

---

# Actual Guide

Now that you have access to Puhti, and you have a rough idea of what you are doing, you can start preparing your student project for training a CNN. We will cover all those steps in this README.md file, but, I will point to other full code files as needed. It is now assumed that: **you are able to log into Puhti using SSH**.

In this document, from now, the following aliases are assumed to exist:

```bash
# in Puhti AND local machine
PROJECTPATH=/projappl/project_1234567 # replace with your project number
SCRATCHPATH=/scratch/project_1234567  # replace with your project number
```

## Moving files to Puhti

You *can* use the graphical file transfer tools, but I recommend using the command line. The `scp` command is your friend. It uses the same SSH protocol as the `ssh` command, so you can use the same authentication method (SSH keys) and the same username.

```bash
# on LOCAL machine
cd path/to/this/repo
scp -r . puhti:$PROJECTPATH
```

![](images/01_scp.png)

**Fig:** Use `scp` command to copy the files from your local machine to Puhti. The `-r` flag is for recursive copying, which is needed to copy the entire directory. Note that the files exist happily in the project directory, as can be seen in the screenshot. During training, you would move the files to scratch and read/write from there, but for now, we can keep them in the project directory.


TODO! Here will be the instructions for moving the files to scratch and running the training script. For now, you can just keep the files in the project directory and run the training script from there. It is not recommended, but it is possible.

## Test GPU

To test if you have access to GPU, let's fetch an example script from CSC's repo and run a dummy training script that uses GPU. You can find the example script at [gh:CSCfi/machine-learning-scripts/](https://github.com/CSCfi/machine-learning-scripts/). The script is called `pytorch-gpu-test.py`. Let's get it to the scratch and run it:

```bash
ssh puhti
cd $SCRATCHPATH
mkdir gputest && cd gputest
URL='https://raw.githubusercontent.com/CSCfi/machine-learning-scripts/refs/heads/master/examples/pytorch-gpu-test.py'
curl $URL -O
```

Create a file called `first_slurm.sh` with the content that is shown is the image below. You cannot copy&paste from an image, but you can find a very similar script from: [gh:CSCfi/pytorch-ddp-examples/blob/master/run-ddp-gpu1-mlflow.sh](https://github.com/CSCfi/pytorch-ddp-examples/blob/master/run-ddp-gpu1-mlflow.sh)

![](images/02_first_slurm_sh.png)

**Fig:** The contents of the `first_slurm.sh` file.

![](images/03_sbatch.png)

**Fig:** Use `sbatch` command to submit the job to Slurm. Note that I was unlucky and ended up in a queue even with this tiny job. After about 20 seconds, the job was visible in the `squeue -u $USER` output. After this, when the job finished, the output was visible in the `slurm-[id].out` file.

![](images/05_seff.png)

**Fig:** Use `seff` command to check the CPU and GPU usage. Note that this tiny job used 0.19 CSC Billing Units in 11 seconds. Energy usage was 0.13 Wh.

## Train a CNN using Custom dataset

TODO. I will add the example to `examples/01_cnn/` directory.

## How to Continue?

* You will find example `.py` files at [gh:CSCfi/machine-learning-scripts/tree/master/examples](https://github.com/CSCfi/machine-learning-scripts/tree/master/examples)
* And Slurm files at [gh:CSCfi/machine-learning-scripts/tree/master/slurm](https://github.com/CSCfi/machine-learning-scripts/tree/master/slurm)

CSC has a very through documentation. Use it. They have also very helpful staff that can be contacted via email or by attending their Zoom sessions: [CSC Research Support Coffee – Every Wednesday at 14:00 Finnish time](https://csc.fi/en/training-calendar/csc-research-support-coffee-every-wednesday-at-1400-finnish-time-2-2/)