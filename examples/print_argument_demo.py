"""This is a simple example of how to use the experimentor module to run
a series of experiments.

This script will run eight experiments, each with a different configuration.
The configuration is a list of dictionaries. Each entry in the list means
one parameter set. In this example, there are three parameter sets. Each entry
in the parameter set is a key-value pair. The key is the name of the parameter,
and the value is the value of the parameter. The experiment has the title
of the parameter value.

In this example, the experiment runner is a simple class that prints the
title, configuration, and file name of the experiment. The log function
is disabled, so no log will be stored.
"""

import experimentor


class EchoExperimentRunner(experimentor.BaseExperimentRunner):
    def __init__(self):
        super().__init__()

    def run_experiment(self, title: str, config: dict, file: str | None):
        print(f"Title: {title}")
        print(f"Config: {config}")
        print(f"File: {file}")
        import time
        time.sleep(1)


configuration = [
    { 'a': 1, 'b': 2 },
    { 'c': 3, 'd': 4 },
    { 'e': 5, 'f': 6 }
]

if __name__ == '__main__':
    experimentor.run_experiments(configuration, EchoExperimentRunner(), None, 1)
