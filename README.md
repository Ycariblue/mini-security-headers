# Mini SecurityHeaders Educativo 🛡️

Uma ferramenta educacional desenvolvida em Python para análise básica e passiva de segurança web. Este projeto foi criado com o objetivo de ensinar conceitos fundamentais de segurança em aplicações web, focando em cabeçalhos HTTP, HTTPS e proteção de cookies, seguindo as melhores práticas da OWASP.

## 🎯 Objetivo
O objetivo principal é gerar um relatório educativo que explique **por que** certas configurações de segurança são importantes, transformando achados técnicos em conhecimento acessível.

> **⚠️ AVISO LEGAL:** Esta ferramenta é estritamente para fins educacionais. Não substitui uma auditoria de segurança profissional ou um teste de intrusão (Pentest). Use apenas em sistemas onde você tenha autorização explícita.

## 🛠️ Funcionalidades
- **Checagem de Transporte (HTTPS):** Verifica se o site usa HTTPS e se redireciona tráfego HTTP corretamente.
- **Análise de Cabeçalhos:** Verifica a presença e qualidade de:
  - `Content-Security-Policy` (CSP)
  - `Strict-Transport-Security` (HSTS)
  - `X-Frame-Options` (Clickjacking protection)
  - `X-Content-Type-Options` (MIME sniffing protection)
  - `Referrer-Policy`
- **Análise de Cookies:** Verifica as flags `Secure` e `HttpOnly` em cookies de resposta.
- **Relatório Educativo:** Gera um relatório detalhado em Markdown com explicações e recomendações.

## 📂 Estrutura do Projeto
- `app.py`: Interface web intuitiva construída com Streamlit.
- `scanner/`: Módulos contendo a lógica de verificação.
  - `http_checks.py`: Verificações de protocolos e certificados.
  - `headers_checks.py`: Lógica de análise de cabeçalhos.
  - `cookies_checks.py`: Inspeção de flags de cookies.
  - `utils.py`: Funções auxiliares.
- `reporting/`: Motor de geração do relatório educativo.
- `tests/`: Testes automatizados básicos.

## 🚀 Como Rodar o Projeto Localmente

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd mini_securityheaders
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   # No Windows:
   .\venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação:**
   ```bash
   streamlit run app.py
   ```

A interface abrirá automaticamente no seu navegador padrão (geralmente em `http://localhost:8501`).

---
Desenvolvido com foco em boas práticas OWASP e segurança web.
