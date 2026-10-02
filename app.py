from flask import Flask, render_template, request
import joblib
import os
import webbrowser
import threading
from datetime import datetime


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)


# ============================================================
# ZODIAC INFORMATION
# ============================================================

zodiac_info = {

    "Aries": {
        "symbol": "♈",
        "element": "Fire",
        "description": "Energetic, confident, adventurous and independent."
    },

    "Taurus": {
        "symbol": "♉",
        "element": "Earth",
        "description": "Patient, reliable, practical and determined."
    },

    "Gemini": {
        "symbol": "♊",
        "element": "Air",
        "description": "Curious, communicative, adaptable and social."
    },

    "Cancer": {
        "symbol": "♋",
        "element": "Water",
        "description": "Caring, emotional, intuitive and supportive."
    },

    "Leo": {
        "symbol": "♌",
        "element": "Fire",
        "description": "Confident, creative, expressive and ambitious."
    },

    "Virgo": {
        "symbol": "♍",
        "element": "Earth",
        "description": "Analytical, organized, practical and detail-oriented."
    },

    "Libra": {
        "symbol": "♎",
        "element": "Air",
        "description": "Balanced, friendly, cooperative and diplomatic."
    },

    "Scorpio": {
        "symbol": "♏",
        "element": "Water",
        "description": "Focused, determined, intuitive and passionate."
    },

    "Sagittarius": {
        "symbol": "♐",
        "element": "Fire",
        "description": "Optimistic, adventurous, independent and curious."
    },

    "Capricorn": {
        "symbol": "♑",
        "element": "Earth",
        "description": "Disciplined, responsible, ambitious and practical."
    },

    "Aquarius": {
        "symbol": "♒",
        "element": "Air",
        "description": "Innovative, independent, intelligent and humanitarian."
    },

    "Pisces": {
        "symbol": "♓",
        "element": "Water",
        "description": "Creative, empathetic, imaginative and sensitive."
    }
}


ZODIACS = list(zodiac_info.keys())


# ============================================================
# PERSONALITY MODEL
# ============================================================

MODEL_PATH = os.path.join(
    "models",
    "personality_model.pkl"
)

ENCODER_PATH = os.path.join(
    "models",
    "zodiac_encoder.pkl"
)

model = None
zodiac_encoder = None


# Load model if available
try:

    if os.path.exists(MODEL_PATH):

        model = joblib.load(MODEL_PATH)

        print("Personality model loaded successfully.")

    else:

        print("WARNING: personality_model.pkl not found.")

except Exception as e:

    print("Model loading error:", e)


# Load zodiac encoder if available
try:

    if os.path.exists(ENCODER_PATH):

        zodiac_encoder = joblib.load(ENCODER_PATH)

        print("Zodiac encoder loaded successfully.")

    else:

        print("WARNING: zodiac_encoder.pkl not found.")

except Exception as e:

    print("Zodiac encoder loading error:", e)


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# PERSONALITY PAGE
# ============================================================

