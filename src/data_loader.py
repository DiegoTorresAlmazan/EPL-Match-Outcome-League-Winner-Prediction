import pandas as pd
import os
import glob

class EPLLoader:
    def __init__(self, raw_dir=None, processed_dir=None):
        # This finds the absolute path to the root directory
        current_file_path = os.path.abspath(__file__) # path to data_loader.py
        src_path = os.path.dirname(current_file_path) # path to src/
        project_root = os.path.dirname(src_path)      # path to project root
        
        # set default directories relative to project root 
        self.raw_dir = raw_dir if raw_dir else os.path.join(project_root, "data", "raw")
        self.processed_dir = processed_dir if processed_dir else os.path.join(project_root, "data", "processed")
        
        self.football_data_path = os.path.join(self.raw_dir, "football_data")
        self.elo_data_path = os.path.join(self.raw_dir, "elo", "club_elo.csv")

        #mapping common name variations to a standard format
        self.team_name_mapping = {
            "Man Utd": "Manchester United",
            "Man City": "Manchester City",
            "Spurs": "Tottenham Hotspur",
            "Chelsea": "Chelsea FC",
            "Arsenal": "Arsenal FC",
            "Liverpool": "Liverpool FC",
            "Newcastle Utd": "Newcastle United",
            "West Ham Utd": "West Ham United",
            "Leicester City": "Leicester City FC",
            "Wolves": "Wolverhampton Wanderers"
        }

    def load_raw_matches(self):
        """combines all csvs from the raw data folder"""
        # Search for CSVs in the absolute path
        search_path = os.path.join(self.football_data_path, "EPL_*.csv")
        all_files = glob.glob(search_path)

        if not all_files:
            raise FileNotFoundError(f"No raw match data files found in: {self.football_data_path}")
        
        li = []
        #only need core columns for now, features.py will handle the rest
        cols_to_use = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'B365H', 'B365D', 'B365A']

        for filename in all_files:
            df = pd.read_csv(filename, encoding= 'latin1')
            #ensure only columns that exist are loaded
            valid_cols = [col for col in cols_to_use if col in df.columns]
            df = df[valid_cols]

            #standardize date format
            df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
            li.append(df)

        combined_df = pd.concat(li, axis=0, ignore_index=True)
        return combined_df.dropna(subset=['Date']).sort_values('Date')
    
    def load_elo_data(self):
        """loads and cleans the club elo data"""
        if not os.path.exists(self.elo_data_path):
            print(f"[ERROR] ELO data file not found at {self.elo_data_path}")
            return None
        
        elo_df = pd.read_csv(self.elo_data_path)
        elo_df["From"] = pd.to_datetime(elo_df["From"])
        elo_df["To"] = pd.to_datetime(elo_df["To"])
        return elo_df
    
    def standardize_teams(self, df):
        """standardizes team names in the given dataframe"""
        df['HomeTeam'] = df['HomeTeam'].replace(self.team_name_mapping)
        df['AwayTeam'] = df['AwayTeam'].replace(self.team_name_mapping)
        return df
        
    def get_full_dataset(self):
        """the main method to call from other scripts"""
        print(f"Searching for data in: {self.football_data_path}")
        matches = self.load_raw_matches()
        matches = self.standardize_teams(matches)

        print(f"Successfully loaded {len(matches)} matches.")
        return matches

if __name__ == "__main__":
    #test the loader
    loader = EPLLoader()
    df = loader.get_full_dataset()

    #save a 'base' version to processed for inspection
    os.makedirs(loader.processed_dir, exist_ok=True)
    output_path = os.path.join(loader.processed_dir, "epl_base_dataset.csv")
    df.to_csv(output_path, index=False)
    print(f"Saved base dataset to {output_path}")