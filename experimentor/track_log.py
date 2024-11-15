import os
import datetime

class TrackLog:
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
