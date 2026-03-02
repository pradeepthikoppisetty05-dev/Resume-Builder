import pandas as pd
import mysql.connector

# ==============================
# DATABASE CONFIG
# ==============================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "resume_builder"
}

# ==============================
# FILE PATHS
# ==============================


OCCUPATION_FILE = "../data/Occupation Data.xlsx"
TECH_FILE = "../data/Technology Skills.xlsx"


def connect_db():
    return mysql.connector.connect(**DB_CONFIG)


def import_occupations(cursor):
    print("Importing occupations...")

    df = pd.read_excel(OCCUPATION_FILE)

    for _, row in df.iterrows():
        onet_code = str(row["O*NET-SOC Code"]).strip()
        title = str(row["Title"]).strip()
        description = str(row.get("Description", "")).strip()

        cursor.execute("""
            INSERT IGNORE INTO occupations (onet_code, title, description)
            VALUES (%s, %s, %s)
        """, (onet_code, title, description))

    print("Occupations imported.")


def import_technologies(cursor):
    print("Importing technologies...")

    df = pd.read_excel(TECH_FILE)

    for _, row in df.iterrows():
        onet_code = str(row["O*NET-SOC Code"]).strip()
        technology = str(row["Example"]).strip()
        trendy = str(row["Hot Technology"]).strip()
        demand = str(row["In Demand"]).strip()

        cursor.execute("""
            INSERT INTO technology_skills (onet_code, technology, trendy, demand)
            VALUES (%s, %s, %s, %s)
        """, (onet_code, technology, trendy, demand))

    print("Technologies imported.")


def main():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        import_occupations(cursor)
        import_technologies(cursor)

        conn.commit()
        print("✅ Import completed successfully.")

    except Exception as e:
        conn.rollback()
        print("❌ Error occurred:", e)

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()