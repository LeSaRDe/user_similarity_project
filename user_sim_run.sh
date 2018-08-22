#!/bin/bash

# Set the time, which is the maximum time your job can run in HH:MM:SS
#SBATCH --time=120:00:00

# Set the number of nodes, and the number of tasks per node (up to 16 per node)
#SBATCH --nodes=1 --ntasks-per-node=32

# Set memory to 10G (may have to switch to mem-per-cpu)
#SBATCH --mem=122368

# Set the partition to submit to (a partition is equivalent to a queue)
#SBATCH -p haswell_q

# Set the account
#SBATCH -A ndssl

# Set the walltime
#SBATCH -t 120:00:00

#SBATCH --exclusive

#echo "Env setup"

#. envsetup-haswell.sh

echo "User Sim..."

python /hpchome/fcmeng/user_similarity_project/src/usersimproj/user_sim.py $1 $2 $3 $4 $5 $6 $7 

echo "Done!"

