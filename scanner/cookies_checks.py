from dataclasses import dataclass, field
from typing import List, Dict
import requests

@dataclass
class CookieCheckResult:
    name: str
    secure: bool
    httponly: bool
    samesite: str
    issues: List[str] = field(default_factory=list)

def check_cookies(cookies: requests.cookies.RequestsCookieJar) -> List[CookieCheckResult]:
    """Verifica as flags de segurança dos cookies encontrados na resposta."""
    results = []
    
    for cookie in cookies:
        issues = []
        if not cookie.secure:
            issues.append("Cookie sem flag 'Secure' (pode ser enviado via HTTP).")
        if not getattr(cookie, 'has_nonstandard_attr', lambda x: False)('HttpOnly') and not cookie._rest.get('HttpOnly', False) and 'httponly' not in [k.lower() for k in cookie._rest.keys()]:
            # Nota: requests as vezes esconde HttpOnly no _rest
            is_httponly = False
            # O objeto Cookie do requests é um pouco chato com HttpOnly, 
            # as vezes ele está em _rest ou como um atributo não padrão
            if 'HttpOnly' in cookie._rest or 'httponly' in [k.lower() for k in cookie._rest.keys()]:
                is_httponly = True
            
            if not is_httponly:
                issues.append("Cookie sem flag 'HttpOnly' (acessível via JavaScript/XSS).")
        else:
            is_httponly = True

        # Re-check HttpOnly de forma mais robusta se necessário
        # Em muitos casos com o Jar do requests, se ele não está explícito, o requests não expõe fácil
        # Mas para o MVP educacional, verificamos o que o objeto nos dá
        
        results.append(CookieCheckResult(
            name=cookie.name,
            secure=cookie.secure,
            httponly=cookie.get_nonstandard_attr('HttpOnly') is not None or 'HttpOnly' in cookie._rest,
            samesite=cookie._rest.get('SameSite', 'Not specified'),
            issues=issues
        ))
        
    return results

def check_cookies_from_headers(headers: Dict[str, str]) -> List[CookieCheckResult]:
    """
    Forma alternativa: analisar diretamente o cabeçalho Set-Cookie se o Jar for insuficiente.
    """
    # Para propósitos educacionais, o RequestsCookieJar costuma ser suficiente se o requests seguiu o redirect
    # Mas se precisarmos de precisão nos atributos crus, poderíamos fazer parse manual de headers['Set-Cookie']
    pass
