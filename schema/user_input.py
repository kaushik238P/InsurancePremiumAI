from pydantic import BaseModel, Field, field_validator
from typing import Annotated

from config.city_tier import VALID_CITIES
from config.occupation_tier import VALID_OCCUPATIONS

# ---------------------------------------------------------------------------
# Pydantic model
# ---------------------------------------------------------------------------

class UserInput(BaseModel):

    age: Annotated[
        int,
        Field(..., gt=0, lt=120, description="Age of the user")
    ]

    weight: Annotated[
        float,
        Field(..., gt=0, description="Weight of the user in kilograms")
    ]

    height: Annotated[
        float,
        Field(..., gt=100, lt=250, description="Height of the user in centimeters")
    ]

    income_lpa: Annotated[
        float,
        Field(..., gt=0, description="Annual income of the user in LPA")
    ]

    smoker: Annotated[
        bool,
        Field(..., description="Whether the user is a smoker")
    ]

    city: Annotated[
        str,
        Field(..., description="City of the user")
    ]

    occupation: Annotated[
        str,
        Field(..., description="Occupation of the user")
    ]

    @field_validator("city")
    @classmethod
    def normalize_city(cls, value: str) -> str:
        normalized = value.strip().title()
        if normalized not in VALID_CITIES:
            raise ValueError(
                f"Invalid city '{value}'. Must be one of: {sorted(VALID_CITIES)}"
            )
        return normalized

    @field_validator("occupation")
    @classmethod
    def normalize_occupation(cls, value: str) -> str:
        normalized = value.strip().title()
        if normalized not in VALID_OCCUPATIONS:
            raise ValueError(
                f"Invalid occupation '{value}'. Must be one of: {sorted(VALID_OCCUPATIONS)}"
            )
        return normalized