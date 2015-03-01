## Pipeline for retrieving fastq from sra archive
import sys
import re
import subprocess
from prepc.sra_commands import *

def main(analysis_params):
	for i in ['miseq','pgm']:
	    for j in analyis_params['accessions']:
    		acc_log_dir = analyis_params['fastq_dir'] + "/log/" + j
        	subprocess.call(['mkdir','-p', acc_log_dir])
        	sra_get_fastq(i,j,analyis_params['fastq_dir'], acc_log_dir)
