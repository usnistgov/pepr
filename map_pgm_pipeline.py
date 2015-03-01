# ## Mapping PGM data using tmap
# To Do
# 1. remove tmp after run
# 2. add run_id to log files
# 3. add parameters/ help with verbose command
from prepc.tmap_commands import *
from prepc.sam_to_bam_pipeline import *
from prepc.define_pipeline_params import define_map_run

def main(analysis_params, pipeline_params):
    for i in analysis_params['pgm']['accessions']:
    	define_map_run(i, analysis_params, pipeline_params)
        ## running tmap
        tmap_map_fq( in_ref = analysis_params['ref'],
                     in_fq = analysis_params[i]['fastq1'],
                     out_sam = analysis_params[i]['sam'],
                     log_dir = analysis_params[i]['mapping_log'])

        #sorting, indexing and adding header
        sam_to_bam(i, analysis_params)

# if __name__ == '__main__':
#     main(analysis_parans)