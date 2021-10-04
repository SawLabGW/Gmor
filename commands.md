## Workflow and Commandline Documentation

### Unicycler assembly commands

```
unicycler \
    -1 combined_illumina/combined1.R1.fastq.gz \
    -2 combined_illumina/combined1.R2.fastq.gz \
    -l trimmed/GV4_nanopore.trimmed2.fastq.gz \
    -t 24 \
    -o hybrid_combo1
```

### Anvi'o commands

```
## copy main gbffs over
cp ../anvio/gbffs/*.gbff gbffs/

## download Aurora and Anthocerotibacter

cd gbffs
wget https://sra-download.ncbi.nlm.nih.gov/traces/wgs01/wgs_aux/JA/AX/LT/JAAXLT01/JAAXLT01.1.gbff.gz
gunzip JAAXLT01.1.gbff.gz
mv JAAXLT01.1.gbff AvLV9.gbff

wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/018/389/385/GCA_018389385.1_ASM1838938v1/GCA_018389385.1_ASM1838938v1_genomic.gbff.gz
gunzip GCA_018389385.1_ASM1838938v1_genomic.gbff.gz

## run prokka for Apan

cd ../
mkdir prokka
cd prokka
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/018/389/385/GCA_018389385.1_ASM1838938v1/GCA_018389385.1_ASM1838938v1_genomic.fna.gz
gunzip GCA_018389385.1_ASM1838938v1_genomic.fna.gz
prokka --outdir out --prefix Apan --cpus 4 GCA_018389385.1_ASM1838938v1_genomic.fna

wget https://sra-download.ncbi.nlm.nih.gov/traces/wgs01/wgs_aux/JA/AX/LT/JAAXLT01/JAAXLT01.1.fsa_nt.gz
gunzip *.gz
prokka --outdir AvLV9 --prefix AvLV9 --cpus 4 JAAXLT01.1.fsa_nt

## copy results over
cp out/Apan.gbk ../gbffs/Apan.gbff
cp AvLV9/AvLV9.gbk ../gbffs/AvLV9.gbff

## run anvio commands
for i in `ls *.gbff | sed 's/.gbff//g'`;do anvi-script-process-genbank -i ${i}.gbff -O ${i}; done
for i in `ls *.fa | sed 's/-contigs.fa//g'`;do anvi-gen-contigs-database -f ${i}-contigs.fa -n ${i} --external-gene-calls ${i}-external-gene-calls.txt --ignore-internal-stop-codons -o ${i}.db; done
for i in `ls *.db`;do anvi-run-hmms -T 4 -c ${i}; done
for i in `ls *.db | sed 's/.db//g'`;do
    anvi-import-functions -c ${i}.db -i ${i}-external-functions.txt
done
cd ..
echo -e "name\tcontigs_db_path" > external_db.list
awk '{print $1 "\t" "gbffs/" $1 ".db"}' genomes.list >> external_db.list
anvi-gen-genomes-storage -e external_db.list -o GENOMES.db --gene-caller 'NCBI_PGAP'
anvi-pan-genome -g GENOMES.db -n Gloeo_pan
anvi-compute-genome-similarity --external-genomes external_db.list --program pyANI --output-dir pyANI --num-threads 4 --pan-db Gloeo_pan/Gloeo_pan-PAN.db
anvi-display-pan -p Gloeo_pan/Gloeo_pan-PAN.db -g GENOMES.db
```

### Phylophlan parameters

```
phylophlan -f custom_phylophlan.cfg -i faas --proteome_extension .faa -d phylophlan --diversity medium --fast --nproc 24 -o phylophlan -t a --verbose 2>&1 | tee phylophlan_rerun3.log
```

### IQ-Tree parameters

```
iqtree -s faas_concatenated.aln -m TESTONLY -T 24

iqtree -s faas_concatenated.aln -m LG+F+G4 -T 24 -alrt 1000 -bb 1000 --prefix Gmor
```

### Tree drawing

```
python draw_cyano_tree.py -t Gmor.contree -m id_mapping.txt -s -o Gmor.contree.pdf
```
