## Pipeline for retrieving fastq from sra archive
import sys
import re
import subprocess
from prepc.sra_commands import *

def main(pipeline_params):
    for i in pipeline_params['accessions']:
    	acc_log_dir = pipeline_params['fastq_dir'] + "/log/" + i
        subprocess.call(['mkdir','-p', acc_log_dir])
        sra_get_fastq(i,pipeline_params['fastq_dir'], acc_log_dir)
