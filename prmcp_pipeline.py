import yaml
from get_fastq_pipeline import main as get_fastq_pipeline 
from index_ref_pipeline import main as index_ref_pipeline 
from map_miseq_pipeline import main as map_miseq_pipeline 
from map_pgm_pipeline import main as map_pgm_pipeline 
from pilon_pipeline import main as pilon_pipeline 
# from qc_stats_pipeline import main as qc_stats_pipeline 
# from homogeneity_analysis_pipeline import main as homogeneity_analysis_pipeline 
# from consensus_base_pipeline import main as consensus_base_pipeline 
from prepc.define_pipeline_params import *

def run_genome_eval_pipeline(parameters):
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
							"_" + pipeline_params['project_id'] + "_parameters.yaml"
	with open(param_out, 'w') as f:
  		yaml.dump(analysis_params, f, default_flow_style=False, encoding = None)

	print "Running step 1 or 9"
	get_fastq_pipeline(analysis_params)

	print "Running step 2 or 9"
	index_ref_pipeline(analysis_params)


	print "Running step 3 or 9"
	map_miseq_pipeline(analysis_params, pipeline_params)
	map_pgm_pipeline(analysis_params, pipeline_params)

	print "Running step 4 or 9"
	pilon_pipeline(analysis_params)

	

def run_genome_characterization_pipeline(parameters):
	''' Full prmcp miseq pipeline takes an input parameter file and;
	1. indexes revised reference
	2. maps all reads to revised reference
	3. calculates fastq and bam summary statistics
	4. performs homogeneity analysis (pairwise variant calling) for miseq data
	5. generates base level summary for reads mapped to the genome
	'''	

	print "Running step 1 or 5"
	index_ref_pipeline(parameters)

	print "Running step 2 or 5"
	map_miseq_pipeline(parameters)
	map_pgm_pipeline(parameters)

	print "Running step 3 or 5"
	qc_stats_pipeline(parameters)

	print "Running step 4 or 5"
	homogeneity_analysis_pipeline(parameters)

	print "Running step 5 or 5"
	consensus_base_pipeline(parameters)