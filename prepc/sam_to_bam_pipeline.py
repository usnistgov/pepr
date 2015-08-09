import os
from picard_commands import picard_add_header


def sam_to_bam(accession, accession_params):
    '''
    Series of commands for converting sam to bam files,
    adding headers, sorting and indexing
    '''
    print "Converting sam to sorted, indexed bam with header ..."

    # checking variables
    assert accession_params
    for variables in ['sam', 'bam', 'mapping_log',
                      'read_group', 'header_file', 'sorted_bam']:
        assert accession_params[variables]

    # checking for inputs
    assert os.path.isfile(accession_params['sam'])
    assert os.path.isdir(accession_params['mapping_log'])

    pacbio = False
    if accession_params['plat'] == 'pacbio':
        pacbio = True

    # add head converts to bam, adds header, sorts and index
    if not os.path.isfile(accession_params['header_file']):
        picard_add_header(in_bam=accession_params['sam'],
                          out_bam=accession_params['sorted_bam'],
                          log_dir=accession_params['mapping_log'],
                          read_group=accession_params['read_group'],
                          pacbio=pacbio)
