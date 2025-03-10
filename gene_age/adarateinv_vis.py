import fastdfe as fd
import pandas as pd
import sys

import matplotlib.pyplot as plt

from collections import defaultdict
from itertools import chain
#conda activate adarate

vcfin="/Users/sophie/workspace/mpiinternship/ogsynpop2/syn_pop2_og_mappedCC9605.snp.vcf.gz"
nspec=10

mappedn=sys.argv[1]

p = fd.Annotator(
    vcf=vcfin,
    fasta='/Users/sophie/workspace/mpiinternship/genomes/Syn_CC9605_rela.fa' ,
    gff=mappedn+'.gff' ,
    annotations=[fd.MaximumLikelihoodAncestralAnnotation(
        outgroups=["Syn_BL107_rela"],
        n_ingroups=nspec
    ), fd.DegeneracyAnnotation()],
    output=mappedn+'.deg.vcf.gz'
)

p.annotate()
#import subprocess
#subprocess.run(["tabix ", "Syn_CC9605_"+mappedn+"_genes.deg.vcf.gz"]) 

#tabix Syn_CC9605_tol_genes.deg.vcf.gz 
# instantiate parser
p = fd.Parser(
    n=nspec,
    vcf=mappedn+'.deg.vcf.gz' ,
    fasta='../genomes/Syn_CC9605_rela.fa' ,
    gff=mappedn+'.gff' ,
    #target_site_counter=fd.TargetSiteCounter(n_target_sites=3500),
    stratifications=[fd.DegeneracyStratification()],
    exclude_samples=["Syn_BL107_rela"]
)


# parse SFS
spectra: fd.Spectra = p.parse()
# visualize SFS


spectra.plot( file=mappedn+'_simplespectra.png', show=False )

sdf = spectra.to_dataframe()
#print(sdf)
sdf.to_csv(mappedn+'_dfe.csv')

sfs_neut = fd.Spectrum(sdf.neutral.tolist())
sfs_sel = fd.Spectrum(sdf.selected.tolist())

# create inference object
inf = fd.BaseInference(
    sfs_neut=sfs_neut,
    sfs_sel=sfs_sel,
    n_runs=10,
    n_bootstrap=100,
    do_bootstrap=True
)

# run inference
inf.run()

axs = plt.subplots(2,2,figsize=(11,7))[1].flatten()

types=['neutral', 'selected']

inf.plot_sfs_comparison(ax=axs[0], show=False, sfs_types=types)
inf.plot_sfs_comparison(ax=axs[1], show=False, colors=['C1','C5'])
inf.plot_inferred_parameters(ax=axs[2], show=False)
inf.plot_discretized(ax=axs[3], file=mappedn+'_spectra.png', show=False )#show=True)

inf.plot_nested_models(file=mappedn+'_nested.png', show=False)
inf.plot_likelihoods(scale='lin',file=mappedn+'_likelihood.png', show=False)


ar=inf.get_discretized()
df_dis=pd.DataFrame([ar[0],ar[1][0],ar[1][1]])
df_dis.columns=['-inf,-100', '-100,-10', '-10-,1', '-1,0', '0,1', '1,inf']
df_dis.index=['val','CI-','CI+']
df_dis.to_csv(mappedn+'_dfe_discretized.csv')



dicci= inf.get_cis_params_mle(ci_level=0.05)
dicb=inf.get_bootstrap_params()
merged_dic = defaultdict(list)
for k, v in chain(dicb.items(), dicci.items()):
    if type(v) is tuple:
        merged_dic[k].append(v[0])
        merged_dic[k].append(v[1])
    else:
        merged_dic[k].append(v)

df_params=pd.DataFrame(merged_dic)
df_params.index=['val','CI-','CI+']
df_params.to_csv(mappedn+'_dfe_params.csv')
