"""
FARS 2023 Integrated Crash-Level Analysis
==========================================
Research Questions:
  1. Which driver, vehicle, and environmental factors are most strongly
     associated with fatal crashes?
  2. How do fatal crash patterns vary across geographic regions, time of day,
     and road types?
  3. What is the impact of alcohol and other impairments on fatality outcomes?
  4. Can we predict the likelihood of a multi-fatality crash given driver,
     vehicle, and environmental variables?

Usage:
    python analyze_fars.py [--data PATH_TO_CSV]

Outputs (saved to ./outputs/):
    figures/01_fatals_distribution.png
    figures/02_crashes_by_region.png
    figures/03_crashes_by_tod_dow.png
    figures/04_road_and_environment.png
    figures/05_impairment_factors.png
    figures/06_vulnerable_road_users.png
    figures/07_driver_age_groups.png
    figures/08_feature_importance.png
    figures/09_crash_correlations.png
    figures/10_state_crashes.png
    results/summary_statistics.csv
    results/logistic_regression_report.txt

"""

import argparse
import os
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")


def _find_repo_root(start: str) -> str:
    current = os.path.abspath(start)
    for _ in range(6):
        if os.path.isdir(os.path.join(current, "data")) and \
           os.path.isdir(os.path.join(current, "scripts")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return os.path.abspath(start)

try:
    _START = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _START = os.path.abspath(os.getcwd())

_REPO_ROOT = _find_repo_root(_START)

DATA_PATH   = os.path.join(_REPO_ROOT, "data", "processed", "fars_integrated_crash_level.csv")
OUTPUT_DIR  = os.path.join(_REPO_ROOT, "outputs")
FIGURES_DIR = os.path.join(OUTPUT_DIR, "figures")
RESULTS_DIR = os.path.join(OUTPUT_DIR, "results")


# Codebook mappings — sourced from NHTSA FARS Analytical User's Manual 2023

REGION_LABELS = {
    1: "New England",
    2: "Mid-Atlantic",
    3: "E. N. Central",
    4: "W. N. Central",
    5: "S. Atlantic",
    6: "E. S. Central",
    7: "W. S. Central",
    8: "Mountain",
    9: "Pacific",
    10: "Puerto Rico",
}

TOD_LABELS = {1: "Daytime", 2: "Nighttime", 3: "Unknown"}

DOW_LABELS = {1: "Weekend (Fri 6pm–Sun)", 2: "Weekday", 3: "Unknown"}

WEATHER_LABELS = {
    1:  "Clear",
    2:  "Cloudy/Overcast",
    3:  "Rain",
    4:  "Sleet/Hail",
    6:  "Snow",
    10: "Fog/Smoke",
    11: "Blowing Sand",
    12: "Freezing Rain",
    13: "Cloudy",
    14: "Blowing Snow",
    15: "Severe Crosswinds",
    98: "Other",
    99: "Unknown",
}

ROADFC_LABELS = {
    1: "Interstate",
    2: "Freeway/Expressway",
    3: "Principal Arterial",
    4: "Minor Arterial",
    5: "Major Collector",
    6: "Minor Collector",
    7: "Local",
    8: "Not in State Inventory",
    9: "Unknown",
}

RU_LABELS     = {1: "Rural", 2: "Urban", 3: "Unknown"}
ALCOHOL_LABELS = {1: "Alcohol Involved", 2: "No Alcohol", 3: "Unknown"}

MANCOL_LABELS = {
    1: "Not Collision w/ MV",
    2: "Front-to-Rear",
    3: "Front-to-Front",
    4: "Angle",
    5: "Sideswipe–Same Dir",
    6: "Sideswipe–Opp Dir",
    7: "Rear-to-Side",
    8: "Rear-to-Rear",
    9: "Other/Unknown",
}

CT_LABELS = {1: "Single-Vehicle", 2: "Two-Vehicle", 3: "3+ Vehicles"}


FLAG_COLS = {
    "A_SPCRA":    "Speeding",
    "A_PED":      "Pedestrian Involved",
    "A_PEDAL":    "Pedalcyclist Involved",
    "A_ROLL":     "Rollover",
    "A_MC":       "Motorcycle Involved",
    "A_LT":       "Large Truck Involved",
    "A_INTER":    "Interstate Highway",      
    "A_INTSEC":   "Intersection Involved",    
    "A_RD":       "Roadway Departure",
    "A_HR":       "Hit and Run",
    "A_DIST":     "Distracted Driving",
    "A_DROWSY":   "Drowsy Driving",
    "A_WRONGWAY": "Wrong-Way Driving",
    "A_D15_19":   "Driver Age 15–19",
    "A_D21_24":   "Driver Age 21–24",
    "A_D65PLS":   "Driver Age 65+",
}

STATE_FIPS = {
    1:"AL",  2:"AK",  4:"AZ",  5:"AR",  6:"CA",  8:"CO",  9:"CT", 10:"DE",
   11:"DC", 12:"FL", 13:"GA", 15:"HI", 16:"ID", 17:"IL", 18:"IN", 19:"IA",
   20:"KS", 21:"KY", 22:"LA", 23:"ME", 24:"MD", 25:"MA", 26:"MI", 27:"MN",
   28:"MS", 29:"MO", 30:"MT", 31:"NE", 32:"NV", 33:"NH", 34:"NJ", 35:"NM",
   36:"NY", 37:"NC", 38:"ND", 39:"OH", 40:"OK", 41:"OR", 42:"PA", 44:"RI",
   45:"SC", 46:"SD", 47:"TN", 48:"TX", 49:"UT", 50:"VT", 51:"VA", 53:"WA",
   54:"WV", 55:"WI", 56:"WY", 72:"PR",
}

PALETTE = "Set2"
ACCENT  = "#E63946"
BG      = "#F8F9FA"


def set_style():
    plt.rcParams.update({
        "figure.facecolor":    BG,
        "axes.facecolor":      BG,
        "axes.spines.top":     False,
        "axes.spines.right":   False,
        "axes.titlesize":      13,
        "axes.titleweight":    "bold",
        "axes.labelsize":      11,
        "xtick.labelsize":     9,
        "ytick.labelsize":     9,
        "font.family":         "sans-serif",
        "figure.dpi":          150,
    })



# Data loading

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"  Loaded {len(df):,} crash records with {df.shape[1]} columns.")

    # Binary (1=Yes) flags for all FLAG_COLS
    for col in FLAG_COLS:
        if col in df.columns:
            df[f"{col}_bin"] = (df[col] == 1).astype(int)

    df["alcohol_involved"] = (df["A_POSBAC"] == 1).astype(int)
    df["multi_fatal"]      = (df["FATALS"] >= 2).astype(int)

    df["region_label"]  = df["A_REGION"].map(REGION_LABELS)
    df["tod_label"]     = df["A_TOD"].map(TOD_LABELS)
    df["dow_label"]     = df["A_DOW"].map(DOW_LABELS)
    df["weather_label"] = df["A_WEATHER"].map(WEATHER_LABELS).fillna("Other")
    df["roadfc_label"]  = df["A_ROADFC"].map(ROADFC_LABELS)
    df["ru_label"]      = df["A_RU"].map(RU_LABELS)
    df["alcohol_label"] = df["A_POSBAC"].map(ALCOHOL_LABELS)
    df["state_abbr"]    = df["STATE"].map(STATE_FIPS)
    df["mancol_label"]  = df["A_MANCOL"].map(MANCOL_LABELS)
    df["ct_label"]      = df["A_CT"].map(CT_LABELS)

    return df


