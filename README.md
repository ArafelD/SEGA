# Secure Email Gateway com IA

Projeto de cibersegurança desenvolvido em Python que simula um **Secure Email Gateway (SEG)** utilizado por empresas de segurança para proteção contra:

- Phishing
- Malware em anexos
- URLs maliciosas
- Spoofing de domínio

O sistema analisa automaticamente emails recebidos utilizando regras de segurança e inteligência artificial.

---

# Arquitetura

O gateway intercepta emails e executa múltiplas camadas de análise:

1. Verificação de domínio
2. Detecção de phishing com IA
3. Análise de URLs
4. Scan de anexos
5. Classificação de risco

Emails maliciosos são enviados automaticamente para quarentena.

---

# Tecnologias utilizadas

- Python
- NLP
- Scikit-learn
- Docker
- Linux
- Email Protocols (IMAP/SMTP)
- Cybersecurity Analysis

---

# Instalação

Clone este repositório


Entre na pasta:

cd secure-email-gateway-ai

Instale dependências:

pip install -r requirements.txt

Execute o gateway:

python gateway/email_listener.py


---

# Funcionalidades

✔ Detecção de phishing  
✔ Verificação de domínios suspeitos  
✔ Scanner de URLs  
✔ Análise de anexos  
✔ Sistema de quarentena  
✔ Logs de segurança  

---

# Futuras melhorias

- Integração com VirusTotal API
- Machine Learning avançado
- Dashboard web
- Sistema de alertas em tempo real
- Integração com SIEM

---

# Autor

Projeto desenvolvido para portfólio de cibersegurança.
