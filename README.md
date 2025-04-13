# 🔐 NIST Password Strength Checker

A lightweight, cross-platform password analysis tool that checks your passwords against [NIST SP 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html) digital identity guidelines.

✅ GUI App  
✅ Strength Scoring  
✅ Real-Time Breach Check via Have I Been Pwned  
✅ macOS `.app` Included  
✅ Buildable on both macOS & Windows

---

## 📁 Project Structure

```
/Mac-App
├── NISTPassChecker.app        → Prebuilt macOS app
├── password.py    → GUI script for Mac users

/Source
├── password.py    → Full source code
├── password.spec              → PyInstaller build config
├── build/                     → Temporary build files
├── dist/                      → Output folder for .app/.exe
├── secpass.icns               → macOS icon
├── securepass.ico             → Windows icon
```

---

## 🍏 How to Run on macOS

### ✅ Option 1: Use the Prebuilt `.app`

1. Git Clone 
>   ```bash
>   https://github.com/BobThePogBuilder/NIST-SP-800-63B-Password-Checker.git
>   ```
2. Open `NISTPassChecker.app` from the Mac-App Folder

> 🛑 If blocked by Gatekeeper:
> - Right-click → Open  
> - Or run:
>   ```bash
>   xattr -d com.apple.quarantine NISTPassChecker.app
>   ```

---

### 🛠 Option 2: Build the App on macOS

```bash
# 1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
pip install pyinstaller Pillow

# 3. Build the macOS .app
pyinstaller --onefile --windowed \
  --icon=secpass.icns \
  --name NISTPassChecker \
  password.py
```

Your `.app` will appear in the `dist/` folder.

---

## 🪟 How to Build on Windows

> ⚠️ Must be done on a Windows system (no cross-compilation).

```bash
# 1. Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# 2. Build the .exe
pyinstaller --onefile --windowed ^
  --icon="securepass.ico" ^
  --name NISTPassChecker ^
  password.py
```

Your `.exe` will appear in the `dist/` folder.

---

## 🔧 Features

- ✔ Password length & character analysis (NIST SP 800-63B)
- ✔ Breach detection using Have I Been Pwned API (k-anonymity)
- ✔ Copy to clipboard + show/hide password toggle
- ✔ GUI built with Tkinter, styled for dark mode
- ✔ Works fully offline (except HIBP check)

---


## 🔐 How Breach Checks Work (HIBP)

This app uses the [Have I Been Pwned API](https://haveibeenpwned.com/API/v3#SearchingPwnedPasswordsByRange) with k-anonymity for secure breach detection.

## 🔒 What that means:
- Your password is **never sent** to the API or over the internet.
- It is **hashed locally using SHA-1** (secure hashing algorithm).
- Only the **first 5 characters** of the hash are sent to the HIBP server.
- HIBP returns a list of suffixes and counts for potential matches.
- The app compares the suffix locally to check if your password was found in breaches.

This method ensures:
- ✅ High security
- ✅ Complete privacy
- ✅ Real-world breach validation

### 🔢 Hashing Process (Example in Python)
```python
import hashlib

password = "MySecurePass123!"
sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
prefix = sha1[:5]
suffix = sha1[5:]
```

Then the app makes a request to:
```
https://api.pwnedpasswords.com/range/{prefix}
```

The returned data is parsed and compared to the `suffix` to check for any matches in known data breaches.



## 🧾 License

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**.

You are free to:

- Use, modify, and distribute this software
- As long as you release any modified version under the same license

For full legal details, see: [GNU GPLv3 License](https://www.gnu.org/licenses/gpl-3.0.html)

---

## 🙌 Credits

Developed by [BobThePogBuilder](https://github.com/BobThePogBuilder)  
Inspired by NIST standards and open-source security tools.
