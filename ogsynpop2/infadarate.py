import fastdfe as fd
import matplotlib.pyplot as plt
import pandas as pd
#pop1
fname='syn_pop2_og_mappedCC9605'

sdf=pd.read_csv(fname+'_dfe.csv')

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
inf.plot_discretized(ax=axs[3], file=fname+'spectra.png', show=False )#show=True)



# disable progress bar and set logging level to warning to avoid cluttering
fd.disable_pbar = True
fd.logger.setLevel('WARNING')

inf.plot_nested_models(file=fname+'_nested.png', show=False);

inf.plot_likelihoods(scale='lin',file=fname+'_likelihood.png', show=False);