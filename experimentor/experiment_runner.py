import subprocess


class BaseExperimentRunner:
    """The base class for experiment runners.

    The experiment runner is a class to run the experiment with the given
    configuration. The configuration is a dictionary where the key is the
    name of the parameter, and the value is the value of the parameter.

    You can inherit this class to change the behaviour. The class must have
    a method called `run_experiment` to run a single experiment. The method
    should take three parameters:

    - title: The title of the experiment. The title is
    used to distinguish different experiments and is therefore unique.
    - config: The configuration of the experiment (as described above).
    - file: The file to store the log. If None, no output will be stored.

    Please note that the third parameter is just supposed to be the log file.
    If you use the default track log object, the third parameter will be the
    path to the log file. However, the behaviour can be changed by customizing
    the track log object. The track log object can be anything derived from
    `experimentor.BaseTrackLog` and the third parameter will be passed from
    the `add_log_file` method of the track log object. See the documentation
    for `experimentor.BaseTrackLog` for more information.
    """
    def __init__(self):
        pass

    def run_experiment(self, title: str, config: dict, file: str | None):
        """Run the experiment with the given configuration.

        Please note that the third parameter is just supposed to be the log
        file. See the documentation above in this class for more information.

        :param title: The title of the experiment.
        :param config: The configuration of the experiment.
        :param file: The "file" to store the output. If None, there's nowhere
            to store the output.
        """
        raise NotImplementedError


class SimpleCommandRunner(BaseExperimentRunner):
    def __init__(self, base_command: str):
        super().__init__()
        self.base_command = base_command

    def run_experiment(self, title: str, config: dict, file: str | None):
        """Run the experiment with command line.

        The options will be generated according to the type of the value
        in the configuration. Only the values in the `config` will be used.
        1) If the value is a dictionary, options will be generated according
           to the key-value pairs in the dictionary. If the key is a single
           character, the option will be a short option. Otherwise, it will
           be a long option.
        2) If the value is not a dictionary, the command will be appended with
           the value. The order of the values will be the same as the order of
           the key-value pairs in the dictionary.

        :param title: The title of the experiment.
        :param config: The configuration of the experiment.
        :param file: The file to store the output. If None, the output will
            be treated as a standard output.
        """
        command = f'{self.base_command}'
        for _, value in config.items():
            if type(value) == dict:
                for k, v in value.items():
                    if len(k) == 1:
                        command += f' -{k} {v}'
                    else:
                        command += f' --{k} {v}'
            else:
                command += f' {value}'
        if file is None:
            result = subprocess.run(command, shell=True)
        else:
            with open(file, 'w') as f:
                result = subprocess.run(command, shell=True, stdout=f)
        if result.returncode != 0:
            raise ValueError(f"{command} returns non-zero value: {result.returncode}")
