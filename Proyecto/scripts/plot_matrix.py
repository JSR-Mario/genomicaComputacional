import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('results/virulence_report.tab', sep='\t')

if '#FILE' in df.columns:
    df.rename(columns={'#FILE': 'FILE'}, inplace=True)

df['FILE'] = df['FILE'].apply(lambda x: str(x).split('/')[-1].replace('.fasta', ''))

matrix = pd.crosstab(df['FILE'], df['GENE'])
matrix = (matrix > 0).astype(int)

print(f"Dimensiones originales: {matrix.shape}")

# Eliminamos genes que están presentes en TODAS las cepas (no diferencian nada)
num_strains = matrix.shape[0]
matrix_filtered = matrix.loc[:, matrix.sum(axis=0) < num_strains]

# Eliminamos genes que nadie tiene 
matrix_filtered = matrix_filtered.loc[:, matrix_filtered.sum(axis=0) > 0]

print(f"Dimensiones tras filtrado: {matrix_filtered.shape} (Se eliminaron genes comunes/vacíos)")
# ----------------------------
# Configuración del Gráfico
width = 10 #max(10, matrix_filtered.shape[1] * 0.05)
height = 8 

plt.figure(figsize=(width, height))

try:
    # Usamos clustermap pero ajustamos la fuente
    g = sns.clustermap(matrix_filtered, 
                       metric='jaccard', 
                       method='average', 
                       cmap='Purples', 
                       linewidths=0.5, 
                       linecolor='gray',
                       figsize=(width, height),
                       # dendrogram_ratio=(0.1, 0.2), # Árboles pequeños para dar espacio a la matriz
                       cbar_pos=None) 

    # Ajuste fino de etiquetas
    # Eje X (Genes): Fuente pequeña
    plt.setp(g.ax_heatmap.get_xticklabels(), rotation=90, fontsize=8)
    # Eje Y (Genomas): Fuente grande y horizontal
    plt.setp(g.ax_heatmap.get_yticklabels(), rotation=0, fontsize=12, fontweight='bold')

    # Guardar
    output_file = 'results/heatmap_virulencia_v2.png'
    g.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Gráfico guardado en: {output_file}")

except Exception as e:
    print(f"Error graficando: {e}")
