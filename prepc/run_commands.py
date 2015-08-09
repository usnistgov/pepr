import sys
import time
import os
import subprocess


def output_assert_error_msg(output_file_name, stderr_file_name):
    outfilenote = "Expected ouput file %s not present.\n" % output_file_name
    debugfilenote = "Check standard error file %s for debugging." % stderr_file_name
    return outfilenote + debugfilenote

# takes care of log and stder files
# runs assertions - for program and result file, generates error message


def run_command(function_name, log_dir, command, program, output, stdout_results=False):
    '''
    If string provided as standard out used as results
    '''

    assert function_name
    assert log_dir
    assert os.path.isdir(log_dir)
    assert command

    # checks for program
    assert program
    assert os.path.isfile(program), "Program %s is not in the exected location.\n" % program +
    "If using the pepr Docker rebuild repull the container.\n" +
    "If running locally move or link to expected location."
    assert output

    # stdout and stderr files
    if stdout_results:
        std_out_file_name = stdout_results
    else:
        stdout_file_name = log_dir + "/" + function_name + time.strftime("-%Y-%m-%d-%H-%M-%S.log")
        stdout_file = open(stdout_file_name, 'w')

        stderr_file_name = log_dir + "/" + function_name + time.strftime("-%Y-%m-%d-%H-%M-%S.stder")
        stderr_file = open(stderr_file_name, 'w')

    # run command
    # TODO - add command run timing and recording the executed command
    subprocess.call(command, stdout=stdout_file, stderr=stderr_file)
    log_file.close(); stderr_file.close()

    if type(output) is list:
    for i in output:
        msg = output_assert_error_msg(i, stderr_file_name)
        assert os.path.isfile(i), msg
    else:
        msg = output_assert_error_msg(output, stderr_file_name)
        assert os.path.isfile(output), msg
