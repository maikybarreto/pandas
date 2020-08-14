# %%
# Importações
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# troca do tema do plot
import seaborn
seaborn.set()

# %%
# Leitura dos arquivos
inv = pd.read_excel('excel/InventarioHUCAM.xls', skiprows=5)
osjan = pd.read_excel('excel/OSjan2020.xls', skiprows=5)
osfev = pd.read_excel('excel/OSfev2020.xls', skiprows=5)
osmar = pd.read_excel('excel/OSmar2020.xls', skiprows=5)

# %%
# concatenação dos arquivos de OS
ostrim = pd.concat([osjan, osfev, osmar])

# %%
# Filtrando as informações de interesse de cada dataframe
ostrimf = ostrim.loc[:,['Núm. O.S.','Classe','Abertura',
'Encerramento','N. Série', 'Patrimônio']]
invf = inv.loc[:,['Patrimônio','Tipo Equipamento',
'Equipamento Crítico']]

# %%
# merge entre o inventário e as OS
df = pd.merge(ostrimf, invf, on='Patrimônio')

# %%
# Formatando as colunas
df.Abertura = df.Abertura.astype(np.datetime64)
df.Encerramento = df.Encerramento.astype(np.datetime64)

# %%
# Separando as classes de OS
dfMC = df[df['Classe']=='Manutenção Corretiva']
dfMP = df[df['Classe']=='Manutenção Preventiva']

# %%
# Contabilizando quantidade por mês
mc_jan = dfMC['Encerramento']<'2020-02'
mc_mar = dfMC['Encerramento']>'2020-03'
mc_fev = (dfMC['Encerramento']>'2020-02')&(dfMC['Encerramento']<'2020-03') 

# %%
# Mostrando essa contagem em gráfico
plt.bar(['Jan', 'Fev', 'Mar'], [mc_jan.sum(),mc_fev.sum(),mc_mar.sum()])
plt.title('MC por mês - 1º Trimestre')
plt.ylabel('Quantidade de OS')
plt.show()
# %%