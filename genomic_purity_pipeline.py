# ### genomic purity pipeline
import sys
import re 
import subprocess
from prepc.pathoscope_commands import *

def main(analysis_params):
    for i in analysis_params['accessions']:
        print "Running pathoscope pipeline"
        ## read quality control - filters low quality reads
        pathoqc_command(plat=analysis_params[i]['plat'],
                        fastq1=analysis_params[i]['fastq1'],
                        fastq2=analysis_params[i]['fastq2'],
                        log_dir = analysis_params[i]['genomic_purity_log'], 
                        out_dir=analysis_params['genomic_purity']['tmp_dir'],
                        thread_num= 8)

        ## running pathomap
        pathomap_command(ref_path=analysis_params['ref'],
                         index_dir=analysis_params['ref_dir'], 
                         exptag = analysis_params[i]['pathoscope_run_id'], 
                         fastq1=analysis_params[i]['trimmed_fastq1'],
                         fastq2=analysis_params[i]['trimmed_fastq2'], 
                         log_dir = analysis_params[i]['genomic_purity_log'],
                         out_dir=analysis_params['genomic_purity']['tmp_dir'],
                         out_sam=analysis_params['pathomap_sam'])
        
        ## cleaning up pathomap files- removes find combined in appendAlign
        # need code to clean up after run
        
        ## running pathoid
        pathoid_command( input_sam=analysis_params[i]['pathomap_sam'],
                         log_dir = analysis_params[i]['genomic_purity_log'],
                         out_dir = analysis_params['genomic_purity']['analysis_dir'], 
                         exptag = analysis_params[i]['pathoscope_run_id'])
