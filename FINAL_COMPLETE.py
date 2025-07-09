# Final Union Code: Full CME-SWIS Overlay, All Factors Integrated

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# === Setup ===
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (14, 6)

# === File Paths ===
base_path = r"C:\Users\ricky\Desktop\BAH"
cdf_path = os.path.join(base_path, "cdf file of oct", "merged_blk_th2_data.csv")
cme_path = os.path.join(base_path, "FINAL_MERGED_PRODUCT", "Merged_CACTus_DONKI_OMNI.csv")
extra_dir = os.path.join(base_path, "FINAL_MERGED_PRODUCT", "ALL_DONKI_ORIGINAL_FILES")
output_dir = os.path.join(base_path, "CME_FINAL_FULL_UNION_OUTPUT")
os.makedirs(output_dir, exist_ok=True)

extra_files = [
    "DONKI_MPC_2024-10-01_to_2024-10-31.csv",
    "DONKI_RBE_2024-10-01_to_2024-10-31.csv",
    "DONKI_SEP_2024-10-01_to_2024-10-31.csv",
    "Flattened_DONKI_CME_Data.csv",
    "DONKI_CME_2024-10-01_to_2024-10-31.csv",
    "DONKI_FLR_2024-10-01_to_2024-10-31.csv",
    "DONKI_HSS_2024-10-01_to_2024-10-31.csv",
    "DONKI_IPS_2024-10-01_to_2024-10-31.csv",
    "DONKI_MPC_2024-10-01_to_2024-10-31.csv",
]

# === Load SWIS Data ===
cdf = pd.read_csv(cdf_path)
cdf.columns = [col.strip().replace("\u00c2³", "³") for col in cdf.columns]
cdf.rename(columns={
    "Density (cm³)": "Density",
    "Speed (km/s)": "Speed_SWIS",
    "Temperature (K)": "Temp_SWIS"
}, inplace=True)
cdf["Time"] = pd.to_datetime(cdf["Time"]).dt.tz_localize(None)

# Add integrated flux if available
flux_cols = [col for col in cdf.columns if "flux" in col.lower()]
cdf["Integrated_Flux"] = cdf[flux_cols].sum(axis=1) if flux_cols else np.nan

# === Load CME Data ===
cme = pd.read_csv(cme_path, parse_dates=["Start", "Arrival_L1", "Datetime"])
cme.columns = cme.columns.str.strip()
cme["Arrival_L1"] = pd.to_datetime(cme["Arrival_L1"]).dt.tz_localize(None)
cme["Start"] = pd.to_datetime(cme["Start"]).dt.tz_localize(None)

# === Drag Transit ===
AU_km = 1.5e6
gamma = 0.1 / 3600
def drag_transit(v0, vsw, D=AU_km):
    if pd.isna(v0) or pd.isna(vsw) or v0 <= vsw:
        return np.nan
    return np.log(1 + (gamma * D / (v0 - vsw))) / gamma / 3600

cme["Speed_init"] = cme.get("Speed_x", cme.get("Speed", np.nan))
cme["Speed_solarwind"] = cme.get("Speed_y", np.nan)
cme["Transit_drag_hr"] = cme.apply(lambda r: drag_transit(r["Speed_init"], r["Speed_solarwind"]), axis=1)
cme["Predicted_Arrival"] = cme["Start"] + pd.to_timedelta(cme["Transit_drag_hr"], unit="h")
cme["Delay_hr"] = (cme["Arrival_L1"] - cme["Predicted_Arrival"]).dt.total_seconds() / 3600

# === Flags ===
cme["HaloFlag"] = cme.get("Halo", "").apply(lambda h: h == "Halo")
cme["GeoEffFlag"] = cme["Accurate"].astype(str).str.lower().str.contains("true") if "Accurate" in cme.columns else False
cme["ImpactType"] = cme.get("ImpactType", "Unknown")

# CME-CME interaction
cme = cme.sort_values("Start")
cme["Next_CME_Start"] = cme["Start"].shift(-1)
cme["CME_Interaction_HourGap"] = (cme["Next_CME_Start"] - cme["Arrival_L1"]).dt.total_seconds() / 3600
cme["CME_Interaction_Flag"] = cme["CME_Interaction_HourGap"] < 24

