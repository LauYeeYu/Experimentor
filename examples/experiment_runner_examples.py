"""This is an example of how to customize the experiment runner.

You can customize the experiment runner by inheriting the
`experimentor.BaseExperimentRunner`, and then implement the `run_experiment`
method. The `run_experiment` method should take three parameters:

- title: The title of the experiment. The title is used to distinguish
  different experiments and is therefore unique.
- config: The configuration of the experiment. The configuration is a
  dictionary where the key is the name of the parameter, and the value
  is the value of the parameter.
- file: The file to store the log. If None, no output will be stored.

This file will show you three examples of how to customize the experiment
runner.
"""

import experimentor
import shutil
import time


print("""Example 1: The follwing class `MaxTrialDemo` will throw an exception
for the first two trials, and then finish the experiment. Since the default
maximum number of trials is 3, every experiment will be finished in the third
trial.
""")
input("""Press Enter to run the demo...""")


class MaxTrialDemo(experimentor.BaseExperimentRunner):
    def __init__(self):
        super().__init__()
        self.trials = 0

    def run_experiment(self, title: str, config: dict, file: str | None):
        time.sleep(0.2)

        if self.trials < 2:
            self.trials += 1
            raise Exception('An exception is thrown')
        else:
            self.trials = 0
            print('Experiment finished')


if __name__ != '__main__':
    exit()

configuration = [
    { 'a': 1, 'b': 2 },
    { 'c': 3, 'd': 4 },
]
experimentor.run_experiments(configuration, MaxTrialDemo(), None)

print()
print()

shutil.rmtree('log', ignore_errors=True)

print("""Example 2: With the same experiment runner class, if we set the
maximum number of trials to 2, the experiment will fail to finish.
In this case, there's an exception thrown in the
`experimentor.run_experiments` function.
""")
input("""Press Enter to run the demo...""")


configuration = [
    { 'a': 1, 'b': 2 },
    { 'c': 3, 'd': 4 },
    { 'e': 5, 'f': 6 },
]

try:
    experimentor.run_experiments(configuration, MaxTrialDemo(), 'log', 2)
except Exception as e:
    print(f'An exception is thrown: {e}')

print("""Failed to finish the experiment is a very common case. It is still
very common to stop midway. To resume the experiment, you can set the
`skip_if_exists` parameter to True. The experiment will skip the configuration
if the log file already exists.

The following example will show you how to resume the experiment.
It will run the same configuration as the previous example, but with maximum
number of trials set to 3. The experiment will be resumed and finished.
The full command is:

experimentor.run_experiments(configuration, MaxTrialDemo(), 'log',
                             skip_if_exists=True)
""")

input("Press Enter to run the demo...")

experimentor.run_experiments(configuration, MaxTrialDemo(), 'log',
                             skip_if_exists=True)




