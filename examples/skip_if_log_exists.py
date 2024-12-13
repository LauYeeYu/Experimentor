"""This is a simple example of how to use the experimentor module to skip
the experiment if the log file already exists.

Our experiment runner can be easily set to skip the experiment if the log file
already exists. This is useful when you want to resume the experiment.
However, you must bear in mind that if you have previously run the experiment
but want to change the configuration, you should move the previous log files
to another directory (or delete them if you don't need them anymore).
"""

import experimentor
import time

class MaxTrialDemo(experimentor.BaseExperimentRunner):
    def __init__(self):
        super().__init__()
        self.next_fail = False

    def run_experiment(self, title: str, config: dict, file: str | None):
        time.sleep(0.2)

        if self.next_fail:
            self.next_fail = False
            raise Exception('An exception is thrown')
        else:
            self.next_fail = True
            print('Experiment finished')


configuration = [
    { 'a': 1, 'b': 2 },
    { 'c': 3, 'd': 4 },
    { 'e': 5, 'f': 6 }
]


if __name__ == '__main__':
    print("First, we will run the experiment which will fail for the second "
          "config.")
    try:
        experimentor.run_experiments(configuration, MaxTrialDemo(), 'log', 1)
    except Exception as e:
        print(f'An exception is thrown: {e}')

    print("Now, we will run the experiment again with the same configuration, "
          "but with the `skip_if_exists` parameter set to True.")
    experimentor.run_experiments(configuration,
                                 experimentor.SimpleCommandRunner("echo"),
                                 'log', 1, skip_if_exists=True)
    print("The first experiment is skipped because the log file already exists.")
