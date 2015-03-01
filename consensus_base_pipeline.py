# ###Whole genome vcf files
# 
# Input: Individually mapped bam files     
# Output: Single VCF file

import sys
import re
import subprocess
from prepc.parse_pipeline_params import *
from prepc.bwa_commands import *
from prepc.samtools_commands import *
from prepc.picard_commands import *
from prepc.gatk_commands import *

def dedup_realign_single_bam(run_params, pipeline_params):
    ''' Processing single bam file'''

    # creating run specific log directory
    subprocess.call(['mkdir','-p',pipeline_params['root_dir']+ \
                                  pipeline_params['analysis_out_dir']+ \
                                  "/logs/" + run_params['run_id'] + "/"])
    
    if run_params['plat'] == "MiSeq":
        bam_group_sort(in_bam = run_params['bam'], 
                       out_bam = run_params['group_sort_file'], 
                       log_dir = run_params['log_dir'])
        
        bam_fixmate(in_bam = run_params['group_sort_file'],
                    out_bam = run_params['fix_file'],
                    log_dir = run_params['log_dir'])

        bam_sort(in_bam = run_params['fix_file'], 
                out_sort = run_params['sort_file'], 
                out_dir = run_params['log_dir'])
    else:
        bam_add_header(in_bam=run_params['bam'], 
                       out_header=run_params['header_file'],
                       log_dir=run_params['log_dir'],
                       read_group=run_params['read_group'])

        bam_sort(in_bam = run_params['header_file'], 
                out_sort = run_params['sort_file'], 
                out_dir = run_params['log_dir'],
                intervals_file = run_params['intervals_file'],
                log_dir = run_params['log_dir'])
    
    bam_markdup(in_bam = run_params['realign_file'], 
                out_bam = run_params['markdup_file'], 
                metrics_file = run_params['metrics_file'],
                log_dir = run_params['log_dir'])
    
    bam_index(bam = run_params['markdup_file'],
              out_dir = run_params['log_dir'])

def run_consensus_base_pipeline(run_params,pipeline_params):
    
    ## creating file with run parameters
    run_log_file = open(run_params['out_dir']+"/" + run_params['run_id'] +"-run_parameters.txt", 'w')
    run_log_file.write("Parameter\tValue\n")
    for i in run_params.keys():
        run_log_file.write("%s\t%s\n" % (i, run_params[i]))
    for i in pipeline_params.keys():
        run_log_file.write("%s\t%s\n" % (i, pipeline_params[i]))
    run_log_file.close()
    
    ## processing bam
    dedup_realign_single_bam(run_params, pipeline_params)

def genome_pileups(pipeline_parameters, markdup_files):
    
    for plat in ["MiSeq", "PGM"]:
        out_dir = pipeline_params['root_dir'] + pipeline_params['analysis_out_dir']
        vcf = out_dir + "/" + pipeline_params['RM'] + "-" + plat + ".vcf"
        genome_calls_mpileup(bams=markdup_files[plat],
                             ref=pipeline_params['ref'],
                             vcf_file=vcf,log_dir=out_dir)

def main(filename):
    #read run parameters from input file and process using pathoscope
    pipeline_params = read_params(filename)
    
    # creating temp and log directories
    subprocess.call(['mkdir','-p',pipeline_params['root_dir']+ pipeline_params['analysis_out_dir']+"/tmp/"])
    subprocess.call(['mkdir','-p',pipeline_params['root_dir']+ pipeline_params['analysis_out_dir']+"/logs/"])
    
    # list of refined bams
    markdup_files = {'PGM':[], 'MiSeq':[]}
    for i in pipeline_params['datasets'].split(","):
        run_params = define_consensus_base_params(i,pipeline_params)
    
        markdup_files[run_params['plat']] += [run_params['markdup_file']]
            
        run_consensus_base_pipeline(run_params, pipeline_params)
       
        # pileups by platform
        genome_pileups(pipeline_params, markdup_files)

# if __name__ == '__main__':
#     main(sys.argv[1])

