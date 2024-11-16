import tqdm
import contextlib
import sys

"""
Override the stdout to make it look better with progress bar.
"""

class CliFile(object):
    file = None
    def __init__(self, file):
        self.file = file

    def flush(self):
        self.file.flush()

    def write(self, x):
        if len(x.rstrip()) > 0:
            tqdm.tqdm.write(x, file=self.file)


@contextlib.contextmanager
def redirect_stream_for_tqdm():
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = CliFile(sys.stdout)
    sys.stderr = CliFile(sys.stderr)
    yield
    sys.stdout = old_stdout
    sys.stderr = old_stderr
