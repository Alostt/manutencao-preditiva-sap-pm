import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

DATA_PATH = os.environ.get("DATA_PATH", "data/sensores.csv")
MODEL_PATH = os.environ.get("MODEL_PATH", "models/model.joblib")

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    return df

def build_pipeline():
    clf = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    )
    pipe = Pipeline([
        ("scaler", StandardScaler(with_mean=False)),
        ("model", clf)
    ])
    return pipe

def main():
    df = load_data(DATA_PATH)
    features = ["vibration_rms", "temperature_c", "pressure_bar"]
    X = df[features].values
    y = df["failure"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipe = build_pipeline()
    pipe.fit(X_train, y_train)

    y_proba = pipe.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= 0.5).astype(int)

    auc = roc_auc_score(y_test, y_proba)
    print("ROC AUC:", round(auc, 4))
    print(classification_report(y_test, y_pred, digits=4))

    # Save model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(pipe, MODEL_PATH)
    print(f"Modelo salvo em: {MODEL_PATH}")

    # Simple risk plot
    import matplotlib.pyplot as plt
    plt.figure()
    plt.hist(y_proba, bins=30)
    plt.title("Distribuição das probabilidades de falha (conjunto de teste)")
    plt.xlabel("Probabilidade de falha")
    plt.ylabel("Frequência")
    plt.tight_layout()
    os.makedirs("models", exist_ok=True)
    plt.savefig("models/prob_hist.png")
    print("Gráfico salvo em: models/prob_hist.png")

if __name__ == "__main__":
    main()