# define pipeline params based on yaml input
import yaml
import sys
import os
import subprocess
from collections import defaultdict

def move_ref_to_ref_dir(ref, name, analysis_params):
    ''' function for copying reference seqeunce to the reference directory and adding it to analysis_params
    @params ref reference sequence file
    @param name key for analysis_params dict
    @param analysis_params
    '''
    
    #copying ref to new ref directory
    subprocess.call(['cp', ref, analysis_params['ref_dir']])
    
    ref_name = os.path.split(ref)[1]
    analysis_params['ref'] = analysis_params['ref_dir'] + "/" + ref_name
    analysis_params['ref_root'] = os.path.splitext(ref_name)[0]
    analysis_params['ref_dict'] = analysis_params['ref_dir'] + "/" + analysis_params['ref_root'] + ".dict"
    analysis_params['ref_log'] = analysis_params['ref_dir'] + "/" + "log"

def init_prj(pipeline_params):
    '''initiating project generates directory structure, copies ref to directory, and initiates the analysis_params dictionary
    @param pipeline_params dictionary generated from pipeline params yaml file
    '''
    
    # initiating directory structure
    abspath = os.path.abspath(".") #%M% need to change for docker
    prj_dir = abspath + "/" + pipeline_params['project_id']
    fastq_dir = prj_dir + "/fastq"
    ref_dir = prj_dir + "/ref"
    subprocess.call(['mkdir','-p', fastq_dir, ref_dir + "/log"])
    
    # generating analysis_params dictionary
    analysis_params = defaultdict(str)
    analysis_params['prj_dir'] = prj_dir
    analysis_params['fastq_dir'] = fastq_dir
    analysis_params['ref_dir'] = ref_dir
    
    move_ref_to_ref_dir(pipeline_params['ref'],'ref', analysis_params)
    
    return analysis_params

def init_params(pipeline_params, analysis_params):
    '''generating a list of accession numbers for get_fastq and initiating data set specific run params
    @param pipeline_params dictionary generated from pipeline params yaml file
    @param analysis_params inititing run specific parameters
    '''
    
    analysis_params['accessions'] = []
    analysis_params['plat'] = pipeline_params['exp_design'].keys()
    for i in pipeline_params['exp_design']:
        analysis_params[i] = defaultdict(str)
        analysis_params[i]['accessions'] = []
        for j in pipeline_params['exp_design'][i]:
            acc = j['accession']
            analysis_params['accessions'].append(acc)
            analysis_params[i]['accessions'].append(acc)
            
            analysis_params[acc] = defaultdict(str)
            analysis_params[acc]['vial'] = j['vial']
            analysis_params[acc]['rep'] = j['rep']
            analysis_params[acc]['plat'] = i
            analysis_params[acc]['lib'] = "%d-%d" % (analysis_params[acc]['vial'], analysis_params[acc]['rep'])

    miseq_accessions = analysis_params['miseq']['accessions']
    pairs = []
    for i in xrange(0, len(miseq_accessions)):
        for j in xrange(i+1, len(miseq_accessions)):
            pair_name = miseq_accessions[i] + "-" + miseq_accessions[j]
            pairs.append(pair_name)
            analysis_params[pair_name] = defaultdict(str)
    analysis_params['pairs'] = pairs

def init_analysis(analysis_name, analysis_params, run_by):
    '''Adding analyis step general parameters to the analysis params dictionary
    @params analysis_name name of the analysis step
    @params analysis_params dictionary with analysis parameter definitions
    @params run_by base unit analyzed 
    '''
    # defining log and temp directories
    analysis_root = analysis_params['prj_dir'] + "/" + analysis_params['ref_root'] + "_" + analysis_name
    tmp_dir = analysis_root + "/tmp"
    log_dir = analysis_root + "/log"
    
    # creating log and tmp directories
    subprocess.call(['mkdir','-p', tmp_dir, log_dir])
    
    analysis_params[analysis_name] = defaultdict(str)
    analysis_params[analysis_name]['analysis_dir'] = analysis_root
    analysis_params[analysis_name]['tmp_dir'] = tmp_dir
    analysis_params[analysis_name]['log_dir'] = log_dir
    
    # accession specific log directories
    # %%TODO% need to cleanup
    if run_by == 'accession':
        for i in analysis_params['accessions']:
            acc_log_dir = analysis_root + "/log/" + i
            subprocess.call(['mkdir','-p', acc_log_dir])
            analysis_params[i][analysis_name + "_log"] = acc_log_dir
    elif run_by == 'plat':
        for i in analysis_params['plat']:
            plat_log_dir = analysis_root + "/log/" + i
            subprocess.call(['mkdir','-p', plat_log_dir])
            analysis_params[i][analysis_name + "_log"] = plat_log_dir
    elif run_by == 'miseq_pairs':
        for i in analysis_params['pairs']:
            pair_log_dir = analysis_root + "/log/" + i
            analysis_params[i][analysis_name + "_log"] = pair_log_dir
            subprocess.call(['mkdir','-p', pair_log_dir])
            
        # analysis_params[analysis_name]['pairs'] = pairs

