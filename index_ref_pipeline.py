## Pipeline for indexing reference file
import sys
import re
import subprocess
import os
from prepc.bwa_commands import *
from prepc.tmap_commands import *
from prepc.picard_commands import *
from prepc.samtools_commands import *


def main(analysis_params):
    #creating log directory

    ## checking inputs
    assert analysis_params
    assert analysis_params['ref']
    assert os.path.isfile(analysis_params['ref'])
    assert analysis_params['ref_log']
    assert os.path.isdir(analysis_params['ref_log'])
    assert analysis_params['ref_dict']


    ## tmap index
    indexed_refs = [analysis_params['ref'] + ".tmap." + i for i in ['anno','bwt','pac','sa']]
    index_check = map(os.path.isfile, indexed_refs)
    if False in index_check:
        tmap_index_ref(analysis_params['ref'], analysis_params['ref_log'])
    else:
        print "skipping tmap indexing, index files present"

    ## bwa index
    indexed_refs = [analysis_params['ref'] + i for i in ['.anb','.ann','.bwt','.pac','.sa']]
    index_check = map(os.path.isfile, indexed_refs)
    if False in index_check:
        bwa_index_ref(analysis_params['ref'], analysis_params['ref_log'])
    else:
        print "skipping bwa indexing, index files present"

    

    # samtools index
    if not os.path.isfile(analysis_params['ref'] + '.fai'):
        samtools_index_ref(analysis_params['ref'], analysis_params['ref_log'])
    else:
        print "skipping fasta index, index files present"

    ## picard create dict
    if not os.path.isfile(analysis_params['ref_dict']):
            picard_create_dict(analysis_params['ref'], 
                       analysis_params['ref_dict'],
                       analysis_params['ref_log'])
    else:
        print "skipping create fasta dict, dict file present"

