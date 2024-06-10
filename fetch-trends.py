from pytrends.request import TrendReq
import pandas as pd
import time
import os

def fetch_trends_data(keywords, timeframe='2020-06-04 2024-06-04'):
    pytrends = TrendReq(hl='fr-FR', tz=0)
    all_data = []

    for keyword in keywords:
        retries = 1  # Number of retries
        delay = 60  # Initial delay in seconds
        while retries > 0:
            try:
                print(f"Fetching data for {keyword} in France...")
                pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo='FR', gprop='')
                interest_over_time_df = pytrends.interest_over_time()
                if not interest_over_time_df.empty:
                    interest_over_time_df = interest_over_time_df.drop(columns=['isPartial'])
                    interest_over_time_df['keyword'] = keyword
                    all_data.append(interest_over_time_df)
                    print(f"Collected data for {keyword} in France")
                else:
                    print(f"No data for {keyword} in France.")
                time.sleep(60)  # 60 sec delay
                break  # Break out of retry loop on success
            except Exception as e:
                retries -= 1
                print(f"An error occurred for keyword {keyword} in France: {e}")
                if retries > 0:
                    print(f"Retrying in {delay} seconds... ({retries} retries left)")
                    time.sleep(delay)
                else:
                    print("Max retries reached, moving to next keyword.")

    if all_data:
        combined_data = pd.concat(all_data, ignore_index=True)
        file_path = os.path.join(os.getcwd(), 'combined_trends_data.csv')
        combined_data.to_csv(file_path, index=False)
        print(f"Saved combined data to {file_path}")
    else:
        print("No data collected for any keyword.")

if __name__ == "__main__":
    kw_list = [
        "smartphone", "laptop",
    ]
    fetch_trends_data(kw_list, timeframe='2020-06-04 2024-06-04')
