
import os
import hashlib

def calculate_file_hash(file_content, hash_algorithm="sha256"):
    """Calcula o hash de um conteúdo de arquivo."""
    hasher = hashlib.new(hash_algorithm)
    hasher.update(file_content)
    return hasher.hexdigest()

def is_dangerous_extension(filename):
    """Verifica se a extensão do arquivo é perigosa."""
    dangerous_extensions = [
        ".exe", ".bat", ".cmd", ".scr", ".vbs", ".js", ".jar", ".msi", ".hta",
        ".com", ".pif", ".gadget", ".ws", ".wsf", ".sh", ".csh", ".ksh",
        ".app", ".dmg", ".apk", ".bin", ".run", ".deb", ".rpm"
    ]
    _, ext = os.path.splitext(filename)
    return ext.lower() in dangerous_extensions

def scan_attachment(attachment_data):
    """Simula a verificação de um anexo.
    Retorna um dicionário com o status da verificação.
    """
    filename = attachment_data["filename"]
    content = attachment_data["payload"]
    file_hash = calculate_file_hash(content)

    results = {
        "filename": filename,
        "hash": file_hash,
        "is_dangerous_extension": is_dangerous_extension(filename),
        "status": "Limpo" # Default
    }

    if results["is_dangerous_extension"]:
        results["status"] = "Malicioso (Extensão Perigosa)"
    # else:
    #     # Aqui seria a integração com VirusTotal ou outro AV
    #     # Exemplo: virus_total_report = query_virustotal(file_hash)
    #     # if virus_total_report and virus_total_report['positives'] > 0:
    #     #     results['status'] = 'Malicioso (VirusTotal)'

    return results

if __name__ == '__main__':
    # Exemplo de uso
    print("Testando scanner de anexos...")

    # Anexo seguro
    safe_attachment = {
        "filename": "documento.pdf",
        "payload": b"Conteudo seguro do PDF"
    }
    print(f"\nAnexo: {safe_attachment['filename']}")
    print(scan_attachment(safe_attachment))

    # Anexo perigoso
    dangerous_attachment = {
        "filename": "virus.exe",
        "payload": b"Conteudo de um executavel malicioso"
    }
    print(f"\nAnexo: {dangerous_attachment['filename']}")
    print(scan_attachment(dangerous_attachment))

    # Anexo com extensão desconhecida
    unknown_attachment = {
        "filename": "script.py",
        "payload": b"print(\'Hello\')"
    }
    print(f"\nAnexo: {unknown_attachment['filename']}")
    print(scan_attachment(unknown_attachment))
