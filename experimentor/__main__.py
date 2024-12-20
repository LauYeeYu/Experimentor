import argparse
import json
import sys

from .const import DEFAULT_MAX_TRIALS
from .experiment_runner import SimpleCommandRunner
from .experimentor import run_experiments


def main():
    parser = argparse.ArgumentParser(description='Run experiments automatically.')
    parser.add_argument('--config-file', type=str,
                        help='Config file', required=True)
    parser.add_argument('--command', type=str,
                        help='Base command to run', required=True)
    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument('--no-log', action='store_true',
                           help='Do not log the output')
    log_group.add_argument('--log-dir', type=str, help='Log directory')
    parser.add_argument('--max-trial', type=int,
                        default=DEFAULT_MAX_TRIALS, help='Maximum number of trials')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    config = json.load(open(args.config_file))
    log_dir = None if args.no_log else args.log_dir
    run_experiments(config, SimpleCommandRunner(args.script),
                    log_dir, args.max_trial)


if __name__ == '__main__':
    main()
