
import email
from email.header import decode_header
import os

def parse_email(msg):
    email_data = {
        "subject": "",
        "from": "",
        "to": "",
        "date": "",
        "body_plain": "",
        "body_html": "",
        "attachments": []
    }

    # Decodificar cabeçalhos
    for header in ['Subject', 'From', 'To', 'Date']:
        if msg[header]:
            decoded_header = decode_header(msg[header])
            header_str = ""
            for part, charset in decoded_header:
                if isinstance(part, bytes):
                    try:
                        header_str += part.decode(charset if charset else 'utf-8')
                    except:
                        header_str += part.decode('latin-1', errors='ignore')
                else:
                    header_str += part
            email_data[header.lower()] = header_str

    # Extrair corpo e anexos
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get("Content-Disposition"))

            # Corpo do email
            if ctype == "text/plain" and "attachment" not in cdispo:
                email_data["body_plain"] = part.get_payload(decode=True).decode()
            elif ctype == "text/html" and "attachment" not in cdispo:
                email_data["body_html"] = part.get_payload(decode=True).decode()
            # Anexos
            elif "attachment" in cdispo:
                filename = part.get_filename()
                if filename:
                    email_data["attachments"].append({
                        "filename": filename,
                        "content_type": ctype,
                        "payload": part.get_payload(decode=True)
                    })
    else:
        ctype = msg.get_content_type()
        if ctype == "text/plain":
            email_data["body_plain"] = msg.get_payload(decode=True).decode()
        elif ctype == "text/html":
            email_data["body_html"] = msg.get_payload(decode=True).decode()

    return email_data

if __name__ == '__main__':
    # Exemplo de uso (para testes)
    # Crie um email de exemplo para testar a função
    msg_str = """
From: Sender <sender@example.com>
To: Recipient <recipient@example.com>
Subject: Test Email with Attachment
Date: Thu, 05 Mar 2026 10:00:00 -0300
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="boundary123"

--boundary123
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: quoted-printable

Este é um email de teste com um anexo.

--boundary123
Content-Type: text/html; charset="utf-8"
Content-Transfer-Encoding: quoted-printable

<html><body><p>Este é um email de teste com um anexo.</p></body></html>

--boundary123
Content-Type: text/plain; name="anexo.txt"
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename="anexo.txt"

SGVsbG8sIHRoaXMgZmlsZSBpcyBhbiBhdHRhY2htZW50Lg==
--boundary123--
"""
    msg = email.message_from_string(msg_str)
    parsed_data = parse_email(msg)
    print(parsed_data)

    # Para um email sem anexo
    msg_str_no_attach = """
From: NoAttach <noattach@example.com>
To: Recipient <recipient@example.com>
Subject: Simple Test Email
Date: Thu, 05 Mar 2026 10:05:00 -0300
Content-Type: text/plain; charset="utf-8"

Este é um email simples sem anexo.
"""
    msg_no_attach = email.message_from_string(msg_str_no_attach)
    parsed_data_no_attach = parse_email(msg_no_attach)
    print(parsed_data_no_attach)
