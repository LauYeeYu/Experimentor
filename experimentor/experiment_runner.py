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


class BashExperimentRunner(BaseExperimentRunner):
    def __init__(self, script: str):
        super().__init__()
        self.script = script

    def run_experiment(self, title: str, config: dict, file: str | None):
        """
        Run the experiment with bash script.
        :param title: The title of the experiment.
        :param config: The configuration of the experiment.
        :param file: The file to store the output. If None, there's nowhere to store the output.
        """
        command = f'bash {self.script}'
        for key, value in config.items():
            command += f' --{key} {value}'
        if file is None:
            result = subprocess.run(command, shell=True)
        else:
            with open(file, 'w') as f:
                result = subprocess.run(command, shell=True, stdout=f)
        if result.returncode != 0:
            raise ValueError(f"{command} returns non-zero value: {result.returncode}")


# This class is solely for testing purposes
class EchoExperimentRunner(BaseExperimentRunner):
    def __init__(self):
        super().__init__()

    def run_experiment(self, title: str, config: dict, file: str | None):
        print(f"Title: {title}")
        print(f"Config: {config}")
        print(f"File: {file}")
        import time
        time.sleep(1)
