"""
patch_nb02.py  — fixes H(t) aggregation in NB02 to use Magnus formula
blending reanalysis_relative_humidity_percent with dew-point-derived RH.
"""
import json

FIXED_CELL_LINES = [
    "def aggregate_covariates(df):\n",
    "    \"\"\"\n",
    "    Aggregate 20 raw features into 4 physically meaningful covariates.\n",
    "    H(t) now blends reanalysis_relative_humidity_percent with a Magnus-formula\n",
    "    RH estimate derived from reanalysis_dew_point_temp_k, per blueprint spec.\n",
    "    \"\"\"\n",
    "    import numpy as np\n",
    "    out = df.copy()\n",
    "\n",
    "    # T(t): Mean temperature in Celsius\n",
    "    # reanalysis_avg_temp_k is in Kelvin -> convert first\n",
    "    temp_c_from_k = df['reanalysis_avg_temp_k'] - 273.15\n",
    "    out['T'] = (df['station_avg_temp_c'] + temp_c_from_k) / 2.0\n",
    "\n",
    "    # P(t): Mean precipitation (mm)\n",
    "    out['P'] = (df['precipitation_amt_mm'] + df['station_precip_mm']) / 2.0\n",
    "\n",
    "    # H(t): Blueprint specifies blending relative_humidity_percent AND dew_point_temp_k.\n",
    "    # Magnus formula converts dew point to an equivalent RH:\n",
    "    #   RH = 100 * exp(17.625*Td/(243.04+Td)) / exp(17.625*T/(243.04+T))\n",
    "    # where Td = dew-point temperature (Celsius), T = air temperature (Celsius).\n",
    "    Td = df['reanalysis_dew_point_temp_k'] - 273.15   # dew point in Celsius\n",
    "    T_c = temp_c_from_k.copy()                         # air temp in Celsius\n",
    "    RH_magnus = (\n",
    "        100.0\n",
    "        * np.exp(17.625 * Td  / (243.04 + Td))\n",
    "        / np.exp(17.625 * T_c / (243.04 + T_c))\n",
    "    )\n",
    "    RH_magnus = RH_magnus.clip(0, 100)   # enforce physical bounds\n",
    "    out['H'] = (df['reanalysis_relative_humidity_percent'] + RH_magnus) / 2.0\n",
    "\n",
    "    # V(t): Mean NDVI across all 4 quadrants\n",
    "    out['V'] = df[NDVI_COLS].mean(axis=1)\n",
    "\n",
    "    return out\n",
    "\n",
    "\n",
    "df_sj_agg = aggregate_covariates(df_sj_clean)\n",
    "df_iq_agg = aggregate_covariates(df_iq_clean)\n",
    "\n",
    "# Quick summary\n",
    "for code, dfc in [('sj', df_sj_agg), ('iq', df_iq_agg)]:\n",
    "    print(f'\\n=== {city_label(code)} -- Aggregated Covariates ===')\n",
    "    print(dfc[['T', 'P', 'H', 'V']].describe().round(3).to_string())\n",
]

with open('notebooks/02_preprocessing.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Cell 8 is the aggregate_covariates cell
nb['cells'][8]['source'] = FIXED_CELL_LINES
nb['cells'][8]['outputs'] = []
nb['cells'][8]['execution_count'] = None

with open('notebooks/02_preprocessing.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('Patched NB02 cell 8 — H(t) now uses Magnus-formula blend.')
