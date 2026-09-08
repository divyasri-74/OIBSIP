import tkinter as tk
from tkinter import ttk, messagebox
import string
import secrets
import random


class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Random Password Generator")
        self.root.geometry("700x850")
        self.root.resizable(False, False)

        self.history = []

        # Variables
        self.length_var = tk.IntVar(value=16)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.number_var = tk.BooleanVar(value=True)
        self.symbol_var = tk.BooleanVar(value=True)
        self.ambiguous_var = tk.BooleanVar(value=False)
        self.password_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Title
        title = ttk.Label(
            self.root,
            text="Advanced Random Password Generator",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=(25, 5))

        subtitle = ttk.Label(
            self.root,
            text="Generate strong and secure passwords using Python",
            font=("Arial", 11)
        )
        subtitle.pack(pady=(0, 20))

        # Generated password
        password_frame = ttk.LabelFrame(
            self.root,
            text="Generated Password",
            padding=15
        )
        password_frame.pack(fill="x", padx=40, pady=10)

        self.password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            font=("Consolas", 16),
            justify="center"
        )
        self.password_entry.pack(fill="x", pady=5)

        button_frame = ttk.Frame(password_frame)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Copy Password",
            command=self.copy_password
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_password
        ).grid(row=0, column=1, padx=5)

        # Password length
        length_frame = ttk.LabelFrame(
            self.root,
            text="Password Length",
            padding=15
        )
        length_frame.pack(fill="x", padx=40, pady=10)

        ttk.Label(
            length_frame,
            text="Length:"
        ).grid(row=0, column=0, padx=5)

        self.length_spinbox = ttk.Spinbox(
            length_frame,
            from_=4,
            to=128,
            textvariable=self.length_var,
            width=10
        )
        self.length_spinbox.grid(row=0, column=1, padx=10)

        # Character options
        options_frame = ttk.LabelFrame(
            self.root,
            text="Character Options",
            padding=15
        )
        options_frame.pack(fill="x", padx=40, pady=10)

        ttk.Checkbutton(
            options_frame,
            text="Uppercase Letters (A-Z)",
            variable=self.upper_var
        ).grid(row=0, column=0, sticky="w", padx=10, pady=5)

        ttk.Checkbutton(
            options_frame,
            text="Lowercase Letters (a-z)",
            variable=self.lower_var
        ).grid(row=0, column=1, sticky="w", padx=10, pady=5)

        ttk.Checkbutton(
            options_frame,
            text="Numbers (0-9)",
            variable=self.number_var
        ).grid(row=1, column=0, sticky="w", padx=10, pady=5)

        ttk.Checkbutton(
            options_frame,
            text="Symbols (!@#$...)",
            variable=self.symbol_var
        ).grid(row=1, column=1, sticky="w", padx=10, pady=5)

        ttk.Checkbutton(
            options_frame,
            text="Exclude Ambiguous Characters (0, O, 1, l)",
            variable=self.ambiguous_var
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # Generate button
        ttk.Button(
            self.root,
            text="🔐 Generate Secure Password",
            command=self.generate_password
        ).pack(pady=15)

        # Password strength
        strength_frame = ttk.LabelFrame(
            self.root,
            text="Password Strength",
            padding=10
        )
        strength_frame.pack(fill="x", padx=40, pady=5)

        self.strength_label = ttk.Label(
            strength_frame,
            text="Strength: -",
            font=("Arial", 11, "bold")
        )
        self.strength_label.pack()

        # Recent password history
        history_frame = ttk.LabelFrame(
            self.root,
            text="Recent Passwords (Current Session)",
            padding=10
        )
        history_frame.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=10
        )

        self.history_listbox = tk.Listbox(
            history_frame,
            height=6,
            font=("Consolas", 10)
        )
        self.history_listbox.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            history_frame,
            orient="vertical",
            command=self.history_listbox.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.history_listbox.config(
            yscrollcommand=scrollbar.set
        )

        # Footer
        footer = ttk.Label(
            self.root,
            text="OASIS INFOBYTE | Python Programming | Task 3",
            font=("Arial", 9)
        )
        footer.pack(pady=(0, 10))

    def generate_password(self):
        try:
            length = int(self.length_var.get())
        except (ValueError, tk.TclError):
            messagebox.showerror(
                "Invalid Length",
                "Please enter a valid password length."
            )
            return

        if length < 4 or length > 128:
            messagebox.showerror(
                "Invalid Length",
                "Password length must be between 4 and 128."
            )
            return

        character_sets = []

        if self.upper_var.get():
            character_sets.append(string.ascii_uppercase)

        if self.lower_var.get():
            character_sets.append(string.ascii_lowercase)

        if self.number_var.get():
            character_sets.append(string.digits)

        if self.symbol_var.get():
            character_sets.append(string.punctuation)

        if not character_sets:
            messagebox.showwarning(
                "No Character Type Selected",
                "Please select at least one character type."
            )
            return

        if length < len(character_sets):
            messagebox.showwarning(
                "Length Too Short",
                f"Password length must be at least {len(character_sets)} "
                "for the selected character types."
            )
            return

        ambiguous = "0O1l"

        # Remove ambiguous characters if selected
        cleaned_sets = []

        for char_set in character_sets:
            if self.ambiguous_var.get():
                char_set = "".join(
                    char for char in char_set
                    if char not in ambiguous
                )

            if char_set:
                cleaned_sets.append(char_set)

        if not cleaned_sets:
            messagebox.showwarning(
                "Invalid Character Selection",
                "The selected options do not provide usable characters."
            )
            return

        # Guarantee one character from every selected category
        password_chars = [
            secrets.choice(char_set)
            for char_set in cleaned_sets
        ]

        all_characters = "".join(cleaned_sets)

        # Fill remaining characters securely
        for _ in range(length - len(password_chars)):
            password_chars.append(
                secrets.choice(all_characters)
            )

        # Securely shuffle
        random.SystemRandom().shuffle(password_chars)

        password = "".join(password_chars)

        self.password_var.set(password)
        self.update_strength(password)
        self.add_to_history(password)

    def update_strength(self, password):
        score = 0

        if len(password) >= 12:
            score += 1

        if len(password) >= 16:
            score += 1

        if any(char.isupper() for char in password):
            score += 1

        if any(char.islower() for char in password):
            score += 1

        if any(char.isdigit() for char in password):
            score += 1

        if any(char in string.punctuation for char in password):
            score += 1

        if score <= 2:
            strength = "Weak"
        elif score <= 4:
            strength = "Medium"
        elif score == 5:
            strength = "Strong"
        else:
            strength = "Very Strong"

        self.strength_label.config(
            text=f"Strength: {strength}"
        )

    def add_to_history(self, password):
        self.history.insert(0, password)

        # Keep only the latest 5 passwords
        self.history = self.history[:5]

        self.history_listbox.delete(0, tk.END)

        for item in self.history:
            self.history_listbox.insert(tk.END, item)

    def copy_password(self):
        password = self.password_var.get()

        if not password:
            messagebox.showwarning(
                "No Password",
                "Generate a password first."
            )
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.root.update()

        messagebox.showinfo(
            "Copied",
            "Password copied to clipboard."
        )

    def clear_password(self):
        self.password_var.set("")
        self.strength_label.config(
            text="Strength: -"
        )


def main():
    root = tk.Tk()
    PasswordGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()