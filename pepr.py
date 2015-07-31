from pepr_pipeline import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument('-c', '--config', action='store', metavar='STR',
                          help='yaml pipeline parameters file')
parser.add_argument('-p', '--pipe', action='store', metavar='STR',
                          help='define which pipeline to run')
args = parser.parse_args()

if args.verbose:
    print "verbosity turned on"

if args.config:
    if args.pipe:
        print "Running '%s' pipeline." % args.pipe
        if args.pipe == "evaluation":
            run_genome_eval_pipeline(args.config)
        # elif args.pipe == "re-evaluation":
        #     run_genome_eval_pipeline(args.config, pipe = "skip_get_fastq")
        elif args.pipe == "characterization":
            run_genome_characterization_pipeline(args.config)
        elif args.pipe == "genomic_purity":
            run_genomic_purity_pipeline(args.config)
        else:
            print "Define which pipeline to run using -p"
    else:
        print "Define which pipeline to run using -p"    
else:
    print "Pipeline requires config file identified with -c"