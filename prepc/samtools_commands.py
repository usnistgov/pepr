# ### Functions for manipulating bam files using samtools

import sys
import time
import subprocess
import os


def samtools_index_ref(in_ref, log_dir):
    ''' Indexing reference sequence using bwa'''
    print "Indexing reference sequence with samtools faidx."

    #checking inputs
    assert in_ref
    assert log_dir
    assert os.path.isfile(in_ref)
    assert os.path.isdir(log_dir)

    stderr_file = open(log_dir + "/samtools_index_ref"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    out_file = open(log_dir + "/samtools_index_ref"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    
    ## run command
    faidx_command = ["samtools","faidx",in_ref]
    subprocess.call(faidx_command, stdout=out_file,stderr=stderr_file) 

    ## check output
    assert os.path.isfile(in_ref + ".fai")
    stderr_file.close()


def samtools_sam_to_bam(in_sam, out_bam, log_dir):
    '''Convert sam to bam'''
    print "Converting sam to bam ..."

    ## checking inputs
    assert in_sam
    assert out_bam
    assert log_dir
    assert os.path.isfile(in_sam)
    assert os.path.isdir(log_dir)

    # log files for standard out and error
    bam_file = open(out_bam,'w')
    stderr_file = open(log_dir + "/samtools_sam_to_bam"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')

    # run command
    sam_to_bam_command = ["samtools","view","-b",in_sam]
    subprocess.call(sam_to_bam_command, stdout=bam_file, stderr=stderr_file)

    # checking output
    assert os.path.isfile(out_bam)

    bam_file.close(); stderr_file.close()


def samtools_bam_sort(in_bam, out_bam, temp, log_dir):
    ''' Sorting bam'''
    print "Sorting bam ..."

    ## checking input
    assert in_bam
    assert out_bam
    assert log_dir
    assert os.path.isfile(in_bam)
    assert os.path.isdir(log_dir)

    ## log files for standard out and error
    out_file = open(out_bam,'w')
    stderr_file = open(log_dir + "/samtools_bam_sort"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')

    ## run command
    bam_sort_command = ["samtools","sort","-T",temp,"-O", "bam", in_bam]
    subprocess.call(bam_sort_command, stdout=out_file,stderr=stderr_file) 

    ## checking output
    assert os.path.isfile(out_bam)

    out_file.close(); stderr_file.close()


def samtools_bam_index(in_bam, log_dir):
    ''' index bam file'''
    print "Indexing bam ..."

    ## checking input
    assert in_bam
    assert log_dir
    assert os.path.isfile(in_bam)
    assert os.path.isdir(log_dir)

    ## log files for standard out and error
    log_file = open(log_dir + "/samtools_bam_index"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/samtools_bam_index"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')

    ## run command
    subprocess.call(["samtools","index",in_bam],stdout=log_file,stderr=stderr_file)

    ## checking output
    index_file = in_bam + ".bai"
    assert os.path.isfile(index_file), "Expected output file %s not found" % index_file

    log_file.close(); stderr_file.close()


def samtools_bam_group_sort(in_bam, out_bam, temp, log_dir):
    ''' Sorting bam'''
    print "Sorting bam by group ..."

    ## checking input
    assert in_bam
    assert out_bam
    assert log_dir
    assert os.path.isfile(in_bam)
    assert os.path.isdir(log_dir)

    # prep files
    log_file = open(log_dir + "/samtools_bam_group_sort"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/samtools_bam_group_sort"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')

    # run command
    bam_group_sort_command = ["samtools", "sort", "-n", "-O", "bam", "-o", out_bam, "-T", temp, in_bam]
    subprocess.call(bam_group_sort_command, stdout=log_file,stderr=stderr_file) 

    ## checking output
    assert os.path.isfile(out_bam)

    log_file.close(); stderr_file.close()


def samtools_bam_fixmate(in_bam,out_bam,log_dir):
    '''Fix mate pairs'''
    print "Fixing mate pairs ..."

    # checking input
    assert in_bam
    assert out_bam
    assert log_dir
    assert os.path.isfile(in_bam)
    assert os.path.isdir(log_dir)

    # log files for standard out and error
    #out_file = open(bam_fix,'w')
    log_file = open(log_dir + "/samtools_bam_fixmate"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/samtools_bam_fixmate"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')

    # run command
    fixmate_command = ["samtools","fixmate",in_bam,out_bam]
    subprocess.call(fixmate_command, stderr=stderr_file, stdout=log_file)  

    # checking output
    assert os.path.isfile(out_bam)

    log_file.close(); stderr_file.close()


def samtools_bam_merge(bam_list, out_bam, log_dir):
    ''' Merge list of bams into a single bam file'''
    print "Merging bams ..."

    # checking input
    assert bam_list
    assert out_bam
    assert log_dir
    assert os.path.isfile(bam_list)
    assert os.path.isdir(log_dir)

    ## prep files
    log_file = open(log_dir + "/samtools_bam_merge"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file_name = log_dir + "/samtools_bam_merge"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder")
    stderr_file = open(stderr_file_name,'w')

    ## run command
    merge_bam_command = ["samtools","merge", "-b",bam_list, out_bam]
    subprocess.call(merge_bam_command, stdout=log_file,stderr=stderr_file)
    log_file.close(); stderr_file.close()

    ## checking output 
    assert os.path.isfile(out_bam), "Expected output file %s not found. See stderr file %s" % (out_bam,stderr_file_name)


def samtools_mpileup(in_ref, in_bams,out_vcf, log_dir, varscan_pairs = False):
    ''' Takes a list of bam files and reference genome then
        performs base level sequence analysis
    '''
    print "Running mpileup ..."

    ## checking input
    assert in_ref
    assert in_bams
    assert out_vcf
    assert log_dir
    for bam in in_bams:
        assert os.path.isfile(bam)
    assert os.path.isdir(log_dir)

    ## prep files
    vcf_file = open(out_vcf,'w')
    stderr_file = open(log_dir + "/samtools_mpileup"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')

    ## run command
    mpileup_command = ["samtools","mpileup", "-uv", "-t", "DP", "-t", "DV",
                     "-t", "DPR", "-t", "SP", "-t", "DP4","-f", in_ref] + in_bams
    subprocess.call(mpileup_command,stdout=vcf_file,stderr=stderr_file)

    ## checking output
    assert os.path.isfile(out_vcf)

    vcf_file.close(); stderr_file.close()


def samtools_mpileup_pairs(in_ref, in_bams, out_mpileup, log_dir):
    ''' Mpileup for varscan
    path/samtools-0.1.18/samtools mpileup -q 1 -f /projects/justin.zook/from-projects/references/human_g1k_v37.fasta $BAM1 $BAM2
    '''
    print "Running mpileup for pairwise bams ..."

    # checking input
    assert in_ref
    assert in_bams
    assert out_mpileup
    assert log_dir
    assert os.path.isfile(in_ref)
    for bam in in_bams:
        assert os.path.isfile(bam)
    assert os.path.isdir(log_dir)

    # prep files
    mpileup_file = open(out_mpileup,'w')
    stderr_file = open(log_dir + "/samtools_mpileup_pairs"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')

    # run command
    mpileup_command_pairs = ["samtools","mpileup", "-q", "1","-f", in_ref] + in_bams
    subprocess.call(mpileup_command_pairs,stdout=mpileup_file,stderr=stderr_file)

    # checking output
    assert os.path.isfile(out_mpileup)

    mpileup_file.close(); stderr_file.close()


def samtools_mpileup_single(in_ref, in_bam, out_mpileup, log_dir):
    ''' Mpileup for varscan '''
    print "Running mpileup for pairwise bams ..."

    # checking input
    assert in_ref
    assert in_bam
    assert out_mpileup
    assert log_dir
    assert os.path.isfile(in_ref)
    assert os.path.isfile(in_bam)
    assert os.path.isdir(log_dir)

    # prep files
    mpileup_file = open(out_mpileup,'w')
    stderr_file = open(log_dir + "/samtools_mpileup_pairs"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')

    # run command
    mpileup_command_pairs = ["samtools","mpileup", "-q", "1","-f", in_ref, in_bam]
    subprocess.call(mpileup_command_pairs,stdout=mpileup_file,stderr=stderr_file)

    # checking output
    assert os.path.isfile(out_mpileup)

    mpileup_file.close(); stderr_file.close()


def samtools_depth(in_bam, out_depth, log_dir):
    ''' Calculating depth for a bam file
    '''
    print "Running samtools depth ..."

    # check for variable name
    assert in_bam
    assert out_depth
    assert log_dir

    # check for input files and log directory
    assert os.path.isdir(log_dir)
    assert os.path.isfile(in_bam)

    # prep files
    depth_file = open(out_depth,'w')
    stderr_file_name = log_dir + "/samtools_depth"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder")
    stderr_file = open(stderr_file_name,'w')

    # run command
    depth_command = ["samtools","depth", in_bam]
    subprocess.call(depth_command,stdout=depth_file,stderr=stderr_file)

    # check that process ran
    assert os.path.isfile(out_depth)
    assert os.path.isfile(stderr_file_name)

    depth_file.close(); stderr_file.close()