def save_fig(fig, name: str):
    path = os.path.join(FIGURES_DIR, name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {path}")



# Figure 1 — Fatality distribution  (RQ1, RQ2)
def plot_fatals_distribution(df: pd.DataFrame):
    counts = df["FATALS"].value_counts().sort_index()
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    fig.suptitle("Distribution of Fatalities per Crash (2023)", fontsize=14, fontweight="bold")

    ax = axes[0]
    bars = ax.bar(counts.index, counts.values, color=sns.color_palette(PALETTE, len(counts)))
    ax.set_xlabel("Number of Fatalities")
    ax.set_ylabel("Number of Crashes")
    ax.set_title("Crashes by Fatality Count")
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 20,
                f"{bar.get_height():,}", ha="center", va="bottom", fontsize=8)

    ax2 = axes[1]
    ru_fat = (df[df["ru_label"].isin(["Rural", "Urban"])]
              .groupby("ru_label")["FATALS"]
              .value_counts()
              .unstack(fill_value=0))
    ru_fat_pct = ru_fat.div(ru_fat.sum(axis=1), axis=0) * 100
    ru_fat_pct.T.plot(kind="bar", ax=ax2, color=["#2196F3", "#FF9800"])
    ax2.set_title("Fatality Distribution: Rural vs Urban")
    ax2.set_xlabel("Number of Fatalities")
    ax2.set_ylabel("Percentage of Crashes (%)")
    ax2.legend(title="Area Type")
    ax2.tick_params(axis="x", rotation=0)

    fig.tight_layout()
    save_fig(fig, "01_fatals_distribution.png")


