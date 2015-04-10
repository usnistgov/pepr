import sys
import time
import subprocess

def pathoqc_command(plat, fastq1, log_dir, out_dir, thread_num, fastq2=False):
    ## log file stores standard out
    log_file = open(log_dir + "/pathoqc"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/pathoqc"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    pathoqc_command = ["python","/PathoScope/pathoqc_v0.1.2/pathoqc.py"]
    
    if fastq2 != None:
        pathoqc_command = pathoqc_command + ['-1',fastq1, '-2',fastq2,'-s',plat,'-p',str(thread_num),'-o',out_dir]
    else:
        pathoqc_command = pathoqc_command + ['-1',fastq1,'-s',plat,'-p',str(thread_num),'-o',out_dir]
    subprocess.call(pathoqc_command, stdout=log_file, stderr=stderr_file)        

def pathomap_command(ref_path, index_dir, fastq1, log_dir, out_dir, out_sam, exptag,fastq2=False):
    ## log file stores standard out
    log_file = open(log_dir + "/pathomap"+time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/pathomap"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')

    ## pathoscope command root
    pathomap_command = ["python", "/PathoScope/pathoscope/pathoscope.py",'--verbose','MAP', '-targetRefFiles',ref_path,\
                        '-indexDir',index_dir,'-outDir',out_dir,'-outAlign', out_sam, '-expTag', exptag]
    
    if fastq2:
        pathomap_command = pathomap_command + ['-1',fastq1, '-2',fastq2]
    else:
        pathomap_command = pathomap_command + ['-U',fastq1]
    subprocess.call(pathomap_command, stdout=log_file, stderr=stderr_file)

def pathoid_command(input_sam, log_dir, out_dir, exptag):
    # command for running pathoid

    ## log file stores standard out
    log_file = open(log_dir + "/pathoid"+time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/pathoid"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    ## pathoscope command root
    pathoid_command = ["python","/PathoScope/pathoscope/pathoscope.py",'--verbose','ID', '-alignFile',input_sam,'-fileType',
                       'sam','-outDir',out_dir,'--outMatrix','-expTag', exptag]
    subprocess.call(pathoid_command, stdout=log_file,stderr=stderr_file)

