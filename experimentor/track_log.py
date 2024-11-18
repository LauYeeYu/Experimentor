import os
import datetime

class TrackLog:
    """Track the log files for experiments

    On initialization, it will create a lock file to make sure that only one
    process is using the directory. The lock file will be removed when the
    object is deleted. You can disable the lock by setting the disable_lock
    parameter to True when initializing the object. In this case, there
    can be multiple processes using the directory at the same time.

    When running experiments, a log file will be created for each experiment.
    The file name is the current time in the format of '%Y_%m_%d_%H_%M_%S.log'
    in UTC time to avoid conflicts. The log file will be stored in a
    subdirectory named after the experiment title.

    You may inherit this class to change the behavior, but please be careful
    because improperly changing the behavior might lead to some unexpected
    results.
    """
    def __init__(self, root_dir: str, disable_lock=False):
        """
        Initialize the TrackLog object.
        :param root_dir: The root directory to store the log files.
        :param disable_lock: Whether to disable the lock file used to
            guarantee that only one process is using the directory.
        """
        self.root_dir = root_dir
        self.disable_lock = disable_lock
        self.init_dir()

    def __del__(self):
        if not self.disable_lock:
            lock_file = os.path.join(self.root_dir, 'lock')
            os.remove(lock_file)

    def init_dir(self):
        os.makedirs(self.root_dir, exist_ok=True)
        if self.disable_lock:
            return

        # Make sure there is no other process using the directory
        lock_file = os.path.join(self.root_dir, 'lock')
        try:
            os.open(lock_file, os.O_CREAT | os.O_EXCL)
        except FileExistsError:
            raise ValueError("Another process is using the directory")

    def add_log_file(self, name: str, skip_exist: bool) -> str | None:
        subdir = os.path.join(self.root_dir, name)
        os.makedirs(subdir, exist_ok=True)
        if skip_exist and len(os.listdir(subdir)) > 0:
            return None
        file_name = datetime.datetime.now(datetime.UTC).strftime('%Y_%m_%d_%H_%M_%S') + '.log'
        file_path = os.path.join(subdir, file_name)
        with open(file_path, 'w'):
            pass
        return file_path


def has_track_log(root_dir: str, name: str) -> bool:
    """
    Check if there's a log file for the experiment with the given name.
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
    """
    Get the latest log file for the experiment with the given name.
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
