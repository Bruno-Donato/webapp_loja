# CONSERTAR METRICAS - VER METODO SORT

import streamlit as st
import numpy as np
import pandas as pd
import feather
import plotly.express as px

st.set_page_config(
    page_title="Dashboard loja",
    layout="wide",
)

st.header("""
          Dom-Dim Instrumentos Musicais
          """)

st.subheader("""
             DASHBOARD INTERATIVO
             """)

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


# Seleção de período
col1, col2, col3 = st.columns([2, 2, 2])
option = col1.selectbox(
        "Selecione o ano",
        ("Todo Período", "2020", "2021", "2022"))

# Seleção de estado
option2 = col2.selectbox(
    "Selecione o estado", 
    ('Todo Brasil', 'sp', 'mg', 'rj', 'pr', 'rs', 'ba', 'sc', 
     'pe', 'go', 'mt', 'es', 'pb', 'ce', 'df', 'ms', 'ma', 'ro', 
     'pa', 'rn', 'se', 'al', 'am', 'pi', 'rr', 'ap', 'to'))


# tab1, tab2 = st.tabs(['Visão Geral', 'Produtos'])

# with tab1:

col1, col2, col3 = st.columns([4, 2.3, 1.2])

if option == "Todo Período":
    if option2 == 'Todo Brasil':
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
        df_estado = df_app[df_app['estado'] == option2]
        df_mapa_estado = df_estado['cidade'].value_counts()
        df_mapa_estado = df_mapa_estado.reset_index()
        df_mapa_estado.columns = ['cidade', 'vendas']
        df_mapa_estado = pd.merge(df_mapa_estado, coordenadas_cidades[coordenadas_cidades['estado'] == option2], on='cidade')
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
    if option2 == 'Todo Brasil':
        # Definindo dataframe
        mapa_ano = df_app[df_app['ano'] == int(option)]['estado'].value_counts()
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
        mapa_ano = df_app[(df_app['ano'] == int(option)) & (df_app['estado'] == option2)]['cidade'].value_counts()
        mapa_ano = mapa_ano.reset_index()
        mapa_ano.columns = ['cidade', 'vendas']
        mapa_ano = pd.merge(mapa_ano, coordenadas_cidades[coordenadas_cidades['estado'] == option2], on='cidade')
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
    

# kpi1, kpi2, kpi3, kpi4, kpi5 = col3.columns(1)

if option == "Todo Período":
    if option2 == 'Todo Brasil':
        col3.header('')
        col3.subheader('')
        # KPI#1
        col3.metric(
            label="Total de vendas",
            value=df_app['estado'].value_counts().sum()
        )
        
        # KPI#2
        col3.metric(
            label="Mês com mais vendas",
            value=df_app['mes'].value_counts().keys()[0]
        )
        
        # KPI#3
        col3.metric(
            label="Tempo de entrega",
            value=str(df_app['tempo_entrega'].mode())[5:12].replace('days', 'dias')
        )
        
        # KPI#4
        col3.metric(
            label="Instrumento mais vendido",
            value=df_app['instrumento'].value_counts().keys()[0]
        )
        
        # KPI#5
        col3.metric(
            label="Marca mais vendida",
            value=df_app['marca'].value_counts().keys()[0]
        )
    else:
        col3.header('')
        col3.subheader('')
        
        # KPI#1
        col3.metric(
            label="Total de vendas",
            value=df_app[df_app['estado'] == option2]['estado'].value_counts().sum()
        )

        # KPI#2
        col3.metric(
            label="Mês com mais vendas",
            value=df_app[df_app['estado'] == option2]['mes'].value_counts().keys()[0]
        )
        
        # KPI#3
        col3.metric(
            label="Tempo de entrega",
            value=str(df_app[df_app['estado'] == option2]['tempo_entrega'].mode())[5:12].replace('days', 'dias')
        )

        # KPI#4
        col3.metric(
            label="Instrumento mais vendido",
            value=df_app[df_app['estado'] == option2]['instrumento'].value_counts().keys()[0]
        )

        # KPI#5
        col3.metric(
            label="Marca mais vendida",
            value=df_app[df_app['estado'] == option2]['marca'].value_counts().keys()[0]
        )
