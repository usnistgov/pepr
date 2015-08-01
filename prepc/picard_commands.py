# ### Functions for running picard functions

import sys
import time
import subprocess
import os

def picard_create_dict(in_ref, out_dict, log_dir):
    ''' Creating dict for reference sequence'''
    print "Creating Sequence Dictionary ..."
    
    ## check input
    assert in_ref
    assert out_dict
    assert log_dir
    assert os.path.isfile(in_ref)
    assert os.path.isdir(log_dir)
    # prep files
    log_file = open(log_dir + "/picard_create_dict"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/picard_create_dict"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    markdup_command = ["java","-Xmx2g","-jar","/usr/local/bin/picard.jar", "CreateSequenceDictionary",
                        ("R=%s" % (in_ref)),("O=%s" % (out_dict))]

    subprocess.call(markdup_command, stdout=log_file,stderr=stderr_file)

    ## checking outputs
    assert os.path.isfile(out_dict), "Error %s not found" % out_dict

    log_file.close(); stderr_file.close()
        
def picard_add_header(in_bam, out_bam, log_dir, read_group):
    ''' Adding header to bam'''
    print "Adding header to bam ..."

    ## checking inputs
    assert in_bam
    assert os.path.isfile(in_bam)
    assert out_bam
    assert log_dir
    assert os.path.isdir(log_dir)
    assert read_group

    # prep files
    log_file = open(log_dir + "/picard_add_header"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/picard_add_header"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    add_header_command = ["java","-Xmx2g","-jar","/usr/local/bin/picard.jar","AddOrReplaceReadGroups",
                        ("INPUT=%s" % (in_bam)),("OUTPUT=%s" % (out_bam))] + read_group
    subprocess.call(add_header_command, stdout=log_file,stderr=stderr_file)

    ## checking outputs
    assert os.path.isfile(out_bam), "Expected output file %s not present" % out_bam

    log_file.close(); stderr_file.close()

def picard_markdup(in_bam, out_bam, metrics_file, log_dir):
    ''' Mark duplicates '''
    print "Marking Duplicates ..."
    
    ## checking inputs
    assert in_bam
    assert os.path.isfile(in_bam)
    assert out_bam
    assert metrics_file
    assert log_dir
    assert os.path.isdir(log_dir)

    # prep files
    log_file = open(log_dir + "/picard_markdup"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file_name = log_dir + "/picard_markdup"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder")
    stderr_file = open(log_dir + "/picard_markdup"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    markdup_command = ["java","-Xmx2g","-jar","/usr/local/bin/picard.jar", "MarkDuplicates", "READ_NAME_REGEX=null", #"VALIDATION_STRINGENCY=LENIENT",
                        ("INPUT=%s" % (in_bam)),("METRICS_FILE=%s" % (metrics_file)),("OUTPUT=%s" % (out_bam))]
    subprocess.call(markdup_command, stdout=log_file,stderr=stderr_file)

    ## checking output
    assert os.path.isfile(out_bam), "Expected output file %s not present, check stderr file %s" % (out_bam, stderr_file_name)
    assert os.path.isfile(metrics_file)

    log_file.close(); stderr_file.close()

def picard_index_stats(in_bam, log_dir):
    ''' Bam index stats using Picard'''
    print "Bam index stats ..."
    # note results are in the log file - rename if you end up using
    # prep files
    log_file = open(log_dir + "/picard_index_stats"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/picard_index_stats"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    index_stats_command = ["java","-Xmx2g","-jar","/usr/local/bin/picard.jar", "BamIndexStats",
                        ("I=%s" % (in_bam))]
    subprocess.call(index_stats_command, stdout=log_file,stderr=stderr_file)
    log_file.close(); stderr_file.close()

def picard_alignment_metrics(in_bam, bam_stats, log_dir):
    ''' Bam alignment stats using Picard'''
    print "Calculating bam alignment stats ..."
    
    ## checking inputs
    assert in_bam
    assert os.path.isfile(in_bam)
    assert bam_stats
    assert log_dir
    assert os.path.isdir(log_dir)

    # prep files
    log_file = open(log_dir + "/picard_alignment_stats"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/picard_alignment_stats"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    alignment_stats_command = ["java","-Xmx2g","-jar","/usr/local/bin/picard.jar","CollectAlignmentSummaryMetrics",
                        ("INPUT=%s" % (in_bam)),("OUTPUT=%s" % (bam_stats))]
    subprocess.call(alignment_stats_command, stdout=log_file,stderr=stderr_file)
    log_file.close(); stderr_file.close()

    ## not sure if bam_stats is a file or a directory
    #assert os.path.isfile(bam_stats)

def picard_multiple_metrics(in_bam, bam_stats, log_dir):
    ''' Bam multiple metrics Picard'''
    print "Calculating bam metrics ..."
    
    ## checking inputs
    assert in_bam
    assert os.path.isfile(in_bam)
    assert bam_stats
    assert log_dir
    assert os.path.isdir(log_dir)

    # prep files
    log_file = open(log_dir + "/picard_multiple_metrics"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/picard_multiple_metrics"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    program_list = ["CollectAlignmentSummaryMetrics","CollectInsertSizeMetrics",
                    "QualityScoreDistribution", "MeanQualityByCycle"]
    program_list = ["PROGRAM=" + i for i in program_list]
    multiple_metrics_command = ["java","-Xmx2g","-jar","/usr/local/bin/picard.jar", "CollectMultipleMetrics",
                        ("INPUT=%s" % (in_bam)),("OUTPUT=%s" % (bam_stats))] + program_list
    subprocess.call(multiple_metrics_command, stdout=log_file,stderr=stderr_file)
    log_file.close(); stderr_file.close()

    ## need to figure out how to validate outputs