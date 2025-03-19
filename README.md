This repository contains scripts and notes from my internship with the Molecular Systems Evolution research group of Prof. J. Dutheil at the Max Planck Institute for evolutionary Biology in spring 2025.


# Population structure

## Initial questions
- Create a genome alignment of Synechococcus genomes to find out if they can be considered a population. 
- Investiage linkage equilibrium/ independent/non-independent recombination
- Are there geographic groups? Separate dataset and use groups to invesitage adaptive evolution.

## Steps
Full protocol is on [gitlab](https://gitlab.gwdg.de/molsysevol/staphylococcus-zins-evolution)!


### Initial guide tree with Andi
get it from [apt](https://github.com/evolbioinf/andi/)

![Initial guide tree with Andi](andi/andi_tree.png "Initial guide tree with Andi")

### Genome alignment with Cactus
was installed on MPI server; tried to install myself with little success

### Filter genome alignment to remove ambigous regions with MafFilter
install Bio++ libraries:  bpp-core, bpp-seq, bpp-phyl, bpp-popgen, bpp-suite and maffilter from git repos

### Reconstruct phylogeny with MafFilter and Aster
install [aster](https://github.com/chaoszhang/ASTER)

![inital aster tree](aster_tree.png)
### Realign genome with cactus and new tree

### Refilter alignment

### Re-reconstruct phylogenies
Compare r1 and r2 trees using phylo.io

![compare phylogenies from repeat cactus](aster_trees_r1r2_compare.png "compare phylogenies from repeat cactus")


### Plot tree vs environmental information
Genome alignment tree reproduces published phylogeny fairily well, no obvious connection between phylogeny, temperature or geography

![Tree with av temperature,  ocean of origin, clade/pigment](vis/syn_tree_supports.png "Tree with av temperature,  ocean of origin, clade/pigment") 

### Establish possible populations
Add supports with bpp consense > pick 2 possible populations with low internal support values:

- POP1:WH8102 to A1840 , 8 members
- POP2:TAK9802 to PROS_U_1 , 10 members


### Create VCF files with SNPs for each population

### Calculate linkage equilibrium decay

Install BCFtools, VCFtools
![LD of population 1](linkage_desequ/syn_pop1_mappedBOUM118_Fig.png "LD of population 1")  ![LD of population 2](linkage_desequ/syn_pop2_mappedCC9605_Fig.png "LD of population 2")

at 25kB is the point at which the decline becomes minimal = distance at which 2 SNPs in the genome can be considered independent (= no linkage) and are informative for population genomics methods

### Assess population structure with plink and smartPCA

keep only biallelic SNPs that are independent based on LD -> PLINK -> smartPCA

- POPULATION 1
![PCA population 1](populationstructure_pca/syn_pop1_mappedBOUM118_pca_variance.png "PCA population 1")
![PCA12 population 1](populationstructure_pca/syn_pop1_mappedBOUM118_pca_12.png "PCA12  population 1" )  
![PCA34 population 1](populationstructure_pca/syn_pop1_mappedBOUM118_pca_34.png "PCA34population 1")  
pop1 PCA2 seems to correlate with ocean of origin

- POPULATION 2
![PCA population 2](populationstructure_pca/syn_pop2_mappedCC9605_pca_variance.png "PCA of population 2")
![PCA12 population 2](populationstructure_pca/syn_pop2_mappedCC9605_pca_12.png "PCA12 of population 2")
![PCA34 population 2](populationstructure_pca/syn_pop2_mappedCC9605_pca_34.png "PCA34 of population 2")

Pop2 PCA 1 = phylogeny

### Run admixture to prove most likely each dataset is 1 population

In both cases, case 1 population is most likely


# Distribution of fitness effects

## Initial questions
- what is the rate of adaptive mutations
- apply phylostratigraphy approaches to get a measure of gene age for shared parameter estimation
- use [FastDFE](https://fastdfe.readthedocs.io/en/latest/reference/Python/inference.html)

## Steps
### Repeat alignments for population with an OUTGROUP (BL107) to get "polarized SNPs"
### Run Fast DFE

- SFS: Site frequency spectrum
    - related to the SNPs; how common they are across the different input species
    - selected = nonsynonymous sites
    - neutral = synonymous sites
- Parameter estimates = probability distribution of the selection coefficients of mutations at selected sites
    - Sb:  average (population-scaled) strength of  beneficial mutations
    - Sd: average (population-scaled) strength of deleterious mutations
    - pb: probability of a mutation being beneficial
    - e:  ancestral misidentification parameter
    - b: shape of the gamma distribution
- Function  a: expected proportion of beneficial nonsynonymous substitutions

Population 1:

![](ogsynpop1/syn_pop1_og_mappedBOUM118spectra.png)

PB=0 --> probability of benefitial mutation =0. Pop1 is unsuitable


Population 2: 


![](ogsynpop2/syn_pop2_og_mappedCC9605spectra.png)

More suitable parameters for further investigations! Very weak benefitial mutations?

### Run DIAMOND blast on mapping genome CC9605

- Installing diamond is easy
- Blast DB download keeps being corrupted; worked on 4th attempt
- Idea: exclude Cyanobacteria from hits, give minimal E parameter >>  genes that are in the outputfile are older then speciation of synechococcus
    - Problem: ca 1/10 hits is not completely annotated; only has an ID but no organism info

- Rerun w NCBI blast 
    - even less annotation beyond id

- Run Diamond blast wo exclusion critera

### Split genome in genes older/younger then cyanobacteria speciation

- parse w python script genes that have only annotation in cyanobacteria <> rest

![](gene_age/Syn_CC9605_cyano_genes_spectra.png 'cyano genes') ![](gene_age/Syn_CC9605_tol_genes_spectra.png 'rest of tree of life genes')

Small difference in the estimated parameters (Sd) can be observed > repeat with more strata!


### Initial attempt at shared parameter estimation 
- misstake in the phylogeny; should repeat the categorisation!
- possible misstakes in running fastDFE; WIP

![](gene_age/2025dbres/jointinf_para.png)