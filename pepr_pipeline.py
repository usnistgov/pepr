import yaml
from get_fastq_pipeline import main as get_fastq_pipeline 
from index_ref_pipeline import main as index_ref_pipeline 
from map_pipeline import main as map_pipeline 
from pilon_pipeline import main as pilon_pipeline 
from qc_stats_pipeline import main as qc_stats_pipeline 
from homogeneity_analysis_pipeline import main as homogeneity_analysis_pipeline 
from consensus_base_pipeline import main as consensus_base_pipeline 
from genomic_purity_pipeline import main as genomic_purity_pipeline 
from prepc.define_pipeline_params import *
from sms_status import main as send_sms

def run_genome_eval_pipeline(parameters, sms_config, pipe = "full"):
	''' Full genome evaluation pipeline takes an input parameter file and;
	1. retrieves fastq files from SRA archive for provided Genbank accessions
	2. indexes user provided reference genome sequence
	3. maps miseq reads to user provided reference genome 
	4. evaluates reference genome using pilon_pipeline with miseq data
	'''
	print "defining run parameters"
	param_file = file(parameters, 'r')
	pipeline_params = yaml.load(param_file)

	#initiating project
	analysis_params = init_prj(pipeline_params)
	init_params(pipeline_params, analysis_params)

	#mapping params
	init_analysis('mapping', analysis_params, run_by = 'accession')
	for i in analysis_params['accessions']:
		define_map_run(i, analysis_params, pipeline_params)

	#pilon params
	init_analysis('pilon', analysis_params, run_by = 'plat')
	for i in analysis_params['plat']:
		define_pilon_run(i, analysis_params)


	print "printing pipeline parameters to file ..."
	param_out = analysis_params['prj_dir'] + "/" + analysis_params['ref_root'] + \
							"_" + pipeline_params['project_id'] + "_" + \
							pipe + "_evaluation_parameters.yaml"
	with open(param_out, 'w') as f:
  		yaml.dump(analysis_params, f, default_flow_style=False, encoding = None)

  	if sms_config:
		print "Sending pipeline start message"
		send_sms(sms_config, message = "Starting PEPR pipeline")
	print "Running step 1 of 4"
	get_fastq_pipeline(analysis_params)
	if(pipe != 'full'):
		print "skipping fastq download"
	else:
	 	print "downloading fastq"
		get_fastq_pipeline(analysis_params)
	#	return 


	print "Running step 2 of 4"
	index_ref_pipeline(analysis_params)


	print "Running step 3 of 4"
	map_pipeline(analysis_params)

	print "Running step 4 of 4"
	#for i in analysis_params['plat']:
	pilon_pipeline('miseq', analysis_params)

	if sms_config:
		print "Sending pipeline completion message"
		send_sms(sms_config)


	

def run_genome_characterization_pipeline(parameters, sms_config):
	''' Full prmcp miseq pipeline takes an input parameter file and;
	1. indexes reference
	2. maps all reads to reference
	3. calculates fastq and bam summary statistics
	4. performs homogeneity analysis (pairwise variant calling) for miseq data
	5. generates base level summary for reads mapped to the genome
	'''	
	# not sure whether to include indexing and mapping reads to reference or just use output from re-eval?
	print "defining run parameters"
	param_file = file(parameters, 'r')
	pipeline_params = yaml.load(param_file)

	## initiating project
	analysis_params = init_prj(pipeline_params)
	init_params(pipeline_params, analysis_params)

	## mapping params
	init_analysis('mapping', analysis_params, run_by = 'accession')
	for i in analysis_params['accessions']:
		define_map_run(i, analysis_params, pipeline_params)

	## qc_stats params
	init_analysis('qc_stats', analysis_params, run_by = 'accession')
	for i in analysis_params['accessions']:
		define_qc_run(i, analysis_params)

	## consensus_base params
	init_analysis('consensus_base', analysis_params, run_by = 'plat')
	for i in analysis_params['plat']:
		define_consensus_base_run(i, analysis_params)

	## homogeneity params
	init_analysis('homogeneity', analysis_params, run_by = 'miseq_pairs')
	for i in analysis_params['pairs']:
		acc1, acc2 = i.split("-")
		define_homogeneity_run(acc1, acc2, analysis_params)	

	print "printing pipeline parameters to file ..."
	param_out = analysis_params['prj_dir'] + "/" + analysis_params['ref_root'] + \
							"_" + pipeline_params['project_id'] + "_charaterization_parameters.yaml"
	with open(param_out, 'w') as f:
  		yaml.dump(analysis_params, f, default_flow_style=False, encoding = None)

  	if sms_config:
		print "Sending pipeline start message"
		send_sms(sms_config, message = "Starting PEPR pipeline")

  	print "Running step 1 of 6"
	get_fastq_pipeline(analysis_params)

	print "Running step 1 of 6"
	index_ref_pipeline(analysis_params)

	print "Running step 2 of 6"
	map_pipeline(analysis_params, refine = True)

	print "Running step 3 of 6"
	qc_stats_pipeline(analysis_params)

	print "Running step 4 of 6"
	consensus_base_pipeline(analysis_params, platforms = ['miseq','pgm'])

	print "Running step 5 of 6"
	homogeneity_analysis_pipeline(analysis_params)

	if sms_config:
		print "Sending pipeline completion message"
		send_sms(sms_config)

def run_genomic_purity_pipeline(parameters, sms_config):
	''' Genomic purity pipeline;
	1. runs pathoqc on input files
	2. maps reads to reference DB
	3. runs pathoid on mapped reads
	'''
	print "defining run parameters"
	param_file = file(parameters, 'r')
	pipeline_params = yaml.load(param_file)

	#initiating project
	analysis_params = init_prj(pipeline_params, move_ref = False)
	init_params(pipeline_params, analysis_params)

	#pathoscope parmas
	init_analysis('genomic_purity', analysis_params, run_by = 'accession')
	for i in analysis_params['accessions']:
		define_pathoscope_run(i, analysis_params)

	print "printing pipeline parameters to file ..."
	param_out = analysis_params['prj_dir'] + "/" + analysis_params['ref_root'] + \
							"_" + pipeline_params['project_id'] + "_genomic_purity_parameters.yaml"
	with open(param_out, 'w') as f:
  		yaml.dump(analysis_params, f, default_flow_style=False, encoding = None)

  	if sms_config:
		print "Sending pipeline start message"
		send_sms(sms_config, message = "Starting PEPR pipeline")
#	print "Downloading fastq files" 
#	get_fastq_pipeline(analysis_params)
	
  	print "Running genomic purity pipeline"
  	genomic_purity_pipeline(analysis_params)

  	if sms_config:
		print "Sending pipeline completion message"
		send_sms(sms_config)
