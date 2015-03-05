# ## Mapping MiSeq Paired End Reads Using bwa
# To Do
# 1. remove tmp after run
# 2. add run_id to log files
# 3. add parameters/ help with verbose command
from prepc.bwa_commands import *
from prepc.sam_to_bam_pipeline import *
from prepc.define_pipeline_params import define_map_run

def main(analysis_params):
    for i in analysis_params['miseq']['accessions']:
        ## running bwa_mem
        bwa_map_fq( in_ref = analysis_params['ref'],
                    in_fq1 = analysis_params[i]['fastq1'],
                    in_fq2 = analysis_params[i]['fastq2'],
                    out_sam = analysis_params[i]['sam'],
                    log_dir = analysis_params[i]['mapping_log'])

        #sorting, indexing and adding header
        sam_to_bam(i, analysis_params)