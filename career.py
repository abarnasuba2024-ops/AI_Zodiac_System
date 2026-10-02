def recommend_careers(
        confidence,
        creativity,
        leadership,
        social,
        communication,
        teamwork
):

    careers = []

    if creativity >= 7:
        careers.append("UI/UX Designer")

    if leadership >= 7:
        careers.append("Project Manager")

    if communication >= 7 and social >= 7:
        careers.append("Marketing / Public Relations")

    if teamwork >= 7:
        careers.append("Software Development")

    if confidence >= 7:
        careers.append("Business / Entrepreneurship")

    if not careers:
        careers.append("Data Analysis")

    return careers[:5]