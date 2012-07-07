import os
import shutil
import sys
import subprocess

class SimplePybotWrapper(object):

    ROBOT_DIR = os.path.dirname(__file__).replace("\\", "/")

    DIRECTORIES = {
        'lib': 'lib',
        'reports': 'reports',
        'resources': 'resources',
        'testcases': 'testcases',
    }

    ROBOT_RUNNER = "pybot"
    TOP_SUITE_NAME = "Robot Tests"

    INCLUDE_TAGS = []
    EXCLUDE_TAGS = ["ignore"]

    CLEANABLE = ["{}/reports".format(ROBOT_DIR)]

    HELP = """
    cpybot.py is a simple wrapper script for pybot(.bat). Tests do not need to be specified when using this script
    Run 'pybot -h' to see available arguments

    cpybot.py will intercept certain arguments
        -h/--help   Shows this help message
        --clean     Cleans out generated directories specified in CLEANABLE in the script
        --debug     Prints the final command for pybot to console instead of running it
        --test      Change the tests to run (defaults to the value specified in DIRECTORIES['testcases'])
    """[1:-1]

    def remove_command_from_arguments(self, arguments):
        arguments.pop(0)

    def handle_test_argument(self, arguments):
        if '--test' in arguments:
            index = arguments.index('--test')
            del arguments[index]
            self.DIRECTORIES['testcases'] = arguments[index]
            del arguments[index]

    def get_static_arguments(self):
        return [
            "--variable", "SUITE_ROBOT_TEST_DIR:{}".format(self.ROBOT_DIR),
            "--variable", "SUITE_TESTCASES:{}/{}".format(self.ROBOT_DIR, self.DIRECTORIES['testcases']),
            "--variable", "SUITE_RESOURCES:{}/{}".format(self.ROBOT_DIR, self.DIRECTORIES['resources']),
            "--pythonpath", "{}/{}".format(self.ROBOT_DIR, self.DIRECTORIES['lib']),
            "--outputdir", "{}/{}".format(self.ROBOT_DIR, self.DIRECTORIES['reports']),
            "--name", self.TOP_SUITE_NAME,
        ]

    def get_tag_arguments(self):
        tags = []
        for tag in self.INCLUDE_TAGS:
            tags += ["-i", tag]
        for tag in self.EXCLUDE_TAGS:
            tags += ["-e", tag]
        return tags

    def run_with_arguments(self, arguments):
        arguments.insert(0, self.ROBOT_RUNNER)
        arguments.append(self.DIRECTORIES['testcases'])
        if "--debug" in arguments:
            print "Command:\n{}".format(' '.join(arguments))
        else:
            subprocess.call(arguments, shell=True)

    def clean_targets(self):
        print "Cleaning target and report directories"
        for target in self.CLEANABLE:
            if os.path.exists(target):
                shutil.rmtree(target)

    def run(self, *arguments):
        if '-h' in arguments or '--help' in arguments:
            print self.HELP
        elif '--clean' in arguments:
            self.clean_targets()
        else:
            arguments = list(arguments)
            self.remove_command_from_arguments(arguments)
            self.handle_test_argument(arguments)
            arguments += self.get_static_arguments()
            arguments += self.get_tag_arguments()
            self.run_with_arguments(arguments)

if __name__ == '__main__':
    SimplePybotWrapper().run(*sys.argv)