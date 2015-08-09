# Whole genome vcf files
from prepc.samtools_commands import samtools_mpileup
from prepc.vcflib_commands import vcflib_vcf2tsv
from joblib import Parallel, delayed
import multiprocessing
num_cores = multiprocessing.cpu_count()


def parallel_consensus(plat, analysis_params):
    # whole genome variant calls
    bam_list = [analysis_params[i]['markdup_file']
                for i in analysis_params[plat]['accessions']]
    samtools_mpileup(in_ref=analysis_params['ref'],
                     in_bams=bam_list,
                     out_vcf=analysis_params[plat]['consensus_vcf'],
                     log_dir=analysis_params[plat]['consensus_base_log'])
    vcflib_vcf2tsv(in_vcf=analysis_params[plat]['consensus_vcf'],
                   out_tsv=analysis_params[plat]['consensus_tsv'],
                   log_dir=analysis_params[plat]['consensus_base_log'])


def main(analysis_params, platforms):
    Parallel(n_jobs=num_cores)(
        delayed(parallel_consensus)(i, analysis_params) for i in platforms)
