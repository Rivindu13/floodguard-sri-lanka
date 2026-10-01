# FloodGuard Sri Lanka — Streamlit starter app

## Files expected in this folder

- `app.py` — Streamlit interface
- `requirements.txt` — Python packages
- `baseline_flood_risk_model.joblib` — your saved baseline Random Forest model
- `waste_risk_dataset (Simulated data).csv` — your 5,000-row NetLogo-generated dataset (optional for prediction, needed for Dataset explorer)

The model and dataset are not bundled because they are your own project outputs.

## Run on your computer (Anaconda Prompt)

1. Put your model and CSV files beside `app.py`.
2. Open Anaconda Prompt.
3. Change directory to this folder, for example:
   `cd Desktop\floodguard_streamlit_app`
4. Install packages:
   `pip install -r requirements.txt`
5. Start the app:
   `streamlit run app.py`
6. Your browser should open the local app. If it does not, open the local URL printed in the terminal (usually `http://localhost:8501`).

## Important
This is an educational interface. Predictions reproduce patterns learned from synthetic NetLogo labels and are not validated real-world flood forecasts.
