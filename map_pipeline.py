#mapping short read data
from prepc.tmap_commands import *
from prepc.bwa_commands import *
from prepc.sam_to_bam_pipeline import *
from prepc.refine_bam_pipeline import main as refine_bam_pipeline
import warnings
import os
import subprocess

def main(analysis_params, refine = False):
	for i in analysis_params['accessions']:
		if analysis_params[i]['plat'] not in ['pgm','miseq', 'pacbio']:
			message = "Accession %s not run, only accessions with plat values 'pgm','miseq'. 'pacbio' are run" % (i)
			warnings.warn(message)
		elif os.path.isfile(analysis_params[i]['sorted_bam']) :
			print "Raw bam present skip mapping"
		else:
			print "Mapping %s" % i
			if analysis_params[i]['plat'] == 'pgm':
				tmap_map_fq( in_ref = analysis_params['ref'],
					in_fq = analysis_params[i]['fastq1'],
					out_sam = analysis_params[i]['sam'],
					log_dir = analysis_params[i]['mapping_log'])
			elif analysis_params[i]['plat'] == 'miseq':
				bwa_map_fq( in_ref = analysis_params['ref'],
					in_fq1 = analysis_params[i]['fastq1'],
					in_fq2 = analysis_params[i]['fastq2'],
					out_sam = analysis_params[i]['sam'],
					log_dir = analysis_params[i]['mapping_log'])
			elif analysis_params[i]['plat'] == 'pacbio':
				bwa_map_pacbio( in_ref = analysis_params['ref'],
					in_fq1 = analysis_params[i]['fastq1'],
					in_fq2 = analysis_params[i]['fastq2'],
					out_sam = analysis_params[i]['sam'],
					log_dir = analysis_params[i]['mapping_log'])	
	        	#sorting, indexing and adding header
	        	sam_to_bam(i, analysis_params[i])

	        #fix pairs, markdup, realignment around indels
        	if refine:
	       		if os.path.isfile(analysis_params[i]['markdup_file']):
	      			print "Refine bam present skip refine mapping"
			elif analysis_params[i]['plat'] == 'pacbio':
   				subprocess.call(["cp",accession_params[i]['sorted_bam'], 
   						analysis_params[i]['markdup_file']])
   			else:
		    		refine_bam_pipeline(i, analysis_params['ref'], analysis_params[i])

