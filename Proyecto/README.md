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
cp ncbi_dataset/data/GCF_*/GCF_*_genomic.fna data/genomes/

# Limpieza
rm -rf ncbi_dataset ncbi_dataset.zip 

# Ejecutar abricate
# --db vfdb: Usar base de datos de factores de virulencia
# --minid 90: Identidad mínima 90% 
# --mincov 80: Cobertura mínima 80%
abricate --db vfdb --minid 90 --mincov 80 data/genomes/*.fasta > results/virulence_report.tab

# Ejecutar el script
python3 scripts/plot_matrix.py
```
