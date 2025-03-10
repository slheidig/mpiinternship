import fastdfe as fd

import sys


vcfin=sys.argv[1]
mappedn=vcfin.split('mapped')[-1].split('.')[0]
nspec=sys.argv[2]
# instantiate parser
p = fd.Annotator(
    #n=nspec,
    vcf=vcfin,
    fasta='Syn_'+mappedn+"_rela.fa" ,
    gff='Syn_'+mappedn+'.gff' ,
    #target_site_counter=fd.TargetSiteCounter(n_target_sites=3500),
    annotations=[
        fd.DegeneracyAnnotation()],
    output='Syn_'+mappedn+".deg.vcf.gz"
    #stratifications=[fd.DegeneracyStratification()]
)

#p.annotate()

# instantiate parser
p = fd.Parser(
    n=nspec,
    vcf=vcfin,
    fasta='Syn_'+mappedn+"_rela.fa" ,
    gff='Syn_'+mappedn+'.gff' ,
    #target_site_counter=fd.TargetSiteCounter(n_target_sites=3500),
    annotations=[fd.DegeneracyAnnotation()],
    stratifications=[fd.DegeneracyStratification()]
)

#target site param does nothing
#no sites have "valid type"
# parse SFS
spectra: fd.Spectra = p.parse()
# visualize SFS
spectra.plot()