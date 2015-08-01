## Pipeline for performing pairwise somatic variant calling
import sys
import re
import os
import subprocess
from prepc.samtools_commands import *
from prepc.varscan_commands import *
from joblib import Parallel, delayed  
import multiprocessing
num_cores = multiprocessing.cpu_count()


def parallelVarscan(i, analysis_params):
    varscan_somatic(in_mpileup1=analysis_params[i]['mpileup_file1'], 
                        in_mpileup2=analysis_params[i]['mpileup_file2'], 
                        snp_out=analysis_params[i]['varscan_snp_file'], 
                        indel_out=analysis_params[i]['varscan_indel_file'], 
                        log_dir=analysis_params[i]['homogeneity_log'])

def parallelVarscanMpileup(i, analysis_params):
    assert analysis_params[i]['mpileup_file']
    assert os.path.isfile(analysis_params[i]['markdup_file'])


    if not os.path.isfile(analysis_params[i]['mpileup_file']) or \
        os.path.getsize(analysis_params[i]['mpileup_file']) == 0:

        samtools_mpileup_single(in_ref= analysis_params['ref'], 
                                in_bam= analysis_params[i]['markdup_file'],
                                out_mpileup=analysis_params[i]['mpileup_file'], 
                                log_dir=analysis_params['homogeneity']['log_dir'])

        assert os.path.isfile(analysis_params[i]['mpileup_file'])
        assert os.path.getsize(analysis_params[i]['mpileup_file']) > 0
    else:
        print "skipping mpileup for %s" % i

def main(analysis_params):
    print "Homogeneity analysis"
    assert os.path.isfile(analysis_params['ref'])
    assert os.path.isdir(analysis_params['homogeneity']['log_dir'])

    # parallel mpileup
    Parallel(n_jobs=num_cores)(delayed(parallelVarscanMpileup)(i, analysis_params) for i in analysis_params['miseq']['accessions'])

    # parallel varscan
    Parallel(n_jobs=num_cores)(delayed(parallelVarscan)(i, analysis_params) for i in analysis_params['pairs'])
