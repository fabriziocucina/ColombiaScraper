# 🇨🇴 Scraper de Leyes - Cámara de Representantes de Colombia

Este proyecto extrae automáticamente información de proyectos de ley publicados en el sitio oficial de la Cámara de Representantes de Colombia. Los datos se limpian y almacenan en una base de datos SQLite.

## 📦 Estructura del Proyecto

```
.
├── app/
│   ├── domain/
│   ├── infrastructure/
│   ├── utils/
│   └── config/
├── main.py
├── Dockerfile
├── docker-compose.yml
├── laws_colombia.db
└── README.md
```

## 🚀 Requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## ⚙️ Configuración

Antes de correr el scraper, asegúrate de tener creado el archivo vacío de SQLite en la raíz del proyecto:

```bash
touch laws_colombia.db
```

## 🐳 Ejecución con Docker Compose

Construye y ejecuta el scraper:

```bash
docker-compose up --build
```

Esto hará lo siguiente:

- Construirá una imagen Docker con tu scraper.
- Ejecutará el script principal (`main.py`) que:
  - Extrae los datos de los proyectos de ley.
  - Limpia y normaliza los datos.
  - Guarda el resultado en la base de datos `laws_colombia.db`.

> **Nota**: El archivo `laws_colombia.db` se montará en tu máquina local gracias al volumen configurado en `docker-compose.yml`.

## 📄 Acceso a los Datos

Puedes abrir la base de datos con herramientas como:

- [DB Browser for SQLite](https://sqlitebrowser.org/)
- Python:

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect("laws_colombia.db")
df = pd.read_sql_query("SELECT * FROM laws", conn)
print(df.head())
```

## ✏️ Personalización

- Para cambiar la cantidad de páginas que se scrapean, modifica la condición en `scrape_colombia_laws()` dentro del archivo `scraper_colombia.py`.
- Los selectores y rutas están configurados desde `config/colombia.yaml`.

## 📌 Autor

Desarrollado por Fabrizio Cucina.  
Para contacto profesional: fabriziocucina23@gmail.com
