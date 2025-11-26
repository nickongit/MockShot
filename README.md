# MockShot

Simple UI to generate mock golf shots based on preset club distances / spin \+ a random variance (but not as much as real life brings in!).

## Python version
This project was developed and tested with Python 3.12.3.

## What it does
MockShot provides a small graphical interface to:
1. Pick a golf club from presets.
2. Adjust shot percent, launch direction and spin axis.
3. Generate a mock shot with club/ball speed, launch angles and spin values.

## Run the prebuilt executable
1. Download `dist/MockShot.exe` and place it where convenient.
2. Run the executable directly:
   - Double\-click `MockShot.exe` or run in PowerShell:
     ```powershell
     .\MockShot.exe
     ```

## Run from source
1. Ensure you have Python 3.12.3 installed (Windows).
2. Create and activate a virtual environment and install dependencies:
   ```powershell
   python -m venv .venv
   . .\.venv\Scripts\Activate
   pip install -r `requirements.txt`

3. Run the application:
   gui.py

## Change Club Presets
They can be updated in settings.py

## Generate Executable
   ```powershell
    pyinstaller MockShot.spec