def sam_to_bam(accession,accession_params):
    ''' Series of commands for converting sam to bam files, adding headers, sorting and indexing'''
    print "Converting sam to sorted, indexed bam with header ..."
    import samtools_commands
    import picard_commands
    import os

    ## checking variables
    assert accession_params
    for variables in ['sam','bam','mapping_log', 'read_group', 'header_file','sorted_bam']:
        assert accession_params[variables]

    ## checking for inputs
    assert os.path.isfile(accession_params['sam'])
    assert os.path.isdir(accession_params['mapping_log'])

    # if not os.path.isfile(accession_params['bam']):
    #   samtools_commands.samtools_sam_to_bam(in_sam = accession_params['sam'], 
    #                                         out_bam = accession_params['bam'], 
    #                                         log_dir=accession_params['mapping_log'])
    # else:
    #   print "bam file present skipping sam to bam for %s" % accession
    pacbio = False
    if accession_params['plat'] == 'pacbio':
      pacbio = True

    ## add head converts to bam, adds header, sorts and index
    if not os.path.isfile(accession_params['header_file']):
      picard_commands.picard_add_header( in_bam=accession_params['sam'],#in_bam=accession_params['bam'], 
                                       out_bam=accession_params['sorted_bam'],
                                       log_dir=accession_params['mapping_log'],
                                       read_group=accession_params['read_group'], 
                                       pacbio = pacbio)

    # else:
    #   print "bam header file present skipping add header for %s" % accession
    
    # if not os.path.isfile(accession_params['sorted_bam']):
    #   samtools_commands.samtools_bam_sort(  in_bam = accession_params['header_file'],
    #                                       out_bam = accession_params['sorted_bam'],
    #                                       log_dir=accession_params['mapping_log'])
    #   assert os.path.isfile(accession_params['sorted_bam'])      
    # else:
    #   print "sorted bam present skipping sort for %s" % accession

    # #if not os.path.isfile(accession_params['sorted_bam'] + ".bai"):
    # #allways runs index - insures index is upto date
    # samtools_commands.samtools_bam_index( in_bam = accession_params['sorted_bam'], 
    #                                       log_dir = accession_params['mapping_log'])
    # assert os.path.isfile(accession_params['sorted_bam'] + ".bai")
    #else:
    #  print "sorted bam index present skipping index for %s" % accession
