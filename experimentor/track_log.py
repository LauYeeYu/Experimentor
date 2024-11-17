import os
import datetime

class TrackLog:
    """Track the log files for experiments

    On initialization, it will create a lock file to make sure that only one
    process is using the directory. The lock file will be removed when the
    object is deleted.

    When running experiments, a log file will be created for each experiment.
    The file name is the current time in the format of '%Y_%m_%d_%H_%M_%S.log'
    in UTC time to avoid conflicts. The log file will be stored in a
    subdirectory named after the experiment title.

    You may inherit this class to change the behavior, but please be careful
    because improperly changing the behavior might lead to some unexpected
    results.
    """
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.init_dir()

    def __del__(self):
        lock_file = os.path.join(self.root_dir, 'lock')
        os.remove(lock_file)

    def init_dir(self):
        os.makedirs(self.root_dir, exist_ok=True)

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


def get_latest_track_log_file(root_dir: str, name: str) -> str | None:
    subdir = os.path.join(root_dir, name)
    if not os.path.exists(subdir):
        return None
    files = os.listdir(subdir)
    if not files:
        return None
    files.sort()
    return os.path.join(subdir, files[-1])
