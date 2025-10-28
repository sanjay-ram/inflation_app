import os
import pandas as pd
import zipfile
import numpy as np
from sklearn.linear_model import LinearRegression

def get_inflation_predictions():
    # Pfad zur ZIP-Datei (relativ zum Skript)
    current_dir = os.path.dirname(__file__)
    zip_path = os.path.join(current_dir, "API_FP.CPI.TOTL.ZG_DS2_en_csv_v2_23195.zip")

    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"ZIP-Datei nicht gefunden: {zip_path}")

    # Lade CSV aus ZIP
    with zipfile.ZipFile(zip_path, "r") as z:
        csv_name = [f for f in z.namelist() if f.startswith("API_") and f.endswith(".csv")][0]
        df = pd.read_csv(z.open(csv_name), skiprows=4)

    # Filtere Schweiz (sicher mit Ländercode)
    switzerland = df[df["Country Code"] == "CHE"]

    # Formatiere Daten
    data = switzerland.melt(
        id_vars=["Country Name", "Country Code", "Indicator Name"],
        var_name="Year",
        value_name="Inflation"
    )
    data = data[data["Year"].str.isnumeric()]
    data["Year"] = data["Year"].astype(int)
    data = data[["Year", "Inflation"]].dropna()

    if data.empty:
        raise ValueError("Keine Inflationsdaten für die Schweiz gefunden.")

    # Trainiere Modell (ohne Test-Set – wir nutzen alle Daten)
    X = data[["Year"]]
    y = data["Inflation"]
    model = LinearRegression()
    model.fit(X, y)

    # Vorhersage bis 2030
    future_years = np.arange(data["Year"].min(), 2031)
    X_all = pd.DataFrame({"Year": future_years})
    y_all_pred = model.predict(X_all)

    # Erstelle Ergebnis-DataFrame
    inflation_map = data.set_index("Year")["Inflation"]
    actual_vals = []
    for year in future_years:
        val = inflation_map.get(year, np.nan)
        # Wandle NaN explizit in None um (→ null in JSON)
        actual_vals.append(None if pd.isna(val) else val)

    df_pred = pd.DataFrame({
        "Year": future_years,
        "Actual": actual_vals,
        "Prediction": y_all_pred
    })

    # 🔥 WICHTIG: Ersetze alle verbliebenen NaN durch None
    df_pred = df_pred.where(pd.notna(df_pred), None)

    return df_pred