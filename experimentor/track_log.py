import os
import datetime

class BaseTrackLog:
    """Base class for tracking log files for experiments.

    You can inherit this class to change the behaviour. The class must have
    a method called `add_log_file` to add a log file for the experiment.

    In specific, the method should take two parameters:
    - name: The name of the experiment.
    - skip_if_exists: Skip creating the log file if the directory already
      has files.

    You may return str or None. Returning None will signal the caller that
    this experiment should be skipped. Otherwise, the return value will be
    pass to the runner (inherit from `experimentor.BaseExperimentRunner`)
    to run the experiment as the third parameter of the runner's
    `run_experiment` method.
    """

    def add_log_file(self, name: str, skip_if_exists: bool) -> str | None:
        """Add a log file for the experiment with the given name.

        This function is supposed to create a unique log file for the
        experiment. But you can change the behaviour to fit your needs. But
        please be aware that the return value will affect the internal
        behaviour. To be specific, if the return value is None, the experiment
        will be skipped. Otherwise, the return value will be passed to the
        runner (inherit from `experimentor.BaseExperimentRunner`)
        to run the experiment as the third parameter of the runner's
        `run_experiment` method.

        If you change the behaviour significantly, you may also need to
        customize your experiment runner. See the documentation for
        `experimentor.BaseExperimentRunner` for more information.

        :param name: The name of the experiment.
        :param skip_if_exists: Skip creating the log file if the directory
            already has files.
        :return: If the log file is created, return the path to the file.
            Otherwise, return None (this indicates the experiment should be
            skipped).
        """
        raise NotImplementedError


class TrackLog(BaseTrackLog):
    """Track the log files for experiments.

    On initialization, it will create a lock file to make sure that only one
    process is using the directory. The lock file will be removed when the
    object is deleted. You can disable the lock by setting the disable_lock
    parameter to True when initializing the object. In this case, there
    can be multiple processes using the directory at the same time.

    When running experiments, a log file will be created for each experiment.
    The file name is the current time in the format of '%Y_%m_%d_%H_%M_%S.log'
    in UTC time to avoid conflicts. The log file will be stored in a
    subdirectory named after the experiment title.
    """

    def __init__(self, root_dir: str, disable_lock=False):
        """Initialize the TrackLog object.

        :param root_dir: The root directory to store the log files.
        :param disable_lock: Whether to disable the lock file used to
            guarantee that only one process is using the directory.
        """
        super().__init__()
        self.root_dir = root_dir
        self.disable_lock = disable_lock
        self.init_dir()

    def __del__(self):
        if not self.disable_lock:
            lock_file = os.path.join(self.root_dir, 'lock')
            os.remove(lock_file)

    def init_dir(self):
        """Initialize the directory.

        If the directory does not exist, it will be created. If the lock is
        enabled, it will create a lock file to make sure that only one process
        is using the directory.
        """
        os.makedirs(self.root_dir, exist_ok=True)
        if self.disable_lock:
            return

        # Make sure there is no other process using the directory
        lock_file = os.path.join(self.root_dir, 'lock')
        try:
            os.open(lock_file, os.O_CREAT | os.O_EXCL)
        except FileExistsError:
            raise ValueError("Another process is using the directory")

    def add_log_file(self, name: str, skip_if_exists: bool) -> str | None:
        """Add a log file for the experiment with the given name.

        This function will create a file named after the current time in the
        format of '%Y_%m_%d_%H_%M_%S.log' in UTC time. If the directory for
        the experiment does not exist, it will be created. If the directory
        already has files, the function will skip creating the log file if
        `skip_if_exists` is true.

        :param name: The name of the experiment.
        :param skip_if_exists: Skip creating the log file if the directory already
            has files.
        :return: If the log file is created, return the path to the file.
            Otherwise, return None.
        """
        subdir = os.path.join(self.root_dir, name)
        os.makedirs(subdir, exist_ok=True)
        if skip_if_exists and len(os.listdir(subdir)) > 0:
            return None
        file_name = f'{datetime.datetime.now(datetime.UTC).strftime('%Y_%m_%d_%H_%M_%S')}.log'
        file_path = os.path.join(subdir, file_name)
        with open(file_path, 'w'):
            pass
        return file_path

    def open_latest_log_file(self, name: str):
        """Open the latest log file for the experiment with the given name.

        :param name: The name of the experiment.
        :return: If there's no log file for the given experiment, raise a ValueError.
            Otherwise, return the file object.
        """
        return open_latest_track_log_file(self.root_dir, name)


def has_track_log(root_dir: str, name: str) -> bool:
    """Check if there's a log file for the experiment with the given name.

    :param root_dir: The root directory to store the log files.
    :param name: The name of the experiment.
    :return: Whether there's a log file for the given experiment.
    """
    subdir = os.path.join(root_dir, name)
    if not os.path.exists(root_dir):
        return False
    files = os.listdir(subdir)
    return len(files) > 0


def get_latest_track_log_file(root_dir: str, name: str) -> str | None:
    """Get the latest log file for the experiment with the given name.

    :param root_dir: The root directory to store the log files.
    :param name: The name of the experiment.
    :return: If there's no log file for the given experiment, return None.
        Otherwise, return the path to the latest log file.
    """
    subdir = os.path.join(root_dir, name)
    if not os.path.exists(subdir):
        return None
    files = os.listdir(subdir)
    if not files:
        return None
    files.sort()
    return os.path.join(subdir, files[-1])


def open_latest_track_log_file(root_dir: str, name: str):
    """Open the latest log file for the experiment with the given name.

    You can use this function to open the log file like this:

    with open_track_log_file('log', 'a_c_e'):
        # Do something
        ...

    :param root_dir: The root directory to store the log files.
    :param name: The name of the experiment.
    :return: If there's no log file for the given experiment, raise a ValueError.
        Otherwise, return the file object.
    """
    file = get_latest_track_log_file(root_dir, name)
    if file is None:
        raise ValueError("No log file for the experiment")
    return open(file, 'r')