@app.route(
    "/personality",
    methods=["GET", "POST"]
)
def personality():

    if request.method == "GET":

        return render_template(
            "personality.html",
            zodiacs=ZODIACS
        )

    # --------------------------------------------------------
    # FORM DATA
    # --------------------------------------------------------

    name = request.form.get(
        "name",
        "User"
    )

    dob = request.form.get(
        "dob",
        ""
    )

    zodiac = request.form.get(
        "zodiac",
        "Aries"
    )

    try:

        confidence = int(
            request.form.get(
                "confidence",
                50
            )
        )

        creativity = int(
            request.form.get(
                "creativity",
                50
            )
        )

        leadership = int(
            request.form.get(
                "leadership",
                50
            )
        )

        communication = int(
            request.form.get(
                "communication",
                50
            )
        )

        teamwork = int(
            request.form.get(
                "teamwork",
                50
            )
        )

        social = int(
            request.form.get(
                "social",
                50
            )
        )

        patience = int(
            request.form.get(
                "patience",
                50
            )
        )

        risk = int(
            request.form.get(
                "risk",
                50
            )
        )

    except ValueError:

        confidence = 50
        creativity = 50
        leadership = 50
        communication = 50
        teamwork = 50
        social = 50
        patience = 50
        risk = 50


    # --------------------------------------------------------
    # ZODIAC VALIDATION
    # --------------------------------------------------------

    if zodiac not in ZODIACS:

        zodiac = "Aries"


    # --------------------------------------------------------
    # AI PREDICTION
    # --------------------------------------------------------

    prediction = "Balanced Personality"

    if model is not None and zodiac_encoder is not None:

        try:

            zodiac_encoded = zodiac_encoder.transform(
                [zodiac]
            )[0]

            features = [[
                zodiac_encoded,
                confidence,
                creativity,
                leadership,
                communication,
                teamwork,
                social,
                patience,
                risk
            ]]

            prediction = model.predict(
                features
            )[0]

        except Exception as e:

            print(
                "Prediction error:",
                e
            )

            prediction = calculate_personality(
                confidence,
                creativity,
                leadership,
                communication,
                teamwork,
                social,
                patience,
                risk
            )

    else:

        prediction = calculate_personality(
            confidence,
            creativity,
            leadership,
            communication,
            teamwork,
            social,
            patience,
            risk
        )


    # --------------------------------------------------------
    # TRAIT DATA
    # --------------------------------------------------------

    traits = {

        "Confidence": confidence,
        "Creativity": creativity,
        "Leadership": leadership,
        "Communication": communication,
        "Teamwork": teamwork,
        "Social": social,
        "Patience": patience,
        "Risk Taking": risk

    }


    strongest_trait = max(
        traits,
        key=traits.get
    )

    weakest_trait = min(
        traits,
        key=traits.get
    )


    # --------------------------------------------------------
    # CAREER SUGGESTIONS
    # --------------------------------------------------------

    career_suggestions = get_career_suggestions(
        traits
    )


    info = zodiac_info[zodiac]


    return render_template(

        "personality_result.html",

        name=name,

        dob=dob,

        zodiac=zodiac,

        symbol=info["symbol"],

        element=info["element"],

        description=info["description"],

        prediction=prediction,

        traits=traits,

        strongest_trait=strongest_trait,

        weakest_trait=weakest_trait,

        career_suggestions=career_suggestions

    )


# ============================================================
# SIMPLE PERSONALITY FALLBACK
# ============================================================

def calculate_personality(
    confidence,
    creativity,
    leadership,
    communication,
    teamwork,
    social,
    patience,
    risk
):

    scores = {

        "Leader": (
            confidence
            + leadership
            + risk
        ) / 3,

        "Creative": (
            creativity
            + communication
            + risk
        ) / 3,

        "Analytical": (
            patience
            + confidence
            + teamwork
        ) / 3,

        "Social": (
            communication
            + social
            + teamwork
        ) / 3,

        "Supportive": (
            teamwork
            + patience
            + social
        ) / 3

    }

    return max(
        scores,
        key=scores.get
    )


# ============================================================
# CAREER SUGGESTIONS
# ============================================================

def get_career_suggestions(traits):

    careers = []

    if traits["Leadership"] >= 65:

        careers.append(
            "Project Management"
        )

    if traits["Creativity"] >= 65:

        careers.append(
            "UI/UX Design"
        )

    if traits["Communication"] >= 65:

        careers.append(
            "Marketing"
        )

    if traits["Confidence"] >= 65:

        careers.append(
            "Software Development"
        )

    if traits["Patience"] >= 65:

        careers.append(
            "Data Analytics"
        )

    if traits["Risk Taking"] >= 65:

        careers.append(
            "Entrepreneurship"
        )

    if not careers:

        careers = [
            "Software Development",
            "Data Analytics",
            "UI/UX Design"
        ]

    return careers


# ============================================================
# COMPATIBILITY
# ============================================================

@app.route(
    "/compatibility",
    methods=["GET", "POST"]
)
def compatibility():

    result = None

    sign1 = None

    sign2 = None


    if request.method == "POST":

        sign1 = request.form.get(
            "zodiac1"
        )

        sign2 = request.form.get(
            "zodiac2"
        )

        if sign1 in ZODIACS and sign2 in ZODIACS:

            result = calculate_compatibility(
                sign1,
                sign2
            )


    return render_template(

        "compatibility.html",

        zodiac_info=zodiac_info,

        zodiacs=ZODIACS,

        sign1=sign1,

        sign2=sign2,

        result=result

    )


