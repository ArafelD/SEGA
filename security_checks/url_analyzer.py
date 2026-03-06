
import re
from urllib.parse import urlparse

def is_suspicious_url(url):
    """Verifica se uma URL possui padrões suspeitos básicos."""
    suspicious_patterns = [
        r"bit\.ly", r"tinyurl\.com", r"goo\.gl", # Encurtadores de URL
        r"login\.[a-zA-Z0-9-]+\.com", # Padrões comuns de phishing para login
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", # Endereços IP em vez de domínios
        r"@"
    ]
    for pattern in suspicious_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return True
    return False

def analyze_url(url):
    """Analisa uma URL e retorna um status de segurança.
    Em um sistema real, isso integraria com APIs de reputação de URL (ex: Google Safe Browsing).
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    results = {
        "url": url,
        "domain": domain,
        "is_suspicious_pattern": is_suspicious_url(url),
        "status": "Limpo" # Default
    }

    if results["is_suspicious_pattern"]:
        results["status"] = "Suspeito (Padrão)"
    # else:
    #     # Aqui seria a integração com serviços de reputação de URL
    #     # Exemplo: reputation = query_url_reputation_service(url)
    #     # if reputation == "malicious":
    #     #     results["status"] = "Malicioso (Reputação)"

    return results

def extract_urls_from_text(text):
    """Extrai URLs de um texto usando regex."""
    # Regex para encontrar URLs (simplificado)
    url_pattern = r"https?://(?:[-\w.]|(?:%[0-9a-fA-F]{2}))+"
    return re.findall(url_pattern, text)

if __name__ == '__main__':
    print("Testando analisador de URL...")

    # URLs de exemplo
    test_urls = [
        "https://www.google.com",
        "http://bit.ly/malicious-link",
        "https://login.paypal.com.phishing.ru/",
        "http://192.168.1.1/admin",
        "https://safe.website.com/page?param=value",
        "http://example.com/redirect@malicious.com"
    ]

    for url in test_urls:
        analysis = analyze_url(url)
        print(f"\nURL: {url}")
        print(f"  Domínio: {analysis["domain"]}")
        print(f"  Padrão Suspeito: {analysis["is_suspicious_pattern"]}")
        print(f"  Status: {analysis["status"]}")

    sample_text = "Visite nosso site em https://www.example.com ou clique aqui: http://bit.ly/phish. Para mais informações, acesse https://secure.bank.com/login."
    print(f"\nExtraindo URLs do texto:\n{sample_text}")
    extracted = extract_urls_from_text(sample_text)
    print("URLs extraídas:", extracted)
    for url in extracted:
        print(f"  {url}: {analyze_url(url)['status']}")
