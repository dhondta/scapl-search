# -*- coding: UTF-8 -*-
import abc
import argparse
import logging
import os
import types
try:
    import coloredlogs
    colored_logs_present = True
except:
    print("(Install 'coloredlogs' for colored logging)")
    colored_logs_present = False


class TaskRunner(object):
    def __init__(self, prog, plugin):
        os.chdir(os.path.dirname(__file__))
        # parse input arguments
        parser = argparse.ArgumentParser(prog=__file__,
                                         description="Task runner for SCAPL plugin {}.".format(plugin),
                                         formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument("-c", "--config", dest="config",
                            help="task configuration dictionary")
        parser.add_argument("--keywords", help="keywords to be scraped")
        parser.add_argument("--task", help="task identifier for logging purpose")
        parser.add_argument("-n", dest="n", type=int, default=0, help="number of results to return [default: 0 (=all)]")
        parser.add_argument("-v", dest="verbose", action="count", default=0,
                            help="verbose level [default: 0 (critical)]")
        args = parser.parse_args()
        args.config = eval(args.config)
        # configure logging and get the root logger
        args.verbose = args.config['LOG_LEVEL_MAPPING'][min(max(args.config['LOG_LEVEL_MAPPING'].keys()), args.verbose)]
        logging.basicConfig(format='%(name)s - %(asctime)s [%(levelname)s] %(message)s', level=args.verbose)
        self.logger = logging.getLogger(args.task)
        if colored_logs_present:
            coloredlogs.install(args.verbose)
        # set arguments as attributes
        for arg in vars(args):
            setattr(self, arg, getattr(args, arg))

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        """ Run the task code, printing the result to stdout for piping the result to the parent task
        :return: None
        """

    @staticmethod
    def bind(prog, plugin, f):
        def _bind(*args, **kwargs):
            runner = TaskRunner(prog, plugin)
            runner.run = types.MethodType(f, runner, TaskRunner)
            return runner.run(*args, **kwargs)
        return _bind
