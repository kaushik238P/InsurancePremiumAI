# InsurancePremiumAI

An end-to-end Machine Learning application for predicting insurance premiums using XGBoost, FastAPI, Streamlit, Docker, and Render.

## Live Demo

### Frontend

https://insurancepremiumai-frontend.onrender.com

### API

https://insurancepremiumai-api.onrender.com

### API Documentation

https://insurancepremiumai-api.onrender.com/docs

---

## Project Overview

InsurancePremiumAI predicts insurance premiums based on customer demographics, lifestyle factors, and financial information.

The project demonstrates a complete ML deployment workflow:

* Data Analysis and Feature Engineering
* Model Training using XGBoost
* REST API Development using FastAPI
* Interactive Frontend using Streamlit
* Containerization using Docker
* Multi-container orchestration using Docker Compose
* Docker Hub image publishing
* Cloud deployment using Render

---

## Architecture

```text
User
 │
 ▼
Streamlit Frontend
 │
 ▼
FastAPI Backend
 │
 ▼
Feature Engineering
 │
 ▼
XGBoost Model
 │
 ▼
Premium Prediction
```

---

## Tech Stack

### Machine Learning

* Python
* Pandas
* NumPy
* Scikit-Learn
* XGBoost

### Backend

* FastAPI
* Uvicorn
* Pydantic

### Frontend

* Streamlit
* Plotly

### Deployment

* Docker
* Docker Compose
* Docker Hub
* Render

---

## Project Structure

```text
InsurancePremiumAI
│
├── app.py
├── frontend.py
├── Dockerfile.api
├── Dockerfile.streamlit
├── docker-compose.yml
├── requirements-api.txt
├── requirements-frontend.txt
│
├── config/
├── data/
├── model/
├── schema/
├── services/
└── logs/
```

---

## Docker Images

### Backend

docker pull kaushik238p/insurancepremiumai-api:latest

### Frontend

docker pull kaushik238p/insurancepremiumai-frontend:latest

---

## Running Locally

### Clone Repository

```bash
git clone https://github.com/kaushik238P/InsurancePremiumAI.git
cd InsurancePremiumAI
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements-api.txt
pip install -r requirements-frontend.txt
```

### Run FastAPI

```bash
uvicorn app:app --reload
```

### Run Streamlit

```bash
streamlit run frontend.py
```

---

## Running with Docker

### Build Containers

```bash
docker compose build
```

### Start Services

```bash
docker compose up
```

---

## Features

* Insurance Premium Prediction
* Real-Time API Inference
* Interactive Streamlit Dashboard
* Dockerized Deployment
* Public Cloud Hosting
* Swagger API Documentation

---

## Deployment

### Backend

Hosted on Render

https://insurancepremiumai-api.onrender.com

### Frontend

Hosted on Render

https://insurancepremiumai-frontend.onrender.com

---

## Author

Kaushik Bairwa

SVNIT Surat

Machine Learning | Backend Development | MLOps | GenAI
