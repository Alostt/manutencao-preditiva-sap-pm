# 🏭 Manutenção Preditiva Integrada ao SAP PM com IA

Projeto de portfólio que prevê falhas em equipamentos a partir de dados de sensores e **simula** a integração com o **SAP PM** (Notificações/Ordens).
Inclui dataset sintético, código de treino do modelo, API de predição e um dashboard simples.

## 📌 Descrição
- **Entrada**: vibração, temperatura e pressão por equipamento ao longo do tempo.
- **Saída**: probabilidade de falha em curto prazo e nível de risco.
- **Integração (simulada)**: geração de payloads prontos para SAP PM via OData/REST/BAPI (mock).

## ⚙️ Tecnologias
- Python 3.10+
- scikit-learn, pandas, numpy, joblib
- matplotlib (visualizações)
- FastAPI + Uvicorn (API opcional)
- Streamlit (dashboard opcional)

## 🎯 Objetivos
1. Treinar um modelo de ML e salvar em `models/model.joblib`.
2. Exibir métricas (ROC AUC e classification_report).
3. Simular abertura de Notificação/Ordem no SAP PM com payloads prontos para uso.

## 📊 Resultados (exemplo esperado)
- ROC AUC e relatório de classificação no treino.
- Priorização de ativos de maior risco no dashboard.
- Logs de "envio" ao SAP PM (mock).

## 📁 Estrutura
```
manutencao-preditiva-sap-pm
├── README.md
├── requirements.txt
├── data/
│   └── sensores.csv
├── models/
│   └── model.joblib                # (gerado após treino)
├── notebooks/
│   └── modelo.ipynb
├── src/
│   ├── train_model.py
│   ├── predict_service.py          # API opcional via FastAPI
│   └── integracao_sap_pm.py        # simulação de integração
└── dashboard/
    └── streamlit_app.py
```

## 🚀 Como executar (passo a passo)
1) Instalar dependências:
```bash
pip install -r requirements.txt
```
2) Treinar o modelo:
```bash
python src/train_model.py
```
3) (Opcional) Subir a API de predição:
```bash
uvicorn src.predict_service:app --reload
```
4) (Opcional) Rodar o dashboard:
```bash
streamlit run dashboard/streamlit_app.py
```

## 🔗 Integração SAP PM (simulada)
Use `src/integracao_sap_pm.py` para montar o **payload** de criação de **Notificação** (ex.: QMEL) ou **Ordem** (ex.: AUFK) com campos típicos (equipamento, descrição, prioridade, data/hora, responsável). O envio é **mockado** (imprime/loga), mas o formato está pronto para adaptação para **BAPIs**/**OData**/**REST** reais.

> **Observação**: os dados são simulados e o projeto é de demonstração para portfólio.