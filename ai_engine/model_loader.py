
from ai_engine.phishing_detector import PhishingDetector
import os

def load_or_train_model():
    detector = PhishingDetector()
    if not os.path.exists(detector.model_path) or not os.path.exists(detector.vectorizer_path):
        print("Modelo de phishing não encontrado. Treinando um modelo de exemplo...")
        # Exemplo de dados de treinamento (simulado)
        sample_emails = [
            "Ganhe um milhão de dólares! Clique aqui agora!",
            "Sua conta bancária foi comprometida. Atualize suas informações.",
            "Reunião de equipe amanhã às 10h. Agenda anexa.",
            "Fatura de serviços de TI para o mês de fevereiro.",
            "URGENTE: Sua senha expirou. Clique para redefinir.",
            "Confirmação de pedido #12345. Obrigado pela compra.",
            "Prezado cliente, sua conta foi bloqueada. Por favor, verifique seus dados aqui.",
            "Atualização de segurança: Por favor, clique no link para verificar sua identidade.",
            "Seu pacote está atrasado. Rastreie-o neste link.",
            "Oferta exclusiva! Ganhe um iPhone grátis!",
            "Convite para webinar sobre cibersegurança.",
            "Relatório de despesas do último trimestre."
        ]
        sample_labels = [1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0] # 1 para phishing, 0 para legítimo
        detector.train_model(sample_emails, sample_labels)
    else:
        detector.load_model()
    return detector

if __name__ == '__main__':
    print("Carregando ou treinando o modelo de phishing...")
    phishing_detector = load_or_train_model()
    print("Modelo de phishing pronto.")
