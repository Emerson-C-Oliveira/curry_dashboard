# ==========================================================
# 1.0 - IMPORTAÇÕES DAS BIBLIOTECAS NECESSÁRIAS
# ==========================================================
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import re as re
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Entregadores', page_icon='🚚', layout='wide')
# ==========================================================
# 2.0 - FUNÇÕES - OTIMIZAÇÃO DO CÓDIGO
# ==========================================================
def clean_code(df1):   
    ## Remover espaço da string
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    ## EXCLUIR LINHAS COM A IDADE DOS ENTREGADORES VAZIA
    linhas_vazias = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]

    linhas_vazias = df1['Weatherconditions'] != 'conditions NaN'
    df1 = df1.loc[linhas_vazias, :]

    linhas_vazias = df1['City'] != 'NaN'
    df1 = df1.loc[linhas_vazias, :]

    linhas_vazias = df1['Road_traffic_density'] != 'NaN'
    df1 = df1.loc[linhas_vazias, :]
    ## CONVERSAO DE TEXTO/CATEGORIA/STRING PARA NUMEROS INTEIROS
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )

    ## CONVERSAO DE TEXTO/CATEGORIA/STRING PARA NUMEROS DECIMAIS
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

    ## CONVERSÃO DE TEXTO PARA DATA
    df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y')

    ## REMOVE AS LINHAS DA COLUNA MULTIPLE_DELIVERIES QUE TENHAM O CONTEUDO IGUAL A 'NaN '
    linhas_vazias = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

    ## REMOVER O TEXTO DE NUMEROS
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split('(min) ')[1])
    # df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )

    return df1

def top_delivers(df1, top_asc):
    df_aux = df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).max().sort_values( ['City', 'Time_taken(min)'], ascending=top_asc).reset_index()
    df_aux1 = df_aux.loc[df_aux['City'] == 'Metropolitian', :].head(10)
    df_aux2 = df_aux.loc[df_aux['City'] == 'Urban', :].head(10)
    df_aux3 = df_aux.loc[df_aux['City'] == 'Semi-Urban', :].head(10)
    df3 = pd.concat([df_aux1, df_aux2, df_aux3]).reset_index()
    return df3

# # ==========================================================
# # 3.0 - IMPORTANDO E LIMPANDO OS DADOS
# # ==========================================================
## Leitura do arquivo CSV
df = pd.read_csv('dataset/train.csv')

## Fazendo uma cópia do DataFrame lido
df1 = clean_code(df)

# ==========================================================
# 4.0 BARRA LATERAL - FILTROS COMUNS A TODAS VISÕES
# ==========================================================
# image_path = '/home/emersds/repos_projetos/curry_company/capa_currycompany.png'
image = Image.open('capa_currycompany.png')
st.sidebar.image(image, use_column_width=True)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## A entrega mais rápida do país')
st.sidebar.markdown("""___""")


# Barra lateral para seleção de intervalo de datas com slider
st.sidebar.markdown('## Selecione o intervalo de datas')

# Componente slider para selecionar o intervalo de datas
date_slider = st.sidebar.slider(
    'Selecione o intervalo de datas',
    value=(datetime(2022, 2, 11), datetime(2022, 6, 4)),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 6, 4),
    format='DD-MM-YYYY'
)

# Exibir o intervalo de datas selecionado
start_date, end_date = date_slider
st.markdown(f'<p style="font-size:16px;">Data selecionada: {start_date.strftime("%d-%m-%Y")} até {end_date.strftime("%d-%m-%Y")}</p>', unsafe_allow_html=True)
st.sidebar.markdown("""____""")

# Selecione o tipo de trânsito
traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam']
)
st.sidebar.markdown("""____""")
st.sidebar.markdown('### Powered by Emerson Oliveira')


# Aplicando os filtros nos dados
df1 = df1[(df1['Order_Date'] >= start_date) & (df1['Order_Date'] <= end_date)]
df1 = df1[df1['Road_traffic_density'].isin(traffic_options)]

# =============================================
# 4.0 - VISÃO ENTREGADORES (LAYOUT NO STREAMLIT)
# =============================================
st.header('Marketplace - Visão Entregadores')

tab1, tab2 = st.tabs(['VISÃO GERENCIAL', '_'])

with tab1:
    with st.container():
        # Overall Metrics
        st.title('Todas as métricas')
        cols1, cols2, cols3, cols4 = st.columns(4, gap='large')
        with cols1:
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            cols1.metric('Maior de idade', maior_idade)

        with cols2:
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            cols2.metric('Menor idade', menor_idade)
       
        with cols3:
            melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
            cols3.metric('Melhor condição', melhor_condicao)


        with cols4:
            pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
            cols4.metric('Pior condição', pior_condicao)
    

    with st.container():
        st.markdown("""___""")
        st.title('Avaliações')

        cols1, cols2 = st.columns(2)

        with cols1:
            st.subheader('Avaliação média por entregador')
            df_avg_ratings_per_deliver = df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']].groupby(['Delivery_person_ID']).mean().reset_index()
            st.dataframe(df_avg_ratings_per_deliver)

        with cols2:
            st.subheader('Avaliação média por trânsito')
            df_avg_ratings_per_traffic = df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']].groupby(['Road_traffic_density']).agg({'Delivery_person_Ratings': ['mean', 'std']})
            df_avg_ratings_per_traffic.columns = ['delivery_mean', 'delivery_std']

            df_avg_ratings_per_traffic = df_avg_ratings_per_traffic.reset_index()
            st.dataframe(df_avg_ratings_per_traffic)

            st.subheader('Avaliação média por clima')
            df_avg_ratings_per_weatherconditions = df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']].groupby(['Weatherconditions']).agg({'Delivery_person_Ratings': ['mean', 'std']})
            df_avg_ratings_per_weatherconditions.columns = ['delivery_mean', 'delivery_std']
            df_avg_ratings_per_weatherconditions = df_avg_ratings_per_weatherconditions.reset_index()
            st.dataframe(df_avg_ratings_per_weatherconditions)
        
    with st.container():
        st.markdown("""___""")
        st.title('Velocidade de entrega')

        cols1, cols2 = st.columns(2)

        with cols1:
            st.markdown('##### Top 10 entregadores mais lentos')
            df3 = top_delivers(df1, top_asc=False)
            st.dataframe(df3)

        with cols2:
            st.markdown('##### Top 10 entregadores mais rápidos')
            df3 = top_delivers(df1, top_asc=True)
            st.dataframe(df3)
