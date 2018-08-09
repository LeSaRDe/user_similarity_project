#!/bin/bash

# Set the time, which is the maximum time your job can run in HH:MM:SS
#SBATCH --time=24:00:00

# Set the number of nodes, and the number of tasks per node (up to 16 per node)
#SBATCH --nodes=20 --ntasks-per-node=16

# Set memory to 10G (may have to switch to mem-per-cpu)
#SBATCH --mem=122368

# Set the partition to submit to (a partition is equivalent to a queue)
#SBATCH -p haswell_q

# Set the account
#SBATCH -A ndssl

# Set the walltime
#SBATCH -t 24:00:00

#SBATCH --exclusive

echo "Env setup"

. envsetup-haswell.sh

echo "Annotation..."

java -Xms20480m usersimproj.AnnotateUserText $1 2015-01-01T00:00:00Z 2017-09-01T00:00:00Z

echo "Done!"

