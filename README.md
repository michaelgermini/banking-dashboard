## Direction Banking Dashboard (Streamlit)

Demo en ligne: [data-banking-dashboard.streamlit.app](https://data-banking-dashboard.streamlit.app/)

Local run:

1) Create venv and install deps
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Launch
```powershell
python -m streamlit run streamlit_app.py
```

Deploy to Streamlit Community Cloud:
- Push this folder to a GitHub repo
- In Streamlit Cloud, select the repo, branch, and app file `streamlit_app.py`
- Optional: add secrets in Streamlit Cloud if needed

