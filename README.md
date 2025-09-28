# 📈 BTC Predictor API + UI

Este proyecto implementa un sistema de predicción para el precio de Bitcoin usando **Python, FastAPI y Streamlit**, empaquetado en **Docker** para fácil despliegue.

---

## 📂 Estructura del proyecto
📂 app/
├── main.py       # API principal con FastAPI
├── ui.py         # Interfaz con Streamlit
└── utils.py      # Funciones auxiliares
Dockerfile
requirements.txt
docker-compose.yml
README.md

---

## ⚙️ Instalación y ejecución local

### 1. Clonar el repositorio
```bash
git https://github.com/Darally06/Predictor_VOL_BTC.git
```

### 2. Crear entorno virtual (opcional)

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar API

```bash
uvicorn app.main:app --reload
```

### 5. Ejecutar UI

```bash
streamlit run app/ui.py
```

---

## 🐳 Ejecución con Docker

### 1. Build del contenedor

```bash
docker build -t btc-app .
```

### 2. Levantar el contenedor

```bash
docker run -p 8000:8000 btc-app
```

Si usas `docker-compose`:

```bash
docker-compose up --build
```

---

## 🌍 Endpoints principales

* **API Docs (Swagger):** `http://localhost:8000/docs`
* **Streamlit UI:** `http://localhost:8501`

---

---

## ✨ Autores

* Daniella GUerra

```