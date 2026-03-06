
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os

class PhishingDetector:
    def __init__(self, model_path="ai_engine/phishing_model.pkl", vectorizer_path="ai_engine/tfidf_vectorizer.pkl"):
        self.model = None
        self.vectorizer = None
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path

    def train_model(self, emails, labels):
        # Para um modelo real, 'emails' seriam o texto do email e 'labels' seriam 0 (legítimo) ou 1 (phishing)
        # Este é um exemplo simplificado.
        df = pd.DataFrame({"email_text": emails, "label": labels})

        X_train, X_test, y_train, y_test = train_test_split(df["email_text"], df["label"], test_size=0.2, random_state=42)

        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
        X_train_vectorized = self.vectorizer.fit_transform(X_train)

        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train_vectorized, y_train)

        # Avaliação do modelo
        X_test_vectorized = self.vectorizer.transform(X_test)
        y_pred = self.model.predict(X_test_vectorized)
        print("\nRelatório de Classificação:")
        print(classification_report(y_test, y_pred))

        # Salvar o modelo e o vetorizador
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.vectorizer, self.vectorizer_path)
        print(f"Modelo salvo em {self.model_path}")
        print(f"Vectorizer salvo em {self.vectorizer_path}")

    def load_model(self):
        if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
            self.model = joblib.load(self.model_path)
            self.vectorizer = joblib.load(self.vectorizer_path)
            print("Modelo e vetorizador carregados com sucesso.")
        else:
            print("Modelo ou vetorizador não encontrados. Treine o modelo primeiro.")

    def predict(self, email_text):
        if not self.model or not self.vectorizer:
            self.load_model()
            if not self.model or not self.vectorizer:
                return "Modelo não carregado. Não é possível prever."

        email_vectorized = self.vectorizer.transform([email_text])
        prediction = self.model.predict(email_vectorized)
        return "Phishing" if prediction[0] == 1 else "Legítimo"

if __name__ == '__main__':
    detector = PhishingDetector()

    # Exemplo de dados de treinamento (simulado)
    sample_emails = [
        "Ganhe um milhão de dólares! Clique aqui agora!",
        "Sua conta bancária foi comprometida. Atualize suas informações.",
        "Reunião de equipe amanhã às 10h. Agenda anexa.",
        "Fatura de serviços de TI para o mês de fevereiro.",
        "URGENTE: Sua senha expirou. Clique para redefinir.",
        "Confirmação de pedido #12345. Obrigado pela compra."
    ]
    sample_labels = [1, 1, 0, 0, 1, 0] # 1 para phishing, 0 para legítimo

    # Treinar o modelo (isso criará os arquivos .pkl)
    detector.train_model(sample_emails, sample_labels)

    # Testar o modelo carregado
    print("\nTestando previsões:")
    print(f"Email 1: {detector.predict('Sua conta será suspensa se você não clicar neste link.')}")
    print(f"Email 2: {detector.predict('Relatório mensal de vendas.')}")
    print(f"Email 3: {detector.predict('Parabéns, você ganhou um prêmio! Responda para resgatar.')}")
