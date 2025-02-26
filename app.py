import streamlit as st
import pandas as pd
import json
import os

# File to store demands, clients, and team members
DATA_FILE = "data.json"

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

# Load data from file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"demands": [], "clients": [], "team_members": []}

# Save data to file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = load_data()

if 'demands' not in st.session_state:
    st.session_state.demands = st.session_state.data["demands"]

if 'clients' not in st.session_state:
    st.session_state.clients = st.session_state.data["clients"]

if 'team_members' not in st.session_state:
    st.session_state.team_members = st.session_state.data["team_members"]

if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Sidebar for navigation and settings
with st.sidebar:
    st.title("Gerenciamento de Demandas - 806")
    menu = st.radio(
        "Menu",
        ["Página Inicial", "Criar Demanda", "Gerenciar Clientes", "Gerenciar Membros da Equipe", "Exportar Dados"]
    )
    st.write("---")
    st.write("Configurações")
    st.session_state.dark_mode = st.checkbox("Modo Escuro", st.session_state.dark_mode)

# Apply dark mode
if st.session_state.dark_mode:
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

    # Filters
    st.write("#### Filtros")
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_status = st.selectbox("Filtrar por Status", ["Todos", "Não Iniciada", "Em Progresso", "Concluída"])
    with col2:
        filter_priority = st.selectbox("Filtrar por Prioridade", ["Todos", "Baixa", "Média", "Alta"])
    with col3:
        filter_team_member = st.selectbox("Filtrar por Membro da Equipe", ["Todos"] + st.session_state.team_members)

    # Filter demands
    filtered_demands = st.session_state.demands
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
                        st.session_state.demands.pop(idx)
                        st.session_state.data["demands"] = st.session_state.demands
                        save_data(st.session_state.data)
                        st.experimental_rerun()

# Edit Demand Page
if hasattr(st.session_state, 'edit_idx'):
    st.title("Editar Demanda")
    idx = st.session_state.edit_idx
    demand = st.session_state.demands[idx]

    team_member = st.selectbox(
        "Membro da Equipe",
        st.session_state.team_members,
        index=st.session_state.team_members.index(demand['team_member'])
    )
    client = st.selectbox(
        "Cliente",
        st.session_state.clients,
        index=st.session_state.clients.index(demand['client'])
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
        st.session_state.demands[idx] = {
            "team_member": team_member,
            "client": client,
            "description": description,
            "priority": priority,
            "status": status
        }
        st.session_state.data["demands"] = st.session_state.demands
        save_data(st.session_state.data)
        del st.session_state.edit_idx
        st.experimental_rerun()

# Create Demand Page
elif menu == "Criar Demanda":
    st.title("Criar Demanda")

    team_member = st.selectbox("Membro da Equipe", st.session_state.team_members)
    client = st.selectbox("Cliente", st.session_state.clients)
    description = st.text_area("Descrição")
    priority = st.selectbox("Prioridade", ["Alta", "Média", "Baixa"])
    status = st.selectbox("Status", ["Não Iniciada", "Em Progresso", "Concluída"])

    if st.button("Criar Demanda"):
        if not description:
            st.error("A descrição não pode estar vazia.")
        else:
            demand = {
                "team_member": team_member,
                "client": client,
                "description": description,
                "priority": priority,
                "status": status
            }
            st.session_state.demands.append(demand)
            st.session_state.data["demands"] = st.session_state.demands
            save_data(st.session_state.data)
            st.success("Demanda criada com sucesso!")
            if priority == "Alta":
                st.warning("Notificação: Demanda de alta prioridade criada!")

# Manage Clients Page
elif menu == "Gerenciar Clientes":
    st.title("Gerenciar Clientes")

    new_client = st.text_input("Adicionar Novo Cliente")
    if st.button("Adicionar Cliente"):
        if new_client:
            st.session_state.clients.append(new_client)
            st.session_state.data["clients"] = st.session_state.clients
            save_data(st.session_state.data)
            st.success(f"Cliente '{new_client}' adicionado com sucesso!")
        else:
            st.error("O nome do cliente não pode estar vazio.")

    st.write("### Lista de Clientes")
    if not st.session_state.clients:
        st.write("Nenhum cliente encontrado.")
    else:
        for client in st.session_state.clients:
            st.write(client)

# Manage Team Members Page
elif menu == "Gerenciar Membros da Equipe":
    st.title("Gerenciar Membros da Equipe")

    new_member = st.text_input("Adicionar Novo Membro da Equipe")
    if st.button("Adicionar Membro da Equipe"):
        if new_member:
            st.session_state.team_members.append(new_member)
            st.session_state.data["team_members"] = st.session_state.team_members
            save_data(st.session_state.data)
            st.success(f"Membro da equipe '{new_member}' adicionado com sucesso!")
        else:
            st.error("O nome do membro da equipe não pode estar vazio.")

    st.write("### Lista de Membros da Equipe")
    if not st.session_state.team_members:
        st.write("Nenhum membro da equipe encontrado.")
    else:
        for member in st.session_state.team_members:
            st.write(member)

# Export Data Page
elif menu == "Exportar Dados":
    st.title("Exportar Dados")

    if st.session_state.demands:
        df = pd.DataFrame(st.session_state.demands)
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
