# TODO this is coming up

*This section will be updated with examples*

## Resources

* You will find example `.py` files at [gh:CSCfi/machine-learning-scripts/tree/master/examples](https://github.com/CSCfi/machine-learning-scripts/tree/master/examples)
* And Slurm files at [gh:CSCfi/machine-learning-scripts/tree/master/slurm](https://github.com/CSCfi/machine-learning-scripts/tree/master/slurm)

CSC has a very through documentation. Use it. They have also very helpful staff that can be contacted via email or by attending their Zoom sessions: [CSC Research Support Coffee – Every Wednesday at 14:00 Finnish time](https://csc.fi/en/training-calendar/csc-research-support-coffee-every-wednesday-at-1400-finnish-time-2-2/)


## TODO

### Check Stats

Use `seff <jobid>` to check CPU and GPU usage stats after the job completes.

!!! tip

    If you want to see the output of `nvidia-smi` during the job, run the following on Puhti login node:

    ```bash
    # Find nodename
    squeue -u $USER
    
    # One-time SSH into the node to check GPU status
    ssh <nodename> nvidia-smi
    ```
