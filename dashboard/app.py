
import streamlit as st
import pandas as pd
import json
import os
import time

LOG_FILE = "logs/email_logs.json"

def load_logs():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        # Lidar com o caso de arquivo vazio ou JSON inválido
        try:
            return [json.loads(line) for line in f if line.strip()]
        except json.JSONDecodeError:
            st.error("Erro ao carregar logs: arquivo JSON inválido.")
            return []

def display_logs(logs):
    if not logs:
        st.info("Nenhum log disponível ainda.")
        return

    df = pd.DataFrame(logs)
    st.dataframe(df)

    st.subheader("Estatísticas de Classificação")
    classification_counts = df["classification"].value_counts()
    st.bar_chart(classification_counts)

st.set_page_config(layout="wide")
st.title("Secure Email Gateway Dashboard")

# Auto-refresh a cada 5 segundos
if st.button("Atualizar Logs Agora"):
    st.experimental_rerun()

st.write("Última atualização: ", time.ctime())

logs = load_logs()
display_logs(logs)

# Adicionar um placeholder para o auto-refresh
# st.empty().write(f"Atualizando em {st.session_state.countdown} segundos...")
# time.sleep(1)
# st.session_state.countdown -= 1
# if st.session_state.countdown <= 0:
#     st.session_state.countdown = 5
#     st.experimental_rerun()

