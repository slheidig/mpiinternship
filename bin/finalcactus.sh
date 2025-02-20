#! /bin/bash
 
#SBATCH --job-name=cactus
#SBATCH --ntasks=10
#SBATCH --nodes=1
#SBATCH --time=10:10:00
#SBATCH --mem=128G
#SBATCH --error=fincactus_slurm.err
#SBATCH --output=fincactus_slurm.out
#SBATCH --mail-type=ALL
##SBATCH --mail-user=heidig@evolbio.mpg.de
#SBATCH --partition=standard

source /data/modules/python/python-miniconda3-2024-03/etc/profile.d/conda.sh

conda activate cactus-v2.9.0

export PATH=/data/biosoftware/cactus/cactus-bin-v2.9.0/bin:$PATH

export PYTHONPATH=/data/biosoftware/cactus/cactus-bin-v2.9.0/lib:$PYTHONPATH

rm -r CactusFinal
mkdir -p CactusFinal
cd CactusFinal
cat ../synechococcus_mappedWH8101.astral4.mad.dnd > synechococcus.txt
echo "" >> synechococcus.txt


for elem in ../genomes/*rela.fa ; do
    fname=$(basename "$elem")
    oname="${fname%.*}"
    echo $elem
    echo "$oname $elem" >> synechococcus.txt
done

echo "files prepped"
cactus ./js synechococcus.txt synechococcus.hal


echo "--------------------------------------"
echo "--------------------------------------"
echo "--------------------------------------"


cactus-hal2maf tmp synechococcus.hal synechococcus_mappedWH8101.maf.gz --refGenome Syn_WH8101_rela --chunkSize 1000000 --noAncestors       

