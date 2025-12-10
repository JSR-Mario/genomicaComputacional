import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Cargar datos
df = pd.read_csv('results/virulence_report.tab', sep='\t')

# Normalizar nombre de columna #FILE a FILE
if '#FILE' in df.columns:
    df.rename(columns={'#FILE': 'FILE'}, inplace=True)

# Limpiar nombres de cepas
df['Strain'] = df['FILE'].apply(lambda x: str(x).split('/')[-1].replace('.fasta', ''))

# 2. Calcular conteos únicos
# Agrupamos por Cepa y contamos genes únicos (para evitar duplicados si hay múltiples hits del mismo gen)
counts = df.groupby('Strain')['GENE'].nunique().reset_index()
counts.columns = ['Cepa', 'Num_Genes']

# Ordenar de mayor a menor para que el gráfico se vea limpio
counts = counts.sort_values('Num_Genes', ascending=False)

# 3. Generar Gráfico de Barras
plt.figure(figsize=(10, 6))

# Usamos una paleta de colores degradada (Rojos para muchos genes, Azules para pocos)
sns.barplot(data=counts, x='Num_Genes', y='Cepa', hue='Num_Genes', palette='viridis', legend=False)

# 4. Estética
plt.title('Carga Total de Genes de Virulencia por Cepa', fontsize=14, fontweight='bold')
plt.xlabel('Número de Genes de Virulencia Detectados (VFDB)', fontsize=12)
plt.ylabel('')
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Añadir el número al final de cada barra para precisión
for index, value in enumerate(counts['Num_Genes']):
    plt.text(value + 2, index, str(value), va='center', fontsize=10, fontweight='bold')

# Ajustar márgenes
plt.tight_layout()

# 5. Guardar
output_file = 'results/conteo_genes.png'
plt.savefig(output_file, dpi=300)
print(f"Gráfico de barras guardado en: {output_file}")
