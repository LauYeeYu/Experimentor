# Experimentor

Experimentor is a Python package that allows you to easily create and run
experiments. It is designed to be flexible and easy to use. It can iterate
over multiple sets of parameters.

Since in most cases, experiments are run in sequence, Experimentor does
not support parallel execution of experiments. However, it is possible to
run multiple instances of Experimentor in parallel.

## Installation

### Prerequisites

To install Experimentor, you need to install python build tools. On Ubuntu,
you can do this by running:

```bash
pip3 install build installer wheel
```

On arch-based systems, you can do this by running:

```bash
sudo pacman -S python-build python-installer python-wheel --needed
```

### Build and Install

Then you can install Experimentor using pip:

```bash
python -m build --wheel --no-isolation
sudo python -m installer dist/*.whl
```

## Features

- **Automatic iteration over multiple sets of parameters:** You don't need to
  manually set all possible combinations of parameters. Experimentor will
  automatically do this for you.
- **Customized maximum number of trials:** You can specify the maximum number
  of trials to run. The default value is 3.
- **Specify the log directory:** You can specify the directory to store the
  logs. The logs will be stored in the directory you specify.
- **No log file will be overwritten:** The log files are uniquely named after
  the UTC time they begin.
- **Disable logging:** You can also disable logging.
- **Customized logger:** You can create your own logger by simply inheriting
  the `BaseTrackLog` class and implementing the `add_log_file` method.
- **Customized runner:** You can create your own runner by inheriting the
  `Runner` class and implementing the `run_experiment` method.

## Usage

An easy demonstration of how to use Experimentor is shown below: (this is
part of the example in the `examples/track_log_demo.py` file)

```python
import experimentor

configuration = [
    { 'a': 1, 'b': 2 },
    { 'c': 3, 'd': 4 },
    { 'e': 5, 'f': 6 }
]

experimentor.run_experiments(configuration,
                             experimentor.SimpleCommandRunner("echo"),
                             'log', 1)
```

The configuration is a **list** of **dictionaries**. Each dictionary
represents a set of parameters for the experiment. The name of the
experiment contains the parameters in the dictionary. For example, the
`a_c_e` experiment will have the parameters `1`, `3`, and `5` respectively.

The `SimpleCommandRunner` is a simple runner that runs a command every time
an experiment is run. The command executed is a concatenation of the
string passed to the constructor (for here, `echo`) and the parameters
in the same order as they are in the configuration dictionary.

The third argument to `run_experiments` is the name of the log directory.
The logs will be stored in this directory. In specific, the log of each
experiment will be named after the time it begins. To make it easier to
manage logs, logs of the same experiment will be stored in the same
directory as their experiment name.

The fourth argument to `run_experiments` is the maximum number of
trails to run. Default value is 3.

## License

MIT License

Copyright (c) 2024 Yiyu Liu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
