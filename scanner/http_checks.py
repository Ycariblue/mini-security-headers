from dataclasses import dataclass, field
from typing import List, Optional
import requests

@dataclass
class HTTPCheckResult:
    uses_https: bool
    redirects_http_to_https: bool
    https_issues: List[str] = field(default_factory=list)
    certificate_info: str = ""

def check_http_to_https_redirect(url: str) -> bool:
    """Verifica se uma URL HTTP redireciona para HTTPS."""
    if url.startswith("https://"):
        http_url = url.replace("https://", "http://", 1)
    else:
        http_url = "http://" + url if not url.startswith("http://") else url

    try:
        response = requests.get(http_url, allow_redirects=False, timeout=10)
        if 300 <= response.status_code < 400:
            location = response.headers.get("Location", "")
            if location.startswith("https://"):
                return True
            
            # Caso seja um redirecionamento relativo ou para outro domínio
            full_location = requests.compat.urljoin(http_url, location)
            return full_location.startswith("https://")
    except requests.exceptions.RequestException:
        pass
    return False

def check_https_and_transport(url: str) -> HTTPCheckResult:
    """Realiza verificações de transporte seguro (HTTPS)."""
    issues = []
    uses_https = url.startswith("https://")
    redirects = False
    cert_info = "Não foi possível obter detalhes do certificado."

    if not uses_https:
        issues.append("O site não está utilizando HTTPS como protocolo inicial.")
    
    # Verifica redirecionamento
    redirects = check_http_to_https_redirect(url)
    if not redirects and not uses_https:
        issues.append("O site não redireciona automaticamente HTTP para HTTPS.")

    try:
        # Faz uma requisição para verificar validade do SSL
        response = requests.get(url, timeout=10)
        if uses_https:
            cert_info = "Certificado parece válido (conexão estabelecida com sucesso)."
    except requests.exceptions.SSLError as e:
        issues.append(f"Erro de SSL/TLS: {str(e)}")
        cert_info = "Erro ao validar certificado."
    except requests.exceptions.RequestException as e:
        issues.append(f"Erro na requisição: {str(e)}")

    return HTTPCheckResult(
        uses_https=uses_https,
        redirects_http_to_https=redirects,
        https_issues=issues,
        certificate_info=cert_info
    )
