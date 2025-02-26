import streamlit as st
import pandas as pd
import os

# Nome do arquivo CSV para armazenar as demandas
FILE_NAME = "demandas.csv"
CLIENTES_FILE = "clientes.csv"
RESPONSAVEIS_FILE = "responsaveis.csv"

# Função para carregar os dados do CSV (ou criar um novo DataFrame)
@st.cache_data
def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME)
    else:
        return pd.DataFrame(columns=["Cliente", "Demanda", "Prioridade", "Status", "Responsável"])

# Função para carregar os clientes e responsáveis
@st.cache_data
def load_clientes_responsaveis():
    if os.path.exists(CLIENTES_FILE):
        clientes = pd.read_csv(CLIENTES_FILE)
    else:
        clientes = pd.DataFrame(columns=["Cliente"])
    
    if os.path.exists(RESPONSAVEIS_FILE):
        responsaveis = pd.read_csv(RESPONSAVEIS_FILE)
    else:
        responsaveis = pd.DataFrame(columns=["Responsável"])

    return clientes, responsaveis

# Função para salvar os dados no CSV
def save_data(df, filename):
    df.to_csv(filename, index=False)

# Carrega os dados existentes
df = load_data()

# Carrega clientes e responsáveis
clientes, responsaveis = load_clientes_responsaveis()

# Título
st.title("📌 Gestão de Demandas")

# Função para criar ou editar cliente
def gerenciar_clientes():
    st.subheader("Gerenciar Clientes")
    option = st.selectbox("Escolha uma ação", ["Criar Novo Cliente", "Editar Cliente", "Excluir Cliente"])
    
    if option == "Criar Novo Cliente":
        novo_cliente = st.text_input("Nome do Novo Cliente")
        if st.button("Adicionar Cliente"):
            if novo_cliente and novo_cliente not in clientes["Cliente"].values:
                clientes = clientes.append({"Cliente": novo_cliente}, ignore_index=True)
                save_data(clientes, CLIENTES_FILE)
                st.success(f"Cliente '{novo_cliente}' adicionado com sucesso!")
            else:
                st.warning("Cliente já existe ou nome inválido.")

    elif option == "Editar Cliente":
        cliente_editar = st.selectbox("Escolha um cliente para editar", clientes["Cliente"])
        novo_nome = st.text_input("Novo Nome do Cliente")
        if st.button("Editar Cliente"):
            if novo_nome:
                clientes.loc[clientes["Cliente"] == cliente_editar, "Cliente"] = novo_nome
                save_data(clientes, CLIENTES_FILE)
                st.success(f"Cliente '{cliente_editar}' alterado para '{novo_nome}' com sucesso!")

    elif option == "Excluir Cliente":
        cliente_excluir = st.selectbox("Escolha um cliente para excluir", clientes["Cliente"])
        if st.button("Excluir Cliente"):
            clientes = clientes[clientes["Cliente"] != cliente_excluir]
            save_data(clientes, CLIENTES_FILE)
            st.success(f"Cliente '{cliente_excluir}' excluído com sucesso!")

# Função para criar ou editar responsável
def gerenciar_responsaveis():
    st.subheader("Gerenciar Responsáveis")
    option = st.selectbox("Escolha uma ação", ["Criar Novo Responsável", "Editar Responsável", "Excluir Responsável"])
    
    if option == "Criar Novo Responsável":
        novo_responsavel = st.text_input("Nome do Novo Responsável")
        if st.button("Adicionar Responsável"):
            if novo_responsavel and novo_responsavel not in responsaveis["Responsável"].values:
                responsaveis = responsaveis.append({"Responsável": novo_responsavel}, ignore_index=True)
                save_data(responsaveis, RESPONSAVEIS_FILE)
                st.success(f"Responsável '{novo_responsavel}' adicionado com sucesso!")
            else:
                st.warning("Responsável já existe ou nome inválido.")

    elif option == "Editar Responsável":
        responsavel_editar = st.selectbox("Escolha um responsável para editar", responsaveis["Responsável"])
        novo_nome = st.text_input("Novo Nome do Responsável")
        if st.button("Editar Responsável"):
            if novo_nome:
                responsaveis.loc[responsaveis["Responsável"] == responsavel_editar, "Responsável"] = novo_nome
                save_data(responsaveis, RESPONSAVEIS_FILE)
                st.success(f"Responsável '{responsavel_editar}' alterado para '{novo_nome}' com sucesso!")

    elif option == "Excluir Responsável":
        responsavel_excluir = st.selectbox("Escolha um responsável para excluir", responsaveis["Responsável"])
        if st.button("Excluir Responsável"):
            responsaveis = responsaveis[responsaveis["Responsável"] != responsavel_excluir]
            save_data(responsaveis, RESPONSAVEIS_FILE)
            st.success(f"Responsável '{responsavel_excluir}' excluído com sucesso!")

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
    cliente = st.selectbox("Cliente", clientes["Cliente"].tolist())
    demanda = st.text_area("Descrição da Demanda")
    prioridade = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])
    status = st.selectbox("Status", ["Pendente", "Em Andamento", "Concluído"])
    responsavel = st.selectbox("Responsável", responsaveis["Responsável"].tolist())
    submitted = st.form_submit_button("Adicionar Demanda")

if submitted and cliente and demanda and responsavel:
    novo_registro = pd.DataFrame([[cliente, demanda, prioridade, status, responsavel]], columns=df.columns)
    df = pd.concat([df, novo_registro], ignore_index=True)
    save_data(df, FILE_NAME)  # Salva os dados no arquivo CSV
    st.success("Demanda adicionada com sucesso!")

# Permite editar as demandas existentes
st.sidebar.subheader("Editar Demandas")
if not df.empty:
    # Exibir a tabela de demandas para edição
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    if edited_df is not None:  # Verifica se houve alguma edição
        save_data(edited_df, FILE_NAME)  # Salva as edições no CSV
        st.success("Demanda(s) atualizada(s) com sucesso!")
else:
    st.info("Nenhuma demanda cadastrada ainda.")
