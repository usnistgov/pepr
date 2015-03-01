def sam_to_bam(accession,analysis_params):
    ''' Series of commands for converting sam to bam files, adding headers, sorting and indexing'''
    print "Converting sam to sorted, indexed bam with header ..."
    import samtools_commands
    import picard_commands

    samtools_commands.samtools_sam_to_bam(in_sam = analysis_params[accession]['sam'], 
                                          out_bam = analysis_params[accession]['bam'], 
                                          log_dir=analysis_params[accession]['mapping_log'])

    picard_commands.picard_add_header( in_bam=analysis_params[accession]['bam'], 
                                       out_bam=analysis_params[accession]['header_file'],
                                       log_dir=analysis_params[accession]['log_dir'],
                                       read_group=analysis_params[accession]['read_group'])

    samtools_commands.samtools_bam_sort(  in_bam = analysis_params[accession]['header_file'],
                                          out_bam = analysis_params[accession]['sorted_bam'],
                                          log_dir=analysis_params[accession]['mapping_log'])

    samtools_commands.samtools_bam_index( in_bam = analysis_params[accession]['sorted_bam'], 
                                          log_dir = analysis_params[accession]['mapping_log'])

