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
            (['-A', '--All'], dict(dest='foo', action='store', help='the notorious foo option')),
            (['-C'], dict(action='store_true', help='the big C option'))
            ]

    @controller.expose(hide=True, aliases=['run'])
    def default(self):
        self.app.log.info('Executing Genome Evaluation')
        if self.app.pargs.params:
            self.app.log.info("Processing parameter file '%s'." % \
                         self.app.pargs.params)
            run_genome_eval_pipeline(self.app.pargs.params)
            
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
    app.args.add_argument('-p', '--params', action='store', metavar='STR',
                          help='yaml pipeline parameters file')

    # run the application
    app.run()
finally:
    # close the app
    app.close()