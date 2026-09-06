import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt


# ============================================================
# DATABASE
# ============================================================

DATABASE_NAME = "bmi_database.db"


def create_database():
    """Create the SQLite database and required tables."""
    try:
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)

        # BMI records table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                date_time TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        connection.commit()
        connection.close()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Unable to create the database.\n\n{error}"
        )


# ============================================================
# USER MANAGEMENT
# ============================================================

def add_user_if_not_exists(name):
    """Add a user to the database if the user does not already exist."""
    try:
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE name = ?",
            (name,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            user_id = existing_user[0]
        else:
            cursor.execute(
                "INSERT INTO users (name) VALUES (?)",
                (name,)
            )
            user_id = cursor.lastrowid

        connection.commit()
        connection.close()

        return user_id

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Unable to save user information.\n\n{error}"
        )
        return None


def load_users():
    """Load all users from the database into the user dropdown."""
    try:
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT name FROM users ORDER BY name"
        )

        users = [row[0] for row in cursor.fetchall()]

        connection.close()

        user_combo["values"] = users

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Unable to load users.\n\n{error}"
        )


# ============================================================
# BMI CALCULATION
# ============================================================

def calculate_bmi():
    """Calculate BMI, classify it, and save the record."""

    name = name_entry.get().strip()
    weight_text = weight_entry.get().strip()
    height_text = height_entry.get().strip()

    # -------------------------
    # Input validation
    # -------------------------

    if not name:
        messagebox.showwarning(
            "Missing Information",
            "Please enter your name."
        )
        return

    if not weight_text:
        messagebox.showwarning(
            "Missing Information",
            "Please enter your weight."
        )
        return

    if not height_text:
        messagebox.showwarning(
            "Missing Information",
            "Please enter your height."
        )
        return

    try:
        weight = float(weight_text)
        height = float(height_text)

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Weight and height must contain numbers only."
        )
        return

    if weight <= 0:
        messagebox.showerror(
            "Invalid Weight",
            "Weight must be greater than 0."
        )
        return

    if height <= 0:
        messagebox.showerror(
            "Invalid Height",
            "Height must be greater than 0."
        )
        return

    # -------------------------
    # BMI calculation
    # -------------------------

    bmi = weight / (height ** 2)
    bmi = round(bmi, 2)

    # -------------------------
    # BMI classification
    # -------------------------

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    # -------------------------
    # Display result
    # -------------------------

    result_label.config(
        text=f"BMI: {bmi}\nCategory: {category}"
    )

    # -------------------------
    # Save user and record
    # -------------------------

    user_id = add_user_if_not_exists(name)

    if user_id is None:
        return

    try:
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        date_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute("""
            INSERT INTO bmi_records
            (user_id, weight, height, bmi, category, date_time)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            weight,
            height,
            bmi,
            category,
            date_time
        ))

        connection.commit()
        connection.close()

        load_users()

        user_combo.set(name)

        messagebox.showinfo(
            "BMI Saved",
            f"BMI calculated successfully!\n\n"
            f"Name: {name}\n"
            f"BMI: {bmi}\n"
            f"Category: {category}"
        )

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Unable to save BMI record.\n\n{error}"
        )


# ============================================================
# CLEAR FORM
# ============================================================

def clear_form():
    """Clear all input fields and result."""
    name_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)

    user_combo.set("")

    result_label.config(
        text="BMI: --\nCategory: --"
    )


# ============================================================
# BMI HISTORY
# ============================================================

def show_history():
    """Display the selected user's BMI history."""

    name = user_combo.get().strip()

    if not name:
        messagebox.showwarning(
            "Select User",
            "Please select a user first."
        )
        return

    try:
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                bmi,
                category,
                weight,
                height,
                date_time
            FROM bmi_records
            INNER JOIN users
            ON bmi_records.user_id = users.id
            WHERE users.name = ?
            ORDER BY bmi_records.id DESC
        """, (name,))

        records = cursor.fetchall()

        connection.close()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Unable to retrieve history.\n\n{error}"
        )
        return

    if not records:
        messagebox.showinfo(
            "No Records",
            f"No BMI records found for {name}."
        )
        return

    # Create history window
    history_window = tk.Toplevel(window)
    history_window.title(f"BMI History - {name}")
    history_window.geometry("700x450")

    heading = tk.Label(
        history_window,
        text=f"BMI History for {name}",
        font=("Arial", 18, "bold")
    )
    heading.pack(pady=15)

    # Table
    columns = (
        "Date",
        "Weight",
        "Height",
        "BMI",
        "Category"
    )

    history_table = ttk.Treeview(
        history_window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        history_table.heading(column, text=column)
        history_table.column(
            column,
            width=120,
            anchor="center"
        )

    for record in records:
        bmi, category, weight, height, date_time = record

        history_table.insert(
            "",
            tk.END,
            values=(
                date_time,
                f"{weight:.1f} kg",
                f"{height:.2f} m",
                bmi,
                category
            )
        )

    history_table.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )


# ============================================================
# BMI TREND GRAPH
# ============================================================

def show_bmi_graph():
    """Display a line chart showing the selected user's BMI trend."""

    name = user_combo.get().strip()

    if not name:
        messagebox.showwarning(
            "Select User",
            "Please select a user first."
        )
        return

    try:
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT bmi, date_time
            FROM bmi_records
            INNER JOIN users
            ON bmi_records.user_id = users.id
            WHERE users.name = ?
            ORDER BY bmi_records.id ASC
        """, (name,))

        records = cursor.fetchall()

        connection.close()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Unable to retrieve BMI data.\n\n{error}"
        )
        return

    if not records:
        messagebox.showinfo(
            "No Data",
            f"No BMI records available for {name}."
        )
        return

    bmi_values = [record[0] for record in records]
    dates = [record[1] for record in records]

    # Create graph
    plt.figure(figsize=(10, 5))

    plt.plot(
        dates,
        bmi_values,
        marker="o",
        linewidth=2
    )

    plt.title(f"BMI Trend - {name}")
    plt.xlabel("Date and Time")
    plt.ylabel("BMI")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.show()


# ============================================================
# DELETE USER RECORDS
# ============================================================

def delete_user_records():
    """Delete all BMI records belonging to the selected user."""

    name = user_combo.get().strip()

    if not name:
        messagebox.showwarning(
            "Select User",
            "Please select a user first."
        )
        return

    confirmation = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete all BMI records "
        f"for {name}?"
    )

    if not confirmation:
        return

    try:
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE name = ?",
            (name,)
        )

        user = cursor.fetchone()

        if user:
            user_id = user[0]

            cursor.execute(
                "DELETE FROM bmi_records WHERE user_id = ?",
                (user_id,)
            )

            cursor.execute(
                "DELETE FROM users WHERE id = ?",
                (user_id,)
            )

        connection.commit()
        connection.close()

        load_users()
        user_combo.set("")

        messagebox.showinfo(
            "Deleted",
            f"All records for {name} have been deleted."
        )

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Unable to delete records.\n\n{error}"
        )


# ============================================================
# MAIN WINDOW
# ============================================================

window = tk.Tk()

window.title("Advanced BMI Calculator")

window.geometry("650x700")

window.minsize(600, 650)


# ============================================================
# TITLE
# ============================================================

title_label = tk.Label(
    window,
    text="Advanced BMI Calculator",
    font=("Arial", 26, "bold")
)

title_label.pack(pady=(25, 5))


subtitle_label = tk.Label(
    window,
    text="Calculate, save and track your BMI",
    font=("Arial", 12)
)

subtitle_label.pack(pady=(0, 20))


# ============================================================
# INPUT FRAME
# ============================================================

input_frame = tk.Frame(
    window,
    padx=20,
    pady=15
)

input_frame.pack()


# Name
name_label = tk.Label(
    input_frame,
    text="Name:",
    font=("Arial", 12)
)

name_label.grid(
    row=0,
    column=0,
    padx=10,
    pady=10,
    sticky="e"
)

name_entry = tk.Entry(
    input_frame,
    font=("Arial", 12),
    width=25
)

name_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


# Weight
weight_label = tk.Label(
    input_frame,
    text="Weight (kg):",
    font=("Arial", 12)
)

weight_label.grid(
    row=1,
    column=0,
    padx=10,
    pady=10,
    sticky="e"
)

weight_entry = tk.Entry(
    input_frame,
    font=("Arial", 12),
    width=25
)

weight_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)


# Height
height_label = tk.Label(
    input_frame,
    text="Height (m):",
    font=("Arial", 12)
)

height_label.grid(
    row=2,
    column=0,
    padx=10,
    pady=10,
    sticky="e"
)

height_entry = tk.Entry(
    input_frame,
    font=("Arial", 12),
    width=25
)

height_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=10
)


# ============================================================
# CALCULATE BUTTON
# ============================================================

calculate_button = tk.Button(
    window,
    text="Calculate BMI",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=10,
    command=calculate_bmi
)

calculate_button.pack(pady=15)


# ============================================================
# RESULT
# ============================================================

result_label = tk.Label(
    window,
    text="BMI: --\nCategory: --",
    font=("Arial", 18, "bold"),
    pady=10
)

result_label.pack()


# ============================================================
# USER HISTORY SECTION
# ============================================================

history_frame = tk.Frame(
    window,
    padx=10,
    pady=10
)

history_frame.pack()


user_label = tk.Label(
    history_frame,
    text="Select User:",
    font=("Arial", 11)
)

user_label.grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)


user_combo = ttk.Combobox(
    history_frame,
    width=22,
    state="readonly"
)

user_combo.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


# ============================================================
# BUTTON FRAME
# ============================================================

button_frame = tk.Frame(
    window,
    pady=10
)

button_frame.pack()


history_button = tk.Button(
    button_frame,
    text="View History",
    width=15,
    command=show_history
)

history_button.grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)


graph_button = tk.Button(
    button_frame,
    text="BMI Trend",
    width=15,
    command=show_bmi_graph
)

graph_button.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


clear_button = tk.Button(
    button_frame,
    text="Clear",
    width=15,
    command=clear_form
)

clear_button.grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)


delete_button = tk.Button(
    button_frame,
    text="Delete User",
    width=15,
    command=delete_user_records
)

delete_button.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)


# ============================================================
# FOOTER
# ============================================================

footer_label = tk.Label(
    window,
    text="OASIS INFOBYTE | Python Programming",
    font=("Arial", 9)
)

footer_label.pack(
    side="bottom",
    pady=10
)


# ============================================================
# START APPLICATION
# ============================================================

create_database()
load_users()

window.mainloop()