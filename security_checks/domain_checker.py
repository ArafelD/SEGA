
import dns.resolver
import dkimpy

def check_spf(domain):
    try:
        txt_records = dns.resolver.resolve(domain, 'TXT')
        for txt_record in txt_records:
            if "v=spf1" in txt_record.to_text():
                return f"SPF Record Found: {txt_record.to_text()}"
        return "No SPF Record Found"
    except dns.resolver.NoAnswer:
        return "No SPF Record Found"
    except Exception as e:
        return f"Error checking SPF: {e}"

def check_dkim(domain):
    # DKIM records are typically found under a selector, e.g., selector._domainkey.example.com
    # This function would need a selector to perform a full check.
    # For simplicity, we'll just check for the presence of _domainkey TXT records.
    try:
        txt_records = dns.resolver.resolve(f"_domainkey.{domain}", 'TXT')
        for txt_record in txt_records:
            if "v=DKIM1" in txt_record.to_text():
                return f"DKIM Record Found: {txt_record.to_text()}"
        return "No DKIM Record Found (or no common selector)"
    except dns.resolver.NoAnswer:
        return "No DKIM Record Found (or no common selector)"
    except Exception as e:
        return f"Error checking DKIM: {e}"

def check_dmarc(domain):
    try:
        txt_records = dns.resolver.resolve(f"_dmarc.{domain}", 'TXT')
        for txt_record in txt_records:
            if "v=DMARC1" in txt_record.to_text():
                return f"DMARC Record Found: {txt_record.to_text()}"
        return "No DMARC Record Found"
    except dns.resolver.NoAnswer:
        return "No DMARC Record Found"
    except Exception as e:
        return f"Error checking DMARC: {e}"

def perform_domain_checks(domain):
    results = {
        "spf": check_spf(domain),
        "dkim": check_dkim(domain),
        "dmarc": check_dmarc(domain)
    }
    return results

if __name__ == '__main__':
    # Exemplo de uso
    test_domain = "google.com"
    print(f"Verificando domínio: {test_domain}")
    results = perform_domain_checks(test_domain)
    for check, result in results.items():
        print(f"  {check.upper()}: {result}")

    test_domain_no_dmarc = "example.com"
    print(f"\nVerificando domínio: {test_domain_no_dmarc}")
    results_no_dmarc = perform_domain_checks(test_domain_no_dmarc)
    for check, result in results_no_dmarc.items():
        print(f"  {check.upper()}: {result}")
