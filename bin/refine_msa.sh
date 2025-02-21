#! /bin/bash

cd CactusFinal
mkdir -p FilteredAlignments
echo realign
#maffilter param=../bin/MafFilter-Realign.bpp

echo cleans
#maffilter param=../bin/MafFilter-Clean.bpp

#Rscript ../bin/plot_cleaned_ali.R

maffilter param=../bin/MafFilter-Phylogeny.bpp
#round1
#291 blocks kept, totalizing 254865bp.

#308 blocks kept, totalizing 267138bp.No more token in tokenizer.
#MafFilter's done. Bye.
#Total execution time: 0.000000d, 2.000000h, 13.000000m, 36.000000s.


conda activate aster
astral4 -t 8 -i synechococcus_mappedWH8101.phyml_trees.dnd -o synechococcus_mappedWH8101.astral4.dnd

Rscript ../bin/reroot_aster.R