import sqlite3

DB_NAME = "nutrition.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        weight REAL,
        height REAL,
        activity_level TEXT,
        bmi REAL,
        bmi_status TEXT,
        calorie_needs REAL,
        protein REAL,
        iron REAL,
        calcium REAL,
        vitamin_a REAL,
        vitamin_c REAL,
        calories REAL,
        risk_level TEXT,
        overall_summary TEXT,
        issue_count INTEGER,
        deficient_count INTEGER,
        excess_count INTEGER,
        interpreted_report TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_result(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO results (
        name, age, gender, weight, height, activity_level,
        bmi, bmi_status, calorie_needs,
        protein, iron, calcium, vitamin_a, vitamin_c, calories,
        risk_level, overall_summary, issue_count, deficient_count, excess_count, interpreted_report
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["name"], data["age"], data["gender"], data["weight"], data["height"],
        data["activity_level"], data["bmi"], data["bmi_status"], data["calorie_needs"],
        data["protein"], data["iron"], data["calcium"],
        data["vitamin_a"], data["vitamin_c"], data["calories"],
        data["risk_level"], data["overall_summary"], data["issue_count"],
        data["deficient_count"], data["excess_count"], data["interpreted_report"]
    ))

    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM results ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    return rows



def get_record(record_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM results WHERE id=?", (record_id,))
    row = cursor.fetchone()

    conn.close()
    return row

def delete_record(record_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM results WHERE id=?", (record_id,))
    conn.commit()

    conn.close()
    
    
    
def get_dashboard_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # total analyses
    cursor.execute("SELECT COUNT(*) FROM results")
    total_records = cursor.fetchone()[0]

    # average BMI
    cursor.execute("SELECT AVG(bmi) FROM results")
    avg_bmi_result = cursor.fetchone()[0]
    avg_bmi = round(avg_bmi_result, 2) if avg_bmi_result else 0

    # risk distribution
    cursor.execute("SELECT COUNT(*) FROM results WHERE risk_level = 'Low'")
    low_risk = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM results WHERE risk_level = 'Moderate'")
    moderate_risk = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM results WHERE risk_level = 'High'")
    high_risk = cursor.fetchone()[0]

    # gender distribution
    cursor.execute("SELECT COUNT(*) FROM results WHERE gender = 'male'")
    male_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM results WHERE gender = 'female'")
    female_count = cursor.fetchone()[0]

    conn.close()

    return {
        "total_records": total_records,
        "avg_bmi": avg_bmi,
        "low_risk": low_risk,
        "moderate_risk": moderate_risk,
        "high_risk": high_risk,
        "male_count": male_count,
        "female_count": female_count,
    }