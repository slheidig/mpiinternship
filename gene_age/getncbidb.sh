

aria2c -x 16 https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nr.gz
aria2c -x 16 https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nr.gz.md5


aria2c -x 16 https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdmp.zip
aria2c -x 16 https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdmp.zip.md5


aria2c -x 16 https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz
aria2c -x 16 https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz.md5


md5sum -c nr.gz.md5
md5sum -c prot.accession2taxid.gz.md5
md5sum -c taxdmp.zip.md5
unzip taxdmp.zip
#wget http://github.com/bbuchfink/diamond/releases/download/v2.1.11/diamond-linux64.tar.gz
#tar xzf diamond-linux64.tar.gz

/home/sophielh/Desktop/diamond makedb \
          --in nr.gz \
          --db nr \
          --taxonmap prot.accession2taxid.gz \
          --taxonnodes nodes.dmp \
          --taxonnames names.dmp --log
/home/sophielh/Desktop/diamond blastp \
          -d nr \
          -q /home/sophielh/Desktop/cactus/gene_age/Syn_CC9605_genes.fasta \
          -e 1e-6 -k100 -b4 \
          -f 6 qseqid sseqid qlen slen pident nident evalue staxids sscinames sskingdoms skingdoms sphylums full_sseq \
          -o matches_2025.csv
         #--taxon-exclude 1117\