# === Overlay CME-SWIS ===
overlay = pd.merge_asof(
    cdf.sort_values("Time"),
    cme.sort_values("Arrival_L1"),
    left_on="Time",
    right_on="Arrival_L1",
    direction="nearest",
    tolerance=pd.Timedelta("2h")
)
overlay.to_csv(os.path.join(output_dir, "SWIS_CME_OVERLAY_FULL.csv"), index=False)

# === Extra DONKI overlays ===
for fname in extra_files:
    fpath = os.path.join(extra_dir, fname)
    try:
        df = pd.read_csv(fpath)
        if "eventTime" in df.columns:
            df["eventTime"] = pd.to_datetime(df["eventTime"]).dt.tz_localize(None)
            merged = pd.merge_asof(
                cdf.sort_values("Time"),
                df.sort_values("eventTime"),
                left_on="Time",
                right_on="eventTime",
                direction="nearest",
                tolerance=pd.Timedelta("3h")
            )
            merged.to_csv(os.path.join(output_dir, f"SWIS_OVERLAY_{fname}"), index=False)

            plt.figure()
            plt.plot(cdf["Time"], cdf["Density"], label="SWIS Density", color='blue')
            plt.scatter(merged["Time"], merged["Density"], alpha=0.4, color='orange', label="Event Overlay")
            plt.title(f"Overlay with {fname.split('.')[0]}")
            plt.legend(); plt.grid(True); plt.xticks(rotation=45); plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f"PLOT_OVERLAY_{fname.split('.')[0]}.png"))
            plt.close()
    except Exception as e:
        print(f"⚠️ Error with {fname}: {e}")

# === Final Plots ===
speed_col = "Speed" if "Speed" in overlay.columns else ("Speed_init" if "Speed_init" in overlay.columns else None)

plt.figure()
plt.plot(cdf["Time"], cdf["Density"], label="SWIS Density", color="blue")
plt.scatter(overlay["Time"], overlay[speed_col], color="red", alpha=0.5, label="CME Speed")
if "HaloFlag" in overlay:
    halo = overlay[overlay["HaloFlag"].fillna(False)]
    if speed_col in halo.columns:
        plt.scatter(halo["Time"], halo[speed_col], color="black", marker="x", label="Halo CME")
plt.title("SWIS Density vs CME Arrival")
plt.xlabel("Time"); plt.ylabel("Density / Speed"); plt.legend(); plt.grid(True); plt.tight_layout(); plt.xticks(rotation=45)
plt.savefig(os.path.join(output_dir, "Overlay_Density_vs_CME.png")); plt.close()

if "Speed_SWIS" in cdf.columns:
    plt.figure()
    plt.plot(cdf["Time"], cdf["Speed_SWIS"], label="SWIS Speed", color="green")
    plt.scatter(overlay["Time"], overlay[speed_col], color="red", alpha=0.5, label="CME Speed")
    plt.title("SWIS Speed vs CME"); plt.legend(); plt.grid(True); plt.tight_layout(); plt.xticks(rotation=45)
    plt.savefig(os.path.join(output_dir, "Overlay_Speed_vs_CME.png")); plt.close()

if "Temp_SWIS" in cdf.columns:
    plt.figure()
    plt.plot(cdf["Time"], cdf["Temp_SWIS"], label="SWIS Temperature", color="orange")
    plt.scatter(overlay["Time"], overlay[speed_col], color="red", alpha=0.5, label="CME Speed")
    plt.title("SWIS Temp vs CME"); plt.legend(); plt.grid(True); plt.tight_layout(); plt.xticks(rotation=45)
    plt.savefig(os.path.join(output_dir, "Overlay_Temp_vs_CME.png")); plt.close()

if "Integrated_Flux" in cdf.columns:
    plt.figure()
    plt.plot(cdf["Time"], cdf["Integrated_Flux"], label="Integrated Flux", color="purple")
    plt.scatter(overlay["Time"], overlay["Integrated_Flux"], color='red', label="CME Arrival", alpha=0.4)
    plt.title("Integrated Flux vs CME"); plt.legend(); plt.grid(True); plt.tight_layout(); plt.xticks(rotation=45)
    plt.savefig(os.path.join(output_dir, "Overlay_Integrated_Flux_vs_CME.png")); plt.close()

# === Final Save ===
cme.to_csv(os.path.join(output_dir, "FINAL_CME_FULL_UNION.csv"), index=False)
print(f"\n✅ All final overlays, CME propagation models, interaction flags, and scientific plots saved in: {output_dir}")
