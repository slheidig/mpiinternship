#parse gff
#source ~/miniconda3/etc/profile.d/conda.sh 
gff_file='gene_age/Syn_CC9605.gff'

incsv='gene_age/2025dbres/matches_1k_2025.csv' #sys.argv[1]
import pandas as pd
import sys  


def gff_to_fasta(gff_file):
    translations = []
    gids=[]
    with open(gff_file, 'r') as f:
        for line in f:
            if line.startswith("#") or line.startswith("##"):  # Skip headers
                continue
            columns = line.strip().split('\t')
            # Check for CDS entries
            if columns[2] == "CDS":
                attributes = columns[8].split(';')
                gid=attributes[0].split('=')[-1]
                cds=attributes[-1].split('=')[-1]
                translations.append(gid+'\n'+cds)
                gids.append(gid)
                
    with open ("Syn_CC9605_genes.fasta",'w') as of:
        for elem in translations:
            of.write('>'+elem+'\n')

    return gids

def filter_gff(glist,fname):

    olines=[]
    with open(gff_file, 'r') as f:
        for line in f:
            if line.startswith("#") or line.startswith("##"):  # Skip headers
                olines.append(line)
            elif 'sequence_assembly' in line:
                olines.append(line)
            else:
                columns = line.strip().split('\t')
                attributes = columns[8].split(';')
                gid=attributes[0].split('=')[-1]
                if gid in glist:
                    olines.append(line)
                
    with open ("gene_age/2025dbres/Syn_CC9605_"+fname+".gff",'w') as of:
        for elem in olines:
            of.write(elem)
#gff_to_fasta(gff_file)

#run blast
#get cyanobacs y/n