def define_map_run(accession, analysis_params, pipeline_params):
    ''' defining parameters, input, and output files for mapping analysis
    @param accession
    @param analysis_params 
    @param pipeline_params
    '''

    # input file names
    fastq_root = analysis_params['fastq_dir'] + "/" + accession
    if analysis_params[accession]['plat'] == "miseq":
        analysis_params[accession]['fastq1'] = fastq_root + "_1.fastq"
        analysis_params[accession]['fastq2'] = fastq_root + "_2.fastq"
    else:
        analysis_params[accession]['fastq1'] = fastq_root + ".fastq"
        analysis_params[accession]['fastq2'] = None
    
    root_name = analysis_params['ref_root'] +"_"+ accession
    
    ## temp files
    tmp_root = analysis_params['mapping']['tmp_dir'] + "/" + root_name
    analysis_params[accession]['sam'] = tmp_root + ".sam"
    analysis_params[accession]['bam'] = tmp_root + ".bam"
    analysis_params[accession]['header_file'] = tmp_root + "_header.bam"
    analysis_params[accession]['fix_file'] = tmp_root + "_fix.bam"
    analysis_params[accession]['sort_fix_file'] = tmp_root + "_sort_fix.bam"
    analysis_params[accession]['group_sort_file'] = tmp_root + "_group_sort.bam"
    analysis_params[accession]['realign_file'] = tmp_root + "_realign.bam"
    analysis_params[accession]['intervals_file'] = tmp_root + ".intervals"
    analysis_params[accession]['metrics_file'] = tmp_root + ".metrics"
    
    ## output files
    output_root = analysis_params['mapping']['analysis_dir'] + "/" + root_name
    analysis_params[accession]['sorted_bam'] = output_root + "_raw.bam"
    analysis_params[accession]['markdup_file'] = output_root + "_refined.bam"
    analysis_params[accession]['read_group'] = [(("RGID=%s") % pipeline_params['project_id']),
                                (("RGLB=%s") % analysis_params[accession]['lib']),
                                (("RGPL=%s") % analysis_params[accession]['plat']),
                                (("RGPU=%s") % 'barcoded'),
                                (("RGSM=%s") % accession),
                                (("RGCN=%s") % pipeline_params['center'])]

def define_pilon_run(plat, analysis_params): 
    ''' Define parameters for running pilon 
    @params plat platform parameters are defined for
    @params analysis_params
    '''

    # list of input bams to merge
    # this is analysis_params[plat]
    
    if plat == "pgm":
        analysis_params[plat]['pilon_input_type'] = "--unpaired"
    else:
        analysis_params[plat]['pilon_input_type'] = "--frags"

    root_name = analysis_params['ref_root'] + "_" + plat
    analysis_params[plat]['pilon_bam_list'] = analysis_params['pilon']['tmp_dir'] + "/" + root_name + "_bam_list.txt"
    analysis_params[plat]['pilon_merged_bam'] = analysis_params['pilon']['tmp_dir'] + "/" + root_name + "_merged.bam"
    analysis_params[plat]['pilon_root'] = analysis_params['pilon']['analysis_dir'] + "/" + root_name

def define_qc_run(accession, analysis_params): 
    ''' Define parameters for running pilon 
    @params plat platform parameters are defined for
    @params analysis_params
    '''
    root_name = analysis_params['qc_stats']['analysis_dir'] + "/" + analysis_params['ref_root'] +"_"+ accession
    analysis_params[accession]['bam_metrics'] = root_name + "_stats"

def define_consensus_base_run(plat,analysis_params):
    ''' defining parameters, input, and output files for consensus base analysis
    @param accession
    @param analysis_params 
    '''
    root_name = analysis_params['ref_root'] +"_"+ plat
        
    ## output files
    output_root = analysis_params['consensus_base']['analysis_dir'] + "/" + root_name
    analysis_params[plat]['consensus_vcf'] = output_root + ".vcf"
    analysis_params[plat]['consensus_tsv'] = output_root + ".tsv"

def define_homogeneity_run(accession1, accession2 ,analysis_params):
    ''' defining parameters, input, and output files for homogeneity analysis
    @param accession1
    @param accession2
    @param analysis_params 
    '''
    
    pair_name = accession1 + "-" + accession2
    root_name = analysis_params['ref_root'] +"_"+ accession1 + "-" + accession2

    ## input files
    analysis_params[pair_name]['bam1_file'] =  analysis_params[accession1]['markdup_file']
    analysis_params[pair_name]['bam2_file'] =  analysis_params[accession2]['markdup_file']
    
    ## temp files
    tmp_root = analysis_params['homogeneity']['tmp_dir'] + "/"
    analysis_params[accession1]['mpileup_file'] = tmp_root + accession1 +".mpileup"
    analysis_params[accession2]['mpileup_file'] = tmp_root + accession2 +".mpileup"
    analysis_params[pair_name]['mpileup_file1'] = analysis_params[accession1]['mpileup_file']
    analysis_params[pair_name]['mpileup_file2'] = analysis_params[accession2]['mpileup_file']
    
    ## output files
    output_root = analysis_params['homogeneity']['analysis_dir'] + "/" + root_name
    analysis_params[pair_name]['varscan_snp_file'] = output_root + "_varscan-snp.txt"
    analysis_params[pair_name]['varscan_indel_file'] = output_root + "_varscan-indel.txt"