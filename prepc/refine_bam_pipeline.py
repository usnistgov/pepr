def main(accession, ref, accession_params):
    ''' Processing single bam file'''
    import bwa_commands
    import samtools_commands
    import picard_commands
    import gatk_commands
    if accession_params['plat'] == "miseq":
        samtools_commands.samtools_bam_group_sort(in_bam = accession_params['sorted_bam'], 
         out_bam = accession_params['group_sort_file'], 
         log_dir = accession_params['mapping_log'])
        
        samtools_commands.samtools_bam_fixmate(in_bam = accession_params['group_sort_file'],
            out_bam = accession_params['fix_file'],
            log_dir = accession_params['mapping_log'])
        bam_file = accession_params['fix_file']
    else:
    	bam_file = accession_params['sorted_bam']

    gatk_commands.gatk_realign(in_ref=ref,
        in_bam=bam_file,
        out_bam=accession_params['realign_file'],
        intervals_file=accession_params['intervals_file'],
        log_dir=accession_params['mapping_log'])

    picard_commands.bam_markdup(in_bam = accession_params['realign_file'], 
        out_bam = accession_params['markdup_file'], 
        metrics_file = accession_params['metrics_file'],
        log_dir = accession_params['mapping_log'])
    
    samtools_commands.samtools_bam_index(in_bam = accession_params['markdup_file'], 
        log_dir = accession_params['mapping_log'])