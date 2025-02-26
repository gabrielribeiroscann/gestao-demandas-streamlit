import streamlit as st
import pandas as pd

# Nome do arquivo CSV para armazenar as demandas
FILE_NAME = "demandas.csv"

# Função para carregar os dados do CSV (ou criar um novo DataFrame)
@st.cache_data
def load_data():
    try:
        return pd.read_csv(FILE_NAME)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Cliente", "Demanda", "Prioridade", "Status", "Responsável"])

# Função para salvar os dados no CSV
def save_data(df):
    df.to_csv(FILE_NAME, index=False)

# Carrega os dados existentes
df = load_data()

# Título
st.title("📌 Gestão de Demandas")

# Barra lateral para filtrar demandas
st.sidebar.header("Filtros")
cliente_filtro = st.sidebar.text_input("Filtrar por Cliente")
responsavel_filtro = st.sidebar.text_input("Filtrar por Responsável")
prioridade_filtro = st.sidebar.selectbox("Filtrar por Prioridade", ["Todas", "Baixa", "Média", "Alta"])
status_filtro = st.sidebar.selectbox("Filtrar por Status", ["Todos", "Pendente", "Em Andamento", "Concluído"])

# Função para filtrar os dados com base nos filtros da sidebar
def aplicar_filtros(df, cliente, responsavel, prioridade, status):
    if cliente:
        df = df[df["Cliente"].str.contains(cliente, case=False)]
    if responsavel:
        df = df[df["Responsável"].str.contains(responsavel, case=False)]
    if prioridade != "Todas":
        df = df[df["Prioridade"] == prioridade]
    if status != "Todos":
        df = df[df["Status"] == status]
    return df

# Aplica os filtros na base de dados
df_filtrado = aplicar_filtros(df, cliente_filtro, responsavel_filtro, prioridade_filtro, status_filtro)

# Exibir as demandas filtradas
st.subheader("📋 Demandas Atuais")
if not df_filtrado.empty:
    st.dataframe(df_filtrado.style.highlight_max(axis=0, color="lightgreen").highlight_min(axis=0, color="lightcoral"))
else:
    st.info("Nenhuma demanda encontrada com os filtros selecionados.")

# Formulário para adicionar nova demanda
st.sidebar.subheader("Adicionar Nova Demanda")
with st.sidebar.form("nova_demanda"):
    cliente = st.text_input("Cliente")
    demanda = st.text_area("Descrição da Demanda")
    prioridade = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])
    status = st.selectbox("Status", ["Pendente", "Em Andamento", "Concluído"])
    responsavel = st.text_input("Responsável")
    submitted = st.form_submit_button("Adicionar Demanda")

if submitted and cliente and demanda and responsavel:
    novo_registro = pd.DataFrame([[cliente, demanda, prioridade, status, responsavel]], columns=df.columns)
    df = pd.concat([df, novo_registro], ignore_index=True)
    save_data(df)
    st.success("Demanda adicionada com sucesso!")
    st.experimental_rerun()

# Atualização em tempo real da demanda com edição de tabela
st.sidebar.subheader("Editar Demandas")
if not df.empty:
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    save_data(edited_df)
else:
    st.info("Nenhuma demanda cadastrada ainda.")

