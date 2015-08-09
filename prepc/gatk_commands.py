import time
import subprocess
import os


def gatk_realign(in_ref, in_bam, out_bam, intervals_file, log_dir):
    ''' Indel relignment'''
    print "Realignment Around Indels"
    assert in_ref
    assert in_bam
    assert out_bam
    assert intervals_file
    assert log_dir

    # file and directory check
    assert os.path.isfile(in_ref)
    assert os.path.isfile(in_bam)
    assert os.path.isdir(log_dir)

    # checking for gatk
    assert os.path.isfile("/pepr/utils/GenomeAnalysisTK.jar")

    # prep files
    log_file_name = log_dir + "/gatk_realign" + \
        time.strftime("-%Y-%m-%d-%H-%M-%S.log")
    log_file = open(log_file_name, 'w')
    stderr_file_name = log_dir + "/gatk_realign" + \
        time.strftime("-%Y-%m-%d-%H-%M-%S.stder")
    stderr_file = open(stderr_file_name, 'w')

    # run commands
    gatk_command = [
        "java", "-jar", "-Xmx4g", "/pepr/utils/GenomeAnalysisTK.jar"]
    realigner_target_command = gatk_command + ["-T", "RealignerTargetCreator",
                                               "-R", in_ref,
                                               "-I", in_bam,
                                               "-o", intervals_file]
    subprocess.call(realigner_target_command,
                    stdout=log_file, stderr=stderr_file)

    assert os.path.isfile(intervals_file)

    realigner_command = gatk_command + ["-T", "IndelRealigner",
                                        "-R", in_ref,
                                        "-I", in_bam,
                                        "-targetIntervals", intervals_file,
                                        "-o", out_bam]
    subprocess.call(realigner_command, stdout=log_file, stderr=stderr_file)

    assert os.path.isfile(out_bam)
    assert os.path.isfile(log_file_name)
    assert os.path.isfile(stderr_file_name)

    log_file.close()
    stderr_file.close()
