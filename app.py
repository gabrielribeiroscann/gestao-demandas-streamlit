import streamlit as st
import pandas as pd

# Custom CSS for styling
def apply_custom_css():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f0f2f6;
        }
        .stButton>button {
            color: #ffffff;
            background-color: #4CAF50;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            border-radius: 5px;
            padding: 10px;
        }
        .stSelectbox>div>div>select {
            border-radius: 5px;
            padding: 10px;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #2e2e2e;
        }
        .stMarkdown p {
            color: #4a4a4a;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply custom CSS
apply_custom_css()

# Initialize session state
if 'demands' not in st.session_state:
    st.session_state.demands = []

if 'clients' not in st.session_state:
    st.session_state.clients = []

if 'team_members' not in st.session_state:
    st.session_state.team_members = []

if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Sidebar for navigation and settings
st.sidebar.title("Gerenciamento de Demandas - 806")
menu = st.sidebar.radio(
    "Menu",
    ["Página Inicial", "Criar Demanda", "Gerenciar Clientes", "Gerenciar Membros da Equipe", "Exportar Dados"]
)
st.sidebar.write("---")
st.sidebar.write("Configurações")
st.session_state.dark_mode = st.sidebar.checkbox("Modo Escuro", st.session_state.dark_mode)

# Apply dark mode
if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        .stButton>button {
            color: #ffffff;
            background-color: #4CAF50;
        }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            color: #ffffff;
            background-color: #2e2e2e;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #ffffff;
        }
        .stMarkdown p {
            color: #e0e0e0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Home Page
if menu == "Página Inicial":
    st.title("Gerenciamento de Demandas - 806")
    st.write("### Todas as Demandas")

    # Filters
    st.write("#### Filtros")
    filter_status = st.selectbox("Filtrar por Status", ["Todos", "Não Iniciada", "Em Progresso", "Concluída"])
    filter_priority = st.selectbox("Filtrar por Prioridade", ["Todos", "Baixa", "Média", "Alta"])
    filter_team_member = st.selectbox("Filtrar por Membro da Equipe", ["Todos"] + st.session_state.team_members)

    filtered_demands = st.session_state.demands
    if filter_status != "Todos":
        filtered_demands = [d for d in filtered_demands if d['status'] == filter_status]
    if filter_priority != "Todos":
        filtered_demands = [d for d in filtered_demands if d['priority'] == filter_priority]
    if filter_team_member != "Todos":
        filtered_demands = [d for d in filtered_demands if d['team_member'] == filter_team_member]

    if not filtered_demands:
        st.write("Nenhuma demanda encontrada.")
    else:
        for idx, demand in enumerate(filtered_demands):
            st.write(f"#### Demanda {idx + 1}")
            st.write(f"**Membro da Equipe:** {demand['team_member']}")
            st.write(f"**Cliente:** {demand['client']}")
            st.write(f"**Descrição:** {demand['description']}")
            st.write(f"**Prioridade:** {demand['priority']}")
            st.write(f"**Status:** {demand['status']}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Editar Demanda {idx + 1}", key=f"edit_{idx}"):
                    st.session_state.edit_idx = idx
                    st.experimental_rerun()
            with col2:
                if st.button(f"Excluir Demanda {idx + 1}", key=f"delete_{idx}"):
                    st.session_state.demands.pop(idx)
                    st.experimental_rerun()

# Create Demand Page
elif menu == "Criar Demanda":
    st.title("Criar Demanda")

    team_member = st.selectbox("Membro da Equipe", st.session_state.team_members)
    client = st.selectbox("Cliente", st.session_state.clients)
    description = st.text_area("Descrição")
    priority = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])
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
            st.success("Demanda criada com sucesso!")
            if priority == "Alta":
                st.warning("Notificação: Demanda de alta prioridade criada!")

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
        ["Baixa", "Média", "Alta"],
        index=["Baixa", "Média", "Alta"].index(demand['priority'])
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
        del st.session_state.edit_idx
        st.experimental_rerun()

# Manage Clients Page
elif menu == "Gerenciar Clientes":
    st.title("Gerenciar Clientes")

    new_client = st.text_input("Adicionar Novo Cliente")
    if st.button("Adicionar Cliente"):
        if new_client:
            st.session_state.clients.append(new_client)
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
