import sqlite3

# ===============================
# DATABASE FUNCTIONS
# ===============================
def get_db():
    return sqlite3.connect("leave_system.db")

def create_tables():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll TEXT UNIQUE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS leaves(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        reason TEXT,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
    """)

    conn.commit()
    conn.close()


# ===============================
# STUDENT FUNCTIONS
# ===============================
def add_student(name, roll):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO students (name, roll) VALUES (?, ?)", (name, roll))
        conn.commit()
        print("Student registered successfully!")
    except sqlite3.IntegrityError:
        print("Error: Roll number already exists!")
    finally:
        conn.close()

def student_login(roll):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM students WHERE roll=?", (roll,))
    student = cur.fetchone()
    conn.close()
    return student

def apply_leave(student_id):
    reason = input("Enter leave reason: ")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO leaves (student_id, reason) VALUES (?, ?)", (student_id, reason))
    conn.commit()
    conn.close()
    print("Leave applied successfully!")


# ===============================
# ADMIN FUNCTIONS
# ===============================
def view_leaves():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    SELECT leaves.id, students.name, leaves.reason, leaves.status
    FROM leaves JOIN students 
    ON leaves.student_id = students.id
    """)
    rows = cur.fetchall()
    conn.close()

    print("\n--- All Leave Requests ---")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Reason: {row[2]}, Status: {row[3]}")
    print("---------------------------\n")

def update_leave():
    leave_id = input("Enter Leave ID: ")
    status = input("Enter status (Approved / Rejected): ")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE leaves SET status=? WHERE id=?", (status, leave_id))
    conn.commit()
    conn.close()
    print("Leave status updated!")


# ===============================
# MAIN MENU
# ===============================
def main():
    create_tables()

    while True:
        print("\n===== College Leave Management System =====")
        print("1. Register Student")
        print("2. Student Login")
        print("3. Admin Panel")
        print("4. Exit")

        choice = input("Choose option: ")

        # REGISTER STUDENT
        if choice == "1":
            name = input("Enter student name: ")
            roll = input("Enter roll number: ")
            add_student(name, roll)

        # STUDENT LOGIN & MENU
        elif choice == "2":
            roll = input("Enter roll number: ")
            student = student_login(roll)

            if student:
                print(f"Welcome, {student[1]}!")
                while True:
                    print("\n--- Student Menu ---")
                    print("1. Apply Leave")
                    print("2. Logout")
                    ch = input("Choose: ")

                    if ch == "1":
                        apply_leave(student[0])
                    else:
                        break
            else:
                print("Invalid roll number!")

        # ADMIN PANEL
        elif choice == "3":
            print("\n--- Admin Panel ---")
            while True:
                print("1. View All Leave Requests")
                print("2. Approve/Reject Leave")
                print("3. Back")
                adm = input("Choose: ")

                if adm == "1":
                    view_leaves()
                elif adm == "2":
                    update_leave()
                else:
                    break

        # EXIT
        elif choice == "4":
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice!")

# Run program
if __name__ == "__main__":
    main()
