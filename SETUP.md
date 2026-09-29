# Windows + VS Code setup

1. Extract `Skill-Bridge-AI.zip` and open the **Skill-Bridge-AI** folder in VS Code (File → Open Folder). Install Python from python.org if needed; enable **Add Python to PATH**.
2. Open Terminal → New Terminal. The prompt should end in `Skill-Bridge-AI`.
3. Run `python -m venv venv` (or `py -m venv venv`).
4. In PowerShell run `venv\Scripts\Activate.ps1`. If blocked, run `Set-ExecutionPolicy -Scope Process Bypass` and try activation again. Or switch the terminal to Command Prompt and run `venv\Scripts\activate.bat`.
5. Run `python -m pip install -r requirements.txt`.
6. Run `Copy-Item .env.example .env` in PowerShell (`copy .env.example .env` in Command Prompt). The project works with the placeholder key.
7. Optional AI: visit https://aistudio.google.com/app/apikey and create a Gemini API key. In the root `.env` file replace `your_api_key_here`: `GEMINI_API_KEY=your_actual_key`. Do not share or commit this file.
8. Run `python app.py`. Open http://127.0.0.1:5000/ in Chrome. Keep the terminal running. Press Ctrl+C to stop.
9. Test: landing → Find My Career → complete five steps → open a match → pathway → roadmap status → dashboard skill gap → career guidance. To test fallback, set the placeholder key and restart Flask.

## Troubleshooting
- Python not recognized: reinstall from python.org with PATH selected, reopen VS Code, or use `py` instead of `python`.
- pip not recognized: use `python -m pip install -r requirements.txt`.
- Activation blocked: use the Process Bypass command above or Command Prompt `venv\Scripts\activate.bat`.
- Missing package: activate the same venv and run `python -m pip install -r requirements.txt`.
- Gemini key missing/invalid: core site still works with fallback; check `.env`, key, network and restart Flask.
- Port 5000 busy: stop other Flask instances, or edit the last line in `app.py` to use `port=5001`, then open http://127.0.0.1:5001/.
- Flask fails to start: verify the terminal is inside the project and run `python -m pip install -r requirements.txt`.
- Page/API connection: open the Flask URL (not `file://` or Live Server), refresh, and inspect the terminal errors.
