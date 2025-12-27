import streamlit as st
import numpy as np
import joblib

st.set_page_config(page_title="CFRP RC Beam Damage Prediction")

model = joblib.load("model1.joblib")
scaler = joblib.load("scaler.joblib")

st.title("Prediction of Damage Degree of CFRP Retrofitted RC Beams")

st.markdown("### Input Beam Configuration")

col1, col2, col3 = st.columns(3)
W   = col1.number_input("Beam width W (mm)", 250.0, 500.0)
WD  = col2.number_input("W/D ratio", 0.357, 1.25)
L   = col3.number_input("Beam length L (mm)", 4600.0, 7600.0)

col4, col5, col6 = st.columns(3)
rl = col4.number_input("ρl (%)", 0.8, 2.5)
rt = col5.number_input("ρt (%)", 0.1, 0.3)
t  = col6.number_input("CFRP thickness (mm)", 0.0, 3.0)

st.markdown("### Material Properties")
col7, col8 = st.columns(2)
fc = col7.selectbox("Concrete fc (MPa)", [20, 30, 40])
fy = col8.selectbox("Steel fy (MPa)", [420, 520, 690])

col9, col10 = st.columns(2)
ft = col9.selectbox("CFRP ft (MPa)", [1500, 2000, 3140])
fb = col10.number_input("Bond strength fb (MPa)", 0.0, 20.0)

st.markdown("### Blast Load")
col11, col12 = st.columns(2)
Mass = col11.number_input("Explosive weight W (kg)", 5.0, 630.0)
Scale = col12.number_input("Scaled distance Z (m/kg¹ᐟ³)", 128.0, 565.0)

if st.button("Predict"):
    X = np.array([[W, WD, L, rl, rt, t,
                   fb, fc, fy, ft, Scale, Mass]])
    X = scaler.transform(X)
    pred = model.predict(X)[0]
    pred = max(0, round(pred, 3))

    damage = "Low" if pred < 2 else "Medium" if pred < 4 else "High" if pred < 8 else "Collapse"

    st.success(f"Support rotation: **{pred}°**")
    st.warning(f"Damage degree: **{damage}**")
