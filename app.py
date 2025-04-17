import streamlit as st
import pandas as pd
from supabase import create_client
import os
from dotenv import load_dotenv
from datetime import datetime

# Configuração inicial
st.set_page_config(page_title="Gestão de Demandas", page_icon="📋", layout="wide")

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa o cliente Supabase
@st.cache_resource
def init_supabase():
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    return create_client(supabase_url, supabase_key)

supabase = init_supabase()

# Funções de banco de dados
def carregar_demandas():
    try:
        response = supabase.table("demands").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"Erro ao carregar demandas: {str(e)}")
        return []

def salvar_demanda(demanda):
    try:
        demanda["created_at"] = datetime.now().isoformat()
        supabase.table("demands").insert(demanda).execute()
        st.success("Demanda salva com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar demanda: {str(e)}")

def atualizar_demanda(id_demanda, dados):
    try:
        supabase.table("demands").update(dados).eq("id", id_demanda).execute()
        st.success("Demanda atualizada com sucesso!")
    except Exception as e:
        st.error(f"Erro ao atualizar demanda: {str(e)}")

def excluir_demanda(id_demanda):
    try:
        supabase.table("demands").delete().eq("id", id_demanda).execute()
        st.success("Demanda excluída com sucesso!")
    except Exception as e:
        st.error(f"Erro ao excluir demanda: {str(e)}")

def carregar_clientes():
    try:
        response = supabase.table("clients").select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"Erro ao carregar clientes: {str(e)}")
        return []

def salvar_cliente(cliente):
    try:
        supabase.table("clients").insert(cliente).execute()
        st.success("Cliente salvo com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar cliente: {str(e)}")

def carregar_membros_equipe():
    try:
        response = supabase.table("team_members").select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"Erro ao carregar membros: {str(e)}")
        return []

def salvar_membro(membro):
    try:
        supabase.table("team_members").insert(membro).execute()
        st.success("Membro salvo com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar membro: {str(e)}")

# CSS personalizado
def aplicar_css():
    st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Arial', sans-serif;
    }
    .demanda-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .sidebar .sidebar-content {
        background-color: #2c3e50;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

aplicar_css()

# Barra lateral
with st.sidebar:
    st.title("📋 Gestão de Demandas")
    menu = st.radio(
        "Menu",
        ["Página Inicial", "Criar Demanda", "Gerenciar Clientes", "Gerenciar Equipe", "Exportar Dados"]
    )
    
    st.markdown("---")
    st.markdown("**Configurações**")
    modo_escuro = st.toggle("Modo Escuro")

    # Verificação de conexão
    if st.button("Testar Conexão com Banco de Dados"):
        try:
            demandas = carregar_demandas()
            st.success(f"Conexão OK! {len(demandas)} demandas encontradas")
        except Exception as e:
            st.error(f"Falha na conexão: {str(e)}")

# Páginas principais
if menu == "Página Inicial":
    st.title("📋 Todas as Demandas")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_status = st.selectbox("Status", ["Todos", "Pendente", "Em Andamento", "Concluído"])
    with col2:
        filtro_prioridade = st.selectbox("Prioridade", ["Todos", "Baixa", "Média", "Alta"])
    
    # Carrega dados
    demandas = carregar_demandas()
    clientes = carregar_clientes()
    membros = carregar_membros_equipe()
    
    # Aplica filtros
    if filtro_status != "Todos":
        demandas = [d for d in demandas if d["status"] == filtro_status]
    if filtro_prioridade != "Todos":
        demandas = [d for d in demandas if d["priority"] == filtro_prioridade]
    
    # Exibe demandas
    for demanda in demandas:
        with st.container():
            st.markdown(f"""
            <div class="demanda-card">
                <h3>{demanda['client']}</h3>
                <p><strong>Responsável:</strong> {demanda['team_member']}</p>
                <p><strong>Descrição:</strong> {demanda['description']}</p>
                <p><strong>Prioridade:</strong> {demanda['priority']}</p>
                <p><strong>Status:</strong> {demanda['status']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Editar {demanda['id']}", key=f"edit_{demanda['id']}"):
                    st.session_state.editar_demanda = demanda
            with col2:
                if st.button(f"Excluir {demanda['id']}", key=f"del_{demanda['id']}"):
                    excluir_demanda(demanda['id'])
                    st.rerun()

elif menu == "Criar Demanda":
    st.title("➕ Criar Nova Demanda")
    
    clientes = carregar_clientes()
    membros = carregar_membros_equipe()
    
    with st.form("nova_demanda"):
        cliente = st.selectbox("Cliente", [c["name"] for c in clientes])
        responsavel = st.selectbox("Responsável", [m["name"] for m in membros])
        descricao = st.text_area("Descrição")
        prioridade = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])
        status = st.selectbox("Status", ["Pendente", "Em Andamento", "Concluído"])
        
        if st.form_submit_button("Salvar Demanda"):
            nova_demanda = {
                "client": cliente,
                "team_member": responsavel,
                "description": descricao,
                "priority": prioridade,
                "status": status
            }
            salvar_demanda(nova_demanda)
            st.rerun()

elif menu == "Gerenciar Clientes":
    st.title("👥 Gerenciar Clientes")
    
    with st.form("novo_cliente"):
        nome_cliente = st.text_input("Nome do Cliente")
        if st.form_submit_button("Adicionar Cliente"):
            salvar_cliente({"name": nome_cliente})
            st.rerun()
    
    st.subheader("Lista de Clientes")
    clientes = carregar_clientes()
    for cliente in clientes:
        st.write(cliente["name"])

elif menu == "Gerenciar Equipe":
    st.title("👥 Gerenciar Equipe")
    
    with st.form("novo_membro"):
        nome_membro = st.text_input("Nome do Membro")
        if st.form_submit_button("Adicionar Membro"):
            salvar_membro({"name": nome_membro})
            st.rerun()
    
    st.subheader("Lista de Membros")
    membros = carregar_membros_equipe()
    for membro in membros:
        st.write(membro["name"])

elif menu == "Exportar Dados":
    st.title("📤 Exportar Dados")
    
    demandas = carregar_demandas()
    if demandas:
        df = pd.DataFrame(demandas)
        st.dataframe(df)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Exportar para CSV",
            data=csv,
            file_name="demandas.csv",
            mime="text/csv"
        )
    else:
        st.warning("Nenhuma demanda para exportar")

# Página de edição (aparece quando clica em editar)
if "editar_demanda" in st.session_state:
    demanda = st.session_state.editar_demanda
    st.title(f"✏️ Editar Demanda {demanda['id']}")
    
    with st.form("editar_demanda"):
        cliente = st.text_input("Cliente", value=demanda["client"])
        responsavel = st.text_input("Responsável", value=demanda["team_member"])
        descricao = st.text_area("Descrição", value=demanda["description"])
        prioridade = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"], index=["Baixa", "Média", "Alta"].index(demanda["priority"]))
        status = st.selectbox("Status", ["Pendente", "Em Andamento", "Concluído"], index=["Pendente", "Em Andamento", "Concluído"].index(demanda["status"]))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Salvar Alterações"):
                dados_atualizados = {
                    "client": cliente,
                    "team_member": responsavel,
                    "description": descricao,
                    "priority": prioridade,
                    "status": status
                }
                atualizar_demanda(demanda["id"], dados_atualizados)
                del st.session_state.editar_demanda
                st.rerun()
        with col2:
            if st.button("Cancelar"):
                del st.session_state.editar_demanda
                st.rerun()
