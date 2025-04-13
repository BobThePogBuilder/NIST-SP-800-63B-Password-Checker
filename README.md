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
├── password_checker_gui.py    → GUI script for Mac users

/Source
├── password_checker_gui.py    → Full source code
├── password.spec              → PyInstaller build config
├── build/                     → Temporary build files
├── dist/                      → Output folder for .app/.exe
├── secpass.icns               → macOS icon
├── securepass.ico             → Windows icon
```

---

## 🍏 How to Run on macOS

### ✅ Option 1: Use the Prebuilt `.app`

1. Navigate to `/Mac-App`
2. Git Clone
3. Open `NISTPassChecker.app`

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
  password_checker_gui.py
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
  password_checker_gui.py
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