else:
    if option2 == 'Todo Brasil':
        col3.header('')
        col3.subheader('')
        
        # KPI#1
        col3.metric(
            label="Total de vendas",
            value=df_app[df_app['ano'] == int(option)]['estado'].value_counts().sum()
        )
        
        # KPI#2
        col3.metric(
            label="Mês com mais vendas",
            value=df_app[df_app['ano'] == int(option)]['mes'].value_counts().keys()[0]
        )

        # KPI#3
        col3.metric(
            label="Tempo de entrega",
            value=str(df_app[df_app['ano'] == int(option)]['tempo_entrega'].mode())[5:12].replace('days', 'dias')
        )

        # KPI#4
        col3.metric(
            label="Instrumento mais vendido",
            value=df_app[df_app['ano'] == int(option)]['instrumento'].value_counts().keys()[0]
        )

        # KPI#5
        col3.metric(
            label="Marca mais vendida",
            value=df_app[df_app['ano'] == int(option)]['marca'].value_counts().keys()[0]
        )
    else:
        col3.header('')
        col3.subheader('')
        
        # KPI#1
        col3.metric(
            label="Total de vendas",
            value=df_app[(df_app['ano'] == int(option)) & (df_app['estado'] == option2)]['estado'].value_counts().sum()
        )
        
        # KPI#2
        col3.metric(
            label="Mês com mais vendas",
            value=df_app[(df_app['ano'] == int(option)) & (df_app['estado'] == option2)]['mes'].value_counts().keys()[0]
        )

        # KPI#3
        col3.metric(
            label="Tempo de entrega",
            value=str(df_app[(df_app['ano'] == int(option)) & (df_app['estado'] == option2)]['tempo_entrega'].mode())[5:12].replace('days', 'dias')
        )

        # KPI#4
        col3.metric(
            label="Instrumento mais vendido",
            value=df_app[(df_app['ano'] == int(option)) & (df_app['estado'] == option2)]['instrumento'].value_counts().keys()[0]
        )

        # KPI#5
        col3.metric(
            label="Marca mais vendida",
            value=df_app[(df_app['ano'] == int(option)) & (df_app['estado'] == option2)]['marca'].value_counts().keys()[0]
        )

# with tab2: PARA MUDAR CONFIGURAÇÃO

col1, col2 = st.columns([10, 3])

if option == "Todo Período":
    if option2 == 'Todo Brasil':
        # Definindo dataframe
        df_linha = df_app.groupby(['ano', 'mes'])['instrumento'].value_counts().to_frame()
        df_linha.columns = ['quantidade']
        df_linha = df_linha.reset_index()
        df_linha = df_linha.groupby(['mes'])['quantidade'].sum().to_frame()
        df_linha = df_linha.reset_index()

        # Grafico linhas vendas
        fig = px.line(df_linha, x='mes', y='quantidade', title=f'Vendas {option2}: {option}')
        
        fig.update_layout(autosize=False, 
                            width=800,
                            height=350)
        
        col1.plotly_chart(fig, use_container_width=False)
        
        col2.header('')
        col2.subheader('')
        
        df_barra1 = df_app.groupby(['estado', 'ano', 'mes'])['vendedor'].value_counts().to_frame()
        df_barra1.columns = ['quantidade']
        df_barra1 = df_barra1.reset_index()
        df_barra1 = df_barra1['vendedor'].value_counts().to_frame()
        df_barra1 = df_barra1.reset_index()
        df_barra1.columns = ['vendedor', 'quantidade']
        df_barra1 = df_barra1.head(7).sort_values(by='quantidade')

        # Gráfico barras caracteristicas produtos #1
        fig2 = px.bar(df_barra1, x='quantidade', y='vendedor')
        
        fig2.update_layout(autosize=False,
                           width=500,
                           height=300)
        
        col2.plotly_chart(fig2, use_container_width=True)
        
        
        
    else:
        # Definindo dataframe
        df_linha = df_app.groupby(['estado', 'ano', 'mes'])['instrumento'].value_counts().to_frame()
        df_linha.columns = ['quantidade']
        df_linha = df_linha.reset_index()
        df_linha = df_linha.drop(columns=['instrumento'])
        df_linha = df_linha[(df_linha['estado'] == option2)].groupby(['mes'])['quantidade'].sum().to_frame()
        df_linha = df_linha.reset_index()

        # Gráfico linhas vendas
        fig = px.line(df_linha, x='mes', y='quantidade', title=f'Vendas {str(option2).upper()}: {option}')
        
        fig.update_layout(autosize=False,
                            width=800,
                            height=350)
        
        col1.plotly_chart(fig, use_container_width=False)

        col2.header('')
        col2.subheader('')
        
        df_barra1 = df_app.groupby(['estado', 'ano', 'mes'])['vendedor'].value_counts().to_frame()
        df_barra1.columns = ['quantidade']
        df_barra1 = df_barra1.reset_index()
        df_barra1 = df_barra1[(df_barra1['estado'] == option2)]['vendedor'].value_counts().to_frame()
        df_barra1 = df_barra1.reset_index()
        df_barra1.columns = ['vendedor', 'quantidade']
        df_barra1 = df_barra1.head(7).sort_values(by='quantidade')
        
        # Gráfico barras caracteristicas produtos #1
        fig2 = px.bar(df_barra1, x='quantidade', y='vendedor')

        fig2.update_layout(autosize=False,
                            width=500,
                            height=300)
        
        col2.plotly_chart(fig2, use_container_width=True)
        
        
                               
