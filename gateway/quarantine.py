
import imaplib
import yaml
import os
from dotenv import load_dotenv

load_dotenv()

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def move_to_quarantine(email_id, mail):
    config = load_config()
    quarantine_folder = config["email_server"]["quarantine_folder"]

    try:
        # Criar a pasta de quarentena se não existir
        mail.create(quarantine_folder)
    except mail.error as e:
        if "already exists" not in str(e):
            print(f"Erro ao criar pasta de quarentena: {e}")
            return False

    try:
        mail.copy(email_id, quarantine_folder)
        mail.store(email_id, '+FLAGS', '\\Deleted')
        mail.expunge()
        print(f"Email {email_id} movido para a quarentena.")
        return True
    except Exception as e:
        print(f"Erro ao mover email para quarentena: {e}")
        return False

if __name__ == '__main__':
    # Exemplo de uso (para testes)
    config = load_config()
    mail = imaplib.IMAP4_SSL(config['email_server']['imap_server'])
    mail.login(config['email_server']['username'], os.getenv(config['email_server']['password_env_var']))
    mail.select('inbox')
    # Suponha que você tenha um email_id para mover
    # status, email_ids = mail.search(None, 'ALL')
    # email_id_list = email_ids[0].split()
    # if email_id_list:
    #     move_to_quarantine(email_id_list[-1], mail) # Move o último email para quarentena
    mail.logout()
