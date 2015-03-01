# sra commands for getting sequence data from ganbank
import sys
import time
import subprocess

def sra_get_fastq(plat, accession, out_dir, log_dir):
	'''Retrieving fastq data from Genbank'''
	print "Retrieving fastq data for %s" % (accession)

	## log files for standard out and error
	log_file = open(log_dir + "/sra_get_fastq"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
	stderr_file = open(log_dir + "/sra_get_fastq"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')

	## run command
	if plat == "miseq":
		sra_get_fastq_command = ["fastq-dump","--split-files","-A", accession, "-O", out_dir]
	else:
		sra_get_fastq_command = ["fastq-dump","-A", accession, "-O", out_dir]
		
	subprocess.call(sra_get_fastq_command, stdout=log_file, stderr=stderr_file)
	log_file.close(); stderr_file.close()