# ### Functions for preparing bams and calling mpileup

import sys
import time
import subprocess

def bam_group_sort(in_bam, out_bam, log_dir):
    ''' Sorting bam'''
    print "Sorting bam ..."
    
    # prep files
    log_file = open(log_dir + "/bwa_group_sort"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/bwa_group_sort"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    # the "-T" had out_dir after it not sure if log_dir will work, or what gets put there
    bam_group_sort_command = ["samtools", "sort", "-n", "-O", "bam", "-o", out_bam, "-T", log_dir, in_bam]
    subprocess.call(bam_group_sort_command, stdout=log_file,stderr=stderr_file) 
    log_file.close(); stderr_file.close()

def bam_add_header(in_bam, out_header, log_dir, read_group):
    ''' Adding header to bam'''
    print "Adding header to bam ..."
    
    # prep files
    log_file = open(log_dir + "/bwa_add_header"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/bwa_add_header"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    markdup_command = ["java","-Xmx2g","-jar","/usr/local/bin/AddOrReplaceReadGroups.jar",
                        ("INPUT=%s" % (in_bam)),("OUTPUT=%s" % (out_header))] + read_group
    subprocess.call(markdup_command, stdout=log_file,stderr=stderr_file)
    
def bam_fixmate(in_bam,out_bam,log_dir):
    '''Fix mate pairs'''
    print "Fixing mate pairs ..."
    
    ## log files for standard out and error
    #out_file = open(bam_fix,'w')
    log_file = open(log_dir + "/bwa_fixmate"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/bwa_fixmate"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    fixmate_command = ["samtools","fixmate",in_bam,out_bam]
    subprocess.call(fixmate_command, stderr=stderr_file, stdout=log_file)  
    log_file.close(); stderr_file.close()
    
def bam_realign(in_bam, ref, intervals_file,out_bam, log_dir):
    ''' Indel relignment'''
    print "Realignment Around Indels ..."
    
    # prep files
    log_file = open(log_dir + "/bwa_realign"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/bwa_realign"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run commands
    GATK_command = ["java","-jar","-Xmx2g","/notebooks/utilities/GenomeAnalysisTK.jar"]
    realigner_target_command = GATK_command + ["-T","RealignerTargetCreator", "-R",ref,"-I",in_bam, "-o", intervals_file]
    subprocess.call(realigner_target_command,stdout=log_file,stderr=stderr_file)
    
    realigner_command = GATK_command + ["-T","IndelRealigner", "-R", ref,"-I",in_bam,
                                "-targetIntervals", intervals_file, "-o", out_bam]
    subprocess.call(realigner_command, stdout=log_file,stderr=stderr_file)
    log_file.close(); stderr_file.close()
    
def bam_markdup(in_bam, out_bam, metrics_file, log_dir):
    ''' Mark duplicates '''
    print "Marking Duplicates ..."
    
    # prep files
    log_file = open(log_dir + "/bwa_markdup"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/bwa_markdup"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    markdup_command = ["java","-Xmx2g","-jar","/usr/local/bin/MarkDuplicates.jar","VALIDATION_STRINGENCY=LENIENT",
                        ("INPUT=%s" % (in_bam)),("METRICS_FILE=%s" % (metrics_file)),("OUTPUT=%s" % (out_bam))]
    subprocess.call(markdup_command, stdout=log_file,stderr=stderr_file)
    log_file.close(); stderr_file.close()

def bam_merge(bam_list, out_bam, log_dir):
    ''' Merge list of bams into a single bam file'''
    print "Merging bams"
    
    # prep files
    log_file = open(log_dir + "/merge_bams"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/merge_bams"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    merge_bam_command = ["samtools","merge", "-b", bam_list, out_bam]
    subprocess.call(merge_bam_command, stdout=log_file,stderr=stderr_file)
    log_file.close(); stderr_file.close()

def genome_calls_mpileup(bams,ref, vcf_file, log_dir):
    ''' Takes a list of bam files and refernece genome then
        performs base level sequence analysis
    '''
    print "Running mpileup ..."
    
    # prep files
    vcf_file = open(vcf_file,'w')
    stderr_file = open(log_dir + "/mpileup"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    mpileup_command = ["samtools","mpileup", "-uv", "-t", "DP", "-t", "DV",
                     "-t", "DPR", "-t", "SP", "-t", "DP4","-f", ref] + bams
    subprocess.call(mpileup_command,stdout=vcf_file,stderr=stderr_file)
    vcf_file.close(); stderr_file.close()