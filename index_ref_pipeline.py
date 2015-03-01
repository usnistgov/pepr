## Pipeline for indexing reference file
import sys
import re
import subprocess
from prepc.bwa_commands import *
from prepc.tmap_commands import *
from prepc.picard_commands import *

def main(pipeline_params):
    #creating log directory
    ref_log_dir = pipeline_params['ref_dir'] + "/log/"
    subprocess.call(['mkdir',ref_log_dir])

    ## tmap index
    tmap_index_ref(pipeline_params['ref'], ref_log_dir)

    ## bwa index
    bwa_index_ref(pipeline_params['ref'], ref_log_dir)

    ## picard create dict
    ref_dict = pipeline_params['ref_dir'] + "/" + \
                pipeline_params['ref_root'] + ".dict"
    picard_create_dict(pipeline_params['ref'], 
    				   ref_dict,
    				   ref_log_dir)
