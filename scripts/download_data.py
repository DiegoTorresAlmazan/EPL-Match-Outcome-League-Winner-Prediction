import os
import requests
import time

# -----------------------------
# Configuration
# -----------------------------

FOOTBALL_DATA_BASE_URL = "https://www.football-data.co.uk/mmz4281"
ELO_DATA_URL = "https://api.clubelo.com/clubelo.csv"

START_SEASON = 2005
END_SEASON = 2024  # 2024/25 is last completed season

RAW_DATA_DIR = "data/raw"
FOOTBALL_DATA_DIR = os.path.join(RAW_DATA_DIR, "football_data")
ELO_DATA_DIR = os.path.join(RAW_DATA_DIR, "elo")

# -----------------------------
# Helpers
# -----------------------------

def ensure_directories():
    os.makedirs(FOOTBALL_DATA_DIR, exist_ok=True)
    os.makedirs(ELO_DATA_DIR, exist_ok=True)

import requests
import time

def download_file(url, output_path, retries=5, timeout=60):
    for attempt in range(1, retries + 1):
        try:
            print(f"[ATTEMPT {attempt}] Downloading {url}")
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                f.write(response.content)

            print(f"[SUCCESS] Saved to {output_path}")
            return

        except requests.exceptions.RequestException as e:
            print(f"[WARNING] Attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(5)
            else:
                print("[ERROR] All retries failed. Skipping download.")

# -----------------------------
# Download EPL Match Data
# -----------------------------

def download_epl_match_data():
    for year in range(START_SEASON, END_SEASON + 1):
        next_year = year + 1

        # Football-Data season code (e.g. 0506)
        season_code = f"{str(year)[-2:]}{str(next_year)[-2:]}"
        url = f"{FOOTBALL_DATA_BASE_URL}/{season_code}/E0.csv"

        output_file = f"EPL_{year}_{next_year}.csv"
        output_path = os.path.join(FOOTBALL_DATA_DIR, output_file)

        download_file(url, output_path)

# -----------------------------
# Download Club ELO Data
# -----------------------------

def download_elo_data():
    output_path = os.path.join(ELO_DATA_DIR, "club_elo.csv")
    try:
        download_file(ELO_DATA_URL, output_path)
    except Exception as e:
        print("[WARNING] Club ELO download failed. Continuing without ELO data.")


# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":
    ensure_directories()

    print("=== Downloading EPL Match Data ===")
    download_epl_match_data()

    print("\n=== Downloading Club ELO Data ===")
    download_elo_data()

    print("\n Data download complete.")
