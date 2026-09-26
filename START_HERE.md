# AstroRisk — START HERE

**Developer: Eva J. Patel**

## Windows setup

Open PowerShell in this folder.

### First run

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and set your NASA API key:

```env
NASA_API_KEY=DEMO_KEY
```

Then start:

```powershell
python run.py
```

Open:

- http://127.0.0.1:8000 — AstroRisk dashboard
- http://127.0.0.1:8000/lab — Gradio Research Lab
- http://127.0.0.1:8000/docs — API documentation

## If PowerShell blocks activation

You do not need activation. Run:

```powershell
py -3.12 -m pip install -r requirements.txt
py -3.12 run.py
```

## Troubleshooting

If you get `ModuleNotFoundError`, run:

```powershell
python -m pip install -r requirements.txt
```

If `/lab` returns `404`, make sure you are running the new `run.py` from this project and not an older AstroRisk folder.

The startup script prints whether the Gradio Research Lab mounted successfully.

## NASA API

`DEMO_KEY` is acceptable for testing. For repeated research collection, use your own NASA key.

Never commit `.env` to GitHub. `.gitignore` already excludes it.
