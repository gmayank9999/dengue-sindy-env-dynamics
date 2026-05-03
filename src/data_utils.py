"""
data_utils.py
─────────────
Reusable data loading, cleaning, and feature engineering helpers
for the DengAI / SINDy dengue project.
"""

import pandas as pd
import numpy as np
from pathlib import Path


# ── Paths ────────────────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).resolve().parent.parent / "dataset"

FEATURES_TRAIN = DATA_DIR / "dengue_features_train (1).csv"
LABELS_TRAIN   = DATA_DIR / "dengue_labels_train (1).csv"
FEATURES_TEST  = DATA_DIR / "dengue_features_test.csv"


# ── City populations (approximate) ──────────────────────────────────────────
CITY_POP = {"sj": 400_000, "iq": 400_000}


# ── Feature groups ──────────────────────────────────────────────────────────
NDVI_COLS = ["ndvi_ne", "ndvi_nw", "ndvi_se", "ndvi_sw"]

TEMP_COLS = [
    "station_avg_temp_c", "reanalysis_avg_temp_k",
    "reanalysis_air_temp_k", "reanalysis_max_air_temp_k",
    "reanalysis_min_air_temp_k", "reanalysis_tdtr_k",
    "station_max_temp_c", "station_min_temp_c",
    "station_diur_temp_rng_c",
]

PRECIP_COLS = [
    "precipitation_amt_mm", "station_precip_mm",
    "reanalysis_precip_amt_kg_per_m2", "reanalysis_sat_precip_amt_mm",
]

HUMIDITY_COLS = [
    "reanalysis_relative_humidity_percent",
    "reanalysis_specific_humidity_g_per_kg",
    "reanalysis_dew_point_temp_k",
]

ENV_FEATURE_COLS = NDVI_COLS + TEMP_COLS + PRECIP_COLS + HUMIDITY_COLS


# ── Loading ─────────────────────────────────────────────────────────────────
def load_raw_data():
    """Load and merge features + labels into a single DataFrame."""
    features = pd.read_csv(FEATURES_TRAIN)
    labels   = pd.read_csv(LABELS_TRAIN)

    df = features.merge(labels, on=["city", "year", "weekofyear"], how="left")
    df["week_start_date"] = pd.to_datetime(df["week_start_date"])
    return df


def split_by_city(df):
    """Return (df_sj, df_iq) sorted by date, with reset index."""
    df_sj = (df[df["city"] == "sj"]
             .sort_values("week_start_date")
             .reset_index(drop=True))
    df_iq = (df[df["city"] == "iq"]
             .sort_values("week_start_date")
             .reset_index(drop=True))
    return df_sj, df_iq


def missing_summary(df):
    """Return a DataFrame summarising missing values per column."""
    n_missing = df.isnull().sum()
    pct_missing = (n_missing / len(df)) * 100
    summary = pd.DataFrame({
        "n_missing": n_missing,
        "pct_missing": pct_missing.round(2),
    })
    return summary[summary["n_missing"] > 0].sort_values(
        "pct_missing", ascending=False
    )
