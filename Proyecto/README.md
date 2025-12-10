## Instrucciones de uso 

Ya teniendo un conda instalado crear un entorno:

```bash
# Crear el entnorno 
conda create -n genomica -c bioconda -c conda-forge abricate ncbi-datasets-cli pandas seaborn matplotlib openpyxl -y

# Activar el entorno
conda activate genomica

# Descargar los genomas usando la herramienta de NCBI 
datasets download genome accession --inputfile accessions.txt --include genome

# Descomprimir el zip 
unzip -o ncbi_dataset.zip

# Mover y renombrar para fácil acceso
cp ncbi_dataset/data/GCF_000005845.2/*.fna data/genomes/K12_Reference.fasta
cp ncbi_dataset/data/GCF_000026545.1/*.fna data/genomes/EPEC_Pathogen.fasta
cp ncbi_dataset/data/GCF_000008865.2/*.fna data/genomes/EHEC_Pathogen.fasta
cp ncbi_dataset/data/GCF_000010485.1/*.fna data/genomes/SE11_Commensal.fasta
cp ncbi_dataset/data/GCF_000006665.1/*.fna data/genomes/EHEC_EDL933.fasta
cp ncbi_dataset/data/GCF_000007445.1/*.fna data/genomes/UPEC_CFT073.fasta
cp ncbi_dataset/data/GCF_000714595.1/*.fna data/genomes/Nissle_Probiotic.fasta
cp ncbi_dataset/data/GCF_000027125.1/*.fna data/genomes/EAEC_042.fasta

# Limpieza
rm -rf ncbi_dataset ncbi_dataset.zip 

# Ejecutar abricate
# --db vfdb: Usar base de datos de factores de virulencia
# --minid 90: Identidad mínima 90% 
# --mincov 80: Cobertura mínima 80%
abricate --db vfdb --minid 90 --mincov 80 data/genomes/*.fasta > results/virulence_report.tab

# Ejecutar los scripts
python3 scripts/plot_matrix.py
python3 scripts/plot_counts.py
python3 scripts/util.py
```