else:
    if option2 == 'Todo Brasil':
        # Definindo dataframe
        df_linha = df_app.groupby(['ano', 'mes'])['instrumento'].value_counts().to_frame()
        df_linha.columns = ['quantidade']
        df_linha = df_linha.reset_index()
        df_linha = df_linha[df_linha['ano'] == int(option)].groupby(['mes'])['quantidade'].sum().to_frame()
        df_linha = df_linha.reset_index()

        # Gráfico linha vendas
        fig = px.line(df_linha, x='mes', y='quantidade', title=f'Vendas {str(option2).upper()}: {option}')

        fig.update_layout(autosize=False, 
                            width=800,
                            height=350)
        
        col1.plotly_chart(fig, use_container_width=False)

        col2.header('')
        col2.subheader('')
        
        df_barra1 = df_app.groupby(['estado', 'ano', 'mes'])['vendedor'].value_counts().to_frame()
        df_barra1.columns = ['quantidade']
        df_barra1 = df_barra1.reset_index()
        df_barra1 = df_barra1[df_barra1['ano'] == int(option)]['vendedor'].value_counts().to_frame()
        df_barra1 = df_barra1.reset_index()
        df_barra1.columns = ['vendedor', 'quantidade']
        df_barra1 = df_barra1.head(7).sort_values(by='quantidade')
        
        # Gráfico barras caracteristicas produtos #1
        fig2 = px.bar(df_barra1, x='quantidade', y='vendedor')

        fig2.update_layout(autosize=False,
                           width=500,
                           height=300)
        
        col2.plotly_chart(fig2, use_container_width=True)
        
        
           
    else:
        # Definindo dataframe
        df_linha = df_app.groupby(['estado', 'ano', 'mes'])['instrumento'].value_counts().to_frame()
        df_linha.columns = ['quantidade']
        df_linha = df_linha.reset_index()
        df_linha = df_linha.drop(columns=['instrumento'])
        df_linha = df_linha[(df_linha['estado'] == option2) & (df_linha['ano'] == int(option))].groupby(['mes'])['quantidade'].sum().to_frame()
        df_linha = df_linha.reset_index()

        # Gráfico linha vendas
        fig = px.line(df_linha, x='mes', y='quantidade', title=f'Vendas {str(option2).upper()}: {option}')

        fig.update_layout(autosize=False, 
                            width=800,
                            height=350)
        
        col1.plotly_chart(fig, use_container_width=False)

        col2.header('')
        col2.subheader('')
        
        df_barra1 = df_app.groupby(['estado', 'ano', 'mes'])['vendedor'].value_counts().to_frame()
        df_barra1.columns = ['quantidade']
        df_barra1 = df_barra1.reset_index()
        df_barra1 = df_barra1[(df_barra1['estado'] == option2) & (df_barra1['ano'] == int(option))]['vendedor'].value_counts().to_frame()
        df_barra1 = df_barra1.reset_index()
        df_barra1.columns = ['vendedor', 'quantidade']
        df_barra1 = df_barra1.head(7).sort_values(by='quantidade')
        
        # Gráfico barras caracteristicas produtos #1
        fig2 = px.bar(df_barra1, x='quantidade', y='vendedor')

        fig2.update_layout(autosize=False,
                           width=500,
                           height=300)
        
        col2.plotly_chart(fig2, use_container_width=True)
        
        
        

