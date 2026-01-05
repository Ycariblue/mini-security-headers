from typing import Dict, Any
import datetime

def build_markdown_report(url: str, results: Dict[str, Any]) -> str:
    """Gera um relatório educativo em Markdown baseado nos resultados do scanner."""
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# Relatório de Análise de Segurança Web - Educativo

**URL Analisada:** {url}
**Data da Análise:** {timestamp}

---

> ### ⚠️ AVISO IMPORTANTE
> Este relatório foi gerado por uma ferramenta educacional. Ele fornece um diagnóstico inicial simplificado e **não substitui** um teste de intrusão (Pentest) profissional ou uma auditoria de segurança completa. Utilize estas informações para aprendizado e melhoria contínua sob sua própria responsabilidade e apenas em sites que você possui autorização para testar.

---

## 1. Visão Geral
{get_summary_text(results)}

---

## 2. HTTPS e Transporte Seguro
O HTTPS (HyperText Transfer Protocol Secure) é a versão segura do HTTP. Ele utiliza criptografia (SSL/TLS) para proteger os dados transmitidos entre o navegador do usuário e o servidor, garantindo confidencialidade e integridade.

**Resultados:**
- **Usa HTTPS:** {"✅ Sim" if results['http']['uses_https'] else "❌ Não"}
- **Redireciona HTTP para HTTPS:** {"✅ Sim" if results['http']['redirects_http_to_https'] else "❌ Não"}
- **Status do Certificado:** {results['http']['certificate_info']}

**Achados e Problemas:**
{format_list(results['http'].get('https_issues', []))}

**Recomendações:**
- Se o site não usa HTTPS, instale um certificado SSL/TLS (ex: Let's Encrypt).
- Configure o servidor para redirecionar permanentemente (301) todo tráfego HTTP para HTTPS.
- Implemente o cabeçalho HSTS (ver seção abaixo) para forçar o uso do protocolo seguro.

---

## 3. Cabeçalhos de Segurança
Cabeçalhos de segurança são instruções enviadas pelo servidor ao navegador para ativar defesas integradas e reduzir a superfície de ataque.

| Cabeçalho | Status | Detalhes |
|-----------|--------|----------|
"""
    
    for h in results['headers']:
        name = getattr(h, 'name', 'N/A')
        status = getattr(h, 'status', 'missing')
        details = getattr(h, 'details', 'N/A')
        status_icon = "✅" if status == "ok" else ("⚠️" if status == "weak" else "❌")
        report += f"| {name} | {status_icon} {status.upper()} | {details} |\n"
    
    report += "\n### Detalhamento e Recomendações por Cabeçalho\n"
    
    for h in results['headers']:
        name = getattr(h, 'name', 'N/A')
        status = getattr(h, 'status', 'missing').upper()
        rec = getattr(h, 'recommendation', 'N/A')
        report += f"\n#### {name}\n"
        report += f"- **O que é:** {get_header_explanation(name)}\n"
        report += f"- **Status:** {status}\n"
        report += f"- **Recomendação:** {rec}\n"

    report += """
---

## 4. Cookies
Cookies são pequenos pedaços de dados armazenados no navegador. Se não forem protegidos com as "flags" corretas, podem ser roubados ou interceptados.

**O que são as flags:**
- **Secure:** Garante que o cookie só seja enviado via conexões HTTPS.
- **HttpOnly:** Impede que scripts (JavaScript) acessem o cookie, mitigando roubo via XSS.

**Cookies Encontrados:**
"""
    
    if not results['cookies']:
        report += "Nenhum cookie foi detectado na resposta principal.\n"
    else:
        for c in results['cookies']:
            name = getattr(c, 'name', 'N/A')
            sec = getattr(c, 'secure', False)
            htt = getattr(c, 'httponly', False)
            iss = getattr(c, 'issues', [])
            report += f"### Cookie: `{name}`\n"
            report += f"- **Secure:** {'✅ Sim' if sec else '❌ Não'}\n"
            report += f"- **HttpOnly:** {'✅ Sim' if htt else '❌ Não'}\n"
            if iss:
                report += "- **Problemas detectados:**\n"
                for issue in iss:
                    report += f"  - {issue}\n"
            report += "\n"

    report += """
---

## 5. Conclusão e Prioridades
A segurança web é uma jornada. Recomendamos focar primeiro no básico:
1. **HTTPS Total:** Garanta que 100% do site use HTTPS e HSTS.
2. **Cookies de Sessão:** Proteja cookies sensíveis com `HttpOnly` e `Secure`.
3. **Cabeçalhos de Defesa:** Implemente `X-Frame-Options` e `X-Content-Type-Options` primeiro, depois planeje um `CSP`.

---
*Gerado por Mini SecurityHeaders Educativo.*
"""
    return report

def get_summary_text(results: Dict[str, Any]) -> str:
    issues_count = len(results['http'].get('https_issues', []))
    missing_headers = len([h for h in results['headers'] if not getattr(h, 'present', False)])
    
    cookie_issues = 0
    for c in results['cookies']:
        cookie_issues += len(getattr(c, 'issues', []))
    
    total = issues_count + missing_headers + cookie_issues
    
    if total == 0:
        return "Excelente! Não detectamos problemas básicos de segurança na URL informada. Continue seguindo as boas práticas OWASP."
    elif total < 4:
        return f"O site possui um bom nível de segurança básica, mas encontramos {total} pontos de atenção que podem ser melhorados para atingir o estado da arte."
    else:
        return f"Foram encontrados {total} pontos de vulnerabilidade simplificada ou ausência de boas práticas. Recomendamos revisar as seções de HTTPS, Cabeçalhos e Cookies abaixo."

def get_header_explanation(name: str) -> str:
    explanations = {
        "Strict-Transport-Security": "Força o navegador a se comunicar apenas via HTTPS por um período definido.",
        "Content-Security-Policy": "Define quais recursos (scripts, estilos, imagens) podem ser carregados no site.",
        "X-Frame-Options": "Controla se o site pode ser exibido dentro de iframes (previne Clickjacking).",
        "X-Content-Type-Options": "Impede o navegador de tentar adivinhar o tipo de conteúdo (MIME Sniffing).",
        "Referrer-Policy": "Controla quanta informação de referência é enviada quando o usuário clica em um link."
    }
    return explanations.get(name, "Cabeçalho de segurança web.")

def format_list(items: list) -> str:
    if not items:
        return "Nenhum problema grave detectado."
    return "\n".join([f"- {item}" for item in items])
