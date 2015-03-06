## Pipeline for indexing reference file
import sys
import re
import subprocess
from prepc.bwa_commands import *
from prepc.tmap_commands import *
from prepc.picard_commands import *
from prepc.samtools_commands import *

def main(analysis_params):
    #creating log directory

    ## tmap index
    tmap_index_ref(analysis_params['ref'], analysis_params['ref_log'])

    ## bwa index
    bwa_index_ref(analysis_params['ref'], analysis_params['ref_log'])

    # samtools index
    samtools_index_ref(analysis_params['ref'], analysis_params['ref_log'])

    ## picard create dict
    picard_create_dict(analysis_params['ref'], 
    				   analysis_params['ref_dict'],
    				   analysis_params['ref_log'])
