def sam_to_bam(accession,accession_params):
    ''' Series of commands for converting sam to bam files, adding headers, sorting and indexing'''
    print "Converting sam to sorted, indexed bam with header ..."
    import samtools_commands
    import picard_commands
    samtools_commands.samtools_sam_to_bam(in_sam = accession_params['sam'], 
                                          out_bam = accession_params['bam'], 
                                          log_dir=accession_params['mapping_log'])

    picard_commands.picard_add_header( in_bam=accession_params['bam'], 
                                       out_bam=accession_params['header_file'],
                                       log_dir=accession_params['mapping_log'],
                                       read_group=accession_params['read_group'])

    samtools_commands.samtools_bam_sort(  in_bam = accession_params['header_file'],
                                          out_bam = accession_params['sorted_bam'],
                                          log_dir=accession_params['mapping_log'])

    samtools_commands.samtools_bam_index( in_bam = accession_params['sorted_bam'], 
                                          log_dir = accession_params['mapping_log'])

