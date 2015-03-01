# ### Functions for preparing bams and calling mpileup

import sys
import time
import subprocess
    
def gatk_realign(in_ref, in_bam, out_bam, intervals_file, log_dir):
    ''' Indel relignment'''
    print "Realignment Around Indels ..."
    
    # prep files
    log_file = open(log_dir + "/gatk_realign"+ time.strftime("-%Y-%m-%d-%H-%M-%S.log"),'w')
    stderr_file = open(log_dir + "/gatk_realign"+ time.strftime("-%Y-%m-%d-%H-%M-%S.stder"),'w')
    
    # run commands
    GATK_command = ["java","-jar","-Xmx2g","/notebooks/utilities/GenomeAnalysisTK.jar"]
    realigner_target_command = GATK_command + ["-T","RealignerTargetCreator", "-R",ref,"-I",in_bam, "-o", intervals_file]
    subprocess.call(realigner_target_command,stdout=log_file,stderr=stderr_file)
    
    realigner_command = GATK_command + ["-T","IndelRealigner", "-R", ref,"-I",in_bam,
                                "-targetIntervals", intervals_file, "-o", out_bam]
    subprocess.call(realigner_command, stdout=log_file,stderr=stderr_file)
    log_file.close(); stderr_file.close()