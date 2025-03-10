#! /bin/bash
 
#SBATCH --job-name=cactus
#SBATCH --ntasks=10
#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --mem=128G
#SBATCH --error=cactus_slurm.err
#SBATCH --output=cactus_slurm.out
#SBATCH --mail-type=ALL
##SBATCH --mail-user=heidig@evolbio.mpg.de
#SBATCH --partition=standard

source /data/modules/python/python-miniconda3-2024-03/etc/profile.d/conda.sh
conda activate cactus-v2.9.0
export PATH=/data/biosoftware/cactus/cactus-bin-v2.9.0/bin:$PATH
export PYTHONPATH=/data/biosoftware/cactus/cactus-bin-v2.9.0/lib:$PYTHONPATH

rm -r .js
rm -r tmp

cactus /home/heidig/ogsynpop1/.js /home/heidig/ogsynpop1/syn_pop1.txt /home/heidig/ogsynpop1/syn_pop1_og.hal

echo start mapping 
cactus-hal2maf /home/heidig/ogsynpop1/tmp  /home/heidig/ogsynpop1/syn_pop1_og.hal /home/heidig/ogsynpop1/syn_pop1_og_mappedBOUM118.maf.gz --refGenome Syn_BOUM118_rela --chunkSize 1000000 --noAncestors 

echo completed!
