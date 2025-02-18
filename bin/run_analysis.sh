

mkdir -p andi

andi --file-of-filenames=input_genomes_andi.txt --join --model=Kimura > andi/andi_distances.phy

Rscript bin/reformat_andi.R andi/andi_distances.phy 48

fastme -i andi/andi_distances_formated.phy -q


Rscript bin/plot_ree.R