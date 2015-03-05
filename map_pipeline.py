#mapping short read data
from prepc.tmap_commands import *
from prepc.bwa_commands import *
from prepc.sam_to_bam_pipeline import *
from prepc.define_pipeline_params import define_map_run
import warnings

def main(analysis_params, pipeline_params):
    for i in analysis_params['accessions']:
        if analysis_params['plat'] == 'pgm':
	        tmap_map_fq( in_ref = analysis_params['ref'],
	                     in_fq = analysis_params[i]['fastq1'],
	                     out_sam = analysis_params[i]['sam'],
	                     log_dir = analysis_params[i]['mapping_log'])
	    elif analysis_params['plat'] == 'miseq':
	    	bwa_map_fq( in_ref = analysis_params['ref'],
                    in_fq1 = analysis_params[i]['fastq1'],
                    in_fq2 = analysis_params[i]['fastq2'],
                    out_sam = analysis_params[i]['sam'],
                    log_dir = analysis_params[i]['mapping_log'])
	    else:
	    	warnings.warn("Accession %s not run, only accessions \
	    					with plat values 'pgm' and 'misq' are run", % i)
	    	continue
        #sorting, indexing and adding header
        sam_to_bam(i, analysis_params)