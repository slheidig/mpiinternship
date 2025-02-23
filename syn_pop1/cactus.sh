#! /bin/bash
 
#SBATCH --job-name=cactus
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --mem=12G
#SBATCH --error=cactus_slurm.err
#SBATCH --output=cactus_slurm.out
#SBATCH --mail-type=ALL
##SBATCH --mail-user=heidig@evolbio.mpg.de
#SBATCH --partition=standard

source /data/modules/python/python-miniconda3-2024-03/etc/profile.d/conda.sh
conda activate cactus-v2.9.0
export PATH=/data/biosoftware/cactus/cactus-bin-v2.9.0/bin:$PATH
export PYTHONPATH=/data/biosoftware/cactus/cactus-bin-v2.9.0/lib:$PYTHONPATH

cactus /home/heidig/syn_pop1/.js /home/heidig/syn_pop1/syn_pop1.txt /home/heidig/cactus/syn_pop1.hal

echo start mapping 
cactus-hal2maf /home/heidig/syn_pop1/tmp  /home/heidig/syn_pop1/syn_pop1.hal /home/heidig/syn_pop1/syn_pop1_mappedBOUM118.maf.gz --refGenome Syn_BOUM118_rela --chunkSize 1000000 --noAncestors 

echo completed!
