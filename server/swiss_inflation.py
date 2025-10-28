import pandas as pd
import zipfile
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

def get_inflation_predictions():
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

    df_pred = pd.DataFrame({
        "Year": X_all.flatten(),
        "Actual": [data.set_index("Year")["Inflation"].get(year, None) for year in X_all.flatten()],
        "Prediction": y_all_pred
    })

    return df_pred
