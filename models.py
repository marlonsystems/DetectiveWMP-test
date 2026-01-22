from database import get_db

def create_person(first_name, last_name, role):
    db = get_db()
    db.execute(
        "INSERT INTO persons (first_name, last_name, role) VALUES (?, ?, ?)",
        (first_name, last_name, role)
    )
    db.commit()
    db.close()

def get_all_persons():
    db = get_db()
    persons = db.execute("SELECT * FROM persons").fetchall()
    db.close()
    return [dict(p) for p in persons]

def create_case(title, description, priority):
    db = get_db()
    db.execute(
        "INSERT INTO cases (title, description, priority) VALUES (?, ?, ?)",
        (title, description, priority)
    )
    db.commit()
    db.close()

def get_all_cases():
    db = get_db()
    cases = db.execute("SELECT * FROM cases").fetchall()
    db.close()
    return [dict(c) for c in cases]