def parse_blast(incsv):

    df=pd.read_csv(incsv, sep='\t' ,
    names=['qseqid','sseqid','qlen','slen','pident','nident','evalue','staxids','sscinames','sskingdoms','skingdoms','sphylums','full_sseq'],
    dtype={'qseqid':'string','sseqid':'string','qlen': 'Int64','slen': 'Int64','pident':'Float32','nident':'Float32','evalue':'Float32','staxids':'string','sscinames':'string','sskingdoms':'string','skingdoms':'string','sphylums':'string','full_sseq':'string'})

    #print(df.sphylums.value_counts(dropna=False).to_dict())
    """
        print(df.nunique())
        100file:
        staxids         5506
        sscinames       5506
        sskingdoms         8
        skingdoms         16
        sphylums          78


        1kfile:
        staxids         60754
        sscinames       60754
        sskingdoms         13
        skingdoms          42
        sphylums          343




        df.sskingdoms.value_counts(dropna=False).to_dict()
        100file
        {'Bacteria': 152676, <NA>: 85232, 'Eukaryota': 366,

        1kfile
        'Bacteria': 1094642, <NA>: 736706, 'Eukaryota': 25518, 'Viruses': 1667, 'Archaea': 1397,

        PHYLUMS1k

        <NA>: 736706, 
        '0': 3354, 

        'Cyanobacteriota': 927551, 

        'Actinomycetota': 23904, 
        'Bacillota': 12269,  'Armatimonadota': 153, 
        'Chloroflexota': 1724, 

        'Pseudomonadota': 100955, 'Bacteroidota': 6311,'Planctomycetota': 2852, 'Thermodesulfobacteriota': 2401, 'Myxococcota': 2315, 'Campylobacterota': 1448,'Verrucomicrobiota': 1389, 'Acidobacteriota': 1275, 'Nitrospirota': 700, 'Spirochaetota': 695, 'Gemmatimonadota': 519, 'Rhodothermota': 280, 'Balneolota': 176, 'Chlorobiota': 161, 'Bdellovibrionota': 155,'Ignavibacteriota': 101, 
        'Thermotogota': 127, 'Deinococcota': 1917, 'Synergistota': 111,


        EUKARYA
        'Streptophyta': 7733, 
        'Chlorophyta': 1878, 
        Rhodophyta': 5516, 

        'Ascomycota': 678, 'Basidiomycota': 269, 'Mucoromycota': 108, 

        'Haptophyta': 176, 
        'Oomycota': 122, 
        'Bacillariophyta': 1556, 
        'Euglenozoa': 97,
        'Cercozoa': 3377, 
        'Chordata': 1292, 
        'Arthropoda': 259, 

        ARCHAEA
        'Methanobacteriota': 977, 
        'Thermoplasmatota': 173, 


        'Uroviricota': 1552, 
        'Cyanobacteriota;Pseudomonadota': 605,
        'Cyanobacteriota;Bacillota': 538,
        'Cyanobacteriota;Planctomycetota': 455,
        'Candidatus Rokuibacteriota': 285,
        'Candidatus Omnitrophota': 101, 


        skingdoms 1kfiles
        'Bacillati': 966338, 
        <NA>: 736706, 
        'Pseudomonadati': 122672, 
        '0': 15186, 
        'Viridiplantae': 9626, ' >plant
        Thermotogati': 2155, 
        'Metazoa': 1799, 
        'Heunggongvirae': 1552, 
        'Fungi': 1199, 
        'Methanobacteriati': 1160,  >arch
        'Bacillati;Pseudomonadati': 1128, 
        'Thermoproteati': 148, '
        0;Pseudomonadati': 101, 

        100file
        #https://lifemap.cnrs.fr/tree?efficiency-mode=false&tool=search
        Cyanobacteriota': 147651, 
        'Bacillota': 151,
        'Actinomycetota': 539, 
        'Pseudomonadota': 2217, :'Bacteroidota': 158, |'Planctomycetota': 719, 


        CAT0: x v archaea
        CAT1: bac vs eukaryota
        CAT2: terrabacteria vs pseudomonadota
        CAT3: Actinomycetota > Bacillota vs cyanobac
        CAT4: cyanobac vs synechococcus

        CAT5: plants v cyanobacteria


        'Cercozoa': 163,  {eukarya!!}



        <NA>: 85232, 
        'Cyanobacteriota;Planctomycetota': 421, 
        'Cyanobacteriota;Pseudomonadota': 354, 
        'Uroviricota': 201, 
        '0': 168, 

    """
    df.fillna('', inplace=True)
    df['sphylums']=df['sphylums'].str.replace('0','').str.replace(';',',').str.replace(',,',',')
    #df['sphylums'].fillna('', inplace=True)
    gdf=df.astype(str).groupby('qseqid').agg(lambda x: list(filter(None,list(set(','.join(sorted(x.unique())).split(','))))))

    selco=['sskingdoms','skingdoms','sphylums']	

    for elem in selco:
        odf = gdf[elem] 
        df = odf.to_frame().reset_index() 
        df.columns = ["qseqid", elem]

        df[elem] = df[elem].apply(lambda x: [part for item in x for part in item.split(";")] if isinstance(x, list) else x.split(";"))      
        df_exploded = df.explode(elem)
        df_encoded = pd.crosstab(df_exploded["qseqid"], df_exploded[elem])

        df_encoded.to_csv('gene_age/2025dbres/1kmatches_'+elem+'.csv', sep='\t')

    tolgenesdf= gdf['sphylums'][gdf['sphylums'].map(len) >1 ]
    unique_to_cyanodf= gdf['sphylums'][gdf['sphylums'].map(len) ==1 ]

    noid=gdf['sphylums'][gdf['sphylums'].map(len) ==0]
    go=False

    if unique_to_cyanodf.explode().unique() == ['Cyanobacteria']:
        unique_to_cyano= unique_to_cyanodf.index.tolist()
        tolgenes = tolgenesdf.index.tolist()


        if len(unique_to_cyano)+len(tolgenes) +noid.shape[0]== gdf.shape[0]:
            print('ok')
            print( 'tol genes: ', len(tolgenes), 'cyano genes: ', len(unique_to_cyano), 'no species: ',noid.shape[0])
            filter_gff(tolgenes,'tol_genes')
            filter_gff(unique_to_cyano,'cyano_genes')
        else:
            
            print('prblem')
            print( 'tol genes: ', len(tolgenes), 'cyano genes: ', len(unique_to_cyano), 'no species: ',noid.shape[0])
    else:
        print('startswith')

#2021 db tol genes:  1671 cyano genes:  1065 no species:  1

#parse_blast(incsv)

