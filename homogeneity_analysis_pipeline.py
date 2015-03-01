## Pipeline for performing pairwise somatic variant calling
import sys
import re
import subprocess
from prepc.parse_pipeline_params import *
from prepc.samtools_commands import *
from prepc.varscan_commands import *

def run_homogeneity(pipeline_params, run_params):
    '''comparing variants for two input bam files'''
    print "Running homogeneity pipeline on %s" % (run_params['run_id'])
    samtools_mpileup_pairs(in_ref= pipeline_params['ref'], 
                           in_bams= [run_params['bam1_file'], run_params['bam2_file']],
                           out_mpileup=run_params['mpileup_file'], 
                           log_dir=run_params['log_dir'])
    varscan_somatic(in_mpileup=run_params['mpileup_file'], 
                    snp_out=run_params['varscan_snp_file'], 
                    indel_out=run_params['varscan_indel_file'], 
                    log_dir=run_params['log_dir'])



def main(filename):
    #read run parameters from input file and map reads to reference using bwa
    pipeline_params = read_params(filename)

    # nested for loops for pairwise comparisons
    datasets = pipeline_params['datasets'].split(",")
    for i in xrange(0, len(datasets)):
    	for j in xrange(i+1, len(datasets)):
            # print "ds 1: %s \t ds 2: %s" % (datasets[i],datasets[j])
            run_params = define_homogeneity_params(pipeline_params,datasets[i],datasets[j])
            subprocess.call(['mkdir','-p',run_params['log_dir']])

            record_params(pipeline_params,run_params)
            run_homogeneity(pipeline_params, run_params)

# if __name__ == '__main__':
#     main(sys.argv[1])

# Code from Justin used to characterize human RM
'''
echo "Running job $JOB_NAME, $JOB_ID on $HOSTNAME"
   path/samtools-0.1.18/samtools mpileup -q 1 -f /projects/justin.zook/from-projects/references/human_g1k_v37.fasta $BAM1 $BAM2 | java -jar -Xmx2g path/varscan/VarScan.v2.3.6.jar somatic - --output-snp "$OUTSTART"_snp.txt --output-indel "$OUTSTART"_indel.txt --mpileup 1 --min-coverage $COV  --min-coverage-tumor $COV --min-coverage-normal $COV --somatic-p-value 0.001

# hold off for now ....
#Filter output for sites with cov < 300 and change to csv for analysis in R
cat "$OUTSTART"_indel.txt | awk '$5 + $6 < 300' | awk '{ print $1,$2,$3,$4,$5,$6,$9,$10,$15 }' | sed 's/\ /,/g' > "$OUTSTART"_indel_covlt300.csv
cat "$OUTSTART"_snp.txt | awk '$5 + $6 < 300' | awk '{ print $1,$2,$3,$4,$5,$6,$9,$10,$15 }' | sed 's/\ /,/g' > "$OUTSTART"_snp_covlt300.csv

'''