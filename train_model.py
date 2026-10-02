import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# --------------------------------------------------
# TRAINING DATA
# --------------------------------------------------

data = {

    "zodiac": [
        "Aries", "Taurus", "Gemini", "Cancer",
        "Leo", "Virgo", "Libra", "Scorpio",
        "Sagittarius", "Capricorn", "Aquarius", "Pisces",

        "Aries", "Leo", "Gemini", "Virgo",
        "Libra", "Scorpio", "Cancer", "Aquarius",
        "Taurus", "Capricorn", "Pisces", "Sagittarius"
    ],

    "confidence": [
        9, 7, 7, 5,
        9, 6, 8, 8,
        9, 7, 7, 5,

        8, 10, 8, 7,
        8, 9, 6, 8,
        7, 8, 6, 9
    ],

    "creativity": [
        7, 6, 9, 8,
        9, 7, 8, 8,
        9, 6, 9, 10,

        8, 9, 10, 7,
        8, 9, 8, 10,
        6, 7, 9, 8
    ],

    "leadership": [
        9, 7, 6, 5,
        10, 6, 7, 8,
        9, 8, 6, 5,

        8, 10, 7, 7,
        8, 9, 6, 8,
        7, 9, 6, 9
    ],

    "communication": [
        8, 6, 9, 6,
        9, 6, 8, 7,
        9, 7, 8, 6,

        8, 9, 10, 7,
        9, 8, 6, 9,
        7, 8, 7, 9
    ],

    "teamwork": [
        7, 8, 8, 9,
        7, 7, 9, 6,
        7, 8, 7, 9,

        8, 7, 9, 8,
        10, 7, 9, 8,
        8, 9, 8, 7
    ],

    "social": [
        8, 6, 9, 7,
        9, 6, 8, 7,
        10, 6, 8, 6,

        9, 8, 10, 7,
        9, 7, 8, 9,
        6, 7, 8, 9
    ],

    "patience": [
        5, 9, 6, 9,
        6, 9, 7, 6,
        5, 8, 7, 9,

        6, 7, 5, 10,
        8, 6, 9, 7,
        9, 8, 8, 6
    ],

    "risk": [
        9, 5, 7, 4,
        9, 6, 8, 8,
        10, 6, 7, 4,

        8, 10, 8, 6,
        8, 9, 5, 8,
        6, 7, 5, 9
    ],

    "personality": [
        "Leader", "Stable", "Communicative", "Empathetic",
        "Leader", "Analytical", "Social", "Determined",
        "Adventurous", "Disciplined", "Innovative", "Creative",

        "Leader", "Leader", "Communicative", "Analytical",
        "Social", "Determined", "Empathetic", "Innovative",
        "Stable", "Disciplined", "Creative", "Adventurous"
    ]
}


df = pd.DataFrame(data)


# --------------------------------------------------
# ENCODE ZODIAC
# --------------------------------------------------

zodiac_encoder = LabelEncoder()

df["zodiac_encoded"] = zodiac_encoder.fit_transform(
    df["zodiac"]
)


# --------------------------------------------------
# FEATURES
# --------------------------------------------------

features = [
    "zodiac_encoded",
    "confidence",
    "creativity",
    "leadership",
    "communication",
    "teamwork",
    "social",
    "patience",
    "risk"
]

X = df[features]

y = df["personality"]


# --------------------------------------------------
# TRAIN MODEL
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X, y)


# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/personality_model.pkl"
)

joblib.dump(
    zodiac_encoder,
    "models/zodiac_encoder.pkl"
)

print("================================")
print("ML MODEL TRAINING COMPLETED")
print("================================")

print("Model saved:")
print("models/personality_model.pkl")

print("Zodiac encoder saved:")
print("models/zodiac_encoder.pkl")