import pandas as pd


def build_features(df):

    df = df.copy()

    df["bmi"] = (
        df["weight"] /
        ((df["height"] / 100) ** 2)
    ).round(2)

    df["income_per_age"] = (
        df["income_lpa"] /
        df["age"]
    )

    df["height_weight_ratio"] = (
        df["height"] /
        df["weight"]
    )

    df["smoker"] = (
        df["smoker"]
        .astype(int)
    )

    df["smoker_income_interaction"] = (
        df["smoker"]
        * df["income_lpa"]
    )

    df["smoker_bmi"] = (
        df["smoker"]
        * df["bmi"]
    )

    df["age_band"] = pd.cut(
        df["age"],
        bins=[17, 25, 35, 45, 55, 65],
        labels=[
            "18-25",
            "26-35",
            "36-45",
            "46-55",
            "56-65"
        ]
    )

    df["income_band"] = pd.cut(
        df["income_lpa"],
        bins=[0, 10, 20, 35, 50],
        labels=[
            "Low",
            "Medium",
            "High",
            "Very_High"
        ]
    )

    return df