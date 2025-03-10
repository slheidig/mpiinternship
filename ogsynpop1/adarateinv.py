import fastdfe as fd
import pandas as pd
import sys

vcfin=sys.argv[1]
mappedn=vcfin.split('mapped')[-1].split('.')[0]
samle=vcfin.split('/')[-1].split('.')[0]
nspec=int(sys.argv[2])

"""
p = fd.Annotator(
    #n=nspec,
    vcf=vcfin,
    fasta='../genomes/Syn_'+mappedn+"_rela.fa" ,
    gff='../ada_rate_est/Syn_'+mappedn+'.gff' ,
    annotations=[
        fd.DegeneracyAnnotation()],
    output='Syn_'+mappedn+".deg.vcf.gz"
)
"""

p = fd.Annotator(
    vcf=vcfin,
    fasta='../genomes/Syn_'+mappedn+"_rela.fa" ,
    gff='../ada_rate_est/Syn_'+mappedn+'.gff' ,
    #stratifications=[fd.DegeneracyStratification()],
    annotations=[fd.MaximumLikelihoodAncestralAnnotation(
        outgroups=["Syn_BL107_rela"],
        n_ingroups=nspec
    ), fd.DegeneracyAnnotation()],
    output=samle+".deg.vcf.gz"
)

p.annotate()

# instantiate parser
p = fd.Parser(
    n=nspec,
    vcf=samle+".deg.vcf.gz" ,
    fasta='../genomes/Syn_'+mappedn+"_rela.fa" ,
    gff='../ada_rate_est/Syn_'+mappedn+'.gff' ,
    #target_site_counter=fd.TargetSiteCounter(n_target_sites=3500),
    stratifications=[fd.DegeneracyStratification()],
    #annotations=[fd.MaximumLikelihoodAncestralAnnotation(
    #    outgroups=["Syn_BL107_rela"],
    #    n_ingroups=nspec
    #), fd.DegeneracyAnnotation()],
    exclude_samples=["Syn_BL107_rela"]
)
#target site param does nothing
#no sites have "valid type"
# parse SFS
spectra: fd.Spectra = p.parse()
# visualize SFS


spectra.plot( file=samle+'simplespectra.png', show=False )


sdf = spectra.to_dataframe()
print(sdf)
sdf.to_csv(samle+'_dfe.csv')