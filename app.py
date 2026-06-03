from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd


from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
from services.feature_engineering import build_features

import logging

import os
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


model = joblib.load(
    "model/insurance_xgboost.pkl"
)

encoder = joblib.load(
    "model/label_encoder.pkl"
)

model_columns = joblib.load(
    "model/model_columns.pkl"
)


app = FastAPI(
    title="Insurance Premium Prediction API",
    description="API to predict insurance premium category",
    version="1.0.0",
    contact={
        "name": "Kaushik"
    }
)

logging.info(
    "Insurance Premium API Started"
)


@app.get("/")
def home():

    logging.info("Home endpoint accessed")
    return {
        "message": "Insurance Premium Prediction API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model_loaded": True
    }

@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(user: UserInput):

    try:

        logging.info(
            f"Request: city={user.city}, occupation={user.occupation}"
        )

        df = pd.DataFrame(
            [user.model_dump()]
        )

        df = build_features(df)

        df = pd.get_dummies(
            df,
            columns=[
                "city",
                "occupation",
                "age_band",
                "income_band"
            ],
            drop_first=True
        )

        df = df.reindex(
            columns=model_columns,
            fill_value=0
        )

        pred = model.predict(df)

        probs = model.predict_proba(df)

        prediction = encoder.inverse_transform(pred)

        class_names = encoder.classes_

        class_probabilities = {
            class_name: round(float(prob), 4)
            for class_name, prob in zip(
                class_names,
                probs[0]
            )
        }

        confidence = round(
            float(probs[0].max()) * 100,
            2
        )

        logging.info(
            f"Prediction={prediction[0]}, Confidence={confidence}%"
        )

        return PredictionResponse(
            predicted_premium=prediction[0],
            confidence=confidence,
            class_probabilities=class_probabilities
        )

    except Exception as e:

        logging.error(
            f"Prediction Failed: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )