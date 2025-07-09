import requests
import pandas as pd
import os

API_KEY = "DEMO_KEY"  # Replace with your actual NASA API key
START_DATE = "2024-10-01"
END_DATE = "2024-10-31"
BASE_URL = "https://api.nasa.gov/DONKI"

# 📂 Folder where script is located
script_folder = os.path.dirname(os.path.abspath(__file__))

# 📂 Second custom save location
custom_folder = r"C:\Users\ricky\Desktop\BAH\DONKI DATA"

# Ensure both folders exist
os.makedirs(script_folder, exist_ok=True)
os.makedirs(custom_folder, exist_ok=True)

event_types = {
    "CME": "CME",
    "FLR": "FLR",
    "SEP": "SEP",
    "HSS": "HSS",
    "RBE": "RBE",
    "IPS": "IPS",
    "MPC": "MPC",
    "GST": "GST"
}

for event, endpoint in event_types.items():
    print(f"🔄 Fetching {event} data...")
    url = f"{BASE_URL}/{endpoint}"

    params = {
        "startDate": START_DATE,
        "endDate": END_DATE,
        "api_key": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data:
            print(f"⚠️ No {event} data found.")
            continue

        df = pd.json_normalize(data)

        filename = f"DONKI_{event}_{START_DATE}_to_{END_DATE}.csv"

        # Save to script folder
        path1 = os.path.join(script_folder, filename)
        df.to_csv(path1, index=False)

        # Save to custom folder
        path2 = os.path.join(custom_folder, filename)
        df.to_csv(path2, index=False)

        print(f"✅ {event} data saved to:\n   • {path1}\n   • {path2} ({len(df)} records)")

    except Exception as e:
        print(f"❌ Error fetching {event}: {e}")
