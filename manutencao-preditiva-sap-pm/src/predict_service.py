import os
import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field

MODEL_PATH = os.environ.get("MODEL_PATH", "models/model.joblib")

app = FastAPI(title="API de Predição - Manutenção Preditiva")

class SensorInput(BaseModel):
    vibration_rms: float = Field(..., example=5.1)
    temperature_c: float = Field(..., example=72.3)
    pressure_bar: float = Field(..., example=3.4)
    equipment_id: str = Field(..., example="EQT-007")

class Prediction(BaseModel):
    equipment_id: str
    failure_proba: float
    risk_level: str

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError("Modelo não encontrado. Treine primeiro com src/train_model.py")
    return joblib.load(MODEL_PATH)

model = None

@app.on_event("startup")
def startup_event():
    global model
    model = load_model()

@app.post("/predict", response_model=Prediction)
def predict(inp: SensorInput):
    proba = model.predict_proba([[inp.vibration_rms, inp.temperature_c, inp.pressure_bar]])[0,1]
    risk = "ALTO" if proba >= 0.7 else "MÉDIO" if proba >= 0.4 else "BAIXO"
    return Prediction(equipment_id=inp.equipment_id, failure_proba=float(proba), risk_level=risk)