graf1, graf2, graf3, graf4, = st.columns([2, 2, 2, 2])                  
if option == "Todo Período":
    if option2 == 'Todo Brasil':
        # Definindo dataframe            
        df_barra1 = df_app.groupby(['estado', 'ano', 'mes'])['instrumento'].value_counts().to_frame()
        df_barra1.columns = ['quantidade']
        df_barra1 = df_barra1.reset_index()
        df_barra1 = df_barra1['instrumento'].value_counts().to_frame()
        df_barra1 = df_barra1.reset_index()
        df_barra1.columns = ['instrumento', 'quantidade']
        df_barra1 = df_barra1.head(7).sort_values(by='quantidade')

        # Gráfico barras caracteristicas produtos #1
        fig = px.bar(df_barra1, x='quantidade', y='instrumento')
        
        fig.update_layout(autosize=False,
                            width=500,
                            height=300)
        
        graf1.plotly_chart(fig, use_container_width=True)
        
        # Definindo dataframe
        df_barra2 = df_app.groupby(['estado', 'ano', 'mes'])['marca'].value_counts().to_frame()
        df_barra2.columns = ['quantidade']
        df_barra2 = df_barra2.reset_index()
        df_barra2 = df_barra2['marca'].value_counts().to_frame()
        df_barra2 = df_barra2.reset_index()
        df_barra2.columns = ['marca', 'quantidade']
        df_barra2 = df_barra2.head(7).sort_values(by='quantidade')

        # Gráfico barras caracteristicas produtos #2
        fig2 = px.bar(df_barra2, x='quantidade', y='marca')

        fig2.update_layout(autosize=False,
                            width=500,
                            height=300)
        
        graf2.plotly_chart(fig2, use_container_width=True)

        # Definindo dataframe
        df_barra3 = df_app.groupby(['estado', 'ano', 'mes'])['canal_venda'].value_counts().to_frame()
        df_barra3.columns = ['quantidade']
        df_barra3 = df_barra3.reset_index()
        df_barra3 = df_barra3['canal_venda'].value_counts().to_frame()
        df_barra3 = df_barra3.reset_index()
        df_barra3.columns = ['canal de venda', 'quantidade']
        df_barra3 = df_barra3.head(7).sort_values(by='quantidade')

        # Gráfico barras caracteristicas produtos #3
        fig3 = px.bar(df_barra3, x='quantidade', y='canal de venda')

        fig3.update_layout(autosize=False,
                            width=500,
                            height=300)
        
        graf3.plotly_chart(fig3, use_container_width=True)

        # Definindo dataframe
        df_barra4 = df_app.groupby(['estado', 'ano', 'mes'])['forma_envio'].value_counts().to_frame()
        df_barra4.columns = ['quantidade']
        df_barra4 = df_barra4.reset_index()
        df_barra4 = df_barra4['forma_envio'].value_counts().to_frame()
        df_barra4 = df_barra4.reset_index()
        df_barra4.columns = ['forma de envio', 'quantidade']
        df_barra4 = df_barra4.head(7).sort_values(by='quantidade')
        
        # Gráfico barras caracteristicas produtos #4
        fig4 = px.bar(df_barra4, x='quantidade', y='forma de envio')

        fig4.update_layout(autosize=False,
                            width=500,
                            height=300)
        
        graf4.plotly_chart(fig4, use_container_width=True)          
    else:
        # Definindo dataframe   
        df_barra1 = df_app.groupby(['estado', 'ano', 'mes'])['instrumento'].value_counts().to_frame()
        df_barra1.columns = ['quantidade']
        df_barra1 = df_barra1.reset_index()
        df_barra1 = df_barra1[df_barra1['estado'] == option2]['instrumento'].value_counts().to_frame()
        df_barra1 = df_barra1.reset_index()
        df_barra1.columns = ['instrumento', 'quantidade']
        df_barra1 = df_barra1.head(7).sort_values(by='quantidade')
        
        # Gráfico barras caracteristicas produtos #1
        fig = px.bar(df_barra1, x='quantidade', y='instrumento')

        fig.update_layout(autosize=False,
                            width=500,
                            height=300)
        
        graf1.plotly_chart(fig, use_container_width=True)
        
        # Definindo dataframe
        df_barra2 = df_app.groupby(['estado', 'ano', 'mes'])['marca'].value_counts().to_frame()
        df_barra2.columns = ['quantidade']
        df_barra2 = df_barra2.reset_index()
        df_barra2 = df_barra2[df_barra2['estado'] == option2]['marca'].value_counts().to_frame()
        df_barra2 = df_barra2.reset_index()
        df_barra2.columns = ['marca', 'quantidade']
        df_barra2 = df_barra2.head(7).sort_values(by='quantidade')
        
        # Gráfico barras caracteristicas produtos #2
        fig2 = px.bar(df_barra2, x='quantidade', y='marca')

        fig2.update_layout(autosize=False,
                            width=500,
                            height=300)
        
        graf2.plotly_chart(fig2, use_container_width=True)

        # Definindo dataframe
        df_barra3 = df_app.groupby(['estado', 'ano', 'mes'])['canal_venda'].value_counts().to_frame()
        df_barra3.columns = ['quantidade']
        df_barra3 = df_barra3.reset_index()
        df_barra3 = df_barra3[df_barra3['estado'] == option2]['canal_venda'].value_counts().to_frame()
        df_barra3 = df_barra3.reset_index()
        df_barra3.columns = ['canal de venda', 'quantidade']
        df_barra3 = df_barra3.head(7).sort_values(by='quantidade')
        
        # Gráfico barras caracteristicas produtos #3
        fig3 = px.bar(df_barra3, x='quantidade', y='canal de venda')

        fig3.update_layout(autosize=False,
                            width=500,
                            height=300)
        
        graf3.plotly_chart(fig3, use_container_width=True)
        
        # Definindo dataframe
        df_barra4 = df_app.groupby(['estado', 'ano', 'mes'])['forma_envio'].value_counts().to_frame()
        df_barra4.columns = ['quantidade']
        df_barra4 = df_barra4.reset_index()
        df_barra4 = df_barra4[df_barra4['estado'] == option2]['forma_envio'].value_counts().to_frame()
        df_barra4 = df_barra4.reset_index()
        df_barra4.columns = ['forma de envio', 'quantidade']
        df_barra4 = df_barra4.head(7).sort_values(by='quantidade')
        
        # Gráfico barras caracteristicas produtos #4
        fig4 = px.bar(df_barra4, x='quantidade', y='forma de envio')

        fig4.update_layout(autosize=False,
                            width=500,
                            height=300)
        
        graf4.plotly_chart(fig4, use_container_width=True)            
