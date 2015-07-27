# ### Functions for using varson for variant calling
import sys
import time
import subprocess
import os

def varscan_somatic(in_mpileup1, in_mpileup2, snp_out, indel_out, log_dir, COV='15'):
	''' Performs somatic variant calling for a pair of input bam files'''
	print "Running varscan for pairwise variant calling ..."
	
	## check for variable names
	assert in_mpileup1
	assert in_mpileup2
	assert snp_out
	assert indel_out
	assert log_dir

	## check for input files and log directory
	assert os.path.isdir(accession_params['mapping_log'])
	assert os.path.isfile(accession_params['sorted_bam'])
	assert os.path.isfile(accession_params['sorted_bam'])

	# prep files
	log_file = open(log_dir + "/varscan_somatic"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
	stderr_file = open(log_dir + "/varscan_somatic"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
	
	# run command
	varscan_somatic_command = ["java","-Xmx8g","-jar","/usr/local/bin/VarScan.v2.3.7.jar","somatic",
								in_mpileup1, in_mpileup2, 
								"--output-snp", snp_out, "--output-indel", indel_out, 
								"--min-coverage", COV,  "--min-coverage-tumor", COV, "--min-coverage-normal", COV,
								"--somatic-p-value", "0.001"]
								
	subprocess.call(varscan_somatic_command,stdout=log_file,stderr=stderr_file)
	
	## check that process ran
	assert os.path.isfile(accession_params['indel_out'])
	assert os.path.isfile(accession_params['snp_out'])
	assert os.path.isfile(accession_params['log_file'])
	assert os.path.isfile(accession_params['stderr_file'])
	
	log_file.close(); stderr_file.close()
