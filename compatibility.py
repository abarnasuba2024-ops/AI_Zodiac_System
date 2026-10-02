compatibility_data = {

    "Aries": {
        "Leo": 90,
        "Sagittarius": 88,
        "Gemini": 82,
        "Cancer": 60,
        "Capricorn": 55
    },

    "Taurus": {
        "Virgo": 90,
        "Capricorn": 88,
        "Cancer": 82,
        "Leo": 60,
        "Aquarius": 55
    },

    "Gemini": {
        "Libra": 90,
        "Aquarius": 88,
        "Aries": 82,
        "Virgo": 60,
        "Scorpio": 55
    },

    "Cancer": {
        "Scorpio": 90,
        "Pisces": 88,
        "Taurus": 82,
        "Aries": 60,
        "Libra": 55
    },

    "Leo": {
        "Aries": 90,
        "Sagittarius": 88,
        "Gemini": 82,
        "Taurus": 60,
        "Scorpio": 55
    },

    "Virgo": {
        "Taurus": 90,
        "Capricorn": 88,
        "Scorpio": 82,
        "Gemini": 60,
        "Sagittarius": 55
    },

    "Libra": {
        "Gemini": 90,
        "Aquarius": 88,
        "Leo": 82,
        "Cancer": 60,
        "Capricorn": 55
    },

    "Scorpio": {
        "Cancer": 90,
        "Pisces": 88,
        "Virgo": 82,
        "Leo": 55,
        "Gemini": 55
    },

    "Sagittarius": {
        "Aries": 90,
        "Leo": 88,
        "Aquarius": 82,
        "Virgo": 55,
        "Cancer": 55
    },

    "Capricorn": {
        "Taurus": 90,
        "Virgo": 88,
        "Scorpio": 82,
        "Aries": 55,
        "Gemini": 55
    },

    "Aquarius": {
        "Gemini": 90,
        "Libra": 88,
        "Sagittarius": 82,
        "Taurus": 55,
        "Cancer": 55
    },

    "Pisces": {
        "Cancer": 90,
        "Scorpio": 88,
        "Taurus": 82,
        "Gemini": 55,
        "Leo": 55
    }
}


def get_compatibility(sign1, sign2):

    if sign1 == sign2:
        score = 80
    else:
        score = compatibility_data.get(
            sign1,
            {}
        ).get(
            sign2,
            compatibility_data.get(sign2, {}).get(sign1, 70)
        )

    return score