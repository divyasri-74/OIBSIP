# 🔐 Advanced Random Password Generator

### OASIS INFOBYTE — Python Programming Internship

**Task 3: Random Password Generator**

**Project Type:** Desktop GUI Application  
**Programming Language:** Python  
**Level:** Advanced

---

## 📌 Overview

The **Advanced Random Password Generator** is a secure desktop application developed using Python and Tkinter.

It allows users to generate strong and customizable passwords based on their selected requirements such as password length, uppercase letters, lowercase letters, numbers, and symbols.

The application uses Python's `secrets` module for secure random password generation and provides additional features such as password strength evaluation, clipboard copying, ambiguous character exclusion, and session-based password history.

---

## ✨ Features

- 🔐 Secure password generation using Python's `secrets` module
- 🔢 Custom password length from **4 to 128 characters**
- 🔠 Uppercase letter support
- 🔡 Lowercase letter support
- 🔢 Number support
- 🔣 Symbol support
- 🚫 Option to exclude ambiguous characters such as `0`, `O`, `1`, and `l`
- 💪 Password strength indicator
- 📋 Copy generated password to clipboard
- 🧹 Clear generated password
- 🕘 Recent password history for the current session
- ⚠️ Input validation and error handling
- 🖥️ User-friendly Tkinter graphical interface

---

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** — GUI development
- **Secrets** — Secure random password generation
- **String** — Character sets
- **Random** — Secure shuffling using `SystemRandom`

---

## 📁 Project Structure

```text
Python-Task3-RandomPasswordGenerator/
│
├── password_generator.py
├── requirements.txt
├── README.md
└── screenshots/
    ├── 01-main-window.png
    ├── 02-generated-password.png
    ├── 03-copy-password.png
    ├── 04-password-history.png
    └── 05-validation.png