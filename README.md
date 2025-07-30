# 🧪 Clinical Study Tracker

Eine vollständige Webanwendung zur **Verwaltung und Analyse klinischer Studiendaten** – inklusive Patienteninformationen, Follow-Up-Beobachtungen und CSV-Export zur Weiterverarbeitung in R oder Python.

## 🚀 Funktionen

- ✅ RESTful API mit **FastAPI**
- 🗃️ PostgreSQL-Datenbank mit **SQLAlchemy ORM**
- 📥 CSV-Upload für Follow-Up-Daten
- 📤 CSV-Export zur Analyse mit R oder Pandas
- 🐳 Vollständig **Dockerisiert** für einfache Installation
- 📑 Automatisch generierte API-Dokumentation via Swagger
- 🔒 Validierung durch **Pydantic**

---

## 🔁 Typischer Workflow

1. Registrierung von Patient:innen
2. Hochladen von Follow-Up-Daten im CSV-Format
3. Datenanalyse über Endpunkte / CSV-Export
4. Verwendung in **RStudio**, **Jupyter**, oder **Excel**

---

## ⚙️ Tech Stack

| Komponente      | Technologie            |
|----------------|------------------------|
| Backend         | FastAPI (Python 3.11)  |
| Datenbank       | PostgreSQL             |
| ORM             | SQLAlchemy             |
| CSV-Analyse     | Pandas                 |
| Deployment      | Docker & Docker Compose|

---

## 🧰 Installation

```bash
git clone https://github.com/roshanzadeh1994/clinical-study.git
```
```bash
cd clinical-study-tracker
```
```bash
docker-compose up --build
```
