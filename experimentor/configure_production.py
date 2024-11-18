"""
This module provides a class that can be iterated to get all possible
configurations.
"""

class ExperimentorError(Exception):
    """
    The exception class for the Experimentor.
    """
    pass


class ConfigureIterable:
    """
    An iterable class that generates all possible configurations.
    """
    class ConfigurePair:
        def __init__(self, key, value):
            self.key = key
            self.value = value

    def __init__(self, config: list):
        # type check
        assert type(config) == list
        for i in config:
            assert type(i) == dict

        self.length = len(config)
        self.config = [[] for _ in range(self.length)]
        self.num_index = [len(config[i]) for i in range(self.length)]
        self.index = [0 for _ in range(self.length)]
        self.finished = False
        for i in range(self.length):
            self.config[i] = [ConfigureIterable.ConfigurePair(key, value)
                              for key, value in config[i].items()]

    def __iter__(self):
        return self

    def __next__(self) -> tuple[str, dict]:
        # exit if all configure are used
        if self.finished:
            raise StopIteration

        conf = {}
        title = ''
        for i in range(self.length):
            if i != 0:
                title += '_'
            title += str(self.config[i][self.index[i]].key)
            sub_config = self.config[i][self.index[i]]
            if sub_config.key in conf:
                raise ValueError(f'Duplicated key: {sub_config.key}')
            conf[sub_config.key] = sub_config.value
        # move to next configure
        self.increment()
        return title, conf

    def increment(self):
        carry = True
        for i in range(self.length - 1, -1, -1):
            if carry:
                self.index[i] += 1
                carry = False
            if self.index[i] >= self.num_index[i]:
                self.index[i] = 0
                carry = True
            else:
                break
        if carry:
            self.finished = True
