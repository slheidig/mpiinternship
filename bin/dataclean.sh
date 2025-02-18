#make sure genomes dont contain . " " also ignore og
#are they in one contig?
rm lookup_table.csv
lookup_table="lookup_table.csv"
echo "original_name,new_name,no_contigs" > "$lookup_table"


for elem in genomes/Syn*.fa ;do 
    fname=$(basename "$elem")
    original_name="${fname%.*}"
    new_name=$(echo "$original_name" | sed 's/[. -]/_/g')
    echo $new_name
    no_contigs=0

    touch genomes/${new_name}_rela.fa
    while IFS= read -r line; do
        if [[ "$line" == ">"* ]]; then
            ((no_contigs++))
            line=">"$new_name"_contig_"$no_contigs
        fi
        echo "$line" >> "genomes/${new_name}_rela.fa"
    done < "$elem"
    
    echo "$original_name,$new_name,$no_contigs" >> "$lookup_table"
    echo $new_name "genomes/${new_name}_rela.fa" >> input_genomes_cactus.txt
    echo "genomes/${new_name}_rela.fa" >> "input_genomes_andi.txt"

done
