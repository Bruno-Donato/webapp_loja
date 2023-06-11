import streamlit as st
import numpy as np
import pandas as pd
import feather
import plotly.express as px

st.set_page_config(page_title="Dashboard loja", layout="wide")

st.header("Dom-Dim Instrumentos Musicais")
st.subheader("DASHBOARD INTERATIVO")
st.write("""
         A Dom-Dim é uma loja fictícia de instrumentos musicais. A criação desse projeto, como portifólio, foi feita a partir de dados reais de uma loja virtual, localizada 
         na região metropolitana de Campinas/SP, fundada em 2016 e que faz vendas para todo o Brasil.\n
         Para essa divulgação os dados sensíveis foram excluídos da análise e, a pedido da empreendedora, os dados analisados foram mascarados de maneira aleatória. Todas as 
         marcas citadas são fictícias.\n
         O registro dos dados, para controle e rastreamento, atingiu maturidade a partir do ano de 2020, e as análises feitas abordam os anos de 2020 até 2022.\n
         Nesse projeto foram utilizadas as bibliotecas ***__PANDAS__*** e ***__NUMPY__*** para análise e tratamento de dados, ***__PLOTLY__*** para visualização de dados e ***__STREAMLIT__***
         para construção e deploy do web app.     
         """)
st.markdown("""---""")

# Carregando dados
coordenadas_cidades = pd.read_feather(r'data/coordenadas_cidades.feather')
coordenadas_estados = pd.read_feather(r'data/coordenadas_estados.feather')
df_app = pd.read_feather(r'data/df_app.feather')

# Definindo funções
def graf_barra(var = None, graf = None):
    df_teste = df_app[var].value_counts().to_frame().head(7).reset_index()
    df_teste.columns = [var, 'contagem']                       
    fig = px.bar(df_teste, y = var, x = 'contagem')
    fig.update_layout(autosize=False, width=500, height=300, yaxis=dict(title=''), yaxis_categoryorder='total ascending')
    return graf.plotly_chart(fig, use_container_width=True)

def graf_barra1(var = None, graf = None, estado = None):
    df_teste = df_app[df_app['estado'] == estado][var].value_counts().to_frame().head(7).reset_index()
    df_teste.columns = [var, 'contagem']            
    fig = px.bar(df_teste, y = var, x = 'contagem')
    fig.update_layout(autosize=False, width=500, height=300, yaxis=dict(title=''), yaxis_categoryorder='total ascending')
    return graf.plotly_chart(fig, use_container_width=True)

def graf_barra2(var = None, graf = None, periodo = None):
    df_teste = df_app[df_app['ano'] == int(periodo)][var].value_counts().to_frame().head(7).reset_index()
    df_teste.columns = [var, 'contagem']            
    fig = px.bar(df_teste, y = var, x = 'contagem')
    fig.update_layout(autosize=False, width=500, height=300, yaxis=dict(title=''), yaxis_categoryorder='total ascending')
    return graf.plotly_chart(fig, use_container_width=True)

def graf_barra3(var = None, graf = None, periodo = None, estado = None):
    df_teste = df_app[(df_app['estado'] == estado) & (df_app['ano'] == int(periodo))][var].value_counts().to_frame().head(7).reset_index()
    df_teste.columns = [var, 'contagem']            
    fig = px.bar(df_teste, y = var, x = 'contagem')
    fig.update_layout(autosize=False, width=500, height=300, yaxis=dict(title=''), yaxis_categoryorder='total ascending')
    return graf.plotly_chart(fig, use_container_width=True)

def linha_df(df = None):
    df_linha = df.groupby(['ano', 'mes'])['instrumento'].value_counts().to_frame()
    df_linha.columns = ['quantidade']
    df_linha = df_linha.reset_index()

    if periodo == 'Todo Período':
        df_linha = df_linha.groupby(['mes'])['quantidade'].sum().to_frame()
    else:
        df_linha = df_linha[df_linha['ano'] == int(periodo)].groupby(['mes'])['quantidade'].sum().to_frame()
    df_linha = df_linha.reset_index()
    return df_linha

