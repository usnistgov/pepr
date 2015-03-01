# ### Quality Control Summary Statistics Commands
# * fastqc for fastq summary stats
# * picard for bam stats


import sys
import time
import subprocess

def fastqc_stats(in_fq, out_dir, log_dir):
    ''' Summary statistics for fastq file'''
    print "Generating summary statistics ...."

    ## log files for standard out and error
    log_file = open(log_dir + "/fastqc"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/fastqc"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')

    ## run command

    fastqc_command = ["fastqc","--extract","-o",out_dir, in_fq]
    subprocess.call(fastqc_command, stdout=log_file, stderr=stderr_file)
    log_file.close(); stderr_file.close()