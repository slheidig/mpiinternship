#infile=$1
sname=$1


echo prep files

#no r prefilter bc i dont have this diversity

gunzip $sname.snp.vcf.gz
bgzip $sname.snp.vcf 
bcftools index $sname.snp.vcf.gz

echo indexed file 

bcftools view $sname.snp.vcf.gz \
  --apply-filters .,PASS \
  --min-alleles 2 --max-alleles 2 |
bcftools view \
  --min-ac 1:minor \
  --genotype ^miss \
  -O z -o $sname.inselection.vcf.gz

echo filered file
#for eigensoft, chromosom has to be a number, but not 0
bcftools annotate --rename-chrs relabelchrom.txt -o $sname.selection.vcf.gz -O z $sname.inselection.vcf.gz 
echot reannotated file

echo "---------------------------------------------------------------"
echo from vcf to plink
echo "---------------------------------------------------------------"
~/Downloads/plink2 --vcf $sname.selection.vcf.gz --make-bed --out $sname.selection

echo "---------------------------------------------------------------"
echo run plink to get independent snps
echo "---------------------------------------------------------------"

#window to scan 30kb
#bad-lb bc <50 founders
#set ids bc non-unique id error

#pop1 has 6 members
    #max r2 at 30kb is 0.3
    #36550/40684 variants removed.
~/Downloads/plink2 --bfile $sname.selection --indep-pairwise 30 6 0.3 --bad-ld --set-all-var-ids @:#[synp1]

#pop2 has 10 members
    #max r2 at 30kb is 0.22
#~/Downloads/plink2 --bfile $sname.selection --indep-pairwise 30 10 0.22 --bad-ld --set-all-var-ids @:#[synp2]


echo "---------------------------------------------------------------"
echo run plink to export  independent snps
echo "---------------------------------------------------------------"
~/Downloads/plink2 --bfile $sname.selection --extract plink2.prune.in --make-bed --out $sname.selection.pruned --set-all-var-ids @:#[synp1]

#~/Downloads/plink2 --bfile $sname.selection --extract plink2.prune.in --make-bed --out $sname.selection.pruned --set-all-var-ids @:#[synp2]

echo "---------------------------------------------------------------"
echo run smartPCA
echo "---------------------------------------------------------------"


mkdir -p ${sname}_smartPCA
awk '{print $1,$2,$3,$4,$5,1}' $sname.selection.pruned.fam > $sname.PCA.fam

smartpca -i $sname.selection.pruned.bed \
         -a $sname.selection.pruned.bim \
         -b $sname.PCA.fam \
         -o ${sname}_smartPCA/$sname.selection.pruned \
         -e ${sname}_smartPCA/$sname.selection.pruned.eval \
         -p ${sname}_smartPCA/$sname.selection.pruned \
         -l ${sname}_smartPCA/$sname.selection.pruned.log

echo "---------------------------------------------------------------"
echo vis in R
echo "---------------------------------------------------------------"
Rscript smartpca_vis.R $sname 6
echo "---------------------------------------------------------------"
echo "check if n populations are likely"
echo "---------------------------------------------------------------"

echo Test panmictic population or sub-populations  > ${sname}_admix.log
for K in 1 2 3; do 
  echo "Running for K=$K..." >> ${sname}_admix.log
  ~/Downloads/admixture_linux-1.3.0/dist/admixture_linux-1.3.0/admixture $sname.selection.pruned.bed $K >> ${sname}_admix.log;
  done


echo "K,Loglikelihood" > ${sname}_admix_summary.csv
while read -r line; do
  if [[ "$line" =~ ^Running\ for\ K=([0-9]+) ]]; then
    K_value="${BASH_REMATCH[1]}"
  fi
  if [[ "$line" =~ ^Loglikelihood:\ (-?[0-9]+\.[0-9]+) ]]; then
    loglik_value="${BASH_REMATCH[1]}"
    echo "$K_value,$loglik_value" >>  ${sname}_admix_summary.csv
  fi
done < ${sname}_admix.log

echo "---------------------------------------------------------------"
echo vis in R if K=1 not most likely
echo "---------------------------------------------------------------"

