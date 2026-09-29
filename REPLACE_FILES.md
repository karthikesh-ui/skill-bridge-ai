# Updating your existing Skill Bridge-AI folder

1. Stop Flask in VS Code with **Ctrl+C**.
2. Copy your current project folder as a backup.
3. Extract this ZIP. Open the inner `Skill-Bridge-AI` folder.
4. Copy its files and folders into the folder where your `app.py` currently lives. Select **Replace the files in the destination** when Windows asks.
5. **Keep your existing `.env` and `venv`**. They are deliberately absent from this ZIP; your Gemini key remains in `.env`.
6. In the VS Code terminal, run `python app.py` and open `http://127.0.0.1:5000/`.
7. Refresh the site with **Ctrl+F5** to load the new CSS and JavaScript. Existing local profile and progress should remain in the same browser.
8. Test discovery, a career page, route switch, roadmap and dashboard. On a career page, click **Ask for personal guidance**. A working key shows `(AI guidance)`; an unavailable key or network shows `(built-in guidance)`.

The courses and routes are examples, not official eligibility decisions. Check institutions and exam authorities for current rules.
