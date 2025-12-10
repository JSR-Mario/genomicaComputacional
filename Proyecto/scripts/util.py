import pandas as pd

# Cargar datos
df = pd.read_csv('results/virulence_report.tab', sep='\t')
if '#FILE' in df.columns: df.rename(columns={'#FILE': 'FILE'}, inplace=True)
df['Strain'] = df['FILE'].apply(lambda x: str(x).split('/')[-1].replace('.fasta', ''))

# 1. Conteo total de genes únicos por cepa
print("--- Genes de Virulencia por Cepa ---")
counts = df.groupby('Strain')['GENE'].nunique().sort_values(ascending=False)
print(counts)

# 2. Chequeo rápido de marcadores
print("\n--- Presencia de Marcadores Clave ---")
markers = ['eae', 'stx1A', 'stx2A', 'bfpA', 'papA', 'hlyA']
for strain in df['Strain'].unique():
    genes = df[df['Strain'] == strain]['GENE'].unique()
    present = [m for m in markers if any(m in g for g in genes)] # búsqueda laxa
    print(f"{strain}: {present}")
