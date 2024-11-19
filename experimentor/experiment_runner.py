import subprocess


class BaseExperimentRunner:
    def __init__(self):
        pass

    def run_experiment(self, title: str, config: dict, file: str | None):
        """
        Run the experiment with the given configuration.
        :param title: The title of the experiment.
        :param config: The configuration of the experiment.
        :param file: The file to store the output. If None, there's nowhere to store the output.
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