# ============================================================
# COMPATIBILITY CALCULATION
# ============================================================

def calculate_compatibility(
    sign1,
    sign2
):

    element1 = zodiac_info[
        sign1
    ]["element"]

    element2 = zodiac_info[
        sign2
    ]["element"]


    element_scores = {

        ("Fire", "Fire"): 90,
        ("Fire", "Air"): 85,
        ("Air", "Fire"): 85,

        ("Earth", "Earth"): 88,
        ("Earth", "Water"): 85,
        ("Water", "Earth"): 85,

        ("Air", "Air"): 82,
        ("Water", "Water"): 80,

        ("Fire", "Water"): 60,
        ("Water", "Fire"): 60,

        ("Earth", "Air"): 65,
        ("Air", "Earth"): 65,

        ("Fire", "Earth"): 70,
        ("Earth", "Fire"): 70,

        ("Air", "Water"): 72,
        ("Water", "Air"): 72

    }


    score = element_scores.get(
        (element1, element2),
        70
    )


    return {

        "score": score,

        "message":
            f"{sign1} and {sign2} "
            f"show a compatibility score "
            f"of {score}% based on the "
            f"project's zodiac-element rules.",

        "element1": element1,

        "element2": element2

    }


# ============================================================
# HOROSCOPE
# ============================================================

@app.route(
    "/horoscope",
    methods=["GET", "POST"]
)
def horoscope():

    selected_zodiac = None

    horoscope_data = None


    if request.method == "POST":

        selected_zodiac = request.form.get(
            "zodiac"
        )

        if selected_zodiac in ZODIACS:

            horoscope_data = generate_horoscope(
                selected_zodiac
            )


    return render_template(

        "horoscope.html",

        zodiacs=ZODIACS,

        zodiac_info=zodiac_info,

        selected_zodiac=selected_zodiac,

        horoscope=horoscope_data

    )


# ============================================================
# HOROSCOPE DATA
# ============================================================

def generate_horoscope(zodiac):

    info = zodiac_info[zodiac]

    return {

        "zodiac": zodiac,

        "symbol": info["symbol"],

        "element": info["element"],

        "general":
            "Today is a good day to focus "
            "on your goals and maintain a "
            "positive mindset.",

        "love":
            "Communication and understanding "
            "can help strengthen relationships.",

        "career":
            "Stay focused on your priorities "
            "and use your strengths effectively.",

        "health":
            "Take regular breaks and maintain "
            "a balanced daily routine."

    }


# ============================================================
# CAREER RECOMMENDATION
# ============================================================

@app.route(
    "/career",
    methods=["GET", "POST"]
)
def career():

    career_results = None

    traits = {}


    if request.method == "POST":

        trait_names = [

            "confidence",
            "creativity",
            "leadership",
            "communication",
            "teamwork",
            "analytical",
            "problem_solving"

        ]


        for trait in trait_names:

            try:

                traits[trait] = int(
                    request.form.get(
                        trait,
                        50
                    )
                )

            except ValueError:

                traits[trait] = 50


        career_results = calculate_careers(
            traits
        )


    return render_template(

        "career.html",

        career_results=career_results,

        traits=traits

    )


# ============================================================
# CAREER CALCULATION
# ============================================================

def calculate_careers(traits):

    scores = {

        "Software Development":
            (
                traits.get("problem_solving", 50)
                + traits.get("analytical", 50)
                + traits.get("confidence", 50)
            ) / 3,

        "Data Analytics":
            (
                traits.get("analytical", 50)
                + traits.get("problem_solving", 50)
                + traits.get("patience", 50)
            ) / 3,

        "UI/UX Design":
            (
                traits.get("creativity", 50)
                + traits.get("communication", 50)
                + traits.get("problem_solving", 50)
            ) / 3,

        "Project Management":
            (
                traits.get("leadership", 50)
                + traits.get("communication", 50)
                + traits.get("teamwork", 50)
            ) / 3,

        "Marketing":
            (
                traits.get("communication", 50)
                + traits.get("creativity", 50)
                + traits.get("confidence", 50)
            ) / 3,

        "Entrepreneurship":
            (
                traits.get("leadership", 50)
                + traits.get("confidence", 50)
                + traits.get("problem_solving", 50)
            ) / 3

    }


    results = []

    for career_name, score in scores.items():

        results.append({

            "name": career_name,

            "score": round(score)

        })


    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    return results


