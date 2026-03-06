
import imaplib
import email
from gateway.email_processor import process_email

import os
import time
import yaml
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def connect_to_imap(config):
    try:
        mail = imaplib.IMAP4_SSL(config['email_server']['imap_server'])
        mail.login(config['email_server']['username'], os.getenv(config['email_server']['password_env_var']))
        return mail
    except Exception as e:
        print(f"Erro ao conectar ou fazer login no IMAP: {e}")
        return None

def fetch_emails(mail):
    mail.select(\'inbox\')
    status, email_ids = mail.search(None, \'UNSEEN\') # Busca emails não lidos
    email_id_list = email_ids[0].split()
    
    emails_to_process = []
    for email_id_raw in email_id_list:
        status, msg_data = mail.fetch(email_id_raw, \'(RFC822)\')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                emails_to_process.append((email_id_raw, msg))
    return emails_to_process

def main():
    config = load_config()
    phishing_detector = PhishingDetector()
    phishing_detector.load_model() # Carrega o modelo uma vez
    
    while True:
        mail = connect_to_imap(config)
        if mail:
            print("Buscando novos emails...")
            new_emails_with_ids = fetch_emails(mail)
            if new_emails_with_ids:
                print(f"Encontrados {len(new_emails_with_ids)} novos emails.")
                for email_id_raw, msg in new_emails_with_ids:
                    process_email(msg, mail, email_id_raw, phishing_detector)
            else:
                print("Nenhum email novo.")
            mail.logout()
        
        time.sleep(60) # Verifica a cada 60 segundos

if __name__ == '__main__':
    main()
