#infile=$1
sname=$1

#filter snps
#bcftools view $infile --min-af 0.20:minor -O z -o ${sname}.maf20.vcf.gz
#./sampleSNPs.sh ${sname}.maf20.snp.vcf.gz ${sname}.maf20.sampled50.vcf 0.50
#bgzip ${sname}.maf20.sampled50.vcf
echo filtering done


#run lddecay
#https://github.com/hewm2008/PopLDdecay
popld=/home/sophielh/Downloads/PopLDdecay/bin
 
$popld/PopLDdecay -InVCF ${sname}.maf20.snp.vcf.gz -OutStat LDdecay -OutType 2 -OutType 3 -MaxDist 50 
perl $popld/Plot_OnePop.pl -inFile LDdecay.stat.gz -output ${sname}_Fig
mv LDdecay.stat.gz ${sname}_LDdecay.stat.gz
mv LDdecay.LD.gz ${sname}_LDdecay.LD.gz

