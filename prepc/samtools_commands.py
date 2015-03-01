# ### Functions for manipulating bam files using samtools

import sys
import time
import subprocess

def samtools_sam_to_bam(in_sam, out_bam, log_dir):
    '''Convert sam to bam'''
    print "Converting sam to bam ..."

    ## log files for standard out and error
    bam_file = open(out_bam,'w')
    stderr_file = open(log_dir + "/samtools_sam_to_bam"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    ## run command
    sam_to_bam_command = ["samtools","view","-b",in_sam]
    subprocess.call(sam_to_bam_command, stdout=bam_file, stderr=stderr_file)  
    bam_file.close(); stderr_file.close()

def samtools_bam_sort(in_bam, out_bam, log_dir):
    ''' Sorting bam'''
    print "Sorting bam ..."

    ## log files for standard out and error
    out_file = open(out_bam,'w')
    stderr_file = open(log_dir + "/samtools_bam_sort"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    ## run command
    bam_sort_command = ["samtools","sort","-T","sort_temp","-O", "bam", in_bam]
    subprocess.call(bam_sort_command, stdout=out_file,stderr=stderr_file) 
    out_file.close(); stderr_file.close()

def samtools_bam_index(in_bam, log_dir):
    ''' index bam file'''
    print "Indexing bam ..."

    ## log files for standard out and error
    log_file = open(log_dir + "/samtools_bam_index"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/samtools_bam_index"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    ## run command
    subprocess.call(["samtools","index",in_bam],stdout=log_file,stderr=stderr_file)
    log_file.close(); stderr_file.close()

def samtools_bam_group_sort(in_bam, out_bam, log_dir):
    ''' Sorting bam'''
    print "Sorting bam ..."
    
    # prep files
    log_file = open(log_dir + "/samtools_bam_group_sort"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/samtools_bam_group_sort"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    # the "-T" had out_dir after it not sure if log_dir will work, or what gets put there
    bam_group_sort_command = ["samtools", "sort", "-n", "-O", "bam", "-o", out_bam, "-T", log_dir, in_bam]
    subprocess.call(bam_group_sort_command, stdout=log_file,stderr=stderr_file) 
    log_file.close(); stderr_file.close()
    
def samtools_bam_fixmate(in_bam,out_bam,log_dir):
    '''Fix mate pairs'''
    print "Fixing mate pairs ..."
    
    ## log files for standard out and error
    #out_file = open(bam_fix,'w')
    log_file = open(log_dir + "/samtools_bam_fixmate"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/samtools_bam_fixmate"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    fixmate_command = ["samtools","fixmate",in_bam,out_bam]
    subprocess.call(fixmate_command, stderr=stderr_file, stdout=log_file)  
    log_file.close(); stderr_file.close()

def samtools_bam_merge(bam_list, out_bam, log_dir):
    ''' Merge list of bams into a single bam file'''
    print "Merging bams ..."
    
    # prep files
    log_file = open(log_dir + "/samtools_bam_merge"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/samtools_bam_merge"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    merge_bam_command = ["samtools","merge", "-b",bam_list, out_bam]
    subprocess.call(merge_bam_command, stdout=log_file,stderr=stderr_file)
    log_file.close(); stderr_file.close()

def samtools_mpileup(in_ref, in_bams,out_vcf, log_dir, varscan_pairs = False):
    ''' Takes a list of bam files and refernece genome then
        performs base level sequence analysis
    '''
    print "Running mpileup ..."
    
    # prep files
    vcf_file = open(out_vcf,'w')
    stderr_file = open(log_dir + "/samtools_mpileup"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    mpileup_command = ["samtools","mpileup", "-uv", "-t", "DP", "-t", "DV",
                     "-t", "DPR", "-t", "SP", "-t", "DP4","-f", in_ref] + in_bams
    subprocess.call(mpileup_command,stdout=vcf_file,stderr=stderr_file)
    vcf_file.close(); stderr_file.close()

def samtools_mpileup_pairs(in_ref, in_bams, out_mpileup, log_dir):
    ''' Mpileup for varscan
    path/samtools-0.1.18/samtools mpileup -q 1 -f /projects/justin.zook/from-projects/references/human_g1k_v37.fasta $BAM1 $BAM2
    '''
    print "Running mpileup for pairwise bams ..."
    
    # prep files
    mpileup_file = open(out_mpileup,'w')
    stderr_file = open(log_dir + "/samtools_mpileup_pairs"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    mpileup_command_pairs = ["samtools","mpileup", "-q", "1","-f", in_ref] + in_bams
    subprocess.call(mpileup_command_pairs,stdout=mpileup_file,stderr=stderr_file)
    mpileup_file.close(); stderr_file.close()
    