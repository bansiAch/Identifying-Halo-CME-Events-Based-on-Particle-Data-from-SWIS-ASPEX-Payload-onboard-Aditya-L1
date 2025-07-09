import pandas as pd
from datetime import datetime, timedelta
import re

# Path to your CACTus CME file
file_path = r'C:\Users\ricky\Desktop\BAH\CACtus of oct\oct.txt'

# Load and read the text file
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Parse CME entries
cme_data = []
for line in lines:
    parts = [p.strip() for p in line.split('|')]
    
    if len(parts) >= 6:  # Ensure enough columns for ID, Start, Duration, Speed, PA, DA
        try:
            # Skip flow entries
            if 'Flow' in parts[0]:
                continue

            # Extract numeric CME ID from HTML
            match = re.search(r'>(\d+)</a>', parts[0])
            cme_id = match.group(1) if match else parts[0]

            start_str = parts[1]                     # e.g., '2024/10/15 14:00'
            duration_hours = float(parts[2])
            speed = float(parts[5])                  # in km/s
            pa = float(parts[3])                     # principal angle
            da = float(parts[4])                     # angular width in degrees

            start_time = datetime.strptime(start_str, '%Y/%m/%d %H:%M')
            end_time = start_time + timedelta(hours=duration_hours)

            # Prepare for arrival delay calculation (Sun to L1 = 1.5 million km)
            sun_to_l1_km = 1.5e6
            travel_time_sec = sun_to_l1_km / speed if speed > 0 else None
            arrival_time = start_time + timedelta(seconds=travel_time_sec) if travel_time_sec else None

            cme_data.append({
                'ID': cme_id,
                'Start': start_time,
                'End': end_time,
                'Speed': speed,
                'PA': pa,
                'da': da,
                'ArrivalTime_L1': arrival_time
            })

        except Exception as e:
            continue  # Skip bad lines

# Convert to DataFrame
cme_df = pd.DataFrame(cme_data)

# Save to CSV
save_path = r'C:\Users\ricky\Desktop\BAH\CACtus of oct\parsed_oct_cmes.csv'
cme_df.to_csv(save_path, index=False)

# Print result
print(f"✅ CME data (with angular width) saved to:\n{save_path}")
print(cme_df.head())
