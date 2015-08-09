# Functions for using varson for variant calling
import time
import subprocess
import os


def varscan_somatic(in_mpileup1, in_mpileup2, snp_out, indel_out, log_dir, cov='15'):
    ''' Performs somatic variant calling for a pair of input bam files'''
    print "Running varscan for pairwise variant calling ..."

    # check for variable names
    assert in_mpileup1
    assert in_mpileup2
    assert snp_out
    assert indel_out
    assert log_dir

    # check for input files and log directory
    assert os.path.isdir(log_dir)
    assert os.path.isfile(in_mpileup1)
    assert os.path.isfile(in_mpileup2)

    # prep files
    log_file_name = log_dir + "/varscan_somatic" + \
        time.strftime("-%Y-%m-%d-%H-%M-%S.log")
    log_file = open(log_file_name, 'w')
    stderr_file_name = log_dir + "/varscan_somatic" + \
        time.strftime("-%Y-%m-%d-%H-%M-%S.stder")
    stderr_file = open(stderr_file_name, 'w')

    # run command
    varscan_somatic_command = ["java", "-Xmx8g", "-jar", "/usr/local/bin/VarScan.v2.3.7.jar",
       						   "somatic", in_mpileup1, in_mpileup2,
                               "--output-snp", snp_out,
                               "--output-indel", indel_out,
                               "--min-coverage", cov,
                               "--min-coverage-tumor", cov,
                               "--min-coverage-normal", cov,
                               "--somatic-p-value", "0.001"]

    subprocess.call(
        varscan_somatic_command, stdout=log_file, stderr=stderr_file)

    # check that process ran
    assert os.path.isfile(indel_out)
    assert os.path.isfile(snp_out)
    assert os.path.isfile(log_file_name)
    assert os.path.isfile(stderr_file_name)

    log_file.close()
    stderr_file.close()
