import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# FloodGuard Sri Lanka — Streamlit interface
# Place baseline_flood_risk_model.joblib and waste_risk_dataset.csv
# in the same folder as this file.
# ---------------------------------------------------------

st.set_page_config(
    page_title="FloodGuard Sri Lanka",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="expanded",
)

FEATURES = [
    "rainfall_intensity",
    "collection_interval",
    "public_awareness",
    "waste_generation_rate",
    "num_households",
    "num_collectors",
]

FRIENDLY_NAMES = {
    "rainfall_intensity": "Rainfall intensity",
    "collection_interval": "Collection interval",
    "public_awareness": "Public awareness",
    "waste_generation_rate": "Waste generation rate",
    "num_households": "Number of households",
    "num_collectors": "Number of collectors",
}

RISK_COLORS = {"Low": "#2E8B57", "Medium": "#E0A126", "High": "#D9534F"}

@st.cache_resource
def load_model(path):
    return joblib.load(path)

@st.cache_data
def load_dataset(path):
    return pd.read_csv(path)

def risk_color(category):
    return RISK_COLORS.get(str(category), "#64748b")

def main():
    st.markdown(
        """
        <style>
        .block-container {padding-top: 1.8rem; padding-bottom: 2rem;}
        .hero {
            padding: 1.5rem 1.7rem; border-radius: 18px;
            background: linear-gradient(115deg, #12352d, #176b50);
            color: white; margin-bottom: 1.2rem;
        }
        .hero h1 {color: white; margin: 0; font-size: 2.2rem;}
        .hero p {color: #d8eee3; margin: .45rem 0 0 0;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.title("🌧️ FloodGuard")
    st.sidebar.caption("Smart Waste & Urban Flood-Risk Simulation")
    page = st.sidebar.radio(
        "Navigate",
        ["Risk prediction", "Dataset explorer", "About & limitations"],
    )

    model_path = Path(__file__).parent / "baseline_flood_risk_model.joblib"
    data_path = Path(__file__).parent / "waste_risk_dataset (Simulated data).csv"

    st.markdown(
        """
        <div class="hero">
            <h1>FloodGuard Sri Lanka</h1>
            <p>Explore waste-management scenarios and a simulation-trained flood-risk classifier.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if page == "Risk prediction":
        st.subheader("Analyse a scenario")
        st.write(
            "Adjust the inputs to estimate the risk category predicted by your "
            "baseline Random Forest model."
        )

        if not model_path.exists():
            st.error("Model file not found: baseline_flood_risk_model.joblib")
            st.info(
                "Copy your saved baseline model into the same folder as app.py. "
                "The app expects the exact filename shown above."
            )
            st.stop()

        model = load_model(str(model_path))

        left, right = st.columns([1, 1.15], gap="large")
        with left:
            st.markdown("#### Scenario settings")
            rainfall = st.slider("Rainfall intensity", 0, 100, 55)
            collection = st.slider("Collection interval (days)", 1, 7, 3)
            awareness = st.slider("Public awareness", 0, 100, 60)
            generation = st.slider("Waste generation rate", 1, 10, 5)
            households = st.slider("Number of households", 10, 100, 50)
            collectors = st.slider("Number of collectors", 1, 10, 5)

            analyse = st.button("🔎 Analyse scenario", type="primary", use_container_width=True)

        with right:
            st.markdown("#### Prediction")
            st.caption("The result is based on the simulation-generated training labels.")
            if analyse:
                row = pd.DataFrame([{
                    "rainfall_intensity": rainfall,
                    "collection_interval": collection,
                    "public_awareness": awareness,
                    "waste_generation_rate": generation,
                    "num_households": households,
                    "num_collectors": collectors,
                }], columns=FEATURES)

                try:
                    prediction = str(model.predict(row)[0])
                    color = risk_color(prediction)
                    st.markdown(
                        f"""
                        <div style="padding:1.25rem;border-radius:14px;
                                    border:1px solid {color};background:{color}15;">
                            <div style="font-size:.95rem;color:#64748b;">Predicted risk category</div>
                            <div style="font-size:2.3rem;font-weight:700;color:{color};">{prediction}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    if hasattr(model, "predict_proba"):
                        probabilities = model.predict_proba(row)[0]
                        classes = [str(c) for c in model.classes_]
                        prob_df = pd.DataFrame({
                            "Risk category": classes,
                            "Model probability": probabilities,
                        }).sort_values("Model probability", ascending=False)
                        st.write("**Model probabilities**")
                        st.bar_chart(prob_df.set_index("Risk category"))
                        st.caption(
                            "These probabilities reflect the classifier's outputs, "
                            "not calibrated probabilities of a real flood occurring."
                        )
                except Exception as exc:
                    st.error(f"Prediction failed: {exc}")
                    st.warning(
                        "Check that the saved model was trained with the six expected input features."
                    )
            else:
                st.info("Choose the scenario settings, then select **Analyse scenario**.")
                st.markdown(
                    """
                    **Risk categories**
                    - 🟢 **Low** — model predicts the Low class
                    - 🟠 **Medium** — model predicts the Medium class
                    - 🔴 **High** — model predicts the High class
                    """
                )

        st.divider()
        st.warning(
            "Educational prototype only. This classifier learns from synthetic NetLogo "
            "labels and is not validated for real-world flood forecasting in Sri Lanka."
        )

    elif page == "Dataset explorer":
        st.subheader("Explore simulation scenarios")
        if not data_path.exists():
            st.error("Dataset not found: waste_risk_dataset.csv")
            st.info("Copy your 5,000-row CSV into the same folder as app.py.")
            st.stop()

        df = load_dataset(str(data_path))
        st.caption(f"Loaded {len(df):,} simulation scenarios.")
        c1, c2, c3 = st.columns(3)
        c1.metric("Scenarios", f"{len(df):,}")
        if "risk_category" in df.columns:
            c2.metric("Risk categories", df["risk_category"].nunique())
            c3.metric("Columns", len(df.columns))
            st.write("**Risk-category distribution**")
            counts = df["risk_category"].value_counts().rename_axis("Risk category").to_frame("Scenarios")
            st.bar_chart(counts)

        if "risk_category" in df.columns:
            choices = ["All"] + sorted(df["risk_category"].dropna().astype(str).unique().tolist())
            selected = st.selectbox("Filter by risk category", choices)
            view = df if selected == "All" else df[df["risk_category"].astype(str) == selected]
        else:
            view = df

        st.write(f"Showing {len(view):,} rows")
        st.dataframe(view.head(1000), use_container_width=True, hide_index=True)
        st.caption("The table displays up to the first 1,000 filtered rows for easier browsing.")
        st.download_button(
            "⬇️ Download displayed data as CSV",
            data=view.to_csv(index=False).encode("utf-8"),
            file_name="filtered_waste_risk_dataset.csv",
            mime="text/csv",
        )

        numeric = df.select_dtypes(include="number").columns.tolist()
        if numeric:
            st.write("**Explore a numeric variable**")
            selected_num = st.selectbox("Choose a variable", numeric)
            st.line_chart(df[selected_num].reset_index(drop=True))

    else:
        st.subheader("About this project")
        st.markdown(
            """
            **Project:** Smart Waste Management and Urban Flood-Risk Simulation in Sri Lanka  
            **Course:** Complex Systems & Agent Technology  
            **Institution:** University of Sri Jayewardenepura  
            **Tools:** NetLogo, Python, pandas, scikit-learn and Streamlit

            The project combines an agent-based model of household waste and collection
            with a Random Forest classifier trained on 5,000 synthetic scenarios.
            """
        )
        st.subheader("Important assumptions and limitations")
        st.markdown(
            """
            - The neighbourhood and scenario dataset are hypothetical.
            - The model does not explicitly simulate drainage networks, elevation,
              runoff, water depth or physical flood propagation.
            - The blockage index and risk thresholds are simplified educational assumptions.
            - The classifier learns to reproduce labels generated by the simulation.
            - Test-set accuracy does not demonstrate accuracy for real flood events.
            """
        )
        st.info(
            "Do not use this prototype for emergency decisions or operational flood-risk assessment. "
            "Real-world use would require observed data and hydrological validation."
        )

    st.sidebar.divider()
    st.sidebar.caption("University of Sri Jayewardenepura · Course prototype")

if __name__ == "__main__":
    main()