# Figure 2 — Geographic distribution  (RQ2)
def plot_geographic(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Geographic Distribution of Fatal Crashes", fontsize=14, fontweight="bold")

    ax = axes[0]
    reg = df["region_label"].value_counts().sort_values(ascending=True)
    ax.barh(reg.index, reg.values, color=sns.color_palette(PALETTE, len(reg)))
    ax.set_title("Total Crashes by NHTSA Region")
    ax.set_xlabel("Number of Fatal Crashes")
    for i, v in enumerate(reg.values):
        ax.text(v + 50, i, f"{v:,}", va="center", fontsize=8)

    ax2 = axes[1]
    state_cnt = (df.groupby("state_abbr")["ST_CASE"]
                   .count()
                   .sort_values(ascending=False)
                   .head(15))
    ax2.bar(state_cnt.index, state_cnt.values, color=ACCENT)
    ax2.set_title("Top 15 States by Fatal Crash Count")
    ax2.set_xlabel("State")
    ax2.set_ylabel("Number of Fatal Crashes")
    ax2.tick_params(axis="x", rotation=45)

    fig.tight_layout()
    save_fig(fig, "02_crashes_by_region.png")


# Figure 3 — Time patterns  (RQ2)
def plot_time_patterns(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Crash Patterns by Time of Day and Day of Week", fontsize=14, fontweight="bold")

    ax = axes[0]
    tod = df[df["tod_label"] != "Unknown"]["tod_label"].value_counts()
    ax.pie(tod.values, labels=tod.index, autopct="%1.1f%%",
           colors=["#FFD54F", "#263238"], startangle=90,
           textprops={"fontsize": 11})
    ax.set_title("Crashes by Time of Day")

    # A_DOW is a weekend flag: 1=Weekend (Fri 6pm–Sun 11:59pm), 2=Weekday
    ax2 = axes[1]
    dow_counts = df[df["dow_label"] != "Unknown"]["dow_label"].value_counts()
    desired_order = ["Weekday", "Weekend (Fri 6pm–Sun)"]
    dow_counts = dow_counts.reindex([d for d in desired_order if d in dow_counts.index])
    bars = ax2.bar(dow_counts.index, dow_counts.values, color=["#90CAF9", ACCENT])
    ax2.set_title("Crashes by Weekend vs. Weekday\n(Weekend = Fri 6pm – Sun 11:59pm)")
    ax2.set_ylabel("Number of Fatal Crashes")
    for bar in bars:
        pct = bar.get_height() / dow_counts.sum() * 100
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 100,
                 f"{bar.get_height():,}\n({pct:.1f}%)", ha="center", va="bottom", fontsize=9)

    fig.tight_layout()
    save_fig(fig, "03_crashes_by_tod_dow.png")


# Figure 4 — Road type, environment, crash type  (RQ1, RQ2)
def plot_road_environment(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Road Type and Environmental Conditions", fontsize=14, fontweight="bold")

    road = (df[~df["roadfc_label"].isin(["Not in State Inventory", "Unknown", None])]
            ["roadfc_label"].value_counts().sort_values(ascending=True))
    ax = axes[0]
    ax.barh(road.index, road.values, color=sns.color_palette("Blues_r", len(road)))
    ax.set_title("Crashes by Road Functional Class\n(Excl. unknown / not in inventory)")
    ax.set_xlabel("Number of Fatal Crashes")
    for i, v in enumerate(road.values):
        ax.text(v + 30, i, f"{v:,}", va="center", fontsize=8)

    ax2 = axes[1]
    weather = (df[df["A_WEATHER"] != 99]["weather_label"]
               .value_counts()
               .sort_values(ascending=True))
    colors = ["#4CAF50" if w == "Clear" else "#607D8B" for w in weather.index]
    ax2.barh(weather.index, weather.values, color=colors)
    ax2.set_title("Crashes by Weather Condition\n(Excl. Unknown)")
    ax2.set_xlabel("Number of Fatal Crashes")
    for i, v in enumerate(weather.values):
        ax2.text(v + 30, i, f"{v:,}", va="center", fontsize=8)

    fig.tight_layout()
    save_fig(fig, "04_road_and_environment.png")


# Figure 5 — Impairment and risky behaviours  (RQ3)
def plot_impairment(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Impact of Impairment and Risky Behaviors", fontsize=14, fontweight="bold")

    ax = axes[0]
    alc = df[df["alcohol_label"] != "Unknown"]["alcohol_label"].value_counts()
    alc_colors = [ACCENT if "Alcohol" in l else "#78909C" for l in alc.index]
    bars = ax.bar(alc.index, alc.values, color=alc_colors)
    ax.set_title("Alcohol Involvement in Fatal Crashes\n(Excluding Unknown BAC)")
    ax.set_ylabel("Number of Crashes")
    for bar in bars:
        pct = bar.get_height() / alc.sum() * 100
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 80,
                f"{bar.get_height():,}\n({pct:.1f}%)", ha="center", va="bottom", fontsize=9)

    ax2 = axes[1]
    risk_cols = {
        "A_SPCRA_bin":    "Speeding",
        "A_DROWSY_bin":   "Drowsy Driving",
        "A_DIST_bin":     "Distracted Driving",
        "A_WRONGWAY_bin": "Wrong-Way Driving",
        "A_HR_bin":       "Hit and Run",
        "alcohol_involved": "Alcohol Involved",
    }
    rates = {label: df[col].mean() * 100
             for col, label in risk_cols.items() if col in df.columns}
    rates_s = pd.Series(rates).sort_values(ascending=True)
    colors = [ACCENT if v >= 20 else "#78909C" for v in rates_s.values]
    ax2.barh(rates_s.index, rates_s.values, color=colors)
    ax2.set_title("Prevalence of Risk Factors\n(% of All Fatal Crashes)")
    ax2.set_xlabel("Percentage of Crashes (%)")
    for i, v in enumerate(rates_s.values):
        ax2.text(v + 0.3, i, f"{v:.1f}%", va="center", fontsize=8)

    fig.tight_layout()
    save_fig(fig, "05_impairment_factors.png")


# Figure 6 — Vulnerable road users  (RQ1)
def plot_vulnerable_users(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Vulnerable Road User Involvement", fontsize=14, fontweight="bold")

    ax = axes[0]
    vru = {
        "Pedestrian":   df["A_PED_bin"].sum(),
        "Pedalcyclist": df["A_PEDAL_bin"].sum(),
        "Motorcyclist": df["A_MC_bin"].sum(),
        "Large Truck":  df["A_LT_bin"].sum(),
    }
    vru_s = pd.Series(vru).sort_values(ascending=True)
    ax.barh(vru_s.index, vru_s.values, color=sns.color_palette(PALETTE, len(vru_s)))
    ax.set_title("Crashes Involving Vulnerable / Special Road Users")
    ax.set_xlabel("Number of Crashes")
    for i, v in enumerate(vru_s.values):
        ax.text(v + 30, i, f"{v:,}", va="center", fontsize=9)

    ax2 = axes[1]
    sub = df[df["ru_label"].isin(["Rural", "Urban"])]
    ped_ru = sub.groupby("ru_label")["A_PED_bin"].mean() * 100
    mc_ru  = sub.groupby("ru_label")["A_MC_bin"].mean()  * 100
    lt_ru  = sub.groupby("ru_label")["A_LT_bin"].mean()  * 100

    x = np.arange(2)
    w = 0.25
    ax2.bar(x - w, ped_ru.values, w, label="Pedestrian",  color="#E63946")
    ax2.bar(x,     mc_ru.values,  w, label="Motorcycle",  color="#457B9D")
    ax2.bar(x + w, lt_ru.values,  w, label="Large Truck", color="#2D6A4F")
    ax2.set_xticks(x)
    ax2.set_xticklabels(["Rural", "Urban"])
    ax2.set_ylabel("% of Crashes")
    ax2.set_title("Vulnerable User Rate by Area Type")
    ax2.legend()

    fig.tight_layout()
    save_fig(fig, "06_vulnerable_road_users.png")


# Figure 7 — Driver age groups  (RQ1)
def plot_driver_age(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Driver Age Group Involvement in Fatal Crashes", fontsize=14, fontweight="bold")

    age_cols = {
        "A_D15_19_bin": "Age 15–19",
        "A_D21_24_bin": "Age 21–24",
        "A_D65PLS_bin": "Age 65+",
    }

    ax = axes[0]
    age_counts = {label: df[col].sum()
                  for col, label in age_cols.items() if col in df.columns}
    age_s = pd.Series(age_counts)
    bars = ax.bar(age_s.index, age_s.values, color=["#FF7043", "#FFA726", "#42A5F5"])
    ax.set_title("Crashes Involving Specific Age Groups")
    ax.set_ylabel("Number of Crashes")
    for bar in bars:
        pct = bar.get_height() / len(df) * 100
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 30,
                f"{bar.get_height():,}\n({pct:.1f}%)", ha="center", va="bottom", fontsize=9)

    ax2 = axes[1]
    tod_valid = df[df["tod_label"] != "Unknown"]
    age_tod = {label: tod_valid.groupby("tod_label")[col].mean() * 100
               for col, label in age_cols.items() if col in tod_valid.columns}
    age_tod_df = pd.DataFrame(age_tod)
    age_tod_df.plot(kind="bar", ax=ax2, color=["#FF7043", "#FFA726", "#42A5F5"])
    ax2.set_title("Age Group Crash Rate by Time of Day")
    ax2.set_ylabel("% of Crashes in That Time Period")
    ax2.set_xlabel("")
    ax2.tick_params(axis="x", rotation=0)
    ax2.legend(title="Age Group", fontsize=8)

    fig.tight_layout()
    save_fig(fig, "07_driver_age_groups.png")


# Figure 8 — Random Forest feature importance  (RQ4)
def plot_feature_importance(df: pd.DataFrame):
    feature_cols = ([f"{c}_bin" for c in FLAG_COLS if f"{c}_bin" in df.columns]
                    + ["alcohol_involved"])
    feature_labels = {f"{c}_bin": FLAG_COLS[c] for c in FLAG_COLS
                      if f"{c}_bin" in df.columns}
    feature_labels["alcohol_involved"] = "Alcohol Involved"

    X = df[feature_cols].fillna(0)
    y = df["multi_fatal"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    rf = RandomForestClassifier(n_estimators=200, class_weight="balanced",
                                random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)

    importances = pd.Series(rf.feature_importances_, index=feature_cols)
    importances.index = [feature_labels[c] for c in importances.index]
    importances = importances.sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(9, 7))
    colors = [ACCENT if importances[k] >= importances.quantile(0.75) else "#90A4AE"
              for k in importances.index]
    ax.barh(importances.index, importances.values, color=colors)
    ax.set_title("Random Forest Feature Importance\n(Predicting Multi-Fatality Crashes)",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Importance Score")
    for i, v in enumerate(importances.values):
        ax.text(v + 0.001, i, f"{v:.3f}", va="center", fontsize=8)

    auc = roc_auc_score(y_test, rf.predict_proba(X_test)[:, 1])
    ax.annotate(f"AUC = {auc:.3f}", xy=(0.98, 0.02), xycoords="axes fraction",
                ha="right", fontsize=10, color="#37474F",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#ECEFF1", edgecolor="none"))

    fig.tight_layout()
    save_fig(fig, "08_feature_importance.png")

    return rf, feature_cols, feature_labels, X_test, y_test


# Figure 9 — Correlation heatmap  (RQ1, RQ3)
def plot_correlations(df: pd.DataFrame):
    corr_cols = ([f"{c}_bin" for c in FLAG_COLS if f"{c}_bin" in df.columns]
                 + ["alcohol_involved", "FATALS"])
    corr_labels = {f"{c}_bin": FLAG_COLS[c] for c in FLAG_COLS
                   if f"{c}_bin" in df.columns}
    corr_labels["alcohol_involved"] = "Alcohol Involved"
    corr_labels["FATALS"] = "Fatalities"

    sub = df[corr_cols].rename(columns=corr_labels)
    corr = sub.corr()

    fig, ax = plt.subplots(figsize=(13, 11))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
                center=0, vmin=-0.4, vmax=0.4, linewidths=0.5,
                ax=ax, annot_kws={"size": 7})
    ax.set_title("Correlation Matrix: Crash Risk Factors & Fatalities",
                 fontsize=14, fontweight="bold", pad=15)
    ax.tick_params(axis="x", rotation=45, labelsize=8)
    ax.tick_params(axis="y", rotation=0,  labelsize=8)

    fig.tight_layout()
    save_fig(fig, "09_crash_correlations.png")


# Figure 10 — State-level crash counts  (RQ2)
def plot_state_crashes(df: pd.DataFrame):
    state_crashes = (df.groupby("state_abbr")["ST_CASE"]
                       .count()
                       .reset_index())
    state_crashes.columns = ["state", "crashes"]
    state_crashes = state_crashes.sort_values("crashes", ascending=False)

    fig, ax = plt.subplots(figsize=(15, 5))
    q75 = state_crashes["crashes"].quantile(0.75)
    colors = [ACCENT if v >= q75 else "#90A4AE" for v in state_crashes["crashes"]]
    ax.bar(state_crashes["state"], state_crashes["crashes"], color=colors)
    ax.set_title("Fatal Crashes by State (2023)", fontsize=14, fontweight="bold")
    ax.set_xlabel("State")
    ax.set_ylabel("Number of Fatal Crashes")
    ax.tick_params(axis="x", rotation=90, labelsize=7)
    top5 = state_crashes.head(5)["state"].tolist()
    for tick in ax.get_xticklabels():
        if tick.get_text() in top5:
            tick.set_color(ACCENT)
            tick.set_fontweight("bold")

    fig.tight_layout()
    save_fig(fig, "10_state_crashes.png")


# Logistic regression report  (RQ4)
def run_logistic_regression(df: pd.DataFrame) -> str:
    feature_cols = ([f"{c}_bin" for c in FLAG_COLS if f"{c}_bin" in df.columns]
                    + ["alcohol_involved"])
    feature_labels = {f"{c}_bin": FLAG_COLS[c] for c in FLAG_COLS
                      if f"{c}_bin" in df.columns}
    feature_labels["alcohol_involved"] = "Alcohol Involved"

    X = df[feature_cols].fillna(0)
    y = df["multi_fatal"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)

    lr = LogisticRegression(class_weight="balanced", max_iter=500, random_state=42)
    lr.fit(X_train_s, y_train)

    y_pred = lr.predict(X_test_s)
    auc    = roc_auc_score(y_test, lr.predict_proba(X_test_s)[:, 1])
    report = classification_report(y_test, y_pred,
                                   target_names=["Single Fatality", "Multi-Fatality"])

    coef_df = pd.DataFrame({
        "Feature":     [feature_labels.get(c, c) for c in feature_cols],
        "Coefficient": lr.coef_[0],
        "Odds Ratio":  np.exp(lr.coef_[0]),
    }).sort_values("Odds Ratio", ascending=False)

    lines = [
        "=" * 65,
        "LOGISTIC REGRESSION: Predicting Multi-Fatality Crashes",
        "=" * 65,
        f"\nTarget: FATALS >= 2  ({y.sum():,} of {len(y):,} crashes = {y.mean()*100:.1f}%)",
        f"\nROC-AUC: {auc:.4f}\n",
        "Classification Report:",
        report,
        "\nOdds Ratios (standardized coefficients):",
        coef_df.to_string(index=False),
        "\nInterpretation: Odds ratio > 1 → associated with HIGHER odds of multi-fatality crash.",
        "=" * 65,
    ]
    return "\n".join(lines)


# Summary statistics CSV  (all RQs)
def save_summary_stats(df: pd.DataFrame):
    rows = []

    rows.append({"Category": "Overall", "Metric": "Total Fatal Crashes",      "Value": len(df)})
    rows.append({"Category": "Overall", "Metric": "Total Fatalities",         "Value": int(df["FATALS"].sum())})
    rows.append({"Category": "Overall", "Metric": "Avg Fatalities per Crash", "Value": round(df["FATALS"].mean(), 3)})
    rows.append({"Category": "Overall", "Metric": "Multi-Fatality Crashes",   "Value": int(df["multi_fatal"].sum())})
    rows.append({"Category": "Overall", "Metric": "Multi-Fatality Rate (%)",  "Value": round(df["multi_fatal"].mean()*100, 2)})

    rows.append({"Category": "Time", "Metric": "Nighttime Crashes",    "Value": int((df["A_TOD"]==2).sum())})
    rows.append({"Category": "Time", "Metric": "Nighttime Rate (%)",   "Value": round((df["A_TOD"]==2).mean()*100, 2)})
    rows.append({"Category": "Time", "Metric": "Weekend Crashes",      "Value": int((df["A_DOW"]==1).sum())})
    rows.append({"Category": "Time", "Metric": "Weekend Rate (%)",     "Value": round((df["A_DOW"]==1).mean()*100, 2)})

    for k, v in df["ru_label"].value_counts().items():
        rows.append({"Category": "Geography", "Metric": f"{k} Crashes", "Value": v})

    rows.append({"Category": "Impairment", "Metric": "Alcohol-Involved Crashes",  "Value": int(df["alcohol_involved"].sum())})
    rows.append({"Category": "Impairment", "Metric": "Alcohol Rate (excl unkn %)", "Value": round(df[df["A_POSBAC"]!=3]["alcohol_involved"].mean()*100, 2)})
    rows.append({"Category": "Impairment", "Metric": "Speeding Crashes",          "Value": int(df["A_SPCRA_bin"].sum())})
    rows.append({"Category": "Impairment", "Metric": "Speeding Rate (%)",         "Value": round(df["A_SPCRA_bin"].mean()*100, 2)})
    rows.append({"Category": "Impairment", "Metric": "Distracted Driving Crashes","Value": int(df["A_DIST_bin"].sum())})
    rows.append({"Category": "Impairment", "Metric": "Drowsy Driving Crashes",    "Value": int(df["A_DROWSY_bin"].sum())})

    rows.append({"Category": "Vulnerable Users", "Metric": "Pedestrian Crashes",  "Value": int(df["A_PED_bin"].sum())})
    rows.append({"Category": "Vulnerable Users", "Metric": "Motorcyclist Crashes", "Value": int(df["A_MC_bin"].sum())})
    rows.append({"Category": "Vulnerable Users", "Metric": "Pedalcyclist Crashes", "Value": int(df["A_PEDAL_bin"].sum())})

    rows.append({"Category": "Road Type", "Metric": "Intersection-Involved Crashes",  "Value": int(df["A_INTSEC_bin"].sum())})
    rows.append({"Category": "Road Type", "Metric": "Interstate Crashes",             "Value": int(df["A_INTER_bin"].sum())})
    rows.append({"Category": "Road Type", "Metric": "Roadway Departure Crashes",      "Value": int(df["A_RD_bin"].sum())})

    summary_df = pd.DataFrame(rows)
    path = os.path.join(RESULTS_DIR, "summary_statistics.csv")
    summary_df.to_csv(path, index=False)
    print(f"  Saved {path}")
    return summary_df


# Main
def main():
    parser = argparse.ArgumentParser(description="FARS 2023 Crash Analysis")
    parser.add_argument("--data", default=DATA_PATH, help="Path to integrated CSV")
    args, _ = parser.parse_known_args()

    os.makedirs(FIGURES_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    set_style()

    print("\n[1/9] Loading data...")
    df = load_data(args.data)

    print("[2/9] Summary statistics...")
    summary = save_summary_stats(df)
    print(summary.to_string(index=False))

    print("\n[3/9] Plot 1: Fatality distributions...")
    plot_fatals_distribution(df)

    print("[4/9] Plot 2: Geographic patterns...")
    plot_geographic(df)

    print("[5/9] Plot 3: Time-of-day & day-of-week patterns...")
    plot_time_patterns(df)

    print("[6/9] Plot 4: Road type & weather...")
    plot_road_environment(df)

    print("[7/9] Plot 5: Impairment & risky behaviors...")
    plot_impairment(df)

    print("[8/9] Plot 6: Vulnerable road users...")
    plot_vulnerable_users(df)

    print("[8b/9] Plot 7: Driver age groups...")
    plot_driver_age(df)

    print("[8c/9] Plot 8: Correlation heatmap...")
    plot_correlations(df)

    print("[8d/9] Fitting Random Forest & plotting feature importance...")
    plot_feature_importance(df)

    print("[8e/9] State-level crash counts...")
    plot_state_crashes(df)

    print("[9/9] Logistic regression model...")
    lr_report = run_logistic_regression(df)
    lr_path = os.path.join(RESULTS_DIR, "logistic_regression_report.txt")
    with open(lr_path, "w") as f:
        f.write(lr_report)
    print(lr_report)
    print(f"  Saved {lr_path}")

    print(f"\n✓ All outputs saved to {OUTPUT_DIR}/")
    print("  Figures:")
    for fn in sorted(os.listdir(FIGURES_DIR)):
        print(f"    {fn}")


if __name__ == "__main__":
    main()