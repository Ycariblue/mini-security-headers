import streamlit as st
import requests
import datetime
import time
from scanner.utils import normalize_url
from scanner.http_checks import check_https_and_transport
from scanner.headers_checks import check_headers
from scanner.cookies_checks import check_cookies
from reporting.report_builder import build_markdown_report

# 1. Configuração da página
st.set_page_config(
    page_title="Mini SecurityHeaders Educativo",
    page_icon="🛡️",
    layout="wide"
)

# 2. Estilo CSS para uma UI premium e moderna
st.markdown("""
    <style>
    /* Estilo para os Cards de KPI */
    .kpi-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 10px;
    }
    .kpi-title {
        font-size: 0.9rem;
        color: #6c757d;
        text-transform: uppercase;
        font-weight: bold;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: bold;
        margin: 10px 0;
    }
    .kpi-desc {
        font-size: 0.8rem;
        color: #adb5bd;
    }
    /* Cores dinâmicas para o nível de atenção */
    .status-baixo { border-left-color: #28a745; color: #28a745; }
    .status-medio { border-left-color: #ffc107; color: #ffc107; }
    .status-alto { border-left-color: #dc3545; color: #dc3545; }
    
    /* Título principal */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1b263b;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #415a77;
        margin-bottom: 2rem;
    }
    
    /* Tabelas compactas */
    .stTable {
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.markdown("# 🛡️ Mini SecurityHeaders")
    st.divider()
    
    target_url = st.text_input("🔗 URL do site:", placeholder="https://www.exemplo.com")
    
    st.markdown("### ⚙️ Opções")
    
    # Toggle do Modo Escuro
    dark_mode = st.toggle("🌙 Modo Escuro", value=False)
    
    if dark_mode:
        st.markdown("""
        <style>
            /* --- VARIAVEIS GLOBAIS DARK --- */
            :root {
                --background-primary: #0e1117;
                --background-secondary: #262730;
                --text-primary: #fafafa;
                --text-secondary: #bdc3c7;
                --accent-color: #ff4b4b; /* Cor padrão do Streamlit ou azul se preferir */
            }
            
            /* Fundo Geral */
            .stApp {
                background-color: var(--background-primary);
                color: var(--text-primary);
            }
            
            /* --- SIDEBAR --- */
            [data-testid="stSidebar"] {
                background-color: var(--background-secondary);
                border-right: 1px solid #333;
            }
            
            /* Textos na Sidebar */
            [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
            [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stMarkdown {
                color: var(--text-primary) !important;
            }
            
            /* --- INPUTS (Text Input, Number Input, etc) --- */
            /* Fundo do input e cor do texto digitado */
            .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
                background-color: #1a1c24 !important;
                color: white !important;
                border: 1px solid #4a4a4a !important;
            }
            /* Label dos inputs */
            .stTextInput label {
                color: var(--text-secondary) !important;
            }
            
            /* --- BOTÕES --- */
            /* Botão Secundário (o padrão) */
            .stButton button {
                background-color: #ffffff !important;
                color: #262730 !important;
                border: none !important;
                font-weight: bold !important;
                transition: all 0.3s ease;
            }
            .stButton button:hover {
                background-color: #e0e0e0 !important;
                transform: scale(1.02);
            }
            /* Botão Primário (se houver/configurado) */
            button[kind="primary"] {
                background-color: #ff4b4b !important;
                color: white !important;
            }
            
            /* --- CHECKBOX & TOGGLE --- */
            .stCheckbox label, .stToggle label, .stToggle p {
                color: var(--text-primary) !important;
            }
            
            /* --- CARDS KPI (Customizados) --- */
            .kpi-card {
                background-color: var(--background-secondary) !important;
                color: var(--text-primary) !important;
                border: 1px solid #444;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }
            .kpi-title { color: #bdc3c7 !important; }
            .kpi-value { color: white !important; }
            .kpi-desc { color: #888 !important; }
            
            /* --- TABELAS E EXPANDERS --- */
            .stExpander {
                background-color: var(--background-secondary) !important;
                color: var(--text-primary) !important;
                border: 1px solid #444;
            }
            .stExpander p, .stExpander li {
                color: var(--text-primary) !important;
            }
            
            /* --- TITULOS PRINCIPAIS --- */
            .main-title { color: white !important; }
            .sub-title { color: #bdc3c7 !important; }
            
            /* Forçar links a terem cor visível */
            a { color: #4da6ff !important; }
            
            /* --- HEADER DO STREAMLIT (Remover faixa branca) --- */
            header[data-testid="stHeader"] {
                background-color: transparent !important;
            }
            
            /* Ajuste crítico para BOTÕES ficarem visíveis (incluindo Download) */
            .stButton > button, .stDownloadButton > button {
                color: #000000 !important;
                background-color: #fafafa !important;
                border: 1px solid #ccc !important;
            }
            
            /* Forçar explicitamente a cor do TEXTO dentro do botão (p, div, span) */
            .stButton > button *, .stDownloadButton > button * {
                color: #000000 !important;
            }
            
            .stButton > button:hover, .stDownloadButton > button:hover {
                 background-color: #e6e6e6 !important;
                 border-color: #adadad !important;
            }
             .stButton > button:hover *, .stDownloadButton > button:hover * {
                color: #000000 !important;
             }
            
        </style>
        """, unsafe_allow_html=True)

    do_cookies = st.checkbox("Fazer análise básica de cookies", value=True)
    show_raw = st.checkbox("Mostrar detalhes técnicos brutos", value=False)
    
    st.divider()
    if st.button("🔍 Escanear site", use_container_width=True):
        st.session_state.run_scan = True
        st.session_state.report_status = "em_analise" # Reset status for new scan
    else:
        if 'run_scan' not in st.session_state:
            st.session_state.run_scan = False
        if 'report_status' not in st.session_state:
            st.session_state.report_status = "idle"

    st.info("""
    **Aviso Educativo:**
    Esta ferramenta é para aprendizado. Use apenas em sites que você possui autorização ou controle.
    """)

# 4. Layout Principal
st.markdown('<p class="main-title">🛡️ Mini SecurityHeaders Educativo</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Análise básica e simplificada de HTTPS, cabeçalhos de segurança e integridade de cookies.</p>', unsafe_allow_html=True)

if not st.session_state.run_scan or not target_url:
    st.info("👋 Seja bem-vindo! Digite a URL de um site na barra lateral e clique em **Escanear site** para começar.")
    st.stop()

# 5. Execução do Scan (Otimizado com Session State)
normalized_url = normalize_url(target_url)

# Só rodamos o scan se for uma nova URL ou se o usuário explicitamente clicou no botão
if 'scan_data' not in st.session_state or st.session_state.get('last_url') != normalized_url:
    with st.spinner(f"Analisando {normalized_url}..."):
        try:
            # Requisição principal
            response = requests.get(normalized_url, timeout=15)
            
            # Chamadas das funções originais
            http_results = check_https_and_transport(normalized_url)
            header_results = check_headers(response.headers)
            cookie_results = check_cookies(response.cookies) if do_cookies else []
            
            # Armazenar tudo no session state
            st.session_state.scan_data = {
                "http": http_results,
                "headers": header_results,
                "cookies": cookie_results,
                "full_results": {
                    "http": http_results.__dict__,
                    "headers": header_results,
                    "cookies": cookie_results
                }
            }
            st.session_state.last_url = normalized_url
            st.session_state.report_status = "em_analise" # Começamos a jornada do relatório
            
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Erro ao acessar a URL: {e}")
            st.stop()
        except Exception as e:
            st.error(f"⚠️ Ocorreu um erro inesperado: {e}")
            st.stop()

# Recuperar dados da sessão para facilitar o uso abaixo
sd = st.session_state.scan_data
http_results = sd["http"]
header_results = sd["headers"]
cookie_results = sd["cookies"]
full_results = sd["full_results"]

# 6. Cálculo de Score e IDs de Atenção
headers_ok = len([h for h in header_results if h.status == "ok"])
total_headers = len(header_results)
cookie_issues_count = sum(len(c.issues) for c in cookie_results)

# Lógica heurística para Nível de Atenção
score_points = headers_ok
if http_results.uses_https: score_points += 1
if http_results.redirects_http_to_https: score_points += 1

if score_points >= 6 and cookie_issues_count == 0:
    atencao_nivel = "Baixo"
    atencao_classe = "status-baixo"
    atencao_msg = "O site demonstra boas práticas iniciais de segurança."
elif score_points >= 4:
    atencao_nivel = "Médio"
    atencao_classe = "status-medio"
    atencao_msg = "Existem pontos importantes de segurança ausentes ou configurados de forma fraca."
else:
    atencao_nivel = "Alto"
    atencao_classe = "status-alto"
    atencao_msg = "O site carece de proteções fundamentais contra ataques comuns."

# 7. Cards de Resumo (KPIs)
kpi_cols = st.columns(3)

with kpi_cols[0]:
    st.markdown(f"""
        <div class="kpi-card {atencao_classe}">
            <div class="kpi-title">Nível de Atenção</div>
            <div class="kpi-value">{atencao_nivel}</div>
            <div class="kpi-desc">Baseado em achados e ausências</div>
        </div>
    """, unsafe_allow_html=True)
    
with kpi_cols[1]:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Cabeçalhos de Segurança</div>
            <div class="kpi-value">{headers_ok} / {total_headers} OK</div>
            <div class="kpi-desc">Proteções ativas detectadas</div>
        </div>
    """, unsafe_allow_html=True)
    
with kpi_cols[2]:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Cookies com Problemas</div>
            <div class="kpi-value">{cookie_issues_count}</div>
            <div class="kpi-desc">Flags Secure/HttpOnly ausentes</div>
        </div>
    """, unsafe_allow_html=True)

# 8. Abas de Resultados
tab_geral, tab_https, tab_headers, tab_cookies, tab_relatorio = st.tabs([
    "📊 Visão Geral", "🔒 HTTPS", "🧱 Cabeçalhos", "🍪 Cookies", "📄 Relatório"
])

with tab_geral:
    st.subheader("Resumo da Análise")
    st.write(atencao_msg)
    st.write(f"Análise realizada em: `{normalized_url}`")
    if show_raw:
        st.json(full_results)

with tab_https:
    st.subheader("Transporte Seguro")
    st.markdown(f"""
    - **Usa HTTPS:** {"✅ Sim" if http_results.uses_https else "❌ Não"}
    - **Redireciona HTTP → HTTPS:** {"✅ Sim" if http_results.redirects_http_to_https else "❌ Não"}
    - **Status do Certificado:** {http_results.certificate_info}
    """)
    
    if http_results.https_issues:
        for issue in http_results.https_issues:
            st.error(issue)
    
    with st.expander("ℹ️ Por que o HTTPS é importante?"):
        st.write("""
        O HTTPS criptografa os dados enviados entre o navegador e o servidor. Sem ele, senhas e informações 
        pessoais podem ser interceptadas por invasores na mesma rede (ataques Man-in-the-Middle).
        """)

with tab_headers:
    st.subheader("Cabeçalhos de Segurança")
    h_table = []
    for h in header_results:
        icon = "✅ OK" if h.status == "ok" else ("⚠️ FRACO" if h.status == "weak" else "❌ AUSENTE")
        h_table.append({
            "Cabeçalho": h.name,
            "Status": icon,
            "Valor Encontrado": h.value if h.value else "N/A"
        })
    st.table(h_table)
    
    with st.expander("📚 O que significa cada cabeçalho?"):
        for h in header_results:
            st.markdown(f"**{h.name}**: {h.details}")
            st.info(f"💡 Sugestão: {h.recommendation}")

with tab_cookies:
    st.subheader("Segurança de Cookies")
    if not cookie_results:
        st.info("Nenhum cookie foi encontrado na resposta.")
    else:
        c_table = []
        for c in cookie_results:
            c_table.append({
                "Nome do Cookie": c.name,
                "Secure": "✅" if c.secure else "❌",
                "HttpOnly": "✅" if c.httponly else "❌",
                "Problemas": ", ".join(c.issues) if c.issues else "Nenhum"
            })
        st.table(c_table)
    
    with st.expander("ℹ️ Importância das Flags Secure e HttpOnly"):
        st.write("""
        - **Secure**: Impede o envio do cookie via conexões HTTP inseguras.
        - **HttpOnly**: Impede que scripts maliciosos (XSS) roubem o cookie de sessão.
        """)

with tab_relatorio:
    st.subheader("Central de Relatórios Profissionais")
    
    def render_status(status_key: str):
        """Renderiza o componente visual de status (Semáforo)."""
        styles = {
            "em_analise": {"color": "#dc3545", "text": "🔴 Em análise", "bg": "#f8d7da"},
            "quase_pronto": {"color": "#ffc107", "text": "🟡 Quase pronto", "bg": "#fff3cd"},
            "finalizado": {"color": "#28a745", "text": "🟢 Finalizado", "bg": "#d4edda"}
        }
        # Se o arquivo já foi gerado, forçamos o status 'finalizado'
        if st.session_state.get("txt_content"):
            status_key = "finalizado"
        
        st_cfg = styles.get(status_key, styles["em_analise"])
        st.markdown(f"""
            <div style="padding: 15px; border-radius: 10px; background-color: {st_cfg['bg']}; 
                        border: 2px solid {st_cfg['color']}; text-align: center; margin-bottom: 20px;">
                <h3 style="color: {st_cfg['color']}; margin: 0;">{st_cfg['text']}</h3>
            </div>
        """, unsafe_allow_html=True)

    # Container para o status
    status_container = st.container()
    
    with status_container:
        # Se ainda não geramos os relatórios, fazemos agora de forma sequencial
        if not st.session_state.get("txt_content"):
            # 1. Em análise
            render_status("em_analise")
            time.sleep(0.6)
            
            # 2. Quase pronto
            status_container.empty()
            render_status("quase_pronto")
            
            from reporting.report_builder import generate_txt_report, generate_pdf_report, generate_docx_report
            scan_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            # Geração real
            st.session_state.txt_content = generate_txt_report(normalized_url, http_results.__dict__, header_results, cookie_results, scan_time)
            st.session_state.pdf_bytes = generate_pdf_report(normalized_url, http_results.__dict__, header_results, cookie_results, scan_time)
            st.session_state.docx_bytes = generate_docx_report(normalized_url, http_results.__dict__, header_results, cookie_results, scan_time)
            
            time.sleep(0.4)
            st.session_state.report_status = "finalizado"
            st.rerun() # Refresh final para mostrar os botões
        else:
            # 3. Finalizado
            render_status("finalizado")
            st.success("✅ Seu relatório está pronto para baixar. Escolha o formato desejado:")
            
            col_txt, col_pdf, col_docx = st.columns(3)
            
            with col_txt:
                st.download_button(
                    label="📥 Baixar (.txt)",
                    data=st.session_state.txt_content,
                    file_name=f"relatorio_{normalized_url.replace('https://', '').replace('/', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            with col_pdf:
                st.download_button(
                    label="📥 Baixar (.pdf)",
                    data=st.session_state.pdf_bytes,
                    file_name=f"relatorio_{normalized_url.replace('https://', '').replace('/', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            with col_docx:
                st.download_button(
                    label="📥 Baixar (.docx)",
                    data=st.session_state.docx_bytes,
                    file_name=f"relatorio_{normalized_url.replace('https://', '').replace('/', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )

            st.markdown("---")
            st.markdown("### Prévia do Conteúdo")
            st.text(st.session_state.txt_content[:1500] + "...")
