import os
import csv
import argparse

#TO DO: make input csv arg optional and grab most recent csv file by date in upload_history folder

def main():
    parser = argparse.ArgumentParser(description="API_link")
    parser.add_argument("token", help="Find token by logging into BrainBox and visiting https://brainbox.pasteur.fr/token")
    parser.add_argument("csv_file", help="Most recent csv file created under upload_history")
    args = parser.parse_args()

    token = args.token
    csv_file=args.csv_file

    tier1_path='/home/feczk001/shared/projects/BCP_BOBs_BIDSified'

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
            aseg='{}/{}/{}/{}_space-INFANTMNIacpc_desc-aseg_dseg.nii.gz'.format(tier1_path, parts[0], parts[1], subses)

            cmd=f'./API_BOBs_submission.sh {awspath} {brainboxsegname} BOBsRepository {aseg} {token}'
            os.system(cmd)

if __name__ == "__main__":
    main()

