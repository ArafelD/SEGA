
import json
import os
import datetime
import yaml

from gateway.email_parser import parse_email
from gateway.quarantine import move_to_quarantine
from security_checks.domain_checker import perform_domain_checks
from security_checks.attachment_scanner import scan_attachment
from security_checks.url_analyzer import analyze_url, extract_urls_from_text
from ai_engine.phishing_detector import PhishingDetector

LOG_FILE = "logs/email_logs.json"

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def log_email_event(log_entry):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def process_email(msg, mail_connection, email_id, phishing_detector):
    config = load_config()
    parsed_email = parse_email(msg)

    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "from": parsed_email["from"],
        "subject": parsed_email["subject"],
        "classification": "Seguro", # Default
        "details": []
    }

    is_suspicious = False

    # 1. Verificação de Domínio (SPF/DKIM/DMARC)
    if config["security_checks"]["spf_dkim_enabled"]:
        sender_domain = parsed_email["from"].split("@")[-1]
        domain_checks = perform_domain_checks(sender_domain)
        log_entry["details"].append({"check": "Domain Checks", "results": domain_checks})
        # Lógica simplificada para marcar como suspeito se não houver SPF/DKIM/DMARC
        if "No SPF Record Found" in domain_checks["spf"] or \
           "No DKIM Record Found" in domain_checks["dkim"] or \
           "No DMARC Record Found" in domain_checks["dmarc"]:
            is_suspicious = True
            log_entry["classification"] = "Suspeito"

    # 2. Análise de Phishing com IA
    if config["security_checks"]["phishing_detection_enabled"]:
        email_text_for_ai = parsed_email["subject"] + " " + parsed_email["body_plain"]
        phishing_prediction = phishing_detector.predict(email_text_for_ai)
        log_entry["details"].append({"check": "Phishing AI", "prediction": phishing_prediction})
        if phishing_prediction == "Phishing":
            is_suspicious = True
            log_entry["classification"] = "Malicioso"

    # 3. Análise de URLs
    if config["security_checks"]["url_analysis_enabled"]:
        urls_in_email = extract_urls_from_text(parsed_email["body_plain"] + " " + parsed_email["body_html"])
        url_analysis_results = []
        for url in urls_in_email:
            analysis = analyze_url(url)
            url_analysis_results.append(analysis)
            if analysis["status"] != "Limpo":
                is_suspicious = True
                if log_entry["classification"] != "Malicioso": # Não sobrescrever se já for malicioso
                    log_entry["classification"] = "Suspeito"
        log_entry["details"].append({"check": "URL Analysis", "results": url_analysis_results})

    # 4. Análise de Anexos
    if config["security_checks"]["attachment_scan_enabled"] and parsed_email["attachments"]:
        attachment_scan_results = []
        for attachment in parsed_email["attachments"]:
            scan_result = scan_attachment(attachment)
            attachment_scan_results.append(scan_result)
            if scan_result["status"] != "Limpo":
                is_suspicious = True
                log_entry["classification"] = "Malicioso"
        log_entry["details"].append({"check": "Attachment Scan", "results": attachment_scan_results})

    log_email_event(log_entry)

    if is_suspicious:
        print(f"Email suspeito/malicioso detectado: {parsed_email["subject"]}. Movendo para quarentena.")
        move_to_quarantine(email_id, mail_connection)
    else:
        print(f"Email seguro: {parsed_email["subject"]}. Entregando na caixa de entrada.")
        # Opcional: Marcar como lido ou mover para uma pasta de "processados"
        mail_connection.store(email_id, "+FLAGS", "\\Seen")

    return log_entry

