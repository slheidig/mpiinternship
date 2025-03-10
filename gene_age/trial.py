import fastdfe as fd
import pandas as pd
# neutral SFS for two types
sfs_neut = fd.Spectra({'cat0_commonwArchaea': [7224.0, 1405.0, 469.0, 196.0, 126.0, 92.0, 92.0, 118.0, 316.0, 729.0, 0.0], 'cat4_commonWPseudomona': [27749.0, 6980.0, 2135.0, 877.0, 654.0, 482.0, 517.0, 695.0, 1562.0, 3817.0, 0.0], 'cat2_commonwFirmicutes': [23070.0, 5387.0, 1622.0, 671.0, 473.0, 431.0, 422.0, 488.0, 1104.0, 2984.0, 0.0], 'cat1_commonwEukaryota': [61938.0, 16909.0, 4833.0, 1920.0, 1358.0, 1114.0, 1246.0, 1556.0, 3717.0, 9304.0, 0.0], 'cat5_onlyCyano': [18102.0, 2504.0, 810.0, 332.0, 216.0, 193.0, 177.0, 222.0, 497.0, 1102.0, 0.0], 'cat3_commonwActino': [6190.0, 1187.0, 317.0, 130.0, 89.0, 94.0, 92.0, 93.0, 241.0, 668.0, 0.0]}
)
# selected SFS for two types
sfs_sel = fd.Spectra({'cat0_commonwArchaea': [49769.0, 1944.0, 410.0, 187.0, 88.0, 77.0, 75.0, 102.0, 197.0, 645.0, 0.0], 'cat4_commonWPseudomona': [216423.0, 9779.0, 1963.0, 859.0, 707.0, 503.0, 527.0, 473.0, 1160.0, 3136.0, 0.0], 'cat2_commonwFirmicutes': [167643.0, 6922.0, 1236.0, 783.0, 350.0, 307.0, 236.0, 297.0, 738.0, 2122.0, 0.0], 'cat1_commonwEukaryota': [487552.0, 15006.0, 2602.0, 922.0, 757.0, 550.0, 602.0, 636.0, 1903.0, 5178.0, 0.0], 'cat5_onlyCyano': [106531.0, 3569.0, 908.0, 380.0, 178.0, 139.0, 115.0, 135.0, 406.0, 942.0, 0.0], 'cat3_commonwActino': [41053.0, 1624.0, 215.0, 83.0, 60.0, 71.0, 53.0, 54.0, 171.0, 481.0, 0.0]}
)
typees=['cat0_commonwArchaea','cat1_commonwEukaryota', 'cat4_commonWPseudomona',  'cat2_commonwFirmicutes', 'cat3_commonwActino', 'cat5_onlyCyano']

# create inference object
inf = fd.JointInference(
    sfs_neut=sfs_neut,
    sfs_sel=sfs_sel,
    shared_params=[fd.SharedParams(types=typees, params=["eps", "b"])],
    do_bootstrap=True
)
# run inference
inf.run();

inf.plot_inferred_parameters( file='2025dbres/jointinf_para.png', show=False );
inf.plot_sfs_comparison( file='2025dbres/jointinf_compare.png', show=False );
inf.plot_discretized(file='2025dbres/jointinf_discrete.png', show=False );
inf.perform_lrt_shared();

inf.get_counts();

inf.create_config().to_file("2025dbres/jointinf_config");

dicci= inf.get_cis_params_mle(ci_level=0.05)
dicb=inf.get_bootstrap_params()

data = []
for key, value in dicb.items():
    category, param = key.rsplit(".", 1)
    print(param)
    marginal_key = f"marginal.{category}"
    joint_key = f"joint.{category}"
    
    ci_marginal = dicci.get(marginal_key, {}).get(param, (None, None))
    ci_joint = dicci.get(joint_key, {}).get(param, (None, None))
    
    data.append([category, param, value, ci_marginal[0], ci_marginal[1], ci_joint[0], ci_joint[1]])

df = pd.DataFrame(data, columns=["Category", "Parameter", "Value", "CI_Marginal_Low", "CI_Marginal_High", "CI_Joint_Low", "CI_Joint_High"])
df=df.round(4)

df_pivot = df.pivot(index="Category", columns="Parameter", values=["Value", "CI_Marginal_Low", "CI_Marginal_High", "CI_Joint_Low", "CI_Joint_High"])
df_pivot.columns = sorted([f"{col[1]}_{col[0]}" for col in df_pivot.columns])

df_pivot.reset_index(inplace=True)
print(df_pivot)

df_pivot.to_csv("2025dbres/jointinf_parameters.csv", index=False)