## Pipeline for retrieving fastq from sra archive
import sys
import re
import subprocess
from prepc.sra_commands import *

def main(analysis_params):
	for i in ['miseq','pgm']:
	    for j in analysis_params[i]['accessions']:
    		acc_log_dir = analysis_params['fastq_dir'] + "/log/" + j
        	subprocess.call(['mkdir','-p', acc_log_dir])
        	sra_get_fastq(i,j,analysis_params['fastq_dir'], acc_log_dir)
