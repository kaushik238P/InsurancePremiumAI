from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):

    predicted_premium: str = Field(
        description="Predicted insurance premium category"
    )

    confidence: float = Field(
        description="Prediction confidence percentage"
    )

    class_probabilities: dict[str, float] = Field(
        description="Probability for each class"
    )