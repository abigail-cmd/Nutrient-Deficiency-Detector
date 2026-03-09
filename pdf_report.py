from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def generate_pdf_report(data):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title = Paragraph(
        f"Nutrition Health Assessment Report - {data['name']}",
        styles["Title"]
    )
    elements.append(title)
    elements.append(Spacer(1, 12))

    # User Information
    user_info = [
        ["Name", data["name"]],
        ["BMI", str(data["bmi"])],
        ["BMI Status", data["bmi_status"]],
        ["Daily Calorie Need", f'{data["calorie_needs"]} kcal'],
        ["Risk Level", data["risk_level"]],
    ]

    user_table = Table(user_info, colWidths=[160, 280])
    user_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    elements.append(user_table)
    elements.append(Spacer(1, 16))

    # Summary
    summary_title = Paragraph("Overall Summary", styles["Heading2"])
    elements.append(summary_title)
    elements.append(Paragraph(data["overall_summary"], styles["BodyText"]))
    elements.append(Spacer(1, 16))

    # Nutrient Table
    report_title = Paragraph("Nutrient Evaluation", styles["Heading2"])
    elements.append(report_title)

    nutrient_rows = [["Nutrient", "Intake", "RDA", "Upper Limit", "Status"]]

    for nutrient, info in data["report"].items():
        nutrient_rows.append([
            nutrient.replace("_", " ").title(),
            str(info["intake"]),
            str(info["rda"]),
            str(info["upper_limit"]),
            info["status"]
        ])

    nutrient_table = Table(nutrient_rows, colWidths=[120, 80, 80, 90, 90])
    nutrient_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(nutrient_table)
    elements.append(Spacer(1, 16))

    # Recommendations
    rec_title = Paragraph("Recommendations", styles["Heading2"])
    elements.append(rec_title)

    has_issue = False

    for nutrient, info in data["report"].items():
        if info["status"] in ["Deficient", "Excess"]:
            has_issue = True
            text = f"<b>{nutrient.replace('_', ' ').title()}:</b> {info['recommendation']}"
            elements.append(Paragraph(text, styles["BodyText"]))
            elements.append(Spacer(1, 8))

    if not has_issue:
        elements.append(
            Paragraph(
                "No nutrient deficiency or excess was detected.",
                styles["BodyText"]
            )
        )

    doc.build(elements)
    buffer.seek(0)

    return buffer