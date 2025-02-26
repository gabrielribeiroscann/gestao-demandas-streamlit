import streamlit as st

# Initialize session state to store data
if 'demands' not in st.session_state:
    st.session_state.demands = []

if 'clients' not in st.session_state:
    st.session_state.clients = []

if 'team_members' not in st.session_state:
    st.session_state.team_members = []

# Sidebar for navigation
st.sidebar.title("Gerenciamento de Demandas - 806")
menu = st.sidebar.radio(
    "Menu",
    ["Página Inicial", "Criar Demanda", "Gerenciar Clientes", "Gerenciar Membros da Equipe"]
)

# Home Page
if menu == "Página Inicial":
    st.title("Gerenciamento de Demandas - 806")
    st.write("### Todas as Demandas")

    if not st.session_state.demands:
        st.write("Nenhuma demanda encontrada.")
    else:
        for idx, demand in enumerate(st.session_state.demands):
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
