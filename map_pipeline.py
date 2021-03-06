#mapping short read data
from prepc.tmap_commands import *
from prepc.bwa_commands import *
from prepc.sam_to_bam_pipeline import *
from prepc.refine_bam_pipeline import main as refine_bam_pipeline
import warnings
import os
from joblib import Parallel, delayed 
import multiprocessing
num_cores = multiprocessing.cpu_count()

mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
mem_gib = mem_bytes/(1024.**3)

# def refine_bam(accession, analysis_params):
# 	if os.path.isfile(analysis_params[accession]['markdup_file']):
# 	    print "Refine bam present skip refine mapping"
# 	else:
# 		refine_bam_pipeline(accession, analysis_params['ref'], analysis_params[accession])


def main(analysis_params, refine = False):
	sam_to_bam_accessions = []
	# separate list for pacbio due to large memory requirements
	pacbio_sam_to_bam_accessions = []
	for i in analysis_params['accessions']:
		print "preparing to map %s" % i
		if analysis_params[i]['plat'] not in ['pgm','miseq', 'pacbio']:
			message = "Accession %s not run, only accessions with plat values 'pgm','miseq'. 'pacbio' are run" % (i)
			warnings.warn(message)
		elif os.path.isfile(analysis_params[i]['sorted_bam']) :
			print "Raw bam present skip mapping"
			# if refine:
			# 	refine_bam(analysis_params, i)
		else:
			if analysis_params[i]['plat'] == 'pacbio':
				pacbio_sam_to_bam_accessions.append(i)
			else:
				sam_to_bam_accessions.append(i)

			print "Mapping %s" % i
			if not os.path.isfile(analysis_params[i]['sam']):
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
			else:
				print "sam file exists skipping initial mapping"

	#sorting, indexing and adding header for non-pacbio
	req_men = num_cores*2
	if req_men > mem_gib:
		job_num = int(mem_gib/2)
	elif mem_gib < 2:
		job_num = 1
	else:
		job_num = int(num_cores)

	Parallel(n_jobs=job_num)(delayed(sam_to_bam)(i, analysis_params[i]) for i in sam_to_bam_accessions)

	#sorting, indexing and adding header for non-pacbio
	req_men = num_cores*24

	if mem_gib < 24:
		job_num = 1
	elif req_men > mem_gib:
		job_num = int(mem_gib/24)
	else:
		job_num = int(num_cores)

	Parallel(n_jobs=job_num)(delayed(sam_to_bam)(i, analysis_params[i]) for i in pacbio_sam_to_bam_accessions)

	if refine:
		refine_accessions = []
		for i in analysis_params['accessions']:
			if os.path.isfile(analysis_params[i]['markdup_file']):
				print "Refine %s bam present skip refine mapping" % i
			else:
				refine_accessions.append(i)
		#fix pairs, markdup, realignment around indels
		req_men = num_cores*4
		if req_men > mem_gib:
			job_num = int(mem_gib/4)
		Parallel(n_jobs=num_cores)(delayed(refine_bam_pipeline)(i, analysis_params['ref'], analysis_params[i]) for i in refine_accessions)
