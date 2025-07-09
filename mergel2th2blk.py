import cdflib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# === PATH SETUP ===
folder_path = r"C:\Users\ricky\Desktop\BAH\cdf file of oct"
output_csv = os.path.join(folder_path, "merged_blk_th2_data.csv")

blk_dfs = []
th2_dfs = []

# === LOOP OVER CDF FILES ===
for file in sorted(os.listdir(folder_path)):
    file_path = os.path.join(folder_path, file)

    if file.endswith(".cdf") and "L2_BLK" in file:
        try:
            cdf = cdflib.CDF(file_path)
            time = pd.to_datetime(cdflib.cdfepoch.to_datetime(cdf.varget('epoch_for_cdf_mod')))
            density = np.array(cdf.varget('proton_density'), dtype=np.float64)
            speed = np.array(cdf.varget('proton_bulk_speed'), dtype=np.float64)
            temp = np.array(cdf.varget('proton_thermal'), dtype=np.float64)
            xpos = np.array(cdf.varget('spacecraft_xpos'), dtype=np.float64)
            ypos = np.array(cdf.varget('spacecraft_ypos'), dtype=np.float64)
            zpos = np.array(cdf.varget('spacecraft_zpos'), dtype=np.float64)

            # Clean fill values
            density[density < -1e30] = np.nan
            speed[speed < -1e30] = np.nan
            temp[temp < -1e30] = np.nan

            df_blk = pd.DataFrame({
                'Time': time,
                'Density (cm³)': density,
                'Speed (km/s)': speed,
                'Temperature (K)': temp,
                'X_Pos': xpos,
                'Y_Pos': ypos,
                'Z_Pos': zpos
            })
            blk_dfs.append(df_blk)

        except Exception as e:
            print(f"⚠️ Skipped BLK {file}: {e}")

    elif file.endswith(".cdf") and "L2_TH2" in file:
        try:
            cdf = cdflib.CDF(file_path)
            time = pd.to_datetime(cdflib.cdfepoch.to_datetime(cdf.varget('epoch_for_cdf_mod')))
            flux = np.array(cdf.varget('integrated_flux_mod'), dtype=np.float64)
            energy = np.array(cdf.varget('energy_center_mod')[0])

            flux[flux < -1e30] = np.nan
            idxs = [0, len(energy)//2, -1]

            df_th2 = pd.DataFrame({'Time': time})
            for i in idxs:
                df_th2[f'Flux @ {energy[i]:.1f} eV'] = flux[:, i]

            th2_dfs.append(df_th2)

        except Exception as e:
            print(f"⚠️ Skipped TH2 {file}: {e}")

# === COMBINE AND MERGE DATA ===
if not blk_dfs or not th2_dfs:
    print("❌ Missing BLK or TH2 data.")
    exit()

df_blk_all = pd.concat(blk_dfs).dropna(subset=['Time']).sort_values(by='Time')
df_th2_all = pd.concat(th2_dfs).dropna(subset=['Time']).sort_values(by='Time')

merged_df = pd.merge_asof(df_blk_all, df_th2_all, on='Time', direction='nearest', tolerance=pd.Timedelta(seconds=60))
merged_df.to_csv(output_csv, index=False)
print(f"✅ Merged data saved to: {output_csv}")

# === PLOTTING FUNCTIONS ===
def plot_variable(columns, title, ylabel, filename):
    plt.figure(figsize=(14, 6))
    for col in columns:
        if col in merged_df:
            plt.plot(merged_df['Time'], merged_df[col], label=col)
    plt.xlabel("Time")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.xticks(rotation=25)
    save_path = os.path.join(folder_path, filename)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"📈 Saved: {filename}")

# === GENERATE ALL PLOTS ===
plot_variable(['Density (cm³)'], "Proton Density Over Time", "cm³", "plot_density.png")
plot_variable(['Speed (km/s)'], "Proton Speed Over Time", "km/s", "plot_speed.png")
plot_variable(['Temperature (K)'], "Proton Temperature Over Time", "K", "plot_temperature.png")
# --- Compute Total Flux Over Time (mean across channels) ---
flux_cols = [col for col in merged_df.columns if col.startswith("Flux @")]
merged_df['Flux_Total'] = merged_df[flux_cols].mean(axis=1)
plot_variable(['Flux_Total'], "Total Integrated Flux (Time Series)", "Flux", "plot_flux_timeseries.png")
plot_variable(['X_Pos', 'Y_Pos', 'Z_Pos'], "Spacecraft Position (L2_BLK)", "Position (km)", "plot_spacecraft_xyz.png")

print("✅ All individual plots saved successfully.")