def df_linha2(df = None):
    df_linha = df_app.groupby(['estado', 'ano', 'mes'])['instrumento'].value_counts().to_frame()
    df_linha.columns = ['quantidade']
    df_linha = df_linha.reset_index()
    df_linha = df_linha.drop(columns=['instrumento'])
    if periodo == 'Todo Período':
        df_linha = df_linha[(df_linha['estado'] == estado)].groupby(['mes'])['quantidade'].sum().to_frame()
    else:
        df_linha = df_linha[(df_linha['estado'] == estado) & (df_linha['ano'] == int(periodo))].groupby(['mes'])['quantidade'].sum().to_frame()
    df_linha = df_linha.reset_index()
    return df_linha

def graf_linha(df = None):
    fig = px.line(df, x='mes', y='quantidade', title=f'Vendas {estado.upper()}: {periodo}')
    fig.update_layout(autosize=False, width=800, height=350)
    return col1.plotly_chart(fig, use_container_width=False)

# Seleção de período
col1, col2, col3 = st.columns([2, 2, 2])
periodo = col1.selectbox("Selecione o ano", ("Todo Período", "2020", "2021", "2022"))
# Seleção de estado
estado = col2.selectbox("Selecione o estado", ('Todo Brasil', 'sp', 'mg', 'rj', 'pr', 'rs', 'ba', 'sc', 'pe', 'go', 'mt', 'es', 'pb', 
                                               'ce', 'df', 'ms', 'ma', 'ro', 'pa', 'rn', 'se', 'al', 'am', 'pi', 'rr', 'ap', 'to'))

col1, col2, col3 = st.columns([4, 2.3, 1.2])
if periodo == "Todo Período":
    if estado == 'Todo Brasil':
        # Definindo dataframe
        mapa_total = df_app['estado'].value_counts()
        mapa_total = mapa_total.reset_index()
        mapa_total.columns = ['estado', 'vendas']
        mapa_total = pd.merge(mapa_total, coordenadas_estados, on='estado')
        mapa_total['%'] = round((mapa_total['vendas']/mapa_total['vendas'].sum())*100, 2)
        mapa_total['%_1'] = mapa_total['%'].astype('str') + '%'
        # Mapa vendas Braisl/Estados
        fig = px.scatter_mapbox(mapa_total, lat = 'lat_est', lon = 'lon_est', size = '%',
                                zoom = 2.5, mapbox_style = "open-street-map", hover_name='estado',
                                color_continuous_scale="bluered", color='vendas', size_max=50)                   
        fig.update_layout(autosize=True, width=610,height=550)                                       
        col1.plotly_chart(fig)
        # Tabela com porcentagem e total de vendas por estados/cidades
        col2.header('')
        col2.subheader('')
        mapa_total.index = np.arange(1, len(mapa_total) + 1) 
        col2.write(mapa_total[['estado', 'vendas', '%']])
    else:
        df_estado = df_app[df_app['estado'] == estado]
        df_mapa_estado = df_estado['cidade'].value_counts()
        df_mapa_estado = df_mapa_estado.reset_index()
        df_mapa_estado.columns = ['cidade', 'vendas']
        df_mapa_estado = pd.merge(df_mapa_estado, coordenadas_cidades[coordenadas_cidades['estado'] == estado], on='cidade')
        df_mapa_estado['%'] = round((df_mapa_estado['vendas']/df_mapa_estado['vendas'].sum())*100, 2)
        df_mapa_estado['%_1'] = df_mapa_estado['%'].astype('str') + '%'
        # Mapa vendas Brasil/Estados
        fig = px.scatter_mapbox(df_mapa_estado, lat = 'lat', lon = 'lon', 
                                zoom = 5, mapbox_style = "open-street-map", hover_name='cidade',
                                color_continuous_scale="bluered", color='vendas', size_max=20)                   
        fig.update_layout(autosize=True, width=610,height=550)
        col1.plotly_chart(fig)
        # Tabela com porcentagem e total de vendas por estados/cidades
        col2.header('')
        col2.subheader('')
        df_mapa_estado.index = np.arange(1, len(df_mapa_estado) + 1)
        col2.write(df_mapa_estado[['cidade', 'vendas', '%']])
