# PEPR --Pipeline for Evaluating Prokaryotic References
Bioinformatic Pipeline for evaluating and charcterizing a reference genome sequence for a prokaryotic reference material using replicate whole genome sequencing data from orthogonal sequencing methods.  This pipeline is being developed for the characterization of NIST candidate microbial genomic DNA reference materials and is provided to the research community for use in characterizing other prokaryotic genomic materials. The pipelines can be used to evaluate other prokaryotic genomic DNA materials labs use in whole genome sequencing method validation and quality control.  

Whole genome sequencing and bioinformatic analysis is a complex process for which the sources of bias and error and not fully understood.  The methods presented here are intended to help users better characterize and understand their material not to provide a error free reference genome.  Results generated from this pipeline are indended for research use only.  

# PEPR Overview

__The bioinformatic component of PEPR consists of three parts:__

  1. evaluation - validates and corrects the reference genome 
  2. characterization - characterizes the base level purity and homogeneity of the material using the corrected reference genome from evaluation pipeline
  3. genomic_purity - performs taxonomic read classification of short read data

The evaluation pipeline is first used to refine the user provided reference
genome, and the characterization pipeline then characterizes the refined
reference genome. The genomic purity pipeline is
independent of the evaluation and characterization pipeline and is used to identify contaminant DNA.

__Running PEPR__

  * Pipeline dependencies are installed in docker containers.
  * A config file is used to define the metadata for the sequencing datasets used in the pipeline.

