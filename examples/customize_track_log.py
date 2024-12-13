"""This is a simple example to show how to customize the track log.

We provide a base class `BaseTrackLog` for you to customize the track log.
To be specific, you need to implement the `add_log_file` method to add a log
file for the experiment. The method should take two parameters:
- name: The name of the experiment.
- skip_if_exists: Skip creating the log file if the directory already has files.

You may return str or None. Returning None will signal the caller that this
experiment should be skipped. Otherwise, the return value will be pass to the
runner (inherit from `experimentor.BaseExperimentRunner`) to run the experiment
as the third parameter of the runner's `run_experiment` method.

In this example, we provide a track log object that will create the log file
with the hierarchical directory structure. For example, if the experiment title
is 'a_b_c', the log file will be stored in the directory 'a/b/c'.
"""

import experimentor
import os

class HierarchicalTrackLog(experimentor.BaseTrackLog):
    def __init__(self, log_dir: str):
        super().__init__()
        self.log_dir = log_dir

    def add_log_file(self, name: str, skip_if_exists: bool) -> str | None:
        # Construct the path
        path = os.path.join(self.log_dir, *name.split('_'))

        # Skip if the directory already has files
        if skip_if_exists and os.path.exists(path):
            return None

        # Create the directory if it doesn't exist
        os.makedirs(path, exist_ok=True)

        # Construct the log file path
        log_file = os.path.join(path, 'log.txt')

        return log_file

# Create the track log object
track_log = HierarchicalTrackLog('log')

# Run the experiments
configuration = [
    { 'a': 1, 'b': 2 },
    { 'c': 3, 'd': 4 },
]


if __name__ == '__main__':
    experimentor.run_experiments(configuration,
                                 experimentor.SimpleCommandRunner('echo'),
                                 None, track_log=track_log)

    # Print the directory structure
    print(f"Under 'log' dir: {os.listdir('log')}")
    print(f"Under 'log/a' dir: {os.listdir('log/a')}")