else:
    if estado == 'Todo Brasil':
        # Definindo dataframe
        mapa_ano = df_app[df_app['ano'] == int(periodo)]['estado'].value_counts()
        mapa_ano = mapa_ano.reset_index()
        mapa_ano.columns = ['estado', 'vendas']
        mapa_ano = pd.merge(mapa_ano, coordenadas_estados, on='estado')
        mapa_ano['%'] = round((mapa_ano['vendas']/mapa_ano['vendas'].sum())*100, 2)
        mapa_ano['%_1'] = mapa_ano['%'].astype('str') + '%'
        # Mapa vendas Brasil/Estados
        fig = px.scatter_mapbox(mapa_ano, lat = 'lat_est', lon = 'lon_est', size = '%',
                                zoom = 2.5, mapbox_style = "open-street-map", hover_name='estado',
                                color_continuous_scale="bluered", color='vendas', size_max=50)                    
        fig.update_layout(autosize=True, width=610,height=550)                                        
        col1.plotly_chart(fig)
        # Tabela com porcentagem e total de vendas por estados/cidades
        col2.header('')
        col2.subheader('')
        mapa_ano.index = np.arange(1, len(mapa_ano) + 1)
        col2.write(mapa_ano[['estado', 'vendas', '%']])
    else:
        # Definindo dataframe
        mapa_ano = df_app[(df_app['ano'] == int(periodo)) & (df_app['estado'] == estado)]['cidade'].value_counts()
        mapa_ano = mapa_ano.reset_index()
        mapa_ano.columns = ['cidade', 'vendas']
        mapa_ano = pd.merge(mapa_ano, coordenadas_cidades[coordenadas_cidades['estado'] == estado], on='cidade')
        mapa_ano['%'] = round((mapa_ano['vendas']/mapa_ano['vendas'].sum())*100, 2)
        mapa_ano['%_1'] = mapa_ano['%'].astype('str') + '%'
        # Mapa vendas Brasil/Estados
        fig = px.scatter_mapbox(mapa_ano, lat = 'lat', lon = 'lon',
                                zoom = 5, mapbox_style = "open-street-map", hover_name='cidade',
                                color_continuous_scale="bluered", color='vendas', size_max=50)                   
        fig.update_layout(autosize=True, width=610,height=550)                                        
        col1.plotly_chart(fig)
        # Tabela com porcentagem e total de vendas por estados/cidades
        col2.header('')
        col2.subheader('')
        mapa_ano.index = np.arange(1, len(mapa_ano) + 1) 
        col2.write(mapa_ano[['cidade', 'vendas', '%']])
if periodo == "Todo Período":
    if estado == 'Todo Brasil':
        col3.header('')
        col3.subheader('')
        # KPI#1
        col3.metric(label="Total de vendas", value=len(df_app))
        # KPI#2
        col3.metric(label="Mês com mais vendas", value=df_app['mes'].value_counts(ascending=False).keys()[0])
        # KPI#3
        col3.metric(label="Tempo de entrega", value=str(df_app['tempo_entrega'].mode())[5:12].replace('days', 'dias'))
        # KPI#4
        col3.metric(label="Instrumento mais vendido", value=df_app['instrumento'].value_counts(ascending=False).keys()[0])
        # KPI#5
        col3.metric(label="Marca mais vendida", value=df_app['marca'].value_counts(ascending=False).keys()[0])
    else:
        col3.header('')
        col3.subheader('')
        # KPI#1
        col3.metric(label="Total de vendas", value= len(df_app[df_app['estado'] == estado]))
        # KPI#2
        col3.metric(label="Mês com mais vendas", value=df_app[df_app['estado'] == estado]['mes'].value_counts(ascending=False).keys()[0])
        # KPI#3
        col3.metric(label="Tempo de entrega", value=str(df_app[df_app['estado'] == estado]['tempo_entrega'].mode())[5:12].replace('days', 'dias'))
        # KPI#4
        col3.metric(label="Instrumento mais vendido", value=df_app[df_app['estado'] == estado]['instrumento'].value_counts(ascending=False).keys()[0])
        # KPI#5
        col3.metric(label="Marca mais vendida", value=df_app[df_app['estado'] == estado]['marca'].value_counts(ascending=False).keys()[0])
