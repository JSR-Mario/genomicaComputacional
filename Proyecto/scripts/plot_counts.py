import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('results/virulence_report.tab', sep='\t')

if '#FILE' in df.columns:
    df.rename(columns={'#FILE': 'FILE'}, inplace=True)

df['Strain'] = df['FILE'].apply(lambda x: str(x).split('/')[-1].replace('.fasta', ''))

# Agrupamos por Cepa y contamos genes únicos 
counts = df.groupby('Strain')['GENE'].nunique().reset_index()
counts.columns = ['Cepa', 'Num_Genes']

# Ordenar de mayor a menor
counts = counts.sort_values('Num_Genes', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=counts, x='Num_Genes', y='Cepa', hue='Num_Genes', palette='viridis', legend=False)

plt.title('Carga Total de Genes de Virulencia por Cepa', fontsize=14, fontweight='bold')
plt.xlabel('Número de Genes de Virulencia Detectados (VFDB)', fontsize=12)
plt.ylabel('')
plt.grid(axis='x', linestyle='--', alpha=0.7)

for index, value in enumerate(counts['Num_Genes']):
    plt.text(value + 2, index, str(value), va='center', fontsize=10, fontweight='bold')
plt.tight_layout()

output_file = 'results/conteo_genes.png'
plt.savefig(output_file, dpi=300)
print(f"Gráfico de barras guardado en: {output_file}")
