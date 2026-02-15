# Introduction

This guide provides a quick overview of how to train a Convolutional Neural Network (CNN) on a GPU using the CSC (Center for Scientific Computing) resources.

It is designed for university students in Finland who need to set up their environment and run training scripts on the Puhti supercomputer.

## Prerequisites

- **Haka** (or Virtu) account. You need to be a university student in Finland.

## Guide Structure

:arrow_left: This same structure can be seen in the left sidebar navigation.

1.  [**Setup**](setup/01-project.md): How to get a CSC account, create a project, and connect to Puhti via SSH.
2.  [**Testing GPU**](testing_gpu/01-moving-files.md): Moving your files to the server and running a simple GPU test job.
3.  [**Training CNN**](training_cnn/01-intro.md): Detailed guide on training a CNN with a custom dataset.

---

!!! abstract "Scope of this guide"

    This guide focuses specifically on analyzing data using **PyTorch** on the **Puhti** supercomputer via **Slurm** batch jobs. While CSC offers other tools (like Notebooks or user interfaces), the command-line approach is the most flexible and powerful skill for a data scientist to learn.

!!! tip

    CSC resources are powerful but require careful usage. Always start small before running heavy jobs.

    If you are new to Linux or Slurm, review the **Linux basics for CSC** or the **CSC Quick reference (pd)** cheat sheet before proceeding. The can be found in [CSC Tutorials](https://docs.csc.fi/support/tutorials/).



