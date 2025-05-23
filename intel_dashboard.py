import yfinance as yf
import streamlit as st
import pandas as pd
import datetime

# --- FONCTION POUR INTERPRÉTER LES RATIOS ---
def analyser_ratios(ratios):
    recommandations = []

    if ratios["PER"] != "N/A":
        if ratios["PER"] < 15:
            recommandations.append("✔️ Valorisation faible (PER < 15)")
        elif ratios["PER"] > 25:
            recommandations.append("⚠️ PER élevé, possible surévaluation")

    if ratios["ROE"] != "N/A" and ratios["ROE"] > 15:
        recommandations.append("✔️ Bonne rentabilité (ROE > 15%)")

    if ratios["Dividende"] != "N/A" and ratios["Dividende"] > 3:
        recommandations.append("✔️ Bon rendement (> 3%)")

    if ratios["Dette/Capitaux propres"] != "N/A" and ratios["Dette/Capitaux propres"] > 100:
        recommandations.append("⚠️ Niveau d’endettement élevé")

    return recommandations if recommandations else ["ℹ️ Ratios dans la moyenne."]

# --- CONFIG STREAMLIT ---
st.set_page_config(page_title="Analyse Intel", layout="centered")
st.title("📊 Analyse Boursière : Intel Corporation (INTC)")

# --- RÉCUPÉRATION DES DONNÉES ---
ticker = "INTC"
intel = yf.Ticker(ticker)
info = intel.info

# --- EXTRACTION DES DONNÉES ---
ratios = {
    "Nom": info.get("longName", "N/A"),
    "Cours actuel": info.get("currentPrice", "N/A"),
    "PER": info.get("trailingPE", "N/A"),
    "Dividende": round(info.get("dividendYield", 0) * 100, 2) if info.get("dividendYield") else "N/A",
    "ROE": round(info.get("returnOnEquity", 0) * 100, 2) if info.get("returnOnEquity") else "N/A",
    "Dette/Capitaux propres": info.get("debtToEquity", "N/A"),
    "Croissance bénéfice (%)": round(info.get("earningsQuarterlyGrowth", 0) * 100, 2) if info.get("earningsQuarterlyGrowth") else "N/A"
}

# --- AFFICHAGE DES RATIOS ---
st.subheader("📌 Ratios financiers")
df_ratios = pd.DataFrame.from_dict(ratios, orient='index', columns=["Valeur"])
st.table(df_ratios)

# --- INTERPRÉTATION SIMPLIFIÉE (IA locale) ---
st.subheader("🧠 Interprétation automatique")
analyses = analyser_ratios(ratios)
for a in analyses:
    st.write(a)

# --- GRAPHIQUE DU COURS ---
st.subheader("📈 Historique du cours de l'action")
hist = intel.history(period="6mo")
st.line_chart(hist["Close"])

st.caption("Données : Yahoo Finance")
