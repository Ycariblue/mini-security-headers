from dataclasses import dataclass
from typing import List, Dict, Optional
import requests

@dataclass
class HeaderCheckResult:
    name: str
    present: bool
    value: Optional[str]
    status: str  # "ok", "missing", "weak"
    details: str
    recommendation: str

def check_headers(response_headers: Dict[str, str]) -> List[HeaderCheckResult]:
    """Verifica a presença e qualidade dos cabeçalhos de segurança."""
    results = []
    
    # 1. Strict-Transport-Security (HSTS)
    hsts = response_headers.get("Strict-Transport-Security")
    if hsts:
        status = "ok"
        details = "HSTS está configurado."
        if "max-age" not in hsts.lower():
            status = "weak"
            details = "HSTS presente mas sem diretiva 'max-age'."
        results.append(HeaderCheckResult(
            "Strict-Transport-Security", True, hsts, status, details,
            "Garanta que max-age seja longo (ex: 31536000) e use 'includeSubDomains'."
        ))
    else:
        results.append(HeaderCheckResult(
            "Strict-Transport-Security", False, None, "missing", "HSTS ausente.",
            "Adicione este cabeçalho para forçar conexões via HTTPS e prevenir ataques de downgrade."
        ))

    # 2. Content-Security-Policy (CSP)
    csp = response_headers.get("Content-Security-Policy")
    if csp:
        status = "ok"
        details = "CSP está presente."
        if "unsafe-inline" in csp.lower() or "unsafe-eval" in csp.lower():
            status = "weak"
            details = "CSP presente mas permite diretivas 'unsafe-inline' ou 'unsafe-eval'."
        results.append(HeaderCheckResult(
            "Content-Security-Policy", True, csp, status, details,
            "Tente restringir o CSP ao máximo, removendo 'unsafe-inline' e especificando domínios confiáveis."
        ))
    else:
        results.append(HeaderCheckResult(
            "Content-Security-Policy", False, None, "missing", "CSP ausente.",
            "Um CSP forte ajuda a mitigar ataques de Cross-Site Scripting (XSS) e injeção de dados."
        ))

    # 3. X-Frame-Options
    xfo = response_headers.get("X-Frame-Options")
    if xfo:
        status = "ok"
        details = f"X-Frame-Options configurado como {xfo}."
        results.append(HeaderCheckResult(
            "X-Frame-Options", True, xfo, status, details,
            "Use 'DENY' ou 'SAMEORIGIN' para evitar ataques de Clickjacking."
        ))
    else:
        results.append(HeaderCheckResult(
            "X-Frame-Options", False, None, "missing", "X-Frame-Options ausente.",
            "Sem este cabeçalho, seu site pode ser carregado em um iframe por terceiros, facilitando Clickjacking."
        ))

    # 4. X-Content-Type-Options
    xcto = response_headers.get("X-Content-Type-Options")
    if xcto and xcto.lower() == "nosniff":
        results.append(HeaderCheckResult(
            "X-Content-Type-Options", True, xcto, "ok", "Configurado corretamente como 'nosniff'.",
            "Mantendo o 'nosniff', o navegador não tentará adivinhar o tipo de conteúdo (MIME sniffing)."
        ))
    else:
        results.append(HeaderCheckResult(
            "X-Content-Type-Options", bool(xcto), xcto, "missing" if not xcto else "weak",
            "X-Content-Type-Options ausente ou incorreto.",
            "Configure como 'nosniff' para evitar que o navegador execute arquivos com tipos MIME incorretos."
        ))

    # 5. Referrer-Policy
    rp = response_headers.get("Referrer-Policy")
    if rp:
        results.append(HeaderCheckResult(
            "Referrer-Policy", True, rp, "ok", f"Configurado como {rp}.",
            "Escolha políticas mais restritivas como 'strict-origin-when-cross-origin' ou 'no-referrer'."
        ))
    else:
        results.append(HeaderCheckResult(
            "Referrer-Policy", False, None, "missing", "Referrer-Policy ausente.",
            "Ajuda a controlar quais informações de referência são enviadas ao sair do seu site."
        ))

    return results
