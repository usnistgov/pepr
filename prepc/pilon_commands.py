# functions for running pilon
import time
import subprocess
import os


def pilon_fixassembly(in_ref, in_bam, out_root, log_dir, input_type):
    '''Validating Assembly with Pilon'''
    print "Validating Assembly with Pilon ..."

    # checking inputs
    assert in_ref
    assert in_bam
    assert out_root
    assert log_dir
    assert input_type
    assert os.path.isfile(in_ref)
    assert os.path.isfile(in_bam)
    assert os.path.isdir(log_dir)

    # prep files
    log_file_name = log_dir + "/pilon-fixassembly" + \
        time.strftime("-%Y-%m-%d-%H-%M-%S.log")
    log_file = open(log_file_name, 'w')
    stderr_file_name = log_dir + "/pilon-fixassembly" + \
        time.strftime("-%Y-%m-%d-%H-%M-%S.stder")
    stderr_file = open(stderr_file_name, 'w')

    # run command
    pilon_command = ["java", "-Xmx24G", "-jar", "/usr/local/bin/pilon.jar",
                     "--genome", in_ref, input_type, in_bam,
                     "--changes", "--vcf", "--tracks",
                     "--fix", "all,breaks,novel", "--output", out_root]
    subprocess.call(pilon_command, stdout=log_file, stderr=stderr_file)

    # checking outputs
    assert os.path.isfile(log_file_name)
    assert os.path.isfile(stderr_file_name)
    # need checks for pilon output

    log_file.close()
    stderr_file.close()
