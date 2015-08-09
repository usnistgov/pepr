# sra commands for getting sequence data from ganbank
import time
import subprocess
import os


def sra_get_fastq(plat, accession, out_dir, log_dir):
    '''Retrieving fastq data from Genbank'''
    print "Retrieving fastq data for %s" % (accession)

    # checking inputs
    assert plat
    assert accession
    assert out_dir
    assert log_dir

    # checking for dirs
    assert os.path.isdir(out_dir)
    assert os.path.isdir(log_dir)

    # log files for standard out and error
    log_file_name = log_dir + "/sra_get_fastq" + \
        time.strftime("-%Y-%m-%d-%H-%M-%S.log")
    log_file = open(log_file_name, 'w')
    stderr_file_name = log_dir + "/sra_get_fastq" + \
        time.strftime("-%Y-%m-%d-%H-%M-%S.stder")
    stderr_file = open(stderr_file_name, 'w')

    # run command
    if plat == "miseq":
        if not os.path.isfile(out_dir + "/" + accession + "_1.fastq") and \
                not os.path.isfile(out_dir + "/" + accession + "_2.fastq"):
            sra_get_fastq_command = [
                "fastq-dump", "--split-files", "-L", "5",
                "-v", "-A", accession, "-O", out_dir]
            subprocess.call(
                sra_get_fastq_command, stdout=log_file, stderr=stderr_file)

            assert os.path.isfile(out_dir + "/" + accession + "_1.fastq")
            assert os.path.isfile(out_dir + "/" + accession + "_2.fastq")
        else:
            print "Skipping download for %s fastq files present" % accession
    else:
        if not os.path.isfile(out_dir + "/" + accession + ".fastq"):
            sra_get_fastq_command = [
                "fastq-dump", "-L", "5", "-v", "-A", accession, "-O", out_dir]
            subprocess.call(
                sra_get_fastq_command, stdout=log_file, stderr=stderr_file)

            assert os.path.isfile(out_dir + "/" + accession + ".fastq")
        else:
            print "Skipping download for %s fastq file present" % accession

    assert os.path.isfile(log_file_name)
    assert os.path.isfile(stderr_file_name)
    log_file.close()
    stderr_file.close()
