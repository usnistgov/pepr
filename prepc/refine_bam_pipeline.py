import bwa_commands
import samtools_commands
import picard_commands
import gatk_commands
import os

def main(accession, ref, accession_params):
    ''' Processing single bam file'''
    
    assert ref
    assert os.path.isfile(ref)
    
    assert accession_params
    assert accession_params['mapping_log']
    assert os.path.isdir(accession_params['mapping_log'])
    assert accession_params['plat']

    if accession_params['plat'] == "miseq":
        assert accession_params
        assert accession_params['sorted_bam']
        assert accession_params['group_sort_file']
        assert accession_params['fix_file']
        assert accession_params['sort_fix_file']

        assert os.path.isfile(accession_params['sorted_bam'])
        if not os.path.isfile(accession_params['group_sort_file']):
            samtools_commands.samtools_bam_group_sort(
                in_bam = accession_params['sorted_bam'], 
                out_bam = accession_params['group_sort_file'], 
                log_dir = accession_params['mapping_log'])
        else:
            print "skipping group sort"
        
        assert os.path.isfile(accession_params['group_sort_file'])
        
        ## look into moving to sam_to_bam
        if not os.path.isfile(accession_params['fix_file']):
            samtools_commands.samtools_bam_fixmate(
                in_bam = accession_params['group_sort_file'],
                out_bam = accession_params['fix_file'],
                log_dir = accession_params['mapping_log'])
        else:
            print "skipping fixmate"
        
        assert os.path.isfile(accession_params['fix_file'])
        if not os.path.isfile(accession_params['sort_fix_file']):
            samtools_commands.samtools_bam_sort(  
                in_bam = accession_params['header_file'],
                out_bam = accession_params['sort_fix_file'],
                log_dir=accession_params['mapping_log'])
        else:
            print "skipping sort"

        #assert os.path.isfile(accession_params['sort_fix_file'])
        #if not os.path.isfile(accession_params['sort_fix_file'] + ".bai"):
        samtools_commands.samtools_bam_index(
                in_bam = accession_params['sort_fix_file'], 
                log_dir = accession_params['mapping_log'])
        #else:
        #    print "skipping index"

        assert os.path.isfile(accession_params['sort_fix_file'] + ".bai")
        bam_file = accession_params['sort_fix_file']
    
    else:
        assert os.path.isfile(accession_params['sorted_bam'])
    	bam_file = accession_params['sorted_bam']

    assert accession_params['intervals_file']
    assert accession_params['realign_file']
    assert accession_params['markdup_file']
    assert accession_params['metrics_file']

    ## move to miseq only pipeline
    if not os.path.isfile(accession_params['realign_file']):
        gatk_commands.gatk_realign(in_ref=ref,
            in_bam=bam_file,
            out_bam=accession_params['realign_file'],
            intervals_file=accession_params['intervals_file'],
            log_dir=accession_params['mapping_log'])
    else:
        print "skipping realignment around indels"
       
    assert os.path.isfile(accession_params['intervals_file'])
    assert os.path.isfile(accession_params['realign_file'])

    if not os.path.isfile(accession_params['markdup_file']):
        picard_commands.picard_markdup(
            in_bam = accession_params['realign_file'], 
            out_bam = accession_params['markdup_file'], 
            metrics_file = accession_params['metrics_file'],
            log_dir = accession_params['mapping_log'])
    else:
        print "skipping mark duplicates"
    assert os.path.isfile(accession_params['markdup_file'])
    assert os.path.isfile(accession_params['metrics_file'])

    #if not os.path.isfile(accession_params['markdup_file'] + ".bai"):
    # samtools_commands.samtools_bam_index(
    #         in_bam = accession_params['markdup_file'], 
    #         log_dir = accession_params['mapping_log'])
    #else:
    #    print "skipping index"
    #assert os.path.isfile(accession_params['markdup_file'] + ".bai"), "Expected file %s not found check "