# genomic purity pipeline
import os
import subprocess
from joblib import Parallel, delayed
import multiprocessing
num_cores = multiprocessing.cpu_count()
from prepc.pathoscope_commands import pathoqc_command
from prepc.pathoscope_commands import pathomap_command
from prepc.pathoscope_commands import pathoid_command


def parallel_pathoqc(i, analysis_params):
    # if not os.path.isfile(analysis_params[i]['trimmed_fastq1']) and \
    #     os.path.isfile(analysis_params[i]['trimmed_fastq2']):
    pathoqc_command(plat=analysis_params[i]['plat'],
                    fastq1=analysis_params[i]['fastq1'],
                    fastq2=analysis_params[i]['fastq2'],
                    log_dir=analysis_params[i]['genomic_purity_log'],
                    out_dir=analysis_params['genomic_purity']['tmp_dir'],
                    thread_num=str(num_cores))

    # assert os.path.isfile(analysis_params[i]['trimmed_fastq1'])
    # assert os.path.isfile(analysis_params[i]['trimmed_fastq2'])


def parallel_pathomap_id(i, analysis_params):
    # need to add skips
    acc_tmp_dir = analysis_params['genomic_purity']['tmp_dir'] + "/" + i
    subprocess.call(['mkdir', '-p', acc_tmp_dir])
    pathomap_command(ref_path=analysis_params['ref'],
                     index_dir=analysis_params['ref_dir'],
                     exptag=analysis_params[i]['pathoscope_run_id'],
                     fastq1=analysis_params[i]['trimmed_fastq1'],
                     fastq2=analysis_params[i]['trimmed_fastq2'],
                     log_dir=analysis_params[i]['genomic_purity_log'],
                     out_dir=acc_tmp_dir,
                     out_sam=analysis_params['pathomap_sam'],
                     thread_num=str(8))
    assert os.path.isfile(analysis_params[i]['pathomap_sam'])
    # running pathoid
    pathoid_command(input_sam=analysis_params[i]['pathomap_sam'],
                    log_dir=analysis_params[i]['genomic_purity_log'],
                    out_dir=analysis_params['genomic_purity']['analysis_dir'],
                    exptag=analysis_params[i]['pathoscope_run_id'])

    subprocess.call(["rm", "-r", acc_tmp_dir])


def main(analysis_params):
    for i in analysis_params['accessions']:
        print "Running pathoscope pipeline"

        # read quality control - filters low quality read
        n_jobs = num_cores / num_cores
        Parallel(n_jobs=n_jobs)(delayed(parallel_pathoqc)(i, analysis_params)
                                for i in analysis_params['accessions'])

        # running pathomap and pathoid
        n_jobs = num_cores / 8
        Parallel(n_jobs=n_jobs)(delayed(parallel_pathomap_id)
                                (i, analysis_params)
                                for i in analysis_params['accessions'])
