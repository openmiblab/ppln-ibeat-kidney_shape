import logging
import os

from ibeat_kidney_shape import (
    stage_1_segment, 
    stage_2_display,
    stage_4_display,
    stage_5_measure,
    stage_6_export,
)

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



if __name__=='__main__':

    ARCHIVE = r'X:\abdominal_imaging\Archive\iBEAt_Build'
    BUILD = r'C:\Users\md1spsx\Documents\Data\iBEAt_Build'

    logging.basicConfig(
        filename=os.path.join(BUILD, 'kidney-shape', 'test_pipeline.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # stage_1_segment.run(BUILD)
    # stage_2_display.run(BUILD)
    # stage_4_display.run(BUILD)
    stage_5_measure.run(BUILD)
    stage_6_export.run(BUILD)