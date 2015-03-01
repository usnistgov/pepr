## functions for mapping fastq files with tmap
import sys
import time
import subprocess

def tmap_index_ref(in_ref, log_dir):
    '''tmap index reference'''
    print "Indexing reference with TMAP ..."
    
    # prep files
    log_file = open(log_dir + "/tmap_index_ref" + time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/tmap_index_ref" + time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    tmap_index_ref_command = ["tmap", "index", "-f",in_ref]
    subprocess.call(tmap_index_ref_command, stdout=log_file,stderr=stderr_file) 
    log_file.close(); stderr_file.close()

def tmap_map_fq(in_ref, in_fq, out_sam, log_dir):
    '''Mapping fastq with tmap'''
    print "Mapping fastq with TMAP ..."
    
    # prep files
    log_file = open(log_dir + "/tmap_map"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/tmap_map"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    tmap_map_command = ["tmap", "mapall", "-n", "8", "-f", in_ref, "-r", in_fq, "-v","-Y", "-s", out_sam, "stage1", "map4"]#, "stage2", "map4","stage3", "map6"]
    subprocess.call(tmap_map_command, stdout=log_file,stderr=stderr_file) 
    log_file.close(); stderr_file.close()