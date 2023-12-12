import os
import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(description="separate_csv_by_age")
    parser.add_argument("csv", help="csv file created by make_csv.py that you want to split into separate csv for each age")
    args = parser.parse_args()

    # Load csv
    input_csv=args.csv
    full_repo_df=pd.read_csv(input_csv, header=None)

    # Isolate filename from full path in case full path is provided and remmove .csv extension
    bn=os.path.basename(input_csv)
    csv_temp=bn.strip('.csv')

    ages = ['1mo', '2mo', '3mo', '4mo', '5mo', '6mo', '7mo', '8mo']
    for age in ages:
        df = full_repo_df[full_repo_df[1].str.contains(f'{age}')]
        csv_file = f'./upload_history/{csv_temp}_{age}.csv'
        df.to_csv(csv_file, index=False, header=None)

if __name__ == "__main__":
    main()


