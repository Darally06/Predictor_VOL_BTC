import streamlit as st
import requests
import json
import plotly.express as px
import numpy as np
import pandas as pd

API_URL = "http://localhost:8000/predict"

st.title("📊 Predicción de Volatilidad BTC")
st.write("Esta calculadora predice la volatilidad en un horizonte de 7 días, dadas las volatilidades en una ventana de tiempo.")


st.write("🔹Selecciona la ventana de tiempo:")

# Selección de ventana
ventana = st.selectbox("Ventana de tiempo (días):", [7, 14, 21, 28])

# Caja de texto para que el usuario ingrese la lista
st.write(f"🔹Ingrese una lista con {ventana} valores de volatilidad anualizada (ej: [0.45, 0.41, 0.42, ...])")
vol_input = st.text_area("Valores de volatilidad:", value="[]")

# Botón para predecir
if st.button("Predecir"):
    try:
        # Intentar parsear la lista
        volatilidad_lista = json.loads(vol_input)
        
        # Validar longitud
        if not isinstance(volatilidad_lista, list):
            st.error("❌ El formato debe ser una lista, por ejemplo: [0.45, 0.41, 0.42]")
        elif len(volatilidad_lista) != ventana:
            st.error(f"❌ Debes ingresar exactamente {ventana} valores, pero recibiste {len(volatilidad_lista)}")
        else:
            # Convertir lista en diccionario con claves day_1...day_N
            volatilidad_dict = {f"day_{i+1}": val for i, val in enumerate(volatilidad_lista)}
            
            payload = {
                "ventana": ventana,
                "volatilidad": volatilidad_dict
            }
            
            # Llamar a la API
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                pred = response.json()["prediccion_final"]
                pred = np.array(pred).flatten().tolist()

                st.success("✅ Predicciones generadas con éxito")
                st.write("Horizontes futuros (7 días):")

                # Crear eje x con la misma longitud
                dias = list(range(1, len(pred) + 1))
                df = pd.DataFrame({"Día": dias, "Predicción": pred})
                fig = px.line(df, x="Día", y="Predicción", markers=True, title="Predicciones de BTC")
                fig.update_layout(xaxis_title="Días", yaxis_title="Precio predicho")
                st.plotly_chart(fig)

                st.json({"prediccion_final": pred})  # mostrar JSON
            else:
                st.error(f"Error en la API: {response.status_code}")
    except json.JSONDecodeError:
        st.error("❌ Formato inválido. Asegúrate de que sea una lista JSON, por ejemplo: [0.45, 0.41, 0.42]")
