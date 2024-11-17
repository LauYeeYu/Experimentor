import tqdm
import sys

from .cli import redirect_stream_for_tqdm
from .configure_production import ConfigureIterable, ExperimentorError
from .const import DEFAULT_MAX_TRIALS
from .experiment_runner import BaseExperimentRunner
from .track_log import TrackLog


def run_experiments(config: list, func: BaseExperimentRunner, log_dir: str | None,
                    max_trial=DEFAULT_MAX_TRIALS, skip_exist=False):
    """
    Run experiments with the given configuration and function.
    :param config: A list of dictionaries.
    :param func:
    :param log_dir: The directory to store logs. If None, no log will be stored.
    :param max_trial: The maximum number of trials for each configuration.
    :param skip_exist: Skip the configuration if the log file already exists.
    """
    Experimentor(config, func, log_dir).run_experiments(max_trial, skip_exist)


class Experimentor:
    """A class to run a series of experiments.

    To construct an Experimentor object, you need to provide a list of
    configurations, a runner class (derived from
    `experimentor.BaseExperimentRunner`) to run the experiment, and
    optionally a log directory. The configuration is a list of dictionaries.
    Each entry in the list means one parameter set.

    If you don't want to store logs, you can set the `log_dir` to None.
    """
    def __init__(self, config: list, runner: BaseExperimentRunner, log_dir: str | None):
        """
        Run experiments with the given configuration and function.
        :param config: A list of dictionaries.
        :param runner: A class to run the experiment. Should be inherited from BaseExperimentRunner.
        :param log_dir: The directory to store logs. If None, no log will be stored.
        """
        self.config = config
        self.runner = runner
        if log_dir is None:
            self.track_log = None
        else:
            self.track_log = TrackLog(log_dir)

    def run_experiments(self, max_trial=DEFAULT_MAX_TRIALS, skip_exist=False):
        total = count(self.config)
        with tqdm.tqdm(total=total, position=0, leave=True,
                       file=sys.stdout, dynamic_ncols=True) as pbar:
            with redirect_stream_for_tqdm():
                try:
                    for title, conf in ConfigureIterable(self.config):
                        successful = False
                        for trial in range(max_trial):
                            try:
                                self.run_single_experiment(title, conf,
                                                           skip_exist)
                                successful = True
                                break
                            except KeyboardInterrupt:
                                raise
                            except Exception as e:
                                print(e)
                                print(f"Failed trial {trial + 1} for config {conf}")
                        if not successful:
                            raise ValueError("Failed to run the function")
                        pbar.update()
                except ExperimentorError as e:
                    print(e)
                    raise ValueError("Experimentor error")
                except KeyboardInterrupt:
                    print("Interrupted")
                    raise

    def run_single_experiment(self, title, config, skip_exist):
        # Create log file
        file = None
        if self.track_log is not None:
            try:
                file = self.track_log.add_log_file(title, skip_exist)
                if file is None:  # No need to run the experiment
                    return
            except Exception:
                print("Failed to create log file")
                raise

        # Run the function
        self.runner.run_experiment(title, config, file)
        return True


def count(config) -> int:
    if len(config) == 0:
        return 0
    num = len(config[0])
    for i in range(1, len(config)):
        num *= len(config[i])
    return num
