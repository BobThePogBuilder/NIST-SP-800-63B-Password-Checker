import hashlib
import requests
import tkinter as tk
from tkinter import messagebox
import os
import sys

# Suppress the unrelated macOS GUI messages
os.environ['TK_SILENCE_DEPRECATION'] = '1'

# Redirect stderr to suppress additional system messages
class DevNull:
    def write(self, msg):
        pass
sys.stderr = DevNull()

# Function to check if password has been pwned
def is_pwned(password):
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]
    try:
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        res = requests.get(url, timeout=5)

        if res.status_code != 200:
            return "⚠️ Error checking HIBP API"

        hashes = (line.split(':') for line in res.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return f"❌ This password has appeared in data breaches ({count.strip()} times)."
    except requests.RequestException:
        return "⚠️ Error connecting to HIBP API"
    return None

# Analyze password strength
def analyze_password(password):
    password = password.strip()

    if not password:
        return "❌ You must enter a password."

    has_lower = has_upper = has_num = has_special = False
    lower_count = upper_count = num_count = special_count = 0
    length = len(password)
    score = 0
    feedback = ""

    # Length check
    if length >= 8 and length <= 64:
        feedback += "✅ Your password meets the Length Requirements (NIST SP 800-63B)\n"
    elif length < 8:
        feedback += "❌ The password needs to be at least 8 characters long\n"
    elif length > 64:
        feedback += "⚠️ The recommended max password length is 64 characters\n"

    # Character type analysis
    for char in password:
        if char.islower():
            has_lower = True
            lower_count += 1
        elif char.isupper():
            has_upper = True
            upper_count += 1
        elif char.isdigit():
            has_num = True
            num_count += 1
        elif not char.isalnum():
            has_special = True
            special_count += 1

    feedback += "\n--Character Types Found--\n"
    feedback += f"{'✅' if has_lower else '❌'} Lowercase Letters: {lower_count}\n"
    feedback += f"{'✅' if has_upper else '❌'} Uppercase Letters: {upper_count}\n"
    feedback += f"{'✅' if has_num else '❌'} Numbers: {num_count}\n"
    feedback += f"{'✅' if has_special else '❌'} Special Characters: {special_count}\n"

    # Scoring logic
    if has_lower: score += 1
    if has_upper: score += 1
    if has_num: score += 1
    if has_special: score += 1

    if length >= 8: score += 2
    if length >= 12: score += 2
    if length >= 16: score += 1
    if length >= 20: score += 1

    if special_count >= 4: score += 1
    if num_count >= 4: score += 1

    hibp_status = is_pwned(password)
    if hibp_status:
        feedback += f"\n{hibp_status}"
        score = 0  # Hard fail if pwned

    # Strength summary
    if score >= 12:
        feedback += "\n🔐 Strength: Excellent"
    elif score >= 9:
        feedback += "\n🟢 Strength: Strong"
    elif score >= 7:
        feedback += "\n🟡 Strength: Moderate"
    elif score == 0 and hibp_status:
        feedback += "\n☢️ DO NOT USE THIS PASSWORD ☢️"
    else:
        feedback += "\n🔴 Strength: Weak – consider improving your password"

    return feedback

# GUI logic
def check_password():
    pw = entry.get()
    result = analyze_password(pw)
    result_label.config(text=result)

def toggle_password():
    if show_password_var.get():
        entry.config(show="")
    else:
        entry.config(show="*")

def copy_password():
    pw = entry.get()
    if pw:
        root.clipboard_clear()
        root.clipboard_append(pw)
        messagebox.showinfo("Copied", "Password copied to clipboard.")
    else:
        messagebox.showwarning("No Password", "There's no password to copy.")

# Main window
root = tk.Tk()
root.title("NIST SP 800-63B Password Strength Checker")
root.geometry("500x580")

# Use a darker background for better contrast
bg_color = "#2b2b2b"  # Dark gray
text_color = "#ffffff"  # White
entry_bg = "#3b3b3b"  # Slightly lighter gray
button_bg = "#4CAF50"  # Green
button_copy_bg = "#2196F3"  # Blue
button_text_color = "#000000"  # Black text for buttons

root.configure(bg=bg_color)

#font sucks
font_main = ("Roboto", 14)
font_result = ("Fira Sans", 12)

# UI layout with updated colors
title_label = tk.Label(root, text="Enter your password:", font=font_main, bg=bg_color, fg=text_color)
title_label.pack(pady=10)

entry = tk.Entry(root, show="*", width=40, font=font_main, bg=entry_bg, fg=text_color, insertbackground=text_color)
entry.pack()

# Show/Hide checkbox with updated colors
show_password_var = tk.BooleanVar()
show_password_cb = tk.Checkbutton(
    root, 
    text="Show Password", 
    variable=show_password_var, 
    command=toggle_password, 
    bg=bg_color, 
    fg=text_color,
    selectcolor=entry_bg,
    activebackground=bg_color,
    activeforeground=text_color
)
show_password_cb.pack(pady=5)

# Buttons with updated colors
check_button = tk.Button(
    root, 
    text="Check Password", 
    command=check_password, 
    bg="#8aff8e",  # Light green
    fg=button_text_color, 
    font=("Helvetica", 12, "bold"),
    activebackground="#72d375",  # Darker green for hover
    activeforeground=button_text_color
)
check_button.pack(pady=10)

copy_button = tk.Button(
    root, 
    text="Copy Password", 
    command=copy_password, 
    bg="#63b4ff",  # Light blue
    fg=button_text_color, 
    font=("Helvetica", 10),
    activebackground="#4d8cc7",  # Darker blue for hover
    activeforeground=button_text_color
)
copy_button.pack(pady=5)

# Output label with updated colors
result_label = tk.Label(
    root, 
    text="", 
    wraplength=480, 
    justify="left", 
    anchor="w", 
    bg=bg_color, 
    fg=text_color, 
    font=font_result
)
result_label.pack(pady=10)

# Run it
root.mainloop() 