import argparse
import json

from .const import DEFAULT_MAX_TRIALS
from .experiment_runner import BashExperimentRunner
from .experimentor import run_experiments


def main():
    parser = argparse.ArgumentParser(description='Run experiments automatically.')
    parser.add_argument('--config-file', type=str,
                        help='Config file', required=True)
    parser.add_argument('--script', type=str,
                        help='Function to run', required=True)
    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument('--no-log', action='store_true',
                           help='Do not log the output')
    log_group.add_argument('--log-dir', type=str, help='Log directory')
    parser.add_argument('--max-trial', type=int,
                        default=DEFAULT_MAX_TRIALS, help='Maximum number of trials')
    args = parser.parse_args()

    config = json.load(open(args.config_file))
    log_dir = None if args.no_log else args.log_dir
    run_experiments(config, BashExperimentRunner(args.script),
                    log_dir, args.max_trial)


if __name__ == '__main__':
    main()
