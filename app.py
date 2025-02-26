import streamlit as st

# Initialize session state to store data
if 'demands' not in st.session_state:
    st.session_state.demands = []

if 'clients' not in st.session_state:
    st.session_state.clients = []

if 'team_members' not in st.session_state:
    st.session_state.team_members = []

# Sidebar for navigation
st.sidebar.title("Demand Management - 806")
menu = st.sidebar.radio(
    "Menu",
    ["Home", "Create Demand", "Manage Clients", "Manage Team Members"]
)

# Home Page
if menu == "Home":
    st.title("Demand Management - 806")
    st.write("### All Demands")

    if not st.session_state.demands:
        st.write("No demands found.")
    else:
        for idx, demand in enumerate(st.session_state.demands):
            st.write(f"#### Demand {idx + 1}")
            st.write(f"**Team Member:** {demand['team_member']}")
            st.write(f"**Client:** {demand['client']}")
            st.write(f"**Description:** {demand['description']}")
            st.write(f"**Priority:** {demand['priority']}")
            st.write(f"**Status:** {demand['status']}")

            if st.button(f"Edit Demand {idx + 1}", key=f"edit_{idx}"):
                st.session_state.edit_idx = idx
                st.experimental_rerun()

            if st.button(f"Delete Demand {idx + 1}", key=f"delete_{idx}"):
                st.session_state.demands.pop(idx)
                st.experimental_rerun()

# Create Demand Page
elif menu == "Create Demand":
    st.title("Create Demand")

    team_member = st.selectbox("Team Member", st.session_state.team_members)
    client = st.selectbox("Client", st.session_state.clients)
    description = st.text_area("Description")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"])

    if st.button("Create Demand"):
        demand = {
            "team_member": team_member,
            "client": client,
            "description": description,
            "priority": priority,
            "status": status
        }
        st.session_state.demands.append(demand)
        st.success("Demand created successfully!")

# Edit Demand Page
if hasattr(st.session_state, 'edit_idx'):
    st.title("Edit Demand")
    idx = st.session_state.edit_idx
    demand = st.session_state.demands[idx]

    team_member = st.selectbox(
        "Team Member",
        st.session_state.team_members,
        index=st.session_state.team_members.index(demand['team_member'])
    )
    client = st.selectbox(
        "Client",
        st.session_state.clients,
        index=st.session_state.clients.index(demand['client'])
    )
    description = st.text_area("Description", value=demand['description'])
    priority = st.selectbox(
        "Priority",
        ["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(demand['priority'])
    )
    status = st.selectbox(
        "Status",
        ["Not Started", "In Progress", "Completed"],
        index=["Not Started", "In Progress", "Completed"].index(demand['status'])
    )

    if st.button("Save Changes"):
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
elif menu == "Manage Clients":
    st.title("Manage Clients")

    new_client = st.text_input("Add New Client")
    if st.button("Add Client"):
        if new_client:
            st.session_state.clients.append(new_client)
            st.success(f"Client '{new_client}' added successfully!")
        else:
            st.error("Client name cannot be empty.")

    st.write("### Client List")
    if not st.session_state.clients:
        st.write("No clients found.")
    else:
        for client in st.session_state.clients:
            st.write(client)

# Manage Team Members Page
elif menu == "Manage Team Members":
    st.title("Manage Team Members")

    new_member = st.text_input("Add New Team Member")
    if st.button("Add Team Member"):
        if new_member:
            st.session_state.team_members.append(new_member)
            st.success(f"Team member '{new_member}' added successfully!")
        else:
            st.error("Team member name cannot be empty.")

    st.write("### Team Member List")
    if not st.session_state.team_members:
        st.write("No team members found.")
    else:
        for member in st.session_state.team_members:
            st.write(member)
