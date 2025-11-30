import streamlit as st
import pandas as pd
import zipfile
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import plotly.express as px

st.title("🇨🇭 Schweizer Inflation – Analyse & Prognose")


with zipfile.ZipFile("API_FP.CPI.TOTL.ZG_DS2_en_csv_v2_23195.zip", "r") as z:
    csv_name = [f for f in z.namelist() if f.startswith("API_") and f.endswith(".csv")][0]
    df = pd.read_csv(z.open(csv_name), skiprows=4)


switzerland = df[df["Country Name"] == "Switzerland"]
data = switzerland.melt(
    id_vars=["Country Name", "Country Code", "Indicator Name"],
    var_name="Year", value_name="Inflation"
)
data = data[data["Year"].str.isnumeric()]
data["Year"] = data["Year"].astype(int)
data = data[["Year", "Inflation"]].dropna()


X = data[["Year"]]
y = data["Inflation"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)


X_all = np.arange(data["Year"].min(), 2031).reshape(-1, 1)
y_all_pred = model.predict(X_all)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

infl_2025 = model.predict(np.array([[2025]]))[0]
infl_2026 = model.predict(np.array([[2026]]))[0]
infl_2027 = model.predict(np.array([[2027]]))[0]
infl_2028 = model.predict(np.array([[2028]]))[0]
infl_2029 = model.predict(np.array([[2029]]))[0]
infl_2030 = model.predict(np.array([[2030]]))[0]
change_pct = ((infl_2030 - infl_2025) / abs(infl_2025)) * 100


fig = px.line(
    data, x="Year", y="Inflation", title="Inflation in der Schweiz",
    labels={"Year": "Jahr", "Inflation": "Inflation (%)"}
)
fig.add_scatter(x=X_all.flatten(), y=y_all_pred, mode="lines", name="Vorhersage (Trend)", line=dict(dash="dash", color="red"))

st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("MSE", f"{mse:.3f}")
col2.metric("R²", f"{r2:.3f}")
col3.metric("Δ 2025–2030", f"{change_pct:.2f}%")

st.subheader("Vorhersagen")
st.write(f" **2025:** {infl_2025:.2f}%")
st.write(f" **2026:** {infl_2026:.2f}%")
st.write(f" **2027:** {infl_2027:.2f}%")
st.write(f" **2028:** {infl_2028:.2f}%")
st.write(f" **2029:** {infl_2029:.2f}%")
st.write(f"**2030:** {infl_2030:.2f}%")

st.caption("Quelle: Weltbank – Consumer Price Index (Inflation)")