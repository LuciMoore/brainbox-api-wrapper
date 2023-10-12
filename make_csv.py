import boto3
import csv
import os
import subprocess
import pandas as pd
from datetime import datetime

# TO DO: add more documentation


# Create BOBSupload_date.csv based on contents of s3 bucket. Outputs a csv file that includes the s3 link to each T1 and T2
# per session in http form in first column and sub-***_ses-***_T1w or T2w in the 2nd column

# Define the Bash script as a string
bash_script = """
#!/bin/bash

# Run the s3info command and store its output in a variable
s3info_output=$(s3info)

# Use grep to find the line containing "Access key" and awk to extract the key
access_key=$(echo "$s3info_output" | grep "Access key" | awk '{print $3}')

# Use grep to find the line containing "Secret key" and awk to extract the key
secret_key=$(echo "$s3info_output" | grep "Secret key" | awk '{print $3}')

# Print 
echo "$access_key"
echo "$secret_key"
"""

# Run the Bash script and capture its output
result_bytes = subprocess.check_output(bash_script, shell=True)

# Decode the bytes to a string
result = result_bytes.decode('utf-8')
final=result.strip()

access=final.split('\n')[0]
secret=final.split('\n')[1] 

bucket_name = 'bobs-repository'

# Initialize the S3 client
s3 = boto3.client(
    service_name='s3',
    aws_access_key_id=access,
    aws_secret_access_key=secret,
    endpoint_url='https://s3.msi.umn.edu',
)

urls = []
try:
    bucket_url = f'https://s3.msi.umn.edu/bobs-repository/'
    response = s3.list_objects_v2(Bucket=bucket_name)

    for obj in response.get('Contents', []):
        object_url = f"{bucket_url}{obj['Key']}"
        #print(f"{obj['Key']}, {object_url}")
        #print(f"{object_url}")
        if 'T1w' in f"{object_url}":
            urls.append(f"{object_url}")
        if 'T2w' in f"{object_url}":
            urls.append(f"{object_url}")

except Exception as e:
    print(f"An error occurred: {str(e)}")

subses=[]
for i in urls:
    file=i.split('/')[-1]
    sub=file.split('_')[0]
    ses=file.split('_')[1]
    if 'T1w' in i:
        subses.append(sub + '_' + ses + '_T1w')
    elif 'T2w' in i:
        subses.append(sub + '_' + ses + '_T2w')

# Create pandas DataFrame to store list of full repo contents
full_repo_df=pd.DataFrame({0: urls, 1: subses})

# Check if there is records of prior BrainBox uploads or not and if not, write csv based on full contents of repo
directory='./upload_history'
if len(os.listdir(directory)) == 0:
    # Write urls and subses lists to 2 separate columns of csv file   
    current_dnt = datetime.now()
    date_format = current_dnt.strftime("%Y-%m-%d")  # Format the date as 'YYYY-MM-DD'
    csv_file = './upload_history/BOBSupload_{}.csv'.format(date_format)
    full_repo_df.to_csv(csv_file, index=False, header=None)

    print(f'Data has been written to {csv_file}')

else:
    # Create DataFrame that is a combination of all prior upload csvs
    # Import prior csv upload files as pandas dataframes 
    dataframes = []

    # Loop through CSV files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path, header=None)
            dataframes.append(df)

    # Combine all DataFrames into a single DataFrame
    prior_uploads_df = pd.concat(dataframes, ignore_index=True)

    # Create new DataFrame that contains only additional lines from  the full_repo_def that are missing from prior uploads
    difference_df = pd.concat([full_repo_df, prior_uploads_df]).drop_duplicates(keep=False)

    # Write urls and subses lists to 2 separate columns of csv file   
    current_dnt = datetime.now()
    date_format = current_dnt.strftime("%Y-%m-%d")  # Format the date as 'YYYY-MM-DD'
    csv_file = './upload_history/BOBSupload_{}.csv'.format(date_format)
    difference_df.to_csv(csv_file, index=False, header=None)

    print(f'Data has been written to {csv_file}')