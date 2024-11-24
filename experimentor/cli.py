"""This module improves the progress bar display in the CLI.

When the stdout is a tty, the progress bar will be displayed in the stdout.
If only the stderr is a tty, the progress bar will be displayed in the stderr.
If neither of them is a tty, the progress bar will be disabled.
This check is done in the `tqdm_file` function.

The `CliFile` class is a wrapper for the stdout and stderr if any of them is
a tty. It will redirect all write calls to the `tqdm.tqdm.write` function.
This makes the progress bar display correctly in the CLI.
"""

import tqdm
import contextlib
import sys


def tqdm_file() -> type(sys.stdout) | None:
    """Get the file to display the progress bar.

    :return: If stdout is a tty, return stdout. If stdout is not but stderr
        is, return stderr. Otherwise, return None.
    """
    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
        return sys.stdout
    elif hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
        return sys.stderr
    else:
        return None

class CliFile(object):
    """A class to redirect the write calls to `tqdm.tqdm.write`.
    """
    file = None
    def __init__(self, file):
        self.file = file

    def flush(self):
        self.file.flush()

    def write(self, x):
        if len(x.rstrip()) > 0: # To avoid unintended empty lines
            tqdm.tqdm.write(x, file=self.file)


@contextlib.contextmanager
def redirect_stream_for_tqdm():
    """Redirect stdout and stderr to `CliFile` if they are tty.
    This makes the progress bar display correctly in the CLI.

    The yield statement is used to separate the setup and teardown code.

    Use it like this:
    ```
    with redirect_stream_for_tqdm():
        # Your code here
        ...
    ```
    """
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
        sys.stdout = CliFile(sys.stdout)
    if hasattr(sys.stdout, 'isatty') and sys.stderr.isatty():
        sys.stderr = CliFile(sys.stderr)
    try:
        yield
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
