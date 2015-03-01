# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# ## Pathoscope pipeline
# Objective: script for processing MiSeq and PGM data using pathoscope

# <codecell>

import sys
import time
import subprocess

# <codecell>

def pathoqc_command(fastq1, out_dir, path_pathoqc, plat, thread_num, fastq2=False):
    ## log file stores standard out
    log_file = open(out_dir + "/pathoqc"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(out_dir + "/pathoqc"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    pathoqc_command = ["python",path_pathoqc]
    
    if fastq2 != None:
        pathoqc_command = pathoqc_command + ['-1',fastq1, '-2',fastq2,'-s',plat,'-p',str(thread_num),'-o',out_dir]
    else:
        pathoqc_command = pathoqc_command + ['-1',fastq1,'-s',plat,'-p',str(thread_num),'-o',out_dir]
    subprocess.call(pathoqc_command, stdout=log_file, stderr=stderr_file)        

# <codecell>

def pathomap_command(ref_path, index_dir, fastq1, out_dir, path_pathoscope,exptag,fastq2=False):
    import re
    ## log file stores standard out
    log_file = open(out_dir + "/pathomap"+time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(out_dir + "/pathomap"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    ## output sam file
    out_sam =  re.sub('fastq|fq', 'sam', fastq1.split("/")[-1])
    
    ## pathoscope command root
    pathomap_command = ["python",path_pathoscope,'--verbose','MAP', '-targetRefFiles',ref_path,\
                        '-indexDir',index_dir,'-outDir',out_dir,'-outAlign', out_sam, '-expTag', exptag]
    
    if fastq2:
        pathomap_command = pathomap_command + ['-1',fastq1, '-2',fastq2]
    else:
        pathomap_command = pathomap_command + ['-U',fastq1]
    subprocess.call(pathomap_command, stdout=log_file,stderr=stderr_file)

# <codecell>

def pathoid_command(path_pathoscope, input_sam, out_dir, exptag):
    # command for running pathoid

    ## log file stores standard out
    log_file = open(out_dir + "/pathoid"+time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(out_dir + "/pathoid"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    ## pathoscope command root
    pathoid_command = ["python",path_pathoscope,'--verbose','ID', '-alignFile',input_sam,'-fileType',
                       'sam','-outDir',out_dir,'--outMatrix','-expTag', exptag]
    subprocess.call(pathoid_command, stdout=log_file,stderr=stderr_file)

