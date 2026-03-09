from flask import Flask, render_template, request, redirect, send_file
from bmi_calorie import calculate_bmi, bmi_status, calculate_calories, bmi_advice
from rules import evaluate_deficiencies
from database import init_db, save_result, get_history, get_record, delete_record
from pdf_report import generate_pdf_report

app = Flask(__name__)
init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
    def get_float(field):
        try:
            return float(request.form.get(field, 0))
        except ValueError:
            return 0.0

    name = request.form["name"]
    age = int(request.form["age"])
    gender = request.form["gender"]
    height = get_float("height")
    weight = get_float("weight")
    activity_level = request.form["activity_level"]

    protein = get_float("protein")
    iron = get_float("iron")
    calcium = get_float("calcium")
    vitamin_a = get_float("vitamin_a")
    vitamin_c = get_float("vitamin_c")
    calories = get_float("calories")

    bmi = calculate_bmi(weight, height)
    bmi_state = bmi_status(bmi)
    calorie_needs = calculate_calories(gender, weight, height, age, activity_level)
    advice = bmi_advice(bmi_state)

    intake = {
        "protein": protein,
        "iron": iron,
        "calcium": calcium,
        "vitamin_a": vitamin_a,
        "vitamin_c": vitamin_c,
        "calories": calories,
    }

    deficiency_report = evaluate_deficiencies(gender, intake)

    issue_count = sum(
        1 for item in deficiency_report.values()
        if item["status"] in ["Deficient", "Excess"]
    )

    deficient_count = sum(
        1 for item in deficiency_report.values()
        if item["status"] == "Deficient"
    )

    excess_count = sum(
        1 for item in deficiency_report.values()
        if item["status"] == "Excess"
    )

    calorie_difference = round(calorie_needs - calories, 2)

    if calorie_difference > 0:
        calorie_message = f"You are below your estimated daily calorie need by {calorie_difference} kcal."
    elif calorie_difference < 0:
        calorie_message = f"You are above your estimated daily calorie need by {abs(calorie_difference)} kcal."
    else:
        calorie_message = "Your calorie intake matches your estimated daily need."

    if issue_count == 0 and bmi_state == "Normal weight":
        risk_level = "Low"
        overall_summary = "Your current health indicators appear stable. No nutrient deficiency or excess was detected and your BMI is within the normal range."
    elif issue_count <= 2:
        risk_level = "Moderate"
        overall_summary = "Some nutritional imbalances were detected. You may need to improve or reduce specific nutrient intake to maintain healthier dietary balance."
    else:
        risk_level = "High"
        overall_summary = "Multiple nutritional imbalances were detected. Improved dietary planning and professional guidance may be necessary."

    interpreted_report_lines = []

    for nutrient, info in deficiency_report.items():
        if info["status"] in ["Deficient", "Excess"]:
            interpreted_report_lines.append(
                f"{nutrient.replace('_', ' ').title()}: {info['status']} - {info['recommendation']}"
            )

    if not interpreted_report_lines:
        interpreted_report = "No nutrient deficiency or excess detected."
    else:
        interpreted_report = " | ".join(interpreted_report_lines)

    save_result(
        {
            "name": name,
            "age": age,
            "gender": gender,
            "weight": weight,
            "height": height,
            "activity_level": activity_level,
            "bmi": bmi,
            "bmi_status": bmi_state,
            "calorie_needs": calorie_needs,
            "protein": protein,
            "iron": iron,
            "calcium": calcium,
            "vitamin_a": vitamin_a,
            "vitamin_c": vitamin_c,
            "calories": calories,
            "risk_level": risk_level,
            "overall_summary": overall_summary,
            "issue_count": issue_count,
            "deficient_count": deficient_count,
            "excess_count": excess_count,
            "interpreted_report": interpreted_report,
        }
    )

    return render_template(
        "result.html",
        name=name,
        bmi=bmi,
        bmi_status=bmi_state,
        calorie_needs=calorie_needs,
        bmi_advice=advice,
        report=deficiency_report,
        issue_count=issue_count,
        deficient_count=deficient_count,
        excess_count=excess_count,
        calorie_difference=calorie_difference,
        calorie_message=calorie_message,
        risk_level=risk_level,
        overall_summary=overall_summary,
    )


@app.route("/history")
def history():
    records = get_history()
    return render_template("history.html", records=records)


@app.route("/record/<int:record_id>")
def view_record(record_id):
    record = get_record(record_id)

    if not record:
        return "Record not found"

    return render_template("record.html", record=record)


@app.route("/delete/<int:record_id>")
def delete(record_id):
    delete_record(record_id)
    return redirect("/history")


@app.route("/download_report", methods=["POST"])
def download_report():
    name = request.form["name"]
    bmi = request.form["bmi"]
    bmi_status_value = request.form["bmi_status"]
    calorie_needs = request.form["calorie_needs"]
    risk_level = request.form["risk_level"]
    overall_summary = request.form["overall_summary"]

    report = {
        "protein": {
            "intake": request.form["protein_intake"],
            "rda": request.form["protein_rda"],
            "upper_limit": request.form["protein_upper"],
            "status": request.form["protein_status"],
            "recommendation": request.form["protein_recommendation"],
        },
        "iron": {
            "intake": request.form["iron_intake"],
            "rda": request.form["iron_rda"],
            "upper_limit": request.form["iron_upper"],
            "status": request.form["iron_status"],
            "recommendation": request.form["iron_recommendation"],
        },
        "calcium": {
            "intake": request.form["calcium_intake"],
            "rda": request.form["calcium_rda"],
            "upper_limit": request.form["calcium_upper"],
            "status": request.form["calcium_status"],
            "recommendation": request.form["calcium_recommendation"],
        },
        "vitamin_a": {
            "intake": request.form["vitamin_a_intake"],
            "rda": request.form["vitamin_a_rda"],
            "upper_limit": request.form["vitamin_a_upper"],
            "status": request.form["vitamin_a_status"],
            "recommendation": request.form["vitamin_a_recommendation"],
        },
        "vitamin_c": {
            "intake": request.form["vitamin_c_intake"],
            "rda": request.form["vitamin_c_rda"],
            "upper_limit": request.form["vitamin_c_upper"],
            "status": request.form["vitamin_c_status"],
            "recommendation": request.form["vitamin_c_recommendation"],
        },
        "calories": {
            "intake": request.form["calories_intake"],
            "rda": request.form["calories_rda"],
            "upper_limit": request.form["calories_upper"],
            "status": request.form["calories_status"],
            "recommendation": request.form["calories_recommendation"],
        },
    }

    pdf_data = {
        "name": name,
        "bmi": bmi,
        "bmi_status": bmi_status_value,
        "calorie_needs": calorie_needs,
        "risk_level": risk_level,
        "overall_summary": overall_summary,
        "report": report,
    }

    pdf_file = generate_pdf_report(pdf_data)

    safe_name = name.strip().replace(" ", "_")
    filename = f"{safe_name}_health_report.pdf"

    return send_file(
        pdf_file,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf",
    )


if __name__ == "__main__":
    app.run(debug=True)