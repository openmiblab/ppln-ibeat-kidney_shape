import os
import logging
import argparse
from datetime import date

import pydmr
import pandas as pd


def run(build):

    logging.basicConfig(
        filename=os.path.join(build, 'kidney-shape', 'stage_6_export.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    dir_measure = os.path.join(build, 'kidney-shape', 'stage_5_measure')
    dir_output = os.path.join(build, 'kidney-shape', 'stage_6_export')
    os.makedirs(dir_output, exist_ok=True)

    run_db(dir_measure, dir_output)
        


def run_db(dir_measure, dir_output):

    today = date.today().strftime("%Y-%m-%d")
    for group in ['Controls', 'Patients']:

        # Outputs
        dmr_output_file = os.path.join(dir_output, f'{group}_KidneyShape_{today}')
        long_format_file = os.path.join(dir_output, f'{group}_KidneyShape_{today}.csv')
        wide_format_file = os.path.join(dir_output, f'{group}_KidneyShape_{today}_wide.csv')

        # Inputs
        db_measure = os.path.join(dir_measure, group)
        dmr_file = os.path.join(db_measure, f'all_kidneys.dmr.zip')
        if not os.path.exists(dmr_file):
            continue
    
        # Append parsed biomarkers in the dictionary
        dmr = pydmr.read(dmr_file)
        dmr['columns'] = ['body_part', 'image', 'biomarker_category', 'biomarker']
        for p in dmr['data']:
            parts = p.split('-')
            # For intrinsic markers add image 'mask'
            if len(parts) == 3:
                parts = [parts[0]] + ['mask'] + parts[1:]
            dmr['data'][p] += parts

        # Change PatientIDs to central format
        pars_harmonized = {}
        for p,v in dmr['pars'].items():
            harmonized_id = f"iBE-{p[0].replace('_','')}"
            visit = visit_nr(p[1])
            harmonized_id, visit = fix_exeter_volunteer(harmonized_id, visit)
            pars_harmonized[(harmonized_id, visit, p[2])] = v
        dmr['pars'] = pars_harmonized

        # Save results
        pydmr.write(dmr_output_file, dmr)
        pydmr.pars_to_long(dmr_output_file, long_format_file)
        pydmr.pars_to_wide(dmr_output_file, wide_format_file)

        # Replace column names in long and wide formats
        new_cols = {
            "subject": "harmonized_id",
            "study": "visit_nr",
            "value": "result",
        }
        df = pd.read_csv(long_format_file)
        df.rename(columns=new_cols, inplace=True)
        df.to_csv(long_format_file, index=False)
        
        df = pd.read_csv(wide_format_file)
        df.rename(columns=new_cols, inplace=True)
        df.to_csv(wide_format_file, index=False)

        logging.info(f"Successfully exported {group}")



def visit_nr(value):
    if value == 'Baseline':
        return 0
    if value == 'Followup':
        return 2
    if value[:5] == 'Visit':
        return int(value[5]) - 1
    
    
def fix_exeter_volunteer(harmonized_id, visit_nr):
    # Correct a mistake in ID 
    # Exeter volunteer 3 is the same person as volunteer 1
    # This needs to be removed when the issue is fixed at the source
    if harmonized_id == 'iBE-3128C03':
        harmonized_id = 'iBE-3128C01'
        visit_nr += 2
    return harmonized_id, visit_nr


if __name__=='__main__':

    BUILD = r'C:\Users\md1spsx\Documents\Data\iBEAt_Build'

    parser = argparse.ArgumentParser()
    parser.add_argument("--build", type=str, default=BUILD, help="Build folder")
    args = parser.parse_args()

    run(args.build)
        