import streamlit as st
import numpy as np
import joblib

st.set_page_config(page_title="CFRP RC Beam Damage Prediction")

# Custom CSS để đổi màu slider sang #00CC99
st.markdown("""
<style>
    /* Màu thanh slider */
    .stSlider > div > div > div > div {
        background: linear-gradient(to right, #00CC99 0%, #00CC99 var(--value), #e0e0e0 var(--value), #e0e0e0 100%);
    }

    /* Màu nút kéo slider */
    .stSlider > div > div > div > div > div {
        background-color: #00AA7F !important;
    }

    /* Màu khi hover */
    .stSlider > div > div > div > div > div:hover {
        box-shadow: 0 0 0 0.2rem rgba(0, 204, 153, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

model = joblib.load("model1.joblib")
scaler = joblib.load("scaler.joblib")

st.title("Damage Degree Prediction of CFRP Retrofitted RC Beams")

st.markdown("### Input Parameters")

col1, col2, col3 = st.columns(3)
W  = col1.slider(r"Beam width, $W$ (mm)", 250, 500, 300, step=10)
WD = col2.slider(r"Width-to-depth ratiio, $W/D$", 0.35, 1.25, 0.6, step=0.01)
L  = col3.slider(r"Beam length, $L$ (mm)", 4600, 7600, 6000, step=100)

col4, col5, col6 = st.columns(3)
rl = col4.slider(r"Longitudinal rebar ratio, $\rho_l$ (%)", 0.8, 2.5, 1.2, step=0.01)
rt = col5.slider(r"Transverse rebar ratio, $\rho_t$ (%)", 0.1, 0.3, 0.15, step=0.01)
t  = col6.slider(r"CFRP thickness, $t_{CFRP}$ (mm)", 0.0, 2.0, 1.0, step=0.5)

col7, col8, col9 = st.columns(3)
fc = col7.slider(r"Concrete compressive strength, $f_c$ (MPa)", 20, 40, 30, step=5)
fy = col8.slider(r"Steel yield strength, $f_y$ (MPa)", 420, 690, 520, step=10)
ft = col9.slider(r"CFRP tensile strength, $f_t$ (MPa)", 1500, 3140, 2000, step=100)

col10, col11, col12 = st.columns(3)
fb = col10.slider(r"Bond strength, $f_b$ (MPa)", 0, 15, 8, step=1)
Mass  = col11.slider(r"Explosive weight, $M$ (kg)", 5.0, 630.0, 50.0, step=5.0)
Scale = col12.slider(r"Scaled distance, $Z$ (m/kg¹ᐟ³)", 128.0, 565.0, 300.0, step=5.0)


if st.button("Predict"):
    X = np.array([[W, WD, L, rl, rt, t, fb, fc, fy, ft, Scale, Mass]])
    X = scaler.transform(X)
    pred = model.predict(X)[0]
    pred = max(0, np.round(pred, 2))

    damage = (
        "Low" if pred < 2 else
        "Medium" if pred < 4 else
        "High" if pred < 8 else
        "Collapse"
    )

    st.success(f"Support rotation: **{pred}°**")
    st.warning(f"Damage degree: **{damage}**")
