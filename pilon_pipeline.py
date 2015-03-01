# ## Validating genome assembly using pilon
# To Do
# document functions
# write tests

from prepc.samtools_commands import *
from prepc.pilon_commands import *

def write_bam_list_to_file(analysis_params, filename):
    ## write bam list to file
    bam_list = []
    for i in analysis_params['miseq']['accessions']:
        bam_list.append(analysis_params[i]['sorted_bam'])
    bam_list_file = open(filename, 'w')
    bam_list_file.write("\n".join(bam_list))
    bam_list_file.close()

def main(analysis_params):
    print "Running pilon pipeline ..."
    write_bam_list_to_file(bam_list = analysis_params['miseq']['accessions'], \
                           filename=analysis_params['miseq']['pilon_bam_list'])
    
    samtools_bam_merge(bam_list=analysis_params['miseq']['pilon_bam_list'], \
                       out_bam=analysis_params['miseq']['pilon_merged_bam'],\
                       log_dir=analysis_params['miseq']['pilon_log'])
    
    samtools_bam_index(in_bam=analysis_params['merged_bam'], \
                       log_dir=analysis_params['miseq']['pilon_log'])
    
    pilon_fixassembly(in_ref=analysis_params['ref'],in_bam=analysis_params['miseq']['pilon_merged_bam'],\
                     out_root=analysis_params['miseq']['pilon_root'],log_dir=analysis_params['miseq']['log_dir'],\
                     input_type=analysis_params['miseq']['pilon_input_type'])