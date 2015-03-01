## functions for running pilon
import sys
import time
import subprocess

def pilon_fixassembly(in_ref, in_bam, out_root, log_dir, input_type):
    '''Validating Assembly with Pilon'''
    print "Validating Assembly with Pilon ..."
    
    # prep files
    log_file = open(log_dir + "/pilon-fixassembly"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/pilon-fixassembly"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run command
    pilon_command = ["java","-Xmx6G","-jar","/usr/local/bin/pilon-1.10.jar",
                    "--genome",in_ref,input_type,in_bam,"--changes","--vcf","--tracks",
                    "--fix","all,breaks,novel","--output", out_root]
    subprocess.call(pilon_command, stdout=log_file,stderr=stderr_file) 
    log_file.close(); stderr_file.close()