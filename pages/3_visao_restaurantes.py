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


st.set_page_config(page_title='Visão Restaurantes', page_icon='🍽️', layout='wide')
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


def distance(df1):
    cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
    df1['distance'] = df1.loc[:, cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'] )), axis=1)
    avg_distance = np.round(df1['distance'].mean(), 2)

    return avg_distance
def avg_std_time_delivery(df1, festival, op):
    # Convertendo 'Time_taken(min)' para float
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(float)

    # Agrupando e calculando a média e o desvio padrão
    df_aux = df1.loc[:, ['Time_taken(min)', 'Festival']].groupby(['Festival']).agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    
    # Seleciona o valor correto de acordo com o parâmetro 'op' (avg_time ou std_time)
    value = df_aux.loc[df_aux['Festival'] == festival, op].iloc[0]

    # Formata o valor para duas casas decimais
    value_formatted = '{:.2f}'.format(value)

    return value_formatted


def avg_std_time_graph(df1):
    df_aux = df1.loc[:, ['City', 'Time_taken(min)']].groupby(['City']).agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Control', x=df_aux['City'], y=df_aux['avg_time'], error_y=dict(type='data', array=df_aux['std_time'])))
    fig.update_layout(barmode='group')
    return fig

def avg_std_time_on_traffic(df1):
    df_aux = df1.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time', color='std_time', color_continuous_scale='RdBu', color_continuous_midpoint=np.average(df_aux['std_time']))
    return fig

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
image_path = '/home/emersds/repos_projetos/curry_company/capa_currycompany.png'
image = Image.open(image_path)
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
# 4.0 - VISÃO RESTAURANTES (LAYOUT NO STREAMLIT)
# =============================================
st.header('Marketplace - Visão Restaurantes')

tab1, tab2 = st.tabs(['VISÃO GERENCIAL', '_']) # CRIA ABAS

with tab1:
    with st.container():
        # Overall Metrics
        st.title('Todas as métricas')
        cols1, cols2, cols3, cols4, cols5, cols6 = st.columns(6)
        with cols1:
            delivery_unique = len(df1.loc[:, 'Delivery_person_ID'].unique())
            cols1.metric('Entregadores', delivery_unique)

        with cols2:
            avg_distance = distance(df1)
            cols2.metric('Distância média', avg_distance)

        with cols3:
            df1_aux = avg_std_time_delivery(df1,'Yes' ,'avg_time')
            cols3.metric('Tempo médio c/ festival', df1_aux)

        with cols4:
            df1_aux = avg_std_time_delivery(df1, 'Yes' ,'std_time')
            cols4.metric('STD entrega c/ festival', df1_aux)

        with cols5:
            df1_aux = avg_std_time_delivery(df1, 'No' ,'avg_time')
            cols5.metric('Tempo médio s/ festival', df1_aux)
        
        with cols6:
            df1_aux = avg_std_time_delivery(df1, 'No' ,'std_time')
            cols6.metric('STD entrega s/ festival', df1_aux)

    with st.container():
        st.markdown("""___""")
        st.title('Distribuição da distância')
        cols1, cols2 = st.columns (2)
        with cols1:
            fig = avg_std_time_graph(df1)
            st.plotly_chart(fig, use_container_width=True)

        with cols2:
            st.markdown("""___""")
            df_aux = df1.loc[:, ['City', 'Time_taken(min)', 'Type_of_order']].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)': ['mean', 'std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            st.dataframe(df_aux)
        
    with st.container():
        st.markdown("""___""")
        st.title('Distribuição do tempo')

        cols1, cols2 = st.columns(2)

        with cols1:
            cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
            df1['distance'] = df1.loc[:, cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'] )), axis=1)
            avg_distance = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()
            fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0])])
            # fig.show()
            st.plotly_chart(fig, use_container_width=True)

        with cols2:
            fig = avg_std_time_on_traffic(df1)
            st.plotly_chart(fig, use_container_width=True)