def bivalent_splitstuff():
    """
            CAT0: x v archaea
            CAT1: bac vs eukaryota
    """
    elem ='sskingdoms'
    df=pd.read_csv('gene_age/2025dbres/1kmatches_'+elem+'.csv', sep='\t')
    cat0dfPOST=df[df.Archaea==0]
    cat0dfPRE=df[df.Archaea>0]
    filter_gff(cat0dfPOST.qseqid.tolist(),'cat0_woArchaea')
    filter_gff(cat0dfPRE.qseqid.tolist(),'cat0_commonwArchaea')
    print("cat0 Archaea", cat0dfPOST.shape[0] , cat0dfPRE.shape[0])

    cat1POST=cat0dfPOST[cat0dfPOST.Eukaryota==0] #not present in euk
    cat1PRE=cat0dfPOST[cat0dfPOST.Eukaryota>0]
    #bacetria always true
    filter_gff(cat1POST.qseqid.tolist(),'cat1_woArEu')
    filter_gff(cat1PRE.qseqid.tolist(),'cat1_commonwArEu')
    print("cat1 Archaea,Eukaryota", cat1POST.shape[0] , cat1PRE.shape[0])

    """
            CAT2: terrabacteria vs pseudomonadota
            
    """

    elem ='skingdoms'
    df=pd.read_csv('gene_age/2025dbres/1kmatches_'+elem+'.csv', sep='\t')
    #Bacillati includes terrabacteria incl synec
    #vs Pseudomonadati
    cat2POST=cat1POST[cat1POST.Pseudomonadati==0]
    cat2PRE=cat1POST[cat1POST.Pseudomonadati>0]
    filter_gff(cat2POST.qseqid.tolist(),'cat2_woArEuPseudomonadati')
    filter_gff(cat2PRE.qseqid.tolist(),'cat2_commonwArEuPseudomonadati')
    print("cat2 Pseudomonadati", cat2POST.shape[0] , cat2PRE.shape[0])

    """
            CAT3:  Bacillota <>   Cyanobacteriota
            Cat4: Actinomycetota <>Cyanobacteriota
            CAT5: plants v cyanobacteria Chlorophyta  Cyanobacteriota
    """

    elem ='sphylums'
    df=pd.read_csv('gene_age/2025dbres/1kmatches_'+elem+'.csv', sep='\t')

    cat3POST=cat2POST[cat2POST.Bacillota==0]
    cat3PRE=cat2POST[cat2POST.Bacillota>0]
    filter_gff(cat3POST.qseqid.tolist(),'cat3_woBacillota')
    filter_gff(cat3PRE.qseqid.tolist(),'cat3_commonwBacillota')
    print("cat3 Bacillota", cat3POST.shape[0] , cat3PRE.shape[0])


    cat4sPOST=cat3POST[cat3POST.Actinomycetota==0]
    cat4sPRE=cat3POST[cat3POST.Actinomycetota>0]
    filter_gff(cat4sPOST.qseqid.tolist(),'cat4_woBacillotaWoActinomycetota')
    filter_gff(cat4sPRE.qseqid.tolist(),'cat4_commonwBacillotaWActinomycetota')
    print("cat4strict Bacillota,Actinomycetota", cat4sPOST.shape[0] , cat4sPRE.shape[0])


    cat4POST=df[df.Actinomycetota==0]
    cat4PRE=df[df.Actinomycetota>0]
    filter_gff(cat4POST.qseqid.tolist(),'cat4_woActinomycetota')
    filter_gff(cat4PRE.qseqid.tolist(),'cat4_commonwActinomycetota')
    print("cat4 Actinomycetota", cat4POST.shape[0] , cat4PRE.shape[0])


    cat5POST=df[df.Chlorophyta==0]
    cat5PRE=df[df.Chlorophyta>0]
    filter_gff(cat5POST.qseqid.tolist(),'cat5_woChlorophyta')
    filter_gff(cat5PRE.qseqid.tolist(),'cat5_commonwChlorophyta')
    print("cat5 Chlorophyta", cat5POST.shape[0] , cat5PRE.shape[0])

    """
            CAT6: cyanobac vs synechococcus taxid 1117 vs 2626047
    """


def nested_split():
    """
            CAT0: x v archaea
            CAT1: bac vs eukaryota
    """
    elem ='sskingdoms'
    df=pd.read_csv('gene_age/2025dbres/1kmatches_'+elem+'.csv', sep='\t')

    df=df[df.Bacteria>0] #should be all but qc
    cat0dfPOST=df[df.Archaea==0]
    cat0dfPRE=df[df.Archaea>0]

    filter_gff(cat0dfPRE.qseqid.tolist(),'cat0_commonwArchaea')
    print("cat0 Archaea", cat0dfPOST.shape[0] , cat0dfPRE.shape[0])

    cat1POST=cat0dfPOST[cat0dfPOST.Eukaryota==0] #not present in euk
    cat1PRE=cat0dfPOST[cat0dfPOST.Eukaryota>0]

    filter_gff(cat1PRE.qseqid.tolist(),'cat1_commonwEukaryota')
    print("cat1 Eukaryota", cat1POST.shape[0] , cat1PRE.shape[0])

    lid=cat1POST.qseqid.tolist()
    """
            CAT2: terrabacteria vs pseudomonadota
    """       

    elem ='skingdoms'
    df=pd.read_csv('gene_age/2025dbres/1kmatches_'+elem+'.csv', sep='\t')

    #only prev selected go further
    df=df[df.qseqid.isin(lid)]
    df=df[df.Bacillati >0]

    cat2POST=df[df.Pseudomonadati==0]
    cat2PRE=df[df.Pseudomonadati>0]
    #filter_gff(cat2PRE.qseqid.tolist(),'cat2_commonwPseudomonadati')
    print("cat2 Pseudomonadati", cat2POST.shape[0] , cat2PRE.shape[0])

    cat2POST=cat2POST.loc[:, (cat2POST != 0).any(axis=0)]
    cat2POST.to_csv('cat2o_commonwPseudomonadati.tsv',sep='\t')
    print(cat2POST.shape)
    lid2=cat2POST.qseqid.tolist()
    """
                CAT3:  Bacillota <>   Cyanobacteriota
                Cat4: Actinomycetota <>Cyanobacteriota
                CAT5: plants v cyanobacteria Chlorophyta  Cyanobacteriota
    """

    elem ='sphylums'
    df=pd.read_csv('gene_age/2025dbres/1kmatches_'+elem+'.csv', sep='\t')


    sdf=df[df.qseqid.isin(lid2)]
    sdf.set_index('qseqid', inplace=True, drop=True)
    sdf['sumscore']=sdf.sum(axis=1)
    sdfPOST=sdf[sdf.sumscore==sdf.Cyanobacteriota ]
    sdfPRE=sdf[sdf.sumscore!=sdf.Cyanobacteriota ]

    print('hcat3 cya from terrabac',sdfPOST.shape[0] , sdfPRE.shape[0] )
    #skip cat 2!!!!

