import tqdm
import sys

from .cli import tqdm_file, redirect_stream_for_tqdm
from .configure_production import ConfigureIterable, ExperimentorError
from .const import DEFAULT_MAX_TRIALS
from .experiment_runner import BaseExperimentRunner
from .track_log import TrackLog


def run_experiments(config: list, runner: BaseExperimentRunner,
                    log_dir: str | None, max_trial=DEFAULT_MAX_TRIALS,
                    skip_exist=False, track_log: TrackLog | None = None):
    """Run experiments with the given configuration and function.

    The function will initialize an `Experimentor` object and run the experiments.

    :param config: A list of dictionaries.
    :param runner: A class to run the experiment. Should be inherited from
        `experimentor.BaseExperimentRunner`.
    :param log_dir: The directory to store logs. If None, no log will be
        stored.
    :param max_trial: The maximum number of trials for each configuration.
    :param skip_exist: Skip the configuration if the log file already exists.
    :param track_log: Specify the track log object. If None and `log_dir` is
        not None, a new track log object will be created. If None and `log_dir`
        is None, no track log will be created.
    """
    Experimentor(
        config, runner, log_dir, track_log
    ).run_experiments(max_trial, skip_exist)


class Experimentor:
    """A class to run a series of experiments.

    To construct an Experimentor object, you need to provide a list of
    configurations, a runner class (derived from
    `experimentor.BaseExperimentRunner`) to run the experiment, and
    optionally a log directory. The configuration is a list of dictionaries.
    Each entry in the list means one parameter set.

    If you don't want to store logs, you can set the `log_dir` to None.
    """
    def __init__(self, config: list, runner: BaseExperimentRunner,
                 log_dir: str | None, track_log: TrackLog | None = None):
        """Init the Experimentor class with the given configuration
        and function.

        :param config: A list of dictionaries.
        :param runner: A class to run the experiment. Should be inherited
            from BaseExperimentRunner.
        :param log_dir: The directory to store logs. If None, no log will
            be stored.
        :param track_log: Specify the track log object. If None and `log_dir`
            is not None, a new track log object will be created. If None and
            `log_dir` is None, no track log will be created.
        """
        self.config = config
        self.runner = runner
        self.track_log = track_log
        if self.track_log is None:
            if log_dir is not None:
                self.track_log = TrackLog(log_dir)

    def run_experiments(self, max_trial=DEFAULT_MAX_TRIALS, skip_exist=False):
        """Run experiments with the given configuration and function.

        This method will run the experiments with the given configuration and
        function. The method will iterate through all the configurations and
        run the function with `max_trial` trials for each configuration. If
        `skip_exist` is True, the method will skip the configuration if the
        log file already exists. This is useful when you want to resume the
        experiment if that is interrupted or failed.

        :param max_trial: The maximum number of trials for each
            configuration.
        :param skip_exist: Whether to skip the configuration if the
            log file already exists.
        """
        total = count(self.config)
        disable_tqdm = False
        progress_bar_file = tqdm_file()
        if progress_bar_file is None:
            progress_bar_file = sys.stdout
            disable_tqdm = True
        with tqdm.tqdm(total=total, leave=True, disable=disable_tqdm,
                       file=progress_bar_file, dynamic_ncols=True) as pbar:
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
                                print(f"Failed trial {trial + 1} for config "
                                      f"{conf}")
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
        """Run a single experiment with the given configuration.

        :param title: The title of the experiment.
        :param config: The configuration of the experiment.
        :param skip_exist: Whether to skip the configuration if the log
            file already exists.
        """
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
    """Count the number of configurations.

    :param config: The configuration list.
    :return: The number of configurations.
    """
    if len(config) == 0:
        return 0
    num = len(config[0])
    for i in range(1, len(config)):
        num *= len(config[i])
    return num
