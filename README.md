# 🧮 Predicción de Volatilidad BTC

Este proyecto permite predecir la volatilidad del precio de Bitcoin en un horizonte de 7 días, utilizando modelos entrenados sobre ventanas históricas de volatilidad anualizada. Incluye una API construida con FastAPI y una interfaz interactiva con Streamlit.

---

## Acciones
- Recibe una lista de volatilidades anualizadas en una ventana de tiempo (7, 14, 21 o 28 días).
- Predice la volatilidad futura para los próximos 7 días.
- Visualiza los resultados en una gráfica interactiva.
- Permite compartir la app vía web (Render).

---

## 📁 Estructura del proyecto

```
MINI_PRY_2/
├── app/
│   ├── main.py              # Backend FastAPI
│   ├── ui.py                # Frontend Streamlit
│   ├── models.py            # Definiciones de modelos
├── data/                    # Datos históricos de BTC
├── notebooks/               # Preprocesamiento, EDA, modelado
|  | figs/                   # Gráficas del rendimiento de modelos
|  | metricas/               # CSV de métricas
|  | models/                 # Joblib de modelos
|  1_preprocesamiento.ipynb  # Preprocesamiento de datos
|  2_EDA.ipynb               # Análisis exploratorio de datos
|  3_modelo.ipynb            # Ejecución de modelos por folds
├── Dockerfile               # Imagen Docker
├── requirements.txt         # Dependencias
├── start.sh                 # Script de arranque
└── render.yaml              # Configuración para Render
```

---

##  Para jecutar localmente

### 1. Clona el repositorio

```bash
git clone https://github.com/tu_usuario/mini_pry_2.git
cd mini_pry_2
```

### 2. Construye la imagen Docker

```bash
docker build -t btc-volatility-app .
```

### 3. Ejecuta el contenedor

```bash
docker run -p 8000:8000 -p 8501:8501 btc-volatility-app
```

- API: `http://localhost:8000/docs`
- Interfaz: `http://localhost:8501`

---

## 📦 Requisitos

- Python 3.10+
- Docker
- FastAPI, Streamlit, Joblib, NumPy, Pandas, Plotly

---

## 📬 Contacto

Creado por **Daniella**  
📍 Baranoa, Atlántico, Colombia  

```