def nested_skip():

    """
            CAT0: x v archaea
            CAT1: bac vs eukaryota
    """
    elem ='sskingdoms'
    df=pd.read_csv('gene_age/2025dbres/1kmatches_'+elem+'.csv', sep='\t')

    df=df[df.Bacteria>0] #should be all but qc

    cat0dfPOST=df[df.Archaea==0]
    cat0dfPRE=df[df.Archaea>0]
    filter_gff(cat0dfPRE.qseqid.tolist(),'cat0_commonwArchaea')
    print("cat0 Archaea", cat0dfPOST.shape[0] , cat0dfPRE.shape[0])


    cat1POST=cat0dfPOST[cat0dfPOST.Eukaryota==0] #not present in euk
    cat1PRE=cat0dfPOST[cat0dfPOST.Eukaryota>0]
    filter_gff(cat1PRE.qseqid.tolist(),'cat1_commonwEukaryota')
    print("cat1 Eukaryota", cat1POST.shape[0] , cat1PRE.shape[0])

    lid=cat1POST.qseqid.tolist()
    """
                CAT3:  Bacillota <>   
                Cat4: Actinomycetota <>
                CAT5:  Cyanobacteriota V PSEUDOMONADOTA??
    """
    elem ='sphylums'
    df=pd.read_csv('gene_age/2025dbres/1kmatches_'+elem+'.csv', sep='\t')
    df=df[df.qseqid.isin(lid)]

    cat2POST=df[df.Bacillota==0]
    cat2PRE=df[df.Bacillota>0]
    filter_gff(cat2PRE.qseqid.tolist(),'cat2_commonwFirmicutes')
    print("cat2 Bacillota/Firmicutes", cat2POST.shape[0] , cat2PRE.shape[0])

    cat2POST=cat2POST.loc[:, (cat2POST != 0).any(axis=0)]
    #cat3POST.to_csv('cat2_commonwFirmicutes.tsv',sep='\t')
    print(cat2POST.shape)

    cat3POST=cat2POST[cat2POST.Actinomycetota==0]
    cat3PRE=cat2POST[cat2POST.Actinomycetota>0]
    filter_gff(cat3PRE.qseqid.tolist(),'cat3_commonwActino')

    print("cat3 Actinomycetota", cat3POST.shape[0] , cat3PRE.shape[0])
    cat3POST=cat3POST.loc[:, (cat3POST != 0).any(axis=0)]
    #cat3POST.to_csv('cat3_commonwActinomycetota.tsv',sep='\t')
    print(cat3POST.shape)

    cat3POST.set_index('qseqid', inplace=True, drop=True)
    cat3POST['sumscore']=cat3POST.sum(axis=1)
    cat4POST=cat3POST[cat3POST.sumscore==cat3POST.Cyanobacteriota ]
    cat4PRE=cat3POST[cat3POST.sumscore!=cat3POST.Cyanobacteriota ]

    cat4PRE=cat4PRE.loc[:, (cat4PRE != 0).any(axis=0)]
    cat4PRE.to_csv('cat4_commonwithinActinomycetota.tsv',sep='\t')
    print(cat4PRE.shape)

    cat4POST=cat4POST.loc[:, (cat4POST != 0).any(axis=0)]
    cat4POST.to_csv('cat5_onlyCyano.tsv',sep='\t')
    print(cat4POST.shape)

    filter_gff(cat4PRE.index.tolist(),'cat4_commonWPseudomona')
    filter_gff(cat4POST.index.tolist(),'cat5_onlyCyano')

    print("cat4 random", cat4PRE.shape[0])
    print("cat5 onlyCyanobacteria", cat4POST.shape[0] )

nested_skip()