else:
    if estado == 'Todo Brasil':
        col3.header('')
        col3.subheader('')
        # KPI#1
        col3.metric(label="Total de vendas", value=len(df_app[df_app['ano'] == int(periodo)]))
        # KPI#2
        col3.metric(label="Mês com mais vendas", value=df_app[df_app['ano'] == int(periodo)]['mes'].value_counts(ascending=False).keys()[0])
        # KPI#3
        col3.metric(label="Tempo de entrega", value=str(df_app[df_app['ano'] == int(periodo)]['tempo_entrega'].mode())[5:12].replace('days', 'dias'))
        # KPI#4
        col3.metric(label="Instrumento mais vendido", value=df_app[df_app['ano'] == int(periodo)]['instrumento'].value_counts(ascending=False).keys()[0])
        # KPI#5
        col3.metric(label="Marca mais vendida", value=df_app[df_app['ano'] == int(periodo)]['marca'].value_counts(ascending=False).keys()[0])
    else:
        col3.header('')
        col3.subheader('')    
        # KPI#1
        col3.metric(label="Total de vendas", value=len(df_app[(df_app['ano'] == int(periodo)) & (df_app['estado'] == estado)]))
        # KPI#2
        col3.metric(label="Mês com mais vendas", value=df_app[(df_app['ano'] == int(periodo)) & (df_app['estado'] == estado)]['mes'].value_counts(ascending=False).keys()[0])
        # KPI#3
        col3.metric(label="Tempo de entrega", value=str(df_app[(df_app['ano'] == int(periodo)) & (df_app['estado'] == estado)]['tempo_entrega'].mode())[5:12].replace('days', 'dias'))
        # KPI#4
        col3.metric(label="Instrumento mais vendido", value=df_app[(df_app['ano'] == int(periodo)) & (df_app['estado'] == estado)]['instrumento'].value_counts(ascending=False).keys()[0])
        # KPI#5
        col3.metric(label="Marca mais vendida", value=df_app[(df_app['ano'] == int(periodo)) & (df_app['estado'] == estado)]['marca'].value_counts(ascending=False).keys()[0])

col1, col2 = st.columns([10, 3])
if periodo == "Todo Período":
    if estado == 'Todo Brasil':
        # Definindo dataframe e gráfico de linha
        linha_df(df_app)
        graf_linha(linha_df(df_app))
        col2.header('')
        col2.subheader('')
        graf_barra(var = 'vendedor', graf = col2)
    else:
        # Definindo dataframe e gráfico de linha
        df_linha2(df_app)
        graf_linha(df_linha2(df_app))
        col2.header('')
        col2.subheader('')
        graf_barra1(var = 'vendedor', graf = col2, estado = estado)              
else:
    if estado == 'Todo Brasil':
        # Definindo dataframe e gráfico de linha
        linha_df(df_app)
        graf_linha(linha_df(df_app))
        col2.header('')
        col2.subheader('')
        graf_barra2(var = 'vendedor', graf = col2, periodo = periodo)    
    else:
        # Definindo dataframe e gráfico de linha
        df_linha2(df_app)
        graf_linha(df_linha2(df_app))
        col2.header('')
        col2.subheader('')
        graf_barra3(var = 'vendedor', graf = col2, periodo = periodo, estado = estado)      

graf1, graf2, graf3, graf4, = st.columns([2, 2, 2, 2])                  
if periodo == "Todo Período":
    if estado == 'Todo Brasil':
        graf_barra('instrumento', graf1)
        graf_barra('marca', graf2)
        graf_barra('canal_venda', graf3)
        graf_barra('forma_envio', graf4)           
    else:
        graf_barra1('instrumento', graf = graf1, estado = estado)
        graf_barra1('marca', graf = graf2, estado = estado)
        graf_barra1('canal_venda', graf = graf3, estado = estado)
        graf_barra1('forma_envio', graf = graf4, estado = estado)               
else:
    if estado == 'Todo Brasil':    
        graf_barra2('instrumento', graf = graf1, periodo = periodo)
        graf_barra2('marca', graf = graf2, periodo = periodo)
        graf_barra2('canal_venda', graf = graf3, periodo = periodo)
        graf_barra2('forma_envio', graf = graf4, periodo = periodo)             
    else:      
        graf_barra3('instrumento', graf = graf1, periodo = periodo, estado = estado)
        graf_barra3('marca', graf = graf2, periodo = periodo, estado = estado)
        graf_barra3('canal_venda', graf = graf3, periodo = periodo, estado = estado)
        graf_barra3('forma_envio', graf = graf4, periodo = periodo, estado = estado)