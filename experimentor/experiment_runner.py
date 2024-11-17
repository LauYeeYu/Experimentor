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
        """
        Run the experiment with command line.
        :param title: The title of the experiment.
        :param config: The configuration of the experiment.
        :param file: The file to store the output. If None, there's nowhere to store the output.
        """
        command = f'{self.base_command}'
        for key, value in config.items():
            if len(key) == 1: # short option
                command += f' -{key} {value}'
            else:
                command += f' --{key} {value}'
        if file is None:
            result = subprocess.run(command, shell=True)
        else:
            with open(file, 'w') as f:
                result = subprocess.run(command, shell=True, stdout=f)
        if result.returncode != 0:
            raise ValueError(f"{command} returns non-zero value: {result.returncode}")
