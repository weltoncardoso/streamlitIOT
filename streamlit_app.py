import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import time
from datetime import datetime
from pymongo import MongoClient
import json
import warnings
warnings.filterwarnings('ignore')

st.title('Dashboard projeto IoT-IBTI')

client = MongoClient("mongodb://ibti:ibti@iotibti.ddns.net:27017/")
device = client["data"]
deviceweltondragino = device["98bb0a3a36f2e3e7"]
devicebrunodragino = device["48bec18e0405f370"]
devicefabiodragino = device["949e1a494f73aaaf"]
devicericardodragino = device["588e6b7a7410c18e"]

deviceandroidwelton = device["a3"]
deviceandroidbruno = device["a1"]
deviceandroidbrunocarro = device["a4"]
deviceandroidfabio = device["a5"]
deviceandroidricardo = device["a2"]

devicetemp1 = device["08c0f90570400000"]
devicetemp2 = device["8cf9574000000000"]

dados = devicefabiodragino.find()
mongo_docs_dados=list(dados)



DATA = pd.DataFrame(mongo_docs_dados)
DATA['date'] = DATA.ts.apply(lambda x: datetime.fromtimestamp(x))
DATA.rename({"long": "lon"}, axis=1, inplace=True)

# salvando arquivo tratado
DATA.to_csv('C:/Users/Welton Cardoso/Desktop/ibtiCodigosPython/dadosProjetoIOT/arquivo.csv')
DATA_URL = ('C:/Users/Welton Cardoso/Desktop/ibtiCodigosPython/dadosProjetoIOT/arquivo.csv')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data['date'] = pd.to_datetime(data['date'])
    return data

data = load_data(10000)

# SIDEBAR 
#numero de arquivos 
st.sidebar.header('Parâmetros')
info_sidebar = st.sidebar.empty()

#Slider de selecao de data
st.sidebar.subheader('Ano')
hour_to_filter = st.sidebar.slider('Dia', 1, 30, 15)


#Chekbox da tabela
st.sidebar.subheader('Tabela')
tabela = st.sidebar.empty() #so sera carregado com o filetred
graficos = st.sidebar.empty() #so sera carregado com o filetred

# Multiselect com os lables únicos dos tipos de classificação
# label_to_filter = st.sidebar.multiselect(
#     label="Escolha as metricas",
#     options=labels,
#     default=["device"]
# )
 
# Informação no rodapé da Sidebar
st.sidebar.markdown("""
A base de dados dos Dispositivos é gerenciada pelo *** Instituto Brasileiro de Tecnologia e Inovanção (IBTI)***.
""")
 
# Somente aqui os dados filtrados por ano são atualizados em novo dataframe
filtered_data = data[data['date'].dt.day == hour_to_filter]
 
# Aqui o placehoder vazio finalmente é atualizado com dados do filtered_df
info_sidebar.info("{} ocorrências selecionadas.".format(filtered_data.shape[0]))
 
 
 
 
# MAIN
st.title("IBTI - Dados de GPS")
st.markdown(f"""
            ℹ️ Estão sendo exibidos dados do dispositivo para o dia **{hour_to_filter}**.
            """)
 
# raw data (tabela) dependente do checkbox
if tabela.checkbox("Mostrar tabela de dados"):
    st.write(filtered_data)
 
if graficos.checkbox("Mostrar Grficos"):
    st.title("Dados de GPS enviados no Mes")
    hist_values = np.histogram(
        data['date'].dt.day, bins=30, range=(0,30))[0]
    st.bar_chart(hist_values)
    st.title("Dados de consumo de bateria no mes")
    chart_data = pd.DataFrame(
        np.random.randn(30, 1),
        columns=['bateria'])
    st.area_chart(chart_data)
 
# mapa
st.subheader("Mapa de ocorrências")
st.map(filtered_data)


# if st.checkbox('Mostrar Dados'):
#     st.subheader('Dados')
#     st.write(data)

# hist_values = np.histogram(
#     data['date'].dt.day, bins=30, range=(0,30))[0]
# st.bar_chart(hist_values)
# chart_data = pd.DataFrame(
#     np.random.randn(30, 1),
#     columns=['bateria'])
# st.area_chart(chart_data)


# #st.write(data)
# hour_to_filter = st.slider('Dia', 1, 30, 15)
# filtered_data = data[data['date'].dt.day == hour_to_filter]
# st.subheader(f' Localizacao do Dispositivo no dia  {hour_to_filter}')
# st.map(filtered_data)


# left_column, right_column = st.beta_columns(2)
# pressed = left_column.button('click?')
# if pressed:
#     right_column.write("Woohoo!")

# expander = st.beta_expander("FAQ")
# expander.write("resposta a sua duvida......")

# 'Starting a long computation...'

# # Add a placeholder
# latest_iteration = st.empty()
# bar = st.progress(0)

# for i in range(100):
#   # Update the progress bar with each iteration.
#   latest_iteration.text(f'Iteration {i+1}')
#   bar.progress(i + 1)
#   time.sleep(0.1)

# '...and now we\'re done!'