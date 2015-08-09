# Validating genome assembly using pilon
# To Do
# document functions
# write tests

from prepc.samtools_commands import *
from prepc.pilon_commands import *
import os


def write_bam_list_to_file(plat, analysis_params):

    # checking input
    assert plat
    assert analysis_params
    assert analysis_params[plat]['accessions']

    # write bam list to file
    bam_list = []
    for i in analysis_params[plat]['accessions']:

        # checking raw bam
        assert analysis_params[i]['sorted_bam']
        assert os.path.isfile(analysis_params[i]['sorted_bam'])

        bam_list.append(analysis_params[i]['sorted_bam'])

    bam_list_file = open(analysis_params[plat]['pilon_bam_list'], 'w')
    bam_list_file.write("\n".join(bam_list))
    bam_list_file.close()

    # checking list file
    assert os.path.isfile(analysis_params[plat]['pilon_bam_list'])


def main(plat, analysis_params):
    print "Running pilon pipeline ..."

    write_bam_list_to_file(plat, analysis_params)

    if not os.path.isfile(analysis_params[plat]['pilon_merged_bam']):
        samtools_bam_merge(bam_list=analysis_params[plat]['pilon_bam_list'],
                           out_bam=analysis_params[plat]['pilon_merged_bam'],
                           log_dir=analysis_params[plat]['pilon_log'])

        samtools_bam_index(in_bam=analysis_params[plat]['pilon_merged_bam'],
                           log_dir=analysis_params[plat]['pilon_log'])
    else:
        print "Skipping merging bams %s present" % analysis_params[plat]['pilon_merged_bam']

    if not os.path.isfile(analysis_params[plat]['pilon_merged_bam']):
        samtools_bam_merge(bam_list=analysis_params[plat]['pilon_bam_list'],
                           out_bam=analysis_params[plat]['pilon_merged_bam'],
                           log_dir=analysis_params[plat]['pilon_log'])

        samtools_bam_index(in_bam=analysis_params[plat]['pilon_merged_bam'],
                           log_dir=analysis_params[plat]['pilon_log'])
    else:
        print "Skipping merging bams %s present" % analysis_params[plat]['pilon_merged_bam']

    # need to add checks for file output
    pilon_fixassembly(in_ref=analysis_params['ref'], in_bam=analysis_params[plat]['pilon_merged_bam'],
                      out_root=analysis_params[plat][
                          'pilon_root'], log_dir=analysis_params[plat]['pilon_log'],
                      input_type=analysis_params[plat]['pilon_input_type'])
