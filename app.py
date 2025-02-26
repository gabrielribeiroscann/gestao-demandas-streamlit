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

st.title("📌 Gestão de Demandas")

# Formulário para adicionar nova demanda
with st.form("nova_demanda"):
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
    st.rerun()  # ✅ Atualizado para evitar erro
     
# Exibir demandas e permitir edição
st.subheader("📋 Demandas Atuais")
if not df.empty:
    edited_df = st.data_editor(df, num_rows="dynamic")
    save_data(edited_df)
else:
    st.info("Nenhuma demanda cadastrada ainda.")
