# ###QC stats for fastq and mapped bam files
# 
# Input: fastq, and mapped bam files    
# Output: summary stat files from picard and fastqc
import sys
import re
import subprocess
from prepc.parse_pipeline_params import *
from prepc.qc_stats_commands import *
from prepc.picard_commands import *

def main(analysis_params):
    for i in analysis_params['accessions']:
        ## processing fastq
        fastqc_stats(in_fq = analysis_params[i]['fastq1'],
                     out_dir = run_params['qc_stats']['analysis_dir'], 
                     log_dir = analysis_params['qc_stats']['log_dir'])
        if run_params['fastq2']:
            fastqc_stats(in_fq = analysis_params[i]['fastq1'],
                     out_dir = analysis_params['qc_stats']['analysis_dir'], 
                     log_dir = analysis_params['qc_stats']['log_dir'])       

        ## processing bam
        picard_multiple_metrics(in_bam = analysis_params[i]['sorted_bam'],
                                 bam_stats = analysis_params[i]['bam_metrics'], 
                                 log_dir = ranalysis_params['qc_stats']['log_dir'])


# def main(filename):
#     #read run parameters from input file and map reads to reference using bwa
#     parameters = read_params(filename)
    
#     # creating temp directory
#     subprocess.call(['mkdir','-p',parameters['root_dir']+ parameters['analysis_out_dir']+"/tmp/"])

#     for i in parameters['datasets'].split(","):
#         run_params = define_mapping_params(i,parameters)
#         record_params(run_params,parameters)
#         run_qc_stat_pipeline(run_params, parameters)