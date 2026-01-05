import urllib.parse

def normalize_url(url: str) -> str:
    """
    Normaliza a URL para garantir que tenha o esquema (http/https).
    Se não tiver, assume https por padrão.
    """
    url = url.strip()
    if not url:
        return ""
    
    parsed = urllib.parse.urlparse(url)
    
    # Se não houver esquema (ex: "google.com"), adiciona https://
    if not parsed.scheme:
        if url.startswith("//"):
            url = "https:" + url
        else:
            url = "https://" + url
            
    return url
