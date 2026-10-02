horoscopes = {

    "Aries": "Focus on your goals and take one step at a time.",

    "Taurus": "A calm and organized approach may help you handle today's tasks.",

    "Gemini": "Communication and learning can be useful themes for today.",

    "Cancer": "Give yourself time to reflect and stay connected with people you value.",

    "Leo": "Creative activities may give you an opportunity to express yourself.",

    "Virgo": "Planning and attention to detail can help you stay organized.",

    "Libra": "Try to maintain balance between responsibilities and personal time.",

    "Scorpio": "Concentrate on one important goal instead of spreading your attention.",

    "Sagittarius": "Learning something new can make your day more interesting.",

    "Capricorn": "Consistent effort can help you make progress toward your goals.",

    "Aquarius": "Explore new ideas and look at familiar problems from another angle.",

    "Pisces": "Creative and relaxing activities may help you recharge."
}


def get_horoscope(sign):
    return horoscopes.get(
        sign,
        "Have a positive and productive day!"
    )