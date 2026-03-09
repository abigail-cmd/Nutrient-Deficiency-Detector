RDA = {
    "male": {
        "protein": 56,
        "iron": 8,
        "calcium": 1000,
        "vitamin_a": 900,
        "vitamin_c": 90,
        "calories": 2500
    },
    "female": {
        "protein": 46,
        "iron": 18,
        "calcium": 1000,
        "vitamin_a": 700,
        "vitamin_c": 75,
        "calories": 2000
    }
}

# Upper safe limits / reasonable maximum thresholds for this academic project
UPPER_LIMITS = {
    "protein": 200,
    "iron": 45,
    "calcium": 2500,
    "vitamin_a": 3000,
    "vitamin_c": 2000,
    "calories": 4000
}

RECOMMENDATIONS = {
    "protein": {
        "low": "Eat eggs, fish, beans, chicken, milk, and soy products.",
        "high": "Reduce excessive protein intake and maintain a balanced diet."
    },
    "iron": {
        "low": "Eat spinach, beans, liver, red meat, and vitamin C rich foods.",
        "high": "Avoid excessive iron intake and seek medical advice if supplements are involved."
    },
    "calcium": {
        "low": "Take milk, yogurt, sardines, cheese, and leafy vegetables.",
        "high": "Reduce excess calcium supplements and maintain balanced intake."
    },
    "vitamin_a": {
        "low": "Eat carrots, sweet potatoes, eggs, and green vegetables.",
        "high": "Avoid too much vitamin A supplementation and reduce excessive intake."
    },
    "vitamin_c": {
        "low": "Eat oranges, pineapples, tomatoes, and peppers.",
        "high": "Reduce excessive vitamin C supplementation."
    },
    "calories": {
        "low": "Increase balanced meals with healthy carbohydrates, proteins, and fats.",
        "high": "Reduce excess calorie intake and maintain healthier meal portions."
    }
}


def evaluate_deficiencies(gender, intake):
    report = {}
    user_rda = RDA[gender]

    for nutrient, value in intake.items():
        rda_value = user_rda[nutrient]
        upper_limit = UPPER_LIMITS[nutrient]

        if value < rda_value:
            status = "Deficient"
            gap = round(rda_value - value, 2)
            recommendation = RECOMMENDATIONS[nutrient]["low"]

        elif value > upper_limit:
            status = "Excess"
            gap = round(value - upper_limit, 2)
            recommendation = RECOMMENDATIONS[nutrient]["high"]

        else:
            status = "Adequate"
            gap = 0
            recommendation = "No deficiency or excess detected."

        report[nutrient] = {
            "intake": value,
            "rda": rda_value,
            "upper_limit": upper_limit,
            "status": status,
            "gap": gap,
            "recommendation": recommendation
        }

    return report