After the running PEPR evaluation, characterization, and genomic_purity
pipelines the R package `peprr` (https://github.com/usnistgov/peprr) is used to generate a SQLite database `peprDB` with the results for use in downstream analysis. `peprDB` is used to generate a generic Report of Analysis.

# Running PEPR
## Generating the config file
YAML file includes sample metadata and accession numbers for the datasets run by the pipeline.  See example YAML file in the repository `utils` directory.

###  Yaml file parameters
* `project_id`, `center`, `RM`, `plat`, `vial`, and `rep` used to define the read group in bam files
    * Read Group Definition ID=`project_id`, LB=`vial-rep`, PL=`plat`, PU=`barcoded`, SM=`accession`, CN=`center`
        * `project_id` - also used as the name of directory where the results are saved
        * `accession` - Genbank SRA accession id for dataset
        * `center` - sequencing center
        * `plat` - sequencing platform
        * `vial` - unique id for sample level technical replicates
        * `rep` - unique id for library prep technical replicates
    * `ref` - name of the reference genome sequence, file root name in name of results directory for run  

### Pipeline datasets
* `evaluation` pipeline should only include Illumina data
* `characterization` includes all datasets
* `genomic_purity` only short read data e.g. Illumina and Ion Torrent

## Running the pipelines
The `evaluation` and `characterization` pipelines can be run directly from the command line, the `genomic_purity` needs to be run from within the container container.

1. PEPR has two primary arguments
  * -c, --config is the path to a YAML file with the sample accessions and metadata
  * -p/ --pipeline is the name of the pipeline being run
2. Additional arguments for status text messaging capability
  1. --send_status is a yaml file with sinch account information [https://www.sinch.com](https://www.sinch.com)
  2. --send_number is the mobile number to the status messages to, use "+1" and ten digit number with no spaces, e.g "+1##########"
  + number must be able to accept sms text messages
  + Status messages are only sent when a pipeline starts and finishes, will not send a message if pipeline crashes.
3. Running the `evaluation` and `characterization` pipelines from host command line
  1. `nohup docker …. >filename.log &` this will save the standard out to `filename.log` and allow you to close the terminal without any errors
  2. The pipeline has checks to make sure the expected output files are produced and skips steps (not present in all places) if file is present. This pipeline does not check to make sure the file is not empty, if a file is incomplete will need to remove that file and subsequent files and rerun the pipeline, an easy way to do this is remove the directory generated for that step of the pipeline. I plan to add additional checks for empty files to avoid this issue
  6. If a text message is not received within the expected period of time check the nohup log file for an error message.

# Specifics to running the individual pipelines
## `evaluation`
1. Pipeline steps
  1. download fastq data from the database
  2. copy ref genome to the `ref` directory in the project_id directory and indexes the genome
  3. maps the miseq data to the reference genome
  4. evaluates the reference genome using Pilon
2. Pipeline command - see running pepr using nohup for additional information

    nohup docker run -v path/to/pepr:/pepr -v path/to/pepr-data:/pepr-data natedolson/pepr python /pepr/pepr.py -c pipeline_config.yaml -p evaluation --send_status sinch_config.yaml --send_number +1########## > run_specific_name.log &

3. Output
  1. `changes` and `fasta` files produced by Pilon
  1. These files will be in the `path/to/pepr-data/project_id/ref_pilon` directory, `project_id` and `ref` are the values in the YAML config file.
  2. Additional 
    1. `path/to/pepr-data/project_id/ref_mapping` - mapping results files
    2. `path/to/pepr-data/project_id/ref` - reference genome sequences and index files
    3. `path/to/pepr-data/project_id/fastq` - sequence data
  5. Next step after the pipeline completes
    1. Check the `path/to/pepr-data/project_id/ref_pilon/ref_miseq.changes` file to see what modifications were made to the reference genome
        1. If no changes move onto the characterization pipeline
        2. If changes re-run evaluation pipeline with `path/to/pepr-data/project_id/ref_pilon/ref_miseq.fasta` as the reference
            1. will need to create a new YAML file
            2. copy `path/to/pepr-data/project_id/ref_pilon/ref_miseq.fasta` to the `path/to/pepr-data/` directory along with the new yaml file
            3. re-run `evaluation` pipeline
    2. If the only changes made undo the changes from the previous run move onto `characterization` pipeline, otherwise continue to re-run until no new changes are made (should only need to run 2-3 times). 

## `characterization`
1. Pipeline steps
  1. download fastq data from the database
  2. copies ref genome to the `ref` directory in the project_id directory and indexes the genome
  3. maps the miseq data to the reference genome
  4. calculates qc metrics for datasets, e.g. read count, length, coverage, ect.
  5. base level purity analysis
  6. homogeneity analysis
2. Pipeline command
    
    nohup docker run -v path/to/pepr:/pepr -v path/to/pepr-data:/pepr-data natedolson/pepr python /pepr/pepr.py -c pipeline_config.yaml -p characterization --send_status sinch_config.yaml --send_number +1########## > run_specific_name.log &

3. Output
  1. Primary
    1. qc - `_stat` and `depth` files in `/media/micro_rm_4TB/pepr-data/project_id/ref_qc_metrics` directory. Directory `project_id` and `ref` are the values in the YAML config file.
    2. `tsv` files in `path/to/pepr-data/project_id/ref_consensus` directory
    3. `snp` and `indel` files in `path/to/pepr-data/project_id/ref_homogeneity`
  2. Additional 
    1. `path/to/pepr-data/project_id/ref_mapping` - mapping results files
    2. `path/to/pepr-data/project_id/ref` - reference genome sequences and index files
    3. `path/to/pepr-data/project_id/fastq` - sequence data
  5. Next step after the pipeline completes
    1. Check for empty files can use ls -lh to check for `bam`, `depth`, and `tsv` files with size 0.
        1. bam files in `path/to/pepr-data/project_id/ref_mapping` 
            1. if empty bam files check size of sam file in `/path/to/pepr-data/project_id/ref_mapping/tmp` 
        1. if both sam and sam files are empty remove the bam, sam files along with the bam index file (`bai`) and rerun the characterization pipeline
        2. if only the bam file is empty remove the bam and bam index file and re-run the pipeline
    2. If `depth` or `tsv` files are empty and bam file for that accession is not, check the appropriate log files.

## genomic_purity

  1. Estimated run time ~2-7 days depending on size of datasets and similarity of genome to sequences in the database
  2. Pipeline steps
      1. download fastq data
      2. quality trimming of fastq files
      3. mapping reads to micro_rm_patho_db
      4. running pathoscope identification module
  3. Pipeline command - run from within the docker-pathoscope container, see notes on running docker containers
    1. Starting docker container
        docker run -it -v /path/to/pepr:/pepr -v /path/to/pepr-data:/pepr-data -v /path/to/patho_db:/patho_db natedolson/docker-pathoscope /bin/bash
    2. From within the container
        python /pepr/pepr.py -c pipeline_config.yaml -p genomic_purity --send_status sinch_config.yaml --send_number +1##########
  4. Output
    1. Primary
        1. `-sam-report.tsv` in `/media/micro_rm_4TB/pepr-data/project_id/ref_genomic_purity` directory
  5. Next step after pipeline completes
    1. use `ls -lh` to check for empty `-sam-report.tsv` files

# Running PEPR using nohup

  1. run the following command 
    
    nohup docker run -v /path/to/pepr:/pepr -v /path/to/pepr-data:/pepr-data natedolson/pepr python /pepr/pepr.py -c pipeline_config.yaml -p pipeline_name --send_status sinch_config.yaml --send_number +1########## > run_specific_name.log &

    1. replace `pipeline_config.yaml` with the name of the config file used for the pipeline run
    2. include mobile number to receive text status update messages
  2. Should receive a text shortly after running the command saying that the pipeline has started then another one after the run has completed.
  3. Keep the ssh connection open until you receive a text message status that the pipeline has started, if you do not receive one in ~1-2 mins
    1. check the log file - `less run_specific_name.log`
        1. if empty - most likely an error with sending the text message
            1. use `top` to see if any pipeline commands are running e.g. bwa, tmap, samtools, picard, ect.
            2. If the pipeline is running can either leave it running and check back later to see if the pipeline completed, with `tail run_specific_name.log`
        2. if not - potential premature termination, or error with text message
            1. check file for indications of premature termination - errors messages, ect.
            2. if no signs of errors
                1. use top similar to above to check is pipeline is still running
                2. if programs are running follow instructions for when the file is empty
                3. To receive text messages, will need to restart the pipeline
                    1. run `docker ps -a`, to get a list of running containers
                    2. record the name of the most recently started container running the pepr pipeline
                    3. force remove container `docker rm -f container_name`
                    4. Check command run the pipeline for errors in the send message function
       
# Notes on running docker containers

  1. to start up a container's command line `docker run -it -v /full_path_to_local_directory:/full_path_mount_directory container-name /bin/bash`

  2. After the pipeline has started and is running okay, simply close the terminal, do not exit out of the container as it will terminate the run. Breaking the ssh connection without exiting the container will keep the container running.
 
  3. To check on the status of the run use top to see if any of the programs executed by the pipeline are still running. 
    1. Programs that you would expect to see foreach pipeline
        1. `evaluation` - bwa, java, and samtools
        2. `characterization` - tmap, bwa, java, samtools, and varscan
        3. `genomic_purity` - python, perl, grep, gzip, and bowtie

# Disclaimer
Certain commercial equipment, instruments, or materials are identified here only to specify the experimental procedure adequately. Such identification is not intended to imply recommendation or endorsement by NIST, nor is it intended to imply that the materials or equipment identified are necessarily the best available for the purpose.
