import os
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class RequestModel(BaseModel):
    ventana: int
    volatilidad: dict

@app.post("/predict")
def predict(request: RequestModel):
    ventana = request.ventana
    volatilidad = request.volatilidad

    # --- Validación ---
    model_dir = f"app/models/ventana_{ventana}"
    if not os.path.exists(model_dir):
        raise HTTPException(status_code=400, detail=f"No existe modelo entrenado para ventana {ventana} días")

    # --- Cargar modelos ---
    model_files = [f for f in os.listdir(model_dir) if f.endswith(".pkl")]
    if not model_files:
        raise HTTPException(status_code=500, detail=f"No hay modelos guardados en {model_dir}")

    X_input = np.array(list(volatilidad.values())).reshape(1, -1)

    preds = []
    for fname in model_files:
        model_path = os.path.join(model_dir, fname)
        with open(model_path, "rb") as f:
            model = joblib.load(f)

        yhat = model.predict(X_input)  # asumiendo que devuelve 7 horizontes
        preds.append(yhat)

    # --- Promedio entre folds ---
    preds = np.array(preds)  # shape: (n_models, 7)
    avg_pred = preds.mean(axis=0).tolist()

    return {"ventana": ventana, "prediccion_final": avg_pred}
