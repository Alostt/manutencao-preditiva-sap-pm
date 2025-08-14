import os
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Manutenção Preditiva", layout="wide")

st.title("📈 Dashboard - Manutenção Preditiva (Simulado)")

DATA_PATH = os.environ.get("DATA_PATH", "data/sensores.csv")
MODEL_PATH = os.environ.get("MODEL_PATH", "models/model.joblib")

@st.cache_data
def load_data(path):
    return pd.read_csv(path, parse_dates=["timestamp"])

def load_model(path):
    if not os.path.exists(path):
        st.warning("Modelo não encontrado. Treine primeiro executando: python src/train_model.py")
        return None
    return joblib.load(path)

df = load_data(DATA_PATH)
model = load_model(MODEL_PATH)

st.sidebar.header("Filtros")
equip = st.sidebar.multiselect("Equipamentos", sorted(df["equipment_id"].unique()))
if equip:
    df = df[df["equipment_id"].isin(equip)]

st.write("Registros:", len(df))

if model is not None:
    feats = df[["vibration_rms", "temperature_c", "pressure_bar"]]
    df["failure_proba"] = model.predict_proba(feats)[:,1]
    st.dataframe(df[["timestamp", "equipment_id", "vibration_rms", "temperature_c", "pressure_bar", "failure_proba"]].sort_values("failure_proba", ascending=False).head(50))

    st.subheader("Top 10 equipamentos por risco médio")
    top = (df.groupby("equipment_id")["failure_proba"].mean().sort_values(ascending=False).head(10)).reset_index()
    st.bar_chart(top.set_index("equipment_id"))
else:
    st.info("Treine o modelo para ver probabilidades de falha.")