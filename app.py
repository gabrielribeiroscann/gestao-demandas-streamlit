import streamlit as st
import pandas as pd
import sqlite3
import os

# Nome do arquivo do banco de dados
DATABASE_FILE = "demands.db"

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
    return conn

# Função para inicializar o banco de dados (cria as tabelas se não existirem)
def init_db():
    if not os.path.exists(DATABASE_FILE):
        conn = get_db_connection()
        cursor = conn.cursor()
        # Tabela de demandas
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS demands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_member TEXT NOT NULL,
                client TEXT NOT NULL,
                description TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL
            )
            """
        )
        # Tabela de clientes
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
            """
        )
        # Tabela de membros da equipe
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS team_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
            """
        )
        conn.commit()
        conn.close()

# Inicializar o banco de dados
init_db()

# Custom CSS for styling
def apply_custom_css():
    st.markdown(
        """
        <style>
        /* General styling */
        .stApp {
            background-color: #f8f9fa;
            font-family: 'Arial', sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            border-radius: 5px;
            padding: 10px;
            border: 1px solid #ced4da;
        }
        .stSelectbox>div>div>select {
            border-radius: 5px;
            padding: 10px;
            border: 1px solid #ced4da;
        }
        /* Card styling for demands */
        .demand-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .demand-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        .demand-card h4 {
            margin-top: 0;
            color: #34495e;
        }
        .demand-card p {
            margin: 5px 0;
            color: #7f8c8d;
        }
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: #2c3e50;
            color: white;
            padding: 20px;
        }
        .sidebar .sidebar-content h2 {
            color: white;
        }
        .sidebar .sidebar-content .stRadio>div {
            color: white;
        }
        .sidebar .sidebar-content .stCheckbox>div {
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply custom CSS
apply_custom_css()

# Sidebar for navigation and settings
with st.sidebar:
    st.title("Gerenciamento de Demandas - 806")
    menu = st.radio(
        "Menu",
        ["Página Inicial", "Criar Demanda", "Gerenciar Clientes", "Gerenciar Membros da Equipe", "Exportar Dados"]
    )
    st.write("---")
    st.write("Configurações")
    dark_mode = st.checkbox("Modo Escuro")

# Apply dark mode
if dark_mode:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        .demand-card {
            background-color: #2e2e2e;
            color: #ffffff;
        }
        .demand-card h4 {
            color: #ffffff;
        }
        .demand-card p {
            color: #e0e0e0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to sort demands by priority
def sort_demands_by_priority(demands):
    priority_order = {"Alta": 1, "Média": 2, "Baixa": 3}
    return sorted(demands, key=lambda x: priority_order[x['priority']])

# Home Page
if menu == "Página Inicial":
    st.title("Gerenciamento de Demandas - 806")
    st.write("### Todas as Demandas")

    # Carregar demandas do banco de dados
    conn = get_db_connection()
    demands = conn.execute("SELECT * FROM demands").fetchall()
    clients = conn.execute("SELECT * FROM clients").fetchall()
    team_members = conn.execute("SELECT * FROM team_members").fetchall()
    conn.close()

    # Filters
    st.write("#### Filtros")
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_status = st.selectbox("Filtrar por Status", ["Todos", "Não Iniciada", "Em Progresso", "Concluída"])
    with col2:
        filter_priority = st.selectbox("Filtrar por Prioridade", ["Todos", "Baixa", "Média", "Alta"])
    with col3:
        filter_team_member = st.selectbox("Filtrar por Membro da Equipe", ["Todos"] + [member["name"] for member in team_members])

    # Filter demands
    filtered_demands = demands
    if filter_status != "Todos":
        filtered_demands = [d for d in filtered_demands if d['status'] == filter_status]
    if filter_priority != "Todos":
        filtered_demands = [d for d in filtered_demands if d['priority'] == filter_priority]
    if filter_team_member != "Todos":
        filtered_demands = [d for d in filtered_demands if d['team_member'] == filter_team_member]

    # Sort demands by priority
    sorted_demands = sort_demands_by_priority(filtered_demands)

    if not sorted_demands:
        st.write("Nenhuma demanda encontrada.")
    else:
        for idx, demand in enumerate(sorted_demands):
            with st.container():
                st.markdown(
                    f"""
                    <div class="demand-card">
                        <h4>Demanda {idx + 1}</h4>
                        <p><strong>Membro da Equipe:</strong> {demand['team_member']}</p>
                        <p><strong>Cliente:</strong> {demand['client']}</p>
                        <p><strong>Descrição:</strong> {demand['description']}</p>
                        <p><strong>Prioridade:</strong> {demand['priority']}</p>
                        <p><strong>Status:</strong> {demand['status']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Editar Demanda {idx + 1}", key=f"edit_{idx}"):
                        st.session_state.edit_idx = idx
                with col2:
                    if st.button(f"Excluir Demanda {idx + 1}", key=f"delete_{idx}"):
                        conn = get_db_connection()
                        conn.execute("DELETE FROM demands WHERE id = ?", (demand["id"],))
                        conn.commit()
                        conn.close()
                        st.success("Demanda excluída com sucesso!")
                        st.experimental_rerun()

# Edit Demand Page
if hasattr(st.session_state, 'edit_idx'):
    st.title("Editar Demanda")
    conn = get_db_connection()
    demand = conn.execute("SELECT * FROM demands WHERE id = ?", (st.session_state.edit_idx + 1,)).fetchone()
    conn.close()

    team_member = st.selectbox(
        "Membro da Equipe",
        [member["name"] for member in team_members],
        index=[member["name"] for member in team_members].index(demand['team_member'])
    )
    client = st.selectbox(
        "Cliente",
        [client["name"] for client in clients],
        index=[client["name"] for client in clients].index(demand['client'])
    )
    description = st.text_area("Descrição", value=demand['description'])
    priority = st.selectbox(
        "Prioridade",
        ["Alta", "Média", "Baixa"],
        index=["Alta", "Média", "Baixa"].index(demand['priority'])
    )
    status = st.selectbox(
        "Status",
        ["Não Iniciada", "Em Progresso", "Concluída"],
        index=["Não Iniciada", "Em Progresso", "Concluída"].index(demand['status'])
    )

    if st.button("Salvar Alterações"):
        conn = get_db_connection()
        conn.execute(
            """
            UPDATE demands
            SET team_member = ?, client = ?, description = ?, priority = ?, status = ?
            WHERE id = ?
            """,
            (team_member, client, description, priority, status, demand["id"]),
        )
        conn.commit()
        conn.close()
        del st.session_state.edit_idx
        st.success("Demanda atualizada com sucesso!")
        st.experimental_rerun()

# Create Demand Page
elif menu == "Criar Demanda":
    st.title("Criar Demanda")

    conn = get_db_connection()
    team_members = conn.execute("SELECT * FROM team_members").fetchall()
    clients = conn.execute("SELECT * FROM clients").fetchall()
    conn.close()

    team_member = st.selectbox("Membro da Equipe", [member["name"] for member in team_members])
    client = st.selectbox("Cliente", [client["name"] for client in clients])
    description = st.text_area("Descrição")
    priority = st.selectbox("Prioridade", ["Alta", "Média", "Baixa"])
    status = st.selectbox("Status", ["Não Iniciada", "Em Progresso", "Concluída"])

    if st.button("Criar Demanda"):
        if not description:
            st.error("A descrição não pode estar vazia.")
        else:
            conn = get_db_connection()
            conn.execute(
                """
                INSERT INTO demands (team_member, client, description, priority, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (team_member, client, description, priority, status),
            )
            conn.commit()
            conn.close()
            st.success("Demanda criada com sucesso!")
            if priority == "Alta":
                st.warning("Notificação: Demanda de alta prioridade criada!")

# Manage Clients Page
elif menu == "Gerenciar Clientes":
    st.title("Gerenciar Clientes")

    new_client = st.text_input("Adicionar Novo Cliente")
    if st.button("Adicionar Cliente"):
        if new_client:
            conn = get_db_connection()
            conn.execute("INSERT INTO clients (name) VALUES (?)", (new_client,))
            conn.commit()
            conn.close()
            st.success(f"Cliente '{new_client}' adicionado com sucesso!")
        else:
            st.error("O nome do cliente não pode estar vazio.")

    conn = get_db_connection()
    clients = conn.execute("SELECT * FROM clients").fetchall()
    conn.close()

    st.write("### Lista de Clientes")
    if not clients:
        st.write("Nenhum cliente encontrado.")
    else:
        for client in clients:
            st.write(client["name"])

# Manage Team Members Page
elif menu == "Gerenciar Membros da Equipe":
    st.title("Gerenciar Membros da Equipe")

    new_member = st.text_input("Adicionar Novo Membro da Equipe")
    if st.button("Adicionar Membro da Equipe"):
        if new_member:
            conn = get_db_connection()
            conn.execute("INSERT INTO team_members (name) VALUES (?)", (new_member,))
            conn.commit()
            conn.close()
            st.success(f"Membro da equipe '{new_member}' adicionado com sucesso!")
        else:
            st.error("O nome do membro da equipe não pode estar vazio.")

    conn = get_db_connection()
    team_members = conn.execute("SELECT * FROM team_members").fetchall()
    conn.close()

    st.write("### Lista de Membros da Equipe")
    if not team_members:
        st.write("Nenhum membro da equipe encontrado.")
    else:
        for member in team_members:
            st.write(member["name"])

# Export Data Page
elif menu == "Exportar Dados":
    st.title("Exportar Dados")

    conn = get_db_connection()
    demands = conn.execute("SELECT * FROM demands").fetchall()
    conn.close()

    if demands:
        df = pd.DataFrame(demands)
        st.write("### Dados das Demandas")
        st.write(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Exportar para CSV",
            data=csv,
            file_name="demandas.csv",
            mime="text/csv"
        )
    else:
        st.write("Nenhuma demanda para exportar.")
