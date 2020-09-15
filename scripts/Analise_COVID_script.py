# Adaptação do notebook Analise_COVID_Plotly.ipynb para script a fim de avaliar diferenças de desempenho

# Pacotes básicos para a análise
import pandas as pd
import numpy as np
import sys
from plotly.subplots import make_subplots

# Fontes de dados
link = 'https://bi.static.es.gov.br/covid19/MICRODADOS.csv' # Web
# link = 'excel/MICRODADOS.csv' # Local

# Regiões de análise
regioes = {'Grande Vitória': ['VILA VELHA', 'VITÓRIA', 'CARIACICA', 'VIANA', 'SERRA'],
           'Vila Velha':['VILA VELHA'],
           'Resto da GV': ['VITÓRIA', 'CARIACICA', 'VIANA', 'SERRA']}

# Leitura dos dados e tratamento
def leitura_e_tratamento(fonte):
    print('Iniciando leitura dos dados')
    try:
        dados = pd.read_csv(fonte, sep = ';', encoding = 'iso8859_15')
    except:
        print('Falha na leitura dos dados')
        sys.exit(1)
    else:
        print('Dados lidos')
        dados.DataNotificacao = dados.DataNotificacao.astype(np.datetime64)
        dados.DataObito = dados.DataObito.astype(np.datetime64)
        return dados

# Extraindo os dados relevantes para a análise
def extracao_dados(dados, *municipios):
    confirmados = dados.query("Classificacao == 'Confirmados'")
    if municipios:
        confirmados = confirmados.query("Municipio == @municipios[0]")

    total_notif = confirmados.groupby('DataNotificacao').count().DataCadastro
    rm_notif = total_notif.rolling(14).mean()
    total_ob = confirmados.groupby('DataObito').count().DataCadastro
    rm_ob = total_ob.rolling(14).mean()

    return total_notif, rm_notif, total_ob, rm_ob

# Figura básica para a análise
def figura_midia(figura, posicao, tipo, total, rm):
    # Definição das características das figuras a partir das entradas
    if tipo == 'mortes':
        legenda = 'Óbitos diários'
        yaxes = 'Pacientes mortos'
    elif tipo == 'casos':
        legenda = 'Notificações diárias'
        yaxes = 'Pacientes infectados'
    else:
        return print('Tipo inválido')
    
    # plotagem da figura dos casos diários
    figura.add_bar(x = total.index, y = total, name = legenda, row = posicao[0], col = posicao[1])
    figura.add_scatter(x = rm.index, y = rm, name = 'Média móvel 14d', row = posicao[0], col = posicao[1])
    figura.update_xaxes(title = 'Data de Notificação')
    figura.update_yaxes(title = yaxes, row = posicao[0], col = posicao[1])
    figura.update_traces(hovertemplate = 'Data: %{x}<br>Casos no dia: %{y}', selector={'name':legenda})
    figura.update_traces(hovertemplate = 'Data: %{x}<br>Média móvel: %{y}', selector={'name':'Média móvel 14d'})

    return figura

# Automatizador do script
def gerar_figuras(dados, regiao, *municipios):
    if municipios:
        total_notif, rm_notif, total_ob, rm_ob = extracao_dados(dados, *municipios)
    else:
        total_notif, rm_notif, total_ob, rm_ob = extracao_dados(dados)
        regiao = 'ES'
    
    figura = make_subplots(rows=2, cols=1, 
                           subplot_titles=('Casos confirmados de COVID-19 - '+regiao,
                                           'Mortes por COVID-19 - '+regiao),
                           shared_xaxes=True)
    figura = figura_midia(figura, [1,1], 'casos', total_notif, rm_notif)
    figura = figura_midia(figura, [2,1], 'mortes', total_ob, rm_ob)
    figura.show()

# Programa a ser executado
dados = leitura_e_tratamento(link)
gerar_figuras(dados, 'ES')
for r in regioes:
    gerar_figuras(dados, r, regioes[r])
