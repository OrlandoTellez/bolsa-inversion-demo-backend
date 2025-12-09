# Bolsa de valores inversión Nicaraguense demo — FastAPI

## Requisitos

* Python 3.10+
* pip
* (Opcional pero recomendado) entorno virtual **venv**

---

## Crear y activar entorno virtual

### 1. Crear entorno virtual

```bash
python3 -m venv .venv
```

### 2. Activar entorno

```bash
source .venv/bin/activate
```

> Si no aparece el prefijo `(venv)` en tu terminal, el entorno no está activo.

---

se puede usar para crear el archivo `requirements.txt`

```bash
pip freeze > requirements.txt
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Ejecutar el servidor

### Modo desarrollo con recarga automática (por defecto puerto 8000)

```bash
fastapi dev app/main.py
```

Esto levanta el proyecto en:

```
http://127.0.0.1:8000
```

---

## Ejecutar FastAPI con uvicorn (personalizando puerto)

### Ejemplo usando puerto **5050**

```bash
uvicorn app.main:app --reload --port 5050
```

### Ejecución estándar (puerto por defecto 8000)

```bash
uvicorn app.main:app --reload
```

---

## Documentación automática

FastAPI genera dos interfaces automáticamente:

* Swagger UI →
  [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

* ReDoc →
  [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

