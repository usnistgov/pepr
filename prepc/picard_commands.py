# ### Functions for running picard functions

import sys
import time
import subprocess

def picard_create_dict(in_ref, out_dict, log_dir):
    ''' Creating dict for reference sequence'''
    print "Creating Sequence Dictionary ..."
    
    # prep files
    log_file = open(log_dir + "/picard_create_dict"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/picard_create_dict"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    markdup_command = ["java","-Xmx40g","-jar","/usr/local/bin/CreateSequenceDictionary.jar",
                        ("R=%s" % (in_ref)),("O=%s" % (out_dict))]
    subprocess.call(markdup_command, stdout=log_file,stderr=stderr_file)
        
def picard_add_header(in_bam, out_bam, log_dir, read_group):
    ''' Adding header to bam'''
    print "Adding header to bam ..."
    
    # prep files
    log_file = open(log_dir + "/picard_add_header"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/picard_add_header"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    markdup_command = ["java","-Xmx40g","-jar","/usr/local/bin/AddOrReplaceReadGroups.jar",
                        ("INPUT=%s" % (in_bam)),("OUTPUT=%s" % (out_bam))] + read_group
    subprocess.call(markdup_command, stdout=log_file,stderr=stderr_file)
        
def picard_markdup(in_bam, out_bam, metrics_file, log_dir):
    ''' Mark duplicates '''
    print "Marking Duplicates ..."
    
    # prep files
    log_file = open(log_dir + "/picard_markdup"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/picard_markdup"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    markdup_command = ["java","-Xmx40g","-jar","/usr/local/bin/MarkDuplicates.jar","VALIDATION_STRINGENCY=LENIENT",
                        ("INPUT=%s" % (in_bam)),("METRICS_FILE=%s" % (metrics_file)),("OUTPUT=%s" % (out_bam))]
    subprocess.call(markdup_command, stdout=log_file,stderr=stderr_file)
    log_file.close(); stderr_file.close()

def picard_index_stats(in_bam, log_dir):
    ''' Bam index stats using Picard'''
    print "Bam index stats ..."
    # note results are in the log file - rename if you end up using
    # prep files
    log_file = open(log_dir + "/picard_index_stats"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/picard_index_stats"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    index_stats_command = ["java","-Xmx40g","-jar","/usr/local/bin/BamIndexStats.jar",
                        ("I=%s" % (in_bam))]
    subprocess.call(index_stats_command, stdout=log_file,stderr=stderr_file)

def picard_alignment_metrics(in_bam, bam_stats, log_dir):
    ''' Bam alignment stats using Picard'''
    print "Calculating bam alignment stats ..."
    
    # prep files
    log_file = open(log_dir + "/picard_alignment_stats"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/picard_alignment_stats"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    alignment_stats_command = ["java","-Xmx40g","-jar","/usr/local/bin/CollectAlignmentSummaryMetrics.jar",
                        ("INPUT=%s" % (in_bam)),("OUTPUT=%s" % (bam_stats))]
    subprocess.call(alignment_stats_command, stdout=log_file,stderr=stderr_file)

def picard_multiple_metrics(in_bam, bam_stats, log_dir):
    ''' Bam multiple metrics Picard'''
    print "Calculating bam metrics ..."
    
    # prep files
    log_file = open(log_dir + "/picard_multiple_metrics"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/picard_multiple_metrics"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    program_list = ["CollectAlignmentSummaryMetrics","CollectInsertSizeMetrics",
                    "QualityScoreDistribution", "MeanQualityByCycle"]
    program_list = ["PROGRAM=" + i for i in program_list]
    multiple_metrics_command = ["java","-Xmx40g","-jar","/usr/local/bin/CollectMultipleMetrics.jar",
                        ("INPUT=%s" % (in_bam)),("OUTPUT=%s" % (bam_stats))] + program_list
    subprocess.call(multiple_metrics_command, stdout=log_file,stderr=stderr_file)

