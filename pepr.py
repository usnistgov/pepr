from pepr_pipeline import run_genome_eval_pipeline, \
    run_genome_characterization_pipeline, run_genomic_purity_pipeline
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', action='store', metavar='STR',
                          help='yaml pipeline parameters file')
parser.add_argument('-p', '--pipe', action='store', metavar='STR',
                          help='define which pipeline to run')
parser.add_argument('--send_status', action='store', metavar='STR',
                    help='yaml file with info for sending status message')
send_number_help = 'mobile number for status message, "+12345678901" format'
parser.add_argument('--send_number', action='store', metavar='STR',
                    help=send_number_help)


args = parser.parse_args()

if args.send_status:
    if not args.send_number:
        print "Mobile number argument '--send_number' required to send sms"
        sms_config = False
    else:
        sms_config = {"config_file": args.send_status,
                      "number": args.send_number}
else:
    sms_config = False

if args.config:
    if args.pipe:
        print "Running '%s' pipeline." % args.pipe
        if args.pipe == "evaluation":
            run_genome_eval_pipeline(args.config, sms_config)
        # elif args.pipe == "re-evaluation":
        #     run_genome_eval_pipeline(args.config, pipe = "skip_get_fastq")
        elif args.pipe == "characterization":
            run_genome_characterization_pipeline(args.config, sms_config)
        elif args.pipe == "genomic_purity":
            run_genomic_purity_pipeline(args.config, sms_config)
        else:
            print "Define which pipeline to run using -p"
    else:
        print "Define which pipeline to run using -p"
else:
    print "Pipeline requires config file identified with -c"
