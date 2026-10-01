# FloodGuard Sri Lanka

### Smart Waste Management and Urban Flood-Risk Simulation

**Project area:** Complex Systems and Agent Technology\
**Institution:** University of Sri Jayewardenepura, Sri Lanka

FloodGuard Sri Lanka is an academic project exploring how household
waste generation, waste collection practices, public awareness, rainfall
intensity, and drainage blockage can interact in a simplified urban
environment. It combines an agent-based simulation developed in NetLogo
with a machine-learning classifier and a Streamlit web application.

> **Important:** The data and risk labels used in this project are
> simulated. The machine-learning model reproduces labels generated from
> the project's simulation assumptions. It is not a validated real-world
> flood forecasting system and should not be used for emergency
> decisions.

## Project components

-   **`Netlogo file/`** --- NetLogo model and simulated dataset.
-   **`Prediction model/`** --- model-training notebook, saved Random
    Forest model, and model report.
-   **`Flood Guard App v1.0/`** --- Streamlit interface, requirements,
    dataset, and saved model.

## Features

-   Explore how rainfall, collection intervals, public awareness, waste
    generation, household count, and collector count relate to simulated
    flood-risk categories.
-   Predict a simulated risk category (**Low**, **Medium**, or **High**)
    using a trained Random Forest classifier.
-   Explore and filter the simulated dataset and view basic charts.
-   Review the model's assumptions and limitations.

## Technology stack

-   NetLogo --- agent-based simulation
-   Python --- data preparation and machine learning
-   pandas --- dataset handling
-   scikit-learn --- Random Forest classifier and evaluation
-   Streamlit --- interactive web application
-   Matplotlib --- visualizations
-   joblib --- saved model loading

## Run the Streamlit app locally

### 1. Open a terminal in the app folder

From the repository root, run:

``` powershell
cd "Flood Guard App v1.0"
```

### 2. Install dependencies

``` powershell
python -m pip install -r requirements.txt
```

### 3. Check required files

The app folder should contain:

-   `app.py`
-   `requirements.txt`
-   `baseline_flood_risk_model.joblib`
-   `waste_risk_dataset (Simulated data).csv`

Keep the model and CSV in the same folder as `app.py` unless the file
paths in the code are updated.

### 4. Start the app

``` powershell
streamlit run app.py
```

Streamlit should open the app in your browser. If it does not, use the
local URL printed in the terminal.

## Dataset

The project dataset contains 5,000 simulated scenarios. The documented
model input features are:

  Feature                   Description
  ------------------------- -------------------------------------------
  `rainfall_intensity`      Simulated rainfall intensity
  `collection_interval`     Interval between waste collections
  `public_awareness`        Simulated public-awareness level
  `waste_generation_rate`   Simulated household waste-generation rate
  `num_households`          Number of households represented
  `num_collectors`          Number of waste collectors represented

The dataset also includes simulation outputs such as `average_blockage`,
`total_waste`, `flood_risk_score`, and `risk_category`. These outputs
are useful for analysis, but should not be treated as independent input
features when evaluating a model that predicts the same generated
labels.

The simulation's risk categories use these score thresholds:

-   **Low:** score below 30
-   **Medium:** score from 30 to below 60
-   **High:** score of 60 or above

These are project-specific assumptions, not official Sri Lankan
flood-warning thresholds.

## Machine-learning approach

The project uses a Random Forest classifier trained on six scenario
input features to predict `risk_category`. The saved model and training
notebook are included in `Prediction model/`; a copy of the model is
also included in `Flood Guard App v1.0/`.

Any reported test metrics describe performance on a held-out split of
this simulated dataset. They do not establish accuracy for real
neighborhoods, actual drainage networks, or future flood events.

## Limitations and responsible use

-   Scenarios and labels are simulated rather than collected from
    verified field measurements.
-   The model has not been calibrated or independently validated against
    observed rainfall, drainage, waste-management, or flood records in
    Sri Lanka.
-   Real flood risk depends on many additional factors, including
    elevation, drainage capacity, land use, soil conditions, river
    levels, tides, and local infrastructure.
-   Predictions should be interpreted as outputs of an educational
    simulation, not as official warnings or operational guidance.
-   Further development would require documented data sources,
    domain-expert review, calibration, independent validation, and
    uncertainty analysis.

## Repository structure

``` text
Complex Systems Project/
├── Flood Guard App v1.0/
│   ├── app.py
│   ├── requirements.txt
│   ├── README.md
│   ├── baseline_flood_risk_model.joblib
│   └── waste_risk_dataset (Simulated data).csv
├── Netlogo file/
│   ├── SriLanka_Waste_Risk.nlogox
│   └── waste_risk_dataset (Simulated data).csv
└── Prediction model/
    ├── Prediction model code.ipynb
    ├── baseline_flood_risk_model.joblib
    └── baseline_model_report (model).csv
```

## Team

-   K.R.D.P. De Zoysa
-   K.W.G.S.B.K.Kulasooriya
-   R.V.S.C. Lenora

## Academic project

Developed for the study of complex systems and agent-based technology at
the University of Sri Jayewardenepura, Sri Lanka.
