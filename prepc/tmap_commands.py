## functions for mapping fastq files with tmap
import sys
import time
import subprocess
import os
import multiprocessing
num_cores = str(multiprocessing.cpu_count())

def tmap_index_ref(in_ref, log_dir):
    '''tmap index reference'''
    print "Indexing reference with TMAP ..."
    
    ## checking input
    assert in_ref
    assert log_dir
    assert os.path.isfile(in_ref), "File check for %s fail" % in_ref
    assert os.path.isdir(log_dir)

    ## prep files
    log_file_name = log_dir + "/tmap_index_ref" + time.strftime("-%Y-%m-%d-%H-%M-%S.log")
    log_file = open(log_file_name,'w')
    stderr_file_name = log_dir + "/tmap_index_ref" + time.strftime("-%Y-%m-%d-%H-%M-%S.stder")
    stderr_file = open(stderr_file_name,'w')
    
    ## run command
    tmap_index_ref_command = ["tmap", "index", "-f",in_ref]
    subprocess.call(tmap_index_ref_command, stdout=log_file,stderr=stderr_file) 

    ## checking output
    ## need to add assertions for index files
    assert os.path.isfile(log_file_name)
    assert os.path.isfile(stderr_file_name)
    for i in ['anno','bwt','pac','sa']:
        assert os.path.isfile(in_ref + ".tmap." + i)

    log_file.close(); stderr_file.close()

def tmap_map_fq(in_ref, in_fq, out_sam, log_dir):
    '''Mapping fastq with tmap'''
    print "Mapping fastq with TMAP ..."
    
    ## checking input 
    for variable in [in_ref, in_fq, out_sam, log_dir]:
        assert variable

    assert os.path.isfile(in_ref)
    assert os.path.isfile(in_fq)
    assert os.path.isdir(log_dir)

    ## prep files
    log_file_name = log_dir + "/tmap_map"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log")
    log_file = open(log_file_name,'w')
    stderr_file_name = log_dir + "/tmap_map"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder")
    stderr_file = open(stderr_file_name,'w')
    
    ## run command
    tmap_map_command = ["tmap", "mapall", "-n", num_cores, "-f", in_ref, "-r", in_fq, "-v","-Y", "-s", out_sam, "stage1", "map4"]#, "stage2", "map4","stage3", "map6"]
    subprocess.call(tmap_map_command, stdout=log_file,stderr=stderr_file) 

    ## checing outputs
    assert os.path.isfile(out_sam), "Mapping file %s not produced" % out_sam
    assert os.path.isfile(log_file_name)
    assert os.path.isfile(stderr_file_name)

    log_file.close(); stderr_file.close()

