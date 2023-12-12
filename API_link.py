import os
import csv
import argparse
import json

#TO DO: make input csv arg optional and grab most recent csv file by date in upload_history folder

def main():
    parser = argparse.ArgumentParser(description="API_link")
    parser.add_argument("token", help="Find token by logging into BrainBox and visiting https://brainbox.pasteur.fr/token")
    parser.add_argument("csv_file", help="Most recent csv file created under upload_history")
    args = parser.parse_args()

    token = args.token
    csv_file=args.csv_file

    with open("config.json") as json_data_file:
        data = json.load(json_data_file)
    
    tier1_path = data['tier1_path']

    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)

        # Loop through each row in the CSV file
        for row in csv_reader:
            awspath = row[0]  
            subinfo = row[1]  

            parts=subinfo.split('_')
            subses=parts[0] + '_' + parts[1]
            subid=parts[0].strip('sub-')
            sesid=parts[1].strip('ses-')
            brainboxsegname=(sesid+subid+'freesurfer')
            aseg='{}/{}/{}/anat/{}_space-INFANTMNIacpc_desc-aseg_dseg.nii.gz'.format(tier1_path, parts[0], parts[1], subses)

            #cmd=f'sbatch API_link.sh {awspath} {brainboxsegname} BOBsRepository {aseg} {token}'
            #os.system(cmd)

            cmd=f'curl -F url={awspath} -F atlasName={brainboxsegname} -F atlasLabelSet=freesurfer.json -F atlasProject=BOBsRepository -F atlas={aseg} -F token={token} https://brainbox.pasteur.fr/mri/upload'
            
            print(cmd)
            os.system(cmd)

if __name__ == "__main__":
    main()

