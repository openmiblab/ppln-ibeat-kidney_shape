import os

import dbdicom as db

# A: "7128_035_R",
#     "7128_090_R",
#     "5128_036_L",
#     "7128_071_R",
#     "1128_025_L",

# B: "3128_072_R",
#     "2128_008_L",
#     "4128_035_L",
#     "5128_012_L",
#     "3128_107_R",

# A  = [0,2]
# B  = [1,3]


def clean_dataset(build):
    database = os.path.join(build, 'dixon', 'stage_5_clean_dixon_data', 'Patients')
    # 260 files in out_phase and in_phas vs 130 in fat and water. 
    # Seems like all Turku Philips data have this problem
    # Needs a fix at the source
    # Same problem in aligned, which is also missing aligned series. Fix clean then run align again
    for series in db.series(database):
        db.remove_duplicate_frames(series, ['SliceLocation'], dry_run=True)
    # vals = db.values(series, 'SliceLocation')
    # vol = db.volume(series)


if __name__=='__main__':

    ARCHIVE = r'X:\abdominal_imaging\Archive\iBEAt_Build'
    BUILD = r'C:\Users\md1spsx\Documents\Data\iBEAt_Build'

    clean_dataset(BUILD)