def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)


def bmi_status(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def calculate_calories(gender, weight, height_cm, age, activity_level):
    if gender == "male":
        bmr = 10 * weight + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height_cm - 5 * age - 161

    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }

    calories = bmr * activity_multipliers.get(activity_level, 1.2)
    return round(calories, 2)


def bmi_advice(status):
    if status == "Underweight":
        return "Increase nutrient-dense meals and seek balanced weight gain."
    elif status == "Normal weight":
        return "Maintain your balanced eating habits and healthy activity level."
    elif status == "Overweight":
        return "Reduce excess calorie intake and increase physical activity."
    else:
        return "Adopt a healthier diet and seek medical guidance if necessary."