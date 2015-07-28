# ###QC stats for fastq and mapped bam files
# 
# Input: fastq, and mapped bam files    
# Output: summary stat files from picard and fastqc
import sys
import re
import subprocess
import os
# from prepc.qc_stats_commands import *
from prepc.picard_commands import picard_multiple_metrics
from prepc.samtools_commands import samtools_depth

from joblib import Parallel, delayed  
import multiprocessing
num_cores = multiprocessing.cpu_count()

def parallelQCstats(i, analysis_params):
    ## variable check
    assert i
    assert analysis_params
    assert analysis_params[i]['bam_metrics']
    assert analysis_params[i]['bam_depth']

    ## input directory and file check
    assert os.path.isfile(analysis_params[i]['sorted_bam'])
    assert os.path.isdir( analysis_params['qc_stats']['log_dir'])

    picard_multiple_metrics(in_bam = analysis_params[i]['sorted_bam'],
       bam_stats = analysis_params[i]['bam_metrics'], 
       log_dir = analysis_params['qc_stats']['log_dir'])
    samtools_depth(in_bam = analysis_params[i]['sorted_bam'], 
        out_depth =analysis_params[i]['bam_depth'], 
        log_dir = analysis_params['qc_stats']['log_dir']) 

def main(analysis_params):
    Parallel(n_jobs=num_cores)(delayed(parallelQCstats)(i, analysis_params) \
        for i in analysis_params['accessions'])

    # for i in analysis_params['accessions']:
        ## processing fastq
        # fastqc_stats(in_fq = analysis_params[i]['fastq1'],
        #              out_dir = analysis_params['qc_stats']['analysis_dir'], 
        #              log_dir = analysis_params['qc_stats']['log_dir'])
        # if analysis_params['fastq2']:
        #     fastqc_stats(in_fq = analysis_params[i]['fastq1'],
        #              out_dir = analysis_params['qc_stats']['analysis_dir'], 
        #              log_dir = analysis_params['qc_stats']['log_dir'])       

        ## processing bam
        # picard_multiple_metrics(in_bam = analysis_params[i]['sorted_bam'],
        #                          bam_stats = analysis_params[i]['bam_metrics'], 
        #                          log_dir = analysis_params['qc_stats']['log_dir'])

        # samtools_depth(in_bam = analysis_params[i]['sorted_bam'], 
        #                 out_depth =analysis_params[i]['bam_depth'], 
        #                 log_dir = analysis_params['qc_stats']['log_dir']) 

# samtools_depth(in_bam = analysis_params[i]['sorted_bam'], 
#     out_depth =analysis_params[i]['bam_depth'], 
#     log_dir = analysis_params['qc_stats']['log_dir']) 


# def main(filename):
#     #read run parameters from input file and map reads to reference using bwa
#     parameters = read_params(filename)

#     # creating temp directory
#     subprocess.call(['mkdir','-p',parameters['root_dir']+ parameters['analysis_out_dir']+"/tmp/"])

#     for i in parameters['datasets'].split(","):
#         run_params = define_mapping_params(i,parameters)
#         record_params(run_params,parameters)
#         run_qc_stat_pipeline(run_params, parameters)
