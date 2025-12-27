import streamlit as st
import numpy as np
import joblib

st.set_page_config(page_title="CFRP RC Beam Damage Prediction")

st.markdown("""
<style>
div[data-baseweb="slider"] div {
    background-color: #1f77b4 !important;
}
div[data-baseweb="slider"] span {
    background-color: #1f77b4 !important;
    border-color: #1f77b4 !important;
}
</style>
""", unsafe_allow_html=True)

model = joblib.load("model1.joblib")
scaler = joblib.load("scaler.joblib")

st.title("Damage Degree Prediction of CFRP Retrofitted RC Beams")

st.markdown("### Beam Configuration")

col1, col2, col3 = st.columns(3)
W  = col1.slider("Beam width, W (mm)", 250, 500, 300, step=10)
WD = col2.slider("Width-to-depth ratiio, W/D", 0.35, 1.25, 0.6, step=0.01)
L  = col3.slider("Beam length, L (mm)", 4600, 7600, 6000, step=100)

col4, col5, col6 = st.columns(3)
rl = col4.slider(r"Longitudinal rebar ratio, $\rho_l$ (%)", 0.8, 2.5, 1.2, step=0.01)
rt = col5.slider("Transverse rebar ratio, ρt (%)", 0.1, 0.3, 0.15, step=0.01)
t  = col6.slider("CFRP thickness, tCFRP (mm)", 0.0, 2.0, 1.0, step=0.1)

st.markdown("### Material Properties")
col7, col8 = st.columns(2)
fc = col7.slider("Concrete compressive strength, fc (MPa)", 20, 40, 30, step=5)
fy = col8.slider("Steel yield strength, fy (MPa)", 420, 690, 520, step=10)

col9, col10 = st.columns(2)
ft = col9.slider("CFRP tensile strength, ft (MPa)", 1500, 3140, 2000, step=100)
fb = col10.slider("Bond strength, fb (MPa)", 0, 15, 8, step=1)

st.markdown("### Blast Load")
col11, col12 = st.columns(2)
Mass  = col11.slider("Explosive weight, M (kg)", 5.0, 630.0, 50.0, step=5.0)
Scale = col12.slider("Scaled distance, Z (m/kg¹ᐟ³)", 128.0, 565.0, 300.0, step=5.0)

if st.button("Predict"):
    X = np.array([[W, WD, L, rl, rt, t,
                   fb, fc, fy, ft, Scale, Mass]])
    X = scaler.transform(X)
    pred = model.predict(X)[0]
    pred = max(0, round(pred, 3))

    damage = (
        "Low" if pred < 2 else
        "Medium" if pred < 4 else
        "High" if pred < 8 else
        "Collapse"
    )

    st.success(f"Support rotation: **{pred}°**")
    st.warning(f"Damage degree: **{damage}**")
