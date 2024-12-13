"""This is a simple example to show how our track log work,

This script will run three experiments, each with a different configuration.
The configuration is a list of dictionaries. Each entry in the list means
one parameter set. In this example, there are three parameter sets. Each entry
in the parameter set is a key-value pair. The key is the name of the parameter,
and the value is the value of the parameter. The experiment has the title
of the parameter value.

In the experiment, the stdout will be redirected to the log file. The log file
will be named after the current time in the format of '%Y_%m_%d_%H_%M_%S.log'
in UTC time to avoid conflicts. The log file will be stored in a subdirectory
named after the experiment title.
"""

import experimentor

configuration = [
    { 'a': 1, 'b': 2 },
    { 'c': 3, 'd': 4 },
    { 'e': 5, 'f': 6 }
]

if __name__ == '__main__':
    experimentor.run_experiments(configuration, experimentor.SimpleCommandRunner("echo"), 'log', 1)
    log_file = experimentor.get_latest_track_log_file('log', 'a_c_e')
    print(f'The log files for experiment \'a_c_e\' are stored at \'{log_file}\'')
    print(f'The content of the log file is:')
    with experimentor.open_latest_track_log_file('log', 'a_c_e') as f:
        print(f.read())