else:
    if option2 == 'Todo Brasil':
        # Definindo dataframe           
        df_barra1 = df_app.groupby(['estado', 'ano', 'mes'])['instrumento'].value_counts().to_frame()
        df_barra1.columns = ['quantidade']
        df_barra1 = df_barra1.reset_index()
        df_barra1 = df_barra1[df_barra1['ano'] == int(option)]['instrumento'].value_counts().to_frame()
        df_barra1 = df_barra1.reset_index()
        df_barra1.columns = ['instrumento', 'quantidade']
        df_barra1 = df_barra1.head(7).sort_values(by='quantidade')
        
        # Gráfico barras caracteristicas produtos #1
        fig = px.bar(df_barra1, x='quantidade', y='instrumento')

        fig.update_layout(autosize=False,
                            width=500,
                            height=300)
        
        graf1.plotly_chart(fig, use_container_width=True)
        
        # Definindo dataframe
        df_barra2 = df_app.groupby(['estado', 'ano', 'mes'])['marca'].value_counts().to_frame()
        df_barra2.columns = ['quantidade']
        df_barra2 = df_barra2.reset_index()
        df_barra2 = df_barra2[df_barra2['ano'] == int(option)]['marca'].value_counts().to_frame()
        df_barra2 = df_barra2.reset_index()
        df_barra2.columns = ['marca', 'quantidade']
        df_barra2 = df_barra2.head(7).sort_values(by='quantidade')
        
        # Gráfico barras caracteristicas produtos #2
        fig2 = px.bar(df_barra2, x='quantidade', y='marca')

        fig2.update_layout(autosize=False,
                            width=500,
                            height=300)
        
        graf2.plotly_chart(fig2, use_container_width=True)

        # Definindo dataframe
        df_barra3 = df_app.groupby(['estado', 'ano', 'mes'])['canal_venda'].value_counts().to_frame()
        df_barra3.columns = ['quantidade']
        df_barra3 = df_barra3.reset_index()
        df_barra3 = df_barra3[df_barra3['ano'] == int(option)]['canal_venda'].value_counts().to_frame()
        df_barra3 = df_barra3.reset_index()
        df_barra3.columns = ['canal de venda', 'quantidade']
        df_barra3 = df_barra3.head(7).sort_values(by='quantidade')
        
        # Gráfico barras caracteristicas produtos #3
        fig3 = px.bar(df_barra3, x='quantidade', y='canal de venda')

        fig3.update_layout(autosize=False,
                            width=500,
                            height=300)
        
        graf3.plotly_chart(fig3, use_container_width=True)
        
        # Definindo dataframe
        df_barra4 = df_app.groupby(['estado', 'ano', 'mes'])['forma_envio'].value_counts().to_frame()
        df_barra4.columns = ['quantidade']
        df_barra4 = df_barra4.reset_index()
        df_barra4 = df_barra4[df_barra4['ano'] == int(option)]['forma_envio'].value_counts().to_frame()
        df_barra4 = df_barra4.reset_index()
        df_barra4.columns = ['forma de envio', 'quantidade']
        df_barra4 = df_barra4.head(7).sort_values(by='quantidade')
        
        # Gráfico barras caracteristicas produtos #4
        fig4 = px.bar(df_barra4, x='quantidade', y='forma de envio')

        fig4.update_layout(autosize=False,
                            width=500,
                            height=300) 
        
        graf4.plotly_chart(fig4, use_container_width=True)           
    else:
        # Definindo dataframe   
        df_barra1 = df_app.groupby(['estado', 'ano', 'mes'])['instrumento'].value_counts().to_frame()
        df_barra1.columns = ['quantidade']
        df_barra1 = df_barra1.reset_index()
        df_barra1 = df_barra1[(df_barra1['estado'] == option2) & (df_barra1['ano'] == int(option))]['instrumento'].value_counts().to_frame()
        df_barra1 = df_barra1.reset_index()
        df_barra1.columns = ['instrumento', 'quantidade']
        df_barra1 = df_barra1.head(7).sort_values(by='quantidade')
        
        # Gráfico barras caracteristicas produtos #1
        fig = px.bar(df_barra1, x='quantidade', y='instrumento')

        fig.update_layout(autosize=False,
                            width=500,
                            height=300)
        
        graf1.plotly_chart(fig, use_container_width=True)
        
        # Definindo dataframe
        df_barra2 = df_app.groupby(['estado', 'ano', 'mes'])['marca'].value_counts().to_frame()
        df_barra2.columns = ['quantidade']
        df_barra2 = df_barra2.reset_index()
        df_barra2 = df_barra2[(df_barra2['estado'] == option2) & (df_barra2['ano'] == int(option))]['marca'].value_counts().to_frame()
        df_barra2 = df_barra2.reset_index()
        df_barra2.columns = ['marca', 'quantidade']
        df_barra2 = df_barra2.head(7).sort_values(by='quantidade')
        
        # Gráfico barras caracteristicas produtos #2
        fig2 = px.bar(df_barra2, x='quantidade', y='marca')

        fig2.update_layout(autosize=False,
                            width=500,
                            height=300)
        
        graf2.plotly_chart(fig2, use_container_width=True)

        # Definindo dataframe
        df_barra3 = df_app.groupby(['estado', 'ano', 'mes'])['canal_venda'].value_counts().to_frame()
        df_barra3.columns = ['quantidade']
        df_barra3 = df_barra3.reset_index()
        df_barra3 = df_barra3[(df_barra3['estado'] == option2) & (df_barra3['ano'] == int(option))]['canal_venda'].value_counts().to_frame()
        df_barra3 = df_barra3.reset_index()
        df_barra3.columns = ['canal de venda', 'quantidade']
        df_barra3 = df_barra3.head(7).sort_values(by='quantidade')
        
        # Gráfico barras caracteristicas produtos #3
        fig3 = px.bar(df_barra3, x='quantidade', y='canal de venda')

        fig3.update_layout(autosize=False,
                            width=500,
                            height=300)
        
        graf3.plotly_chart(fig3, use_container_width=True)
        
        # Definindo dataframe
        df_barra4 = df_app.groupby(['estado', 'ano', 'mes'])['forma_envio'].value_counts().to_frame()
        df_barra4.columns = ['quantidade']
        df_barra4 = df_barra4.reset_index()
        df_barra4 = df_barra4[(df_barra4['estado'] == option2) & (df_barra4['ano'] == int(option))]['forma_envio'].value_counts().to_frame()
        df_barra4 = df_barra4.reset_index()
        df_barra4.columns = ['forma de envio', 'quantidade']
        df_barra4 = df_barra4.head(7).sort_values(by='quantidade')
        
        # Gráfico barras caracteristicas produtos #4
        fig4 = px.bar(df_barra4, x='quantidade', y='forma de envio')

        fig4.update_layout(autosize=False,
                            width=500,
                            height=300)
        
        graf4.plotly_chart(fig4, use_container_width=True)