# Advanced BMI Calculator

## OASIS INFOBYTE — Python Programming Internship

### Task 2: BMI Calculator

**Project Type:** Desktop GUI Application  
**Programming Language:** Python  
**Level:** Advanced

---

## 📌 Project Overview

The Advanced BMI Calculator is a Python-based desktop application that calculates Body Mass Index (BMI), classifies the result, stores BMI records, and tracks BMI changes over time.

The application provides a user-friendly graphical interface and uses SQLite for persistent local data storage.

---

## ✨ Features

- Calculate BMI using weight and height
- BMI classification
- Input validation
- Multiple user profiles
- Persistent BMI history
- View previous BMI records
- BMI trend visualization
- Delete user records
- SQLite database integration
- Database error handling
- User-friendly graphical interface

---

## 📊 BMI Classification

| BMI Range | Classification |
|-----------|----------------|
| Below 18.5 | Underweight |
| 18.5 – 24.9 | Normal |
| 25.0 – 29.9 | Overweight |
| 30.0 and above | Obese |

---

## 🛠️ Technologies Used

- Python 3
- Tkinter
- SQLite3
- Matplotlib

### Libraries

- `tkinter` — GUI development
- `sqlite3` — database management
- `datetime` — date and time records
- `matplotlib` — BMI trend visualization

---

## 📂 Project Structure

```text
Python-Task2-BMICalculator/
│
├── bmi_calculator.py
├── requirements.txt
├── .gitignore
├── README.md
│
└── screenshots/
    ├── 01-main-window.png
    ├── 02-bmi-result.png
    ├── 03-bmi-history.png
    ├── 04-bmi-trend.png
    └── 05-validation.png
```

> `bmi_database.db` is created automatically when the application runs and is excluded from GitHub using `.gitignore`.

---

## ⚙️ Installation

### Prerequisites

- Python 3.x
- Windows, macOS, or Linux
- Internet connection for installing the Matplotlib dependency

### Install Dependencies

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

Open the terminal in the project folder and run:

```bash
python bmi_calculator.py
```

The Advanced BMI Calculator application will open.

The SQLite database is automatically created when the application is launched.

---

## 🧮 How to Use

1. Enter the user's name.
2. Enter the weight in kilograms.
3. Enter the height in metres.
4. Click **Calculate BMI**.
5. The application displays the calculated BMI and classification.
6. The BMI record is automatically saved to the SQLite database.
7. Select a saved user from the **Select User** dropdown.
8. Click **View History** to view previous BMI records.
9. Click **BMI Trend** to visualize BMI changes over time.
10. Click **Clear** to reset the input fields.
11. Click **Delete User** to remove a user's stored records.

---

## ✅ Input Validation

The application validates user input and displays appropriate messages for invalid data.

Validation includes:

- Empty name
- Empty weight
- Empty height
- Non-numeric weight
- Non-numeric height
- Zero weight
- Negative weight
- Zero height
- Negative height

---

## 💾 Database

The application uses **SQLite3** for persistent local data storage.

### Users Table

Stores:

- User ID
- User name

### BMI Records Table

Stores:

- Record ID
- User ID
- Weight
- Height
- BMI
- BMI category
- Date and time

The database is automatically created when the application starts.

---

## 📈 BMI Trend Visualization

The application uses **Matplotlib** to display a line chart of the user's BMI values over time.

The chart provides:

- Date and time of measurements
- BMI values
- Visual representation of BMI changes

---

## 🖼️ Screenshots

The `screenshots` folder contains evidence of the application's functionality:

1. **Main Application** — displays the application interface.
2. **BMI Result** — demonstrates BMI calculation and classification.
3. **BMI History** — demonstrates persistent record storage.
4. **BMI Trend** — demonstrates BMI trend visualization.
5. **Input Validation** — demonstrates validation and error handling.

---

## 🧪 Testing

The application was tested for:

- Successful BMI calculation
- BMI classification
- Multiple BMI records
- User history retrieval
- BMI trend visualization
- Empty input validation
- Invalid numerical input
- Non-positive weight and height
- Database operations

---

## 🔐 Data Handling

BMI records are stored locally using SQLite.

The local database file is excluded from version control through `.gitignore` to avoid uploading local/test records to the public repository.

---

## 🎯 Internship Task

This project was developed as part of the:

**OASIS INFOBYTE Python Programming Internship**

**Task:** Python Programming — Task 2: BMI Calculator

**Tier:** Advanced

---

## 👩‍💻 Author

**Divya Sri**

Python Programming Intern

---

## ⚠️ Disclaimer

BMI is a general screening measure and is not a medical diagnosis. The results provided by this application should not be considered a substitute for professional medical advice.
