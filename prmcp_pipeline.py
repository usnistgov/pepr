import yaml
from get_fastq_pipeline import main as get_fastq_pipeline 
from index_ref_pipeline import main as index_ref_pipeline 
from map_pipeline import main as map_pipeline 
from pilon_pipeline import main as pilon_pipeline 
from qc_stats_pipeline import main as qc_stats_pipeline 
from homogeneity_analysis_pipeline import main as homogeneity_analysis_pipeline 
from consensus_base_pipeline import main as consensus_base_pipeline 
from prepc.define_pipeline_params import *

def run_genome_eval_pipeline_base(parameters):
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
	accession_params(pipeline_params, analysis_params)

	#mapping params
	init_analysis('mapping', analysis_params, run_by = 'accession')
	for i in analysis_params['accessions']:
		define_map_run(i, analysis_params, pipeline_params)

	#pilon params
	init_analysis('pilon', analysis_params, run_by = 'plat')
	define_pilon_run('miseq', analysis_params)

	print "printing pipeline parameters to file ..."
	param_out = analysis_params['prj_dir'] + "/" + analysis_params['ref_root'] + \
							"_" + pipeline_params['project_id'] + "_evaluation_parameters.yaml"
	with open(param_out, 'w') as f:
  		yaml.dump(analysis_params, f, default_flow_style=False, encoding = None)

def run_genome_eval_pipeline(parameters, pipe = "full"):
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
	accession_params(pipeline_params, analysis_params)

	#mapping params
	init_analysis('mapping', analysis_params, run_by = 'accession')
	for i in analysis_params['accessions']:
		define_map_run(i, analysis_params, pipeline_params)

	#pilon params
	init_analysis('pilon', analysis_params, run_by = 'plat')
	define_pilon_run('miseq', analysis_params)

	print "printing pipeline parameters to file ..."
	param_out = analysis_params['prj_dir'] + "/" + analysis_params['ref_root'] + \
							"_" + pipeline_params['project_id'] + "_" + \
							pipe + "_evaluation_parameters.yaml"
	with open(param_out, 'w') as f:
  		yaml.dump(analysis_params, f, default_flow_style=False, encoding = None)

	print "Running step 1 of 4"
	if(pipe != 'full'):
		print "skipping fastq download"
	else:
		print "downloading fastq"
		get_fastq_pipeline(analysis_params)


	print "Running step 2 of 4"
	index_ref_pipeline(analysis_params)


	print "Running step 3 of 4"
	map_pipeline(analysis_params)

	print "Running step 4 of 4"
	pilon_pipeline(analysis_params)

	

def run_genome_characterization_pipeline(parameters):
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

	#initiating project
	analysis_params = init_prj(pipeline_params)
	accession_params(pipeline_params, analysis_params)

	#mapping params
	init_analysis('mapping', analysis_params, run_by = 'accession')
	for i in analysis_params['accessions']:
		define_map_run(i, analysis_params, pipeline_params)

	#qc_stats params
	init_analysis('qc_stats', analysis_params, run_by = 'accession')
	for i in analysis_params['accessions']:
		define_qc_run(i, analysis_params)

	#consensus_base params
	init_analysis('consensus_base', analysis_params, run_by = 'accession')
	for i in analysis_params['accessions']:
		define_consensus_base_run(i, analysis_params)

	# Still need to work out bug in parameter definitions
	#homogeneity params
	init_analysis('homogeneity', analysis_params, run_by = 'miseq_pairs')
	for i in analysis_params['homogeneity']['pairs']:
		acc1, acc2 = i.split("-")
		define_homogeneity_run(acc1, acc2, analysis_params)	

	print "printing pipeline parameters to file ..."
	param_out = analysis_params['prj_dir'] + "/" + analysis_params['ref_root'] + \
							"_" + pipeline_params['project_id'] + "_charaterization_parameters.yaml"
	with open(param_out, 'w') as f:
  		yaml.dump(analysis_params, f, default_flow_style=False, encoding = None)


	print "Running step 1 of 5"
	index_ref_pipeline(analysis_params)
	
	print "Running step 2 of 5"
	map_pipeline(analysis_params, refine = True)


	print "Running step 3 of 5"
	qc_stats_pipeline(analysis_params)

	print "Running step 4 of 5"
	homogeneity_analysis_pipeline(analysis_params)

	print "Running step 5 of 5"
	consensus_base_pipeline(analysis_params)