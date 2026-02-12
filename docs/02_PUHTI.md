# Puhti - Getting There and Back Again

## Project Login

![](images/05_puhti_login.png)

**Fig:** When your student project has been created, you can find the **Puhti Supercomputer** in the Services panel. Choose login.

![alt text](images/06_puhti_metrics.png)

## Test Puhti Availability

**Fig:** In the login screen, you can see how much of the resources are being used at the moment.

![alt text](images/07_puhti_apps.png)

**Fig:** If your login was succesful, you will see the Pinned interactive (containerized) apps you can run on CSC as managed services. If your login did not success, you have been too hasty. Wait a while and try again. Have a tea, read the docs, and touch the grass.

> **Note**: We will not be really using any of these services in this tutorial. Feel free to utilize e.g. Tensorboard of MLflow for tracking your training runs, but we will not cover that in this tutorial. We will be using Slurm to run our training scripts, and we will be tracking the runs with a simple custom logging solution.

## Setting up SSH Access

To interact with Puhti efficiently via the command line, you need to set up SSH keys. This allows for secure authentication without typing your password every time.

![](images/08_puhti_add_key.png)

**Fig**:** In the MyCSC portal, navigate to your profile settings to add your SSH public key. This is necessary for secure access to Puhti.


<details>
<summary>How to add key? Click me open.</summary>

### 1. Generate an SSH Key Pair

If you don't have an SSH key pair yet, open your **local** terminal and run:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Press `Enter` to save the key to the default location (`~/.ssh/id_ed25519`). It is recommended to set a passphrase.

### 2. Add the Public Key to CSC

Next, you need to provide your **public key** to the service.

1.  Display your public key content:
    ```bash
    cat ~/.ssh/id_ed25519.pub
    ```
2.  In the MyCSC portal (or the specific service view shown above), navigate to your **Profile** or **Settings**.
3.  Find the **SSH Public Keys** section.
4.  Add a new key and paste the output from the `cat` command.

If you need further instructions, you can refer to the [Setting up SSH keys](https://docs.csc.fi/computing/connecting/ssh-keys/) documentation.
</details>

---

## Connect to Puhti

Now you can direct connect to the login node using your CSC username.

```bash
ssh <username>@puhti.csc.fi
```

> **Important:** The login node is shared by all users. Do not run heavy calculations here!

To make logging easier, you can set up an SSH config file (`~/.ssh/config`) with the following content:

```bash
Host puhti
    HostName puhti.csc.fi
    User your-username
```

If you do that, you can simply connect with:

```bash
ssh puhti
```

![](images/09_puhti_SSH_MOTD.png)

**Fig:** After a successful login, you will see the Message of the Day (MOTD) with some useful information about the system status and usage tips.

---

**Next Steps:** We have established a connection. The basic prerequisites are done. We will continue the journey by setting up a Slurm job to train a CNN.

Proceed to the [Project README](../README.md) to continue.
