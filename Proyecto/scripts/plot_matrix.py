import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Cargar y limpiar datos
df = pd.read_csv('results/virulence_report.tab', sep='\t')

# Arreglo del nombre de columna #FILE
if '#FILE' in df.columns:
    df.rename(columns={'#FILE': 'FILE'}, inplace=True)

df['FILE'] = df['FILE'].apply(lambda x: str(x).split('/')[-1].replace('.fasta', ''))

# 2. Crear Matriz
matrix = pd.crosstab(df['FILE'], df['GENE'])
matrix = (matrix > 0).astype(int)

print(f"Dimensiones originales: {matrix.shape}")

# --- FILTRADO ESTRATÉGICO ---
# Eliminamos genes que están presentes en TODAS las cepas (no diferencian nada)
# Si matrix.shape[0] es 4, borramos columnas que sumen 4.
num_strains = matrix.shape[0]
matrix_filtered = matrix.loc[:, matrix.sum(axis=0) < num_strains]

# Eliminamos genes que nadie tiene (por si acaso)
matrix_filtered = matrix_filtered.loc[:, matrix_filtered.sum(axis=0) > 0]

print(f"Dimensiones tras filtrado: {matrix_filtered.shape} (Se eliminaron genes comunes/vacíos)")
# ----------------------------

# 3. Configuración del Gráfico
# Calculamos un ancho dinámico: 0.2 pulgadas por cada gen (para que no se aprieten)
# Mínimo 10 pulgadas, Máximo 50.
width = max(10, matrix_filtered.shape[1] * 0.2)
height = 8 

plt.figure(figsize=(width, height))

try:
    # Usamos clustermap pero ajustamos la fuente
    g = sns.clustermap(matrix_filtered, 
                       metric='jaccard', 
                       method='average', 
                       cmap='Blues', 
                       linewidths=0.5, 
                       linecolor='gray',
                       figsize=(width, height),
                       dendrogram_ratio=(0.1, 0.2), # Árboles pequeños para dar espacio a la matriz
                       cbar_pos=None) # Quitamos la barra de color (es binario, no aporta)

    # Ajuste fino de etiquetas
    # Eje X (Genes): Fuente pequeña
    plt.setp(g.ax_heatmap.get_xticklabels(), rotation=90, fontsize=8)
    # Eje Y (Genomas): Fuente grande y horizontal
    plt.setp(g.ax_heatmap.get_yticklabels(), rotation=0, fontsize=12, fontweight='bold')

    # Guardar
    output_file = 'results/heatmap_virulencia_v2.png'
    g.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Gráfico optimizado guardado en: {output_file}")

except Exception as e:
    print(f"Error graficando: {e}")
