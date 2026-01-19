"""
Mohamad Abdelrahman

Population Health Outcomes & Intervention Optimization

This script builds an analytics pipeline using life expectancy and GDP
data as a proxy for population health. It includes:

1. Data loading and feature engineering
2. Descriptive analytics and visualizations
3. Diagnostic analytics (regression + outcome gaps)
4. Prescriptive analytics (clustering + intervention simulations)

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


# -------------------------------------------------------
# 1. Data Loading & Feature Engineering
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "all_data.csv"
FIGURES_DIR = BASE_DIR / "reports" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def load_data(data_path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(data_path)
    df = df.rename(columns={
        "Life expectancy at birth (years)": "life_expectancy",
        "GDP": "gdp"
    })
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["gdp_log"] = np.log(df["gdp"])
    df["year_index"] = df["Year"] - df["Year"].min()

    # Risk tiers based solely on life expectancy quartiles
    df["risk_tier"] = pd.qcut(
        df["life_expectancy"], 
        4, 
        labels=[1, 2, 3, 4]
    ).astype(int)

    return df


# -------------------------------------------------------
# 2. Descriptive Analytics
# -------------------------------------------------------

def describe_population(df: pd.DataFrame) -> None:
    print("\n--- Population Summary ---")
    print(df[["life_expectancy", "gdp"]].describe())

    gap = df["life_expectancy"].max() - df["life_expectancy"].min()
    print(f"\nLife expectancy gap: {gap:.1f} years")


def plot_descriptive_figures(df: pd.DataFrame, output_dir: Path | None = None) -> None:
    sns.set(style="whitegrid")

    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    # Distribution
    plt.figure()
    sns.histplot(df["life_expectancy"], kde=True)
    plt.title("Distribution of Life Expectancy")
    plt.xlabel("Life expectancy")
    plt.savefig(FIGURES_DIR / "life_expectancy_distribution.png", bbox_inches="tight")
    plt.show()

    # GDP vs Life Expectancy
    plt.figure()
    sns.scatterplot(data=df, x="gdp_log", y="life_expectancy", hue="Country", legend=False)
    plt.title("Life Expectancy vs log(GDP)")
    plt.savefig(FIGURES_DIR / "life_exp_vs_gdp.png", bbox_inches="tight")
    plt.show()

    # Global Trend
    trend = df.groupby("Year")["life_expectancy"].mean().reset_index()
    plt.figure()
    plt.plot(trend["Year"], trend["life_expectancy"], marker="o")
    plt.title("Global Average Life Expectancy Over Time")
    plt.savefig(FIGURES_DIR / "global_life_expectancy_trend.png", bbox_inches="tight")
    plt.show()


# -------------------------------------------------------
# 3. Diagnostic Analytics (Regression)
# -------------------------------------------------------

def fit_outcome_regression(df: pd.DataFrame) -> LinearRegression:
    X = df[["gdp_log", "year_index"]]
    y = df["life_expectancy"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    print("\n--- Outcome Regression Diagnostics ---")
    print(f"R² (train): {model.score(X_train, y_train):.3f}")
    print(f"R² (test):  {model.score(X_test, y_test):.3f}")

    # Residuals
    df["pred"] = model.predict(X)
    df["residual"] = df["life_expectancy"] - df["pred"]

    underperformers = (
        df.groupby("Country")["residual"]
        .mean()
        .sort_values()
        .head(10)
    )

    print("\nUnderperforming Countries:")
    print(underperformers)

    # Residual Plot
    plt.figure()
    sns.scatterplot(data=df, x="gdp_log", y="residual", hue="Country", legend=False)
    plt.axhline(0, color="black", linestyle="--")
    plt.title("Outcome Gap (Residuals)")
    plt.savefig(FIGURES_DIR / "outcome_gap_residuals.png", bbox_inches="tight")
    plt.show()

    return model


# -------------------------------------------------------
# 4. Prescriptive Analytics (Clustering + Simulation)
# -------------------------------------------------------

def cluster_populations(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    scaler = StandardScaler()
    scaled = scaler.fit_transform(df[["life_expectancy", "gdp_log"]])

    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(scaled)

    # Label clusters based on average life expectancy
    profile = df.groupby("cluster")["life_expectancy"].mean().sort_values()
    label_map = {cluster: label for cluster, label in zip(profile.index, 
        ["High Risk", "Elevated Risk", "Moderate Risk", "Low Risk"])}

    df["cluster_label"] = df["cluster"].map(label_map)

    plt.figure()
    sns.scatterplot(data=df, x="gdp_log", y="life_expectancy", hue="cluster_label")
    plt.title("Population Segments (K-Means Clusters)")
    plt.savefig(FIGURES_DIR / "population_segments_clusters.png", bbox_inches="tight")
    plt.show()
    

    return df


def simulate_life_expectancy_change(
    gdp_current: float, 
    year_index: int, 
    delta_gdp_pct: float, 
    model: LinearRegression
) -> tuple[float, float, float]:
    
    gdp_new = gdp_current * (1 + delta_gdp_pct / 100)

    X_curr = pd.DataFrame({"gdp_log": [np.log(gdp_current)], "year_index": [year_index]})
    X_new = pd.DataFrame({"gdp_log": [np.log(gdp_new)], "year_index": [year_index]})

    y_curr = model.predict(X_curr)[0]
    y_new = model.predict(X_new)[0]

    return y_curr, y_new, y_new - y_curr


# -------------------------------------------------------
# 5. Main
# -------------------------------------------------------

def main() -> None:
    df = load_data()
    df = engineer_features(df)

    describe_population(df)
    plot_descriptive_figures(df, output_dir=Path("reports/figures"))

    model = fit_outcome_regression(df)

    df_clusters = cluster_populations(df)

    # Example scenario
    row = df_clusters.iloc[0]
    y_curr, y_new, dy = simulate_life_expectancy_change(
        row["gdp"], row["year_index"], 10, model
    )

    print("\n--- Scenario Simulation (10% GDP Increase) ---")
    print(f"Baseline: {y_curr:.2f} years")
    print(f"After Intervention: {y_new:.2f} years")
    print(f"Δ Life Expectancy: {dy:.2f} years")


if __name__ == "__main__":
    main()