# ============================================================
# ANALYTICS DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

    # --------------------------------------------------------
    # ZODIAC DATA
    # --------------------------------------------------------

    zodiac_labels = [

        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces"

    ]


    zodiac_values = [

        12,
        10,
        15,
        8,
        14,
        11,
        13,
        9,
        16,
        7,
        10,
        12

    ]


    # --------------------------------------------------------
    # PERSONALITY DATA
    # --------------------------------------------------------

    personality_labels = [

        "Leader",
        "Creative",
        "Analytical",
        "Social",
        "Supportive"

    ]


    personality_values = [

        25,
        20,
        18,
        22,
        15

    ]


    # --------------------------------------------------------
    # TRAIT DATA
    # --------------------------------------------------------

    trait_labels = [

        "Confidence",
        "Creativity",
        "Leadership",
        "Communication",
        "Teamwork",
        "Social",
        "Patience",
        "Risk Taking"

    ]


    trait_values = [

        75,
        82,
        68,
        80,
        72,
        77,
        65,
        70

    ]


    # --------------------------------------------------------
    # CAREER DATA
    # --------------------------------------------------------

    career_labels = [

        "Software Development",
        "Data Analytics",
        "UI/UX Design",
        "Project Management",
        "Marketing",
        "Entrepreneurship"

    ]


    career_values = [

        30,
        22,
        15,
        12,
        10,
        11

    ]


    return render_template(

        "dashboard.html",

        zodiac_labels=zodiac_labels,

        zodiac_values=zodiac_values,

        personality_labels=personality_labels,

        personality_values=personality_values,

        trait_labels=trait_labels,

        trait_values=trait_values,

        career_labels=career_labels,

        career_values=career_values

    )


# ============================================================
# 404 PAGE
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return """

    <div style="
        font-family:Arial;
        text-align:center;
        margin-top:100px;
    ">

        <h1>🔮 Page Not Found</h1>

        <p>The requested page does not exist.</p>

        <a href="/" style="
            padding:12px 25px;
            background:#6d28d9;
            color:white;
            text-decoration:none;
            border-radius:20px;
        ">
            🏠 Back Home
        </a>

    </div>

    """, 404


# ============================================================
# 500 ERROR
# ============================================================

@app.errorhandler(500)
def server_error(error):

    return """

    <div style="
        font-family:Arial;
        text-align:center;
        margin-top:100px;
    ">

        <h1>⚠️ Something went wrong</h1>

        <p>Please check the Flask terminal for the error.</p>

        <a href="/" style="
            padding:12px 25px;
            background:#6d28d9;
            color:white;
            text-decoration:none;
            border-radius:20px;
        ">
            🏠 Back Home
        </a>

    </div>

    """, 500


# ============================================================
# AUTO OPEN BROWSER
# ============================================================

def open_browser():

    webbrowser.open(
        "http://127.0.0.1:5001/"
    )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 55)
    print("       AI ZODIAC PERSONALITY SYSTEM")
    print("=" * 55)
    print()
    print("Server starting...")
    print()
    print("Home:")
    print("http://127.0.0.1:5001/")
    print()
    print("Dashboard:")
    print("http://127.0.0.1:5001/dashboard")
    print()
    print("Personality:")
    print("http://127.0.0.1:5001/personality")
    print()
    print("Compatibility:")
    print("http://127.0.0.1:5001/compatibility")
    print()
    print("Horoscope:")
    print("http://127.0.0.1:5001/horoscope")
    print()
    print("Career:")
    print("http://127.0.0.1:5001/career")
    print()
    print("=" * 55)
    print()


    # Open browser after Flask starts
    threading.Timer(
        1.5,
        open_browser
    ).start()


    app.run(

        host="127.0.0.1",

        port=5001,

        debug=True,

        use_reloader=False

    )