import os
import logging
import argparse

from tqdm import tqdm
import numpy as np
import dbdicom as db
import pydmr
import numpyradiomics as npr


def run(build):

    logging.basicConfig(
        filename=os.path.join(build, 'kidney_shape', 'stage_5_measure.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    dir_masks = os.path.join(build, 'kidney_shape', 'stage_3_edit') 
    dir_output = os.path.join(build, 'kidney_shape', 'stage_5_measure')
    os.makedirs(dir_output, exist_ok=True)

    for database in ['Controls', 'Patients']:
        db_masks = os.path.join(dir_masks, database) 
        db_measure = os.path.join(dir_output, database) 
        run_db(db_masks, db_measure)


def run_db(db_masks, db_measure):

    os.makedirs(db_measure, exist_ok=True)
    class_map = {1: "kidney_left", 2: "kidney_right"}
    dmr_files = []

    for series_mask in tqdm(db.series(db_masks), desc='Extracting metrics'):
        for idx, roi in class_map.items():

            # Get IDs
            patient_id = series_mask[1]
            study_desc = series_mask[2][0]

            # Define outputs
            fname = f"{patient_id}_{study_desc}_{roi}.dmr.zip"
            dmr_file = os.path.join(db_measure, fname)

            # Skip if output exists
            if os.path.exists(dmr_file):
                continue

            try:

                # Read binary mask
                rsf_vol = db.volume(series_mask, verbose=0)
                rsf_mask = (rsf_vol.values==idx).astype(np.float32)
                if np.sum(rsf_mask) == 0:
                    logging.info(f"{fname}: empty mask")
                    continue

                # Get radiomics shape features in cm
                results = npr.shape(rsf_mask, rsf_vol.spacing / 10, transpose=True, extend=True)
                units = npr.shape_units(3, 'cm')

                # Write to dmr file
                dmr = {
                    'data': {f"{roi}-shape-{p}": [f"Shape measure {p} for {roi}", u, 'float'] for p, u in units.items()},
                    'pars': {(patient_id, study_desc, f"{roi}-shape-{p}"): v for p, v in results.items()}
                }
                pydmr.write(dmr_file, dmr)
                dmr_files.append(dmr_file)
                logging.info(f"Successfully computed shapes: {fname}")

            except:

                logging.exception(f"Error computing shapes: {fname}")

    if dmr_files != []:
        dmr_file = os.path.join(db_measure, f'all_kidneys')
        pydmr.concat(dmr_files, dmr_file)



if __name__=='__main__':

    BUILD = r'C:\Users\md1spsx\Documents\Data\iBEAt_Build'

    parser = argparse.ArgumentParser()
    parser.add_argument("--build", type=str, default=BUILD, help="Build folder")
    args = parser.parse_args()


    run(args.build)
