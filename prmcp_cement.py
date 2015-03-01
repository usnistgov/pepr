from cement.core import backend, foundation, controller, handler
from prmcp_pipeline import *

# define an application base controller
class MyAppBaseController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = "My Application does amazing things!"

        # config_defaults = dict(
        #     foo='bar',
        #     some_other_option='my default value',
        #     )

        arguments = [
            (['-L', '--Lpipeline'], dict(dest='blank', action='store', help='defining pipeline to run')),
            (['-C'], dict(action='store_true', help='the big C option'))
            ]
        # need to workout defining pipeline to run ...
    @controller.expose(hide=True, aliases=['run'])
    def default(self):
        if self.app.pargs.config:
            self.app.log.info("Processing config file '%s'." % \
                         self.app.pargs.config)
            if self.app.pargs.pipe:
                self.app.log.info("Running '%s' pipeline." % \
                         self.app.pargs.pipe)
                if "%s" % self.app.pargs.pipe == "evaluation":
                    run_genome_eval_pipeline(self.app.pargs.config)
                elif "%s" % self.app.pargs.pipe == "re-evaluation":
                    run_genome_eval_pipeline(self.app.pargs.config, pipe = "skip_get_fastq")
                elif "%s" % self.app.pargs.pipe == "characterization":
                    run_genome_characterization_pipeline(self.app.pargs.config)
                else:
                    self.app.log.info("Define which pipeline to run using -P")
            else:
                self.app.log.info("Define which pipeline to run using -P")     
        else:
            self.app.log.info("Pipeline requires config file identified with -c")
            
"""
    @controller.expose(help="this command does relatively nothing useful.")
    def command1(self):
        self.app.log.info("Inside base.command1 function.")

    @controller.expose(aliases=['cmd2'], help="more of nothing.")
    def command2(self):
        self.app.log.info("Inside base.command2 function.")

# define a second controller
class MySecondController(controller.CementBaseController):
    class Meta:
        label = 'secondary'
        stacked_on = 'base'

    @controller.expose(help='this is some command', aliases=['some-cmd'])
    def some_other_command(self):
        pass
"""

class MyApp(foundation.CementApp):
    class Meta:
        label = 'helloworld'
        base_controller = MyAppBaseController

# create the app
app = MyApp()

# Register any handlers that aren't passed directly to CementApp
# handler.register(MySecondController)

try:
    # setup the application
    app.setup()

    # add arguments to the parser
    app.args.add_argument('-c', '--config', action='store', metavar='STR',
                          help='yaml pipeline parameters file')
    app.args.add_argument('-P', '--pipe', action='store', metavar='STR',
                          help='define which pipeline to run')

    # run the application
    app.run()
finally:
    # close the app
    app.close()