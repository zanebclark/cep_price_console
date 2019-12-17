import argparse

parser = argparse.ArgumentParser(description="The Price Console")
parser.add_argument('-s', '--schedule_mode',
                    action='store',
                    choices=['recreate', 'update', 'daily'],
                    help='Run the scheduled script and close',
                    dest='schedule_mode',
                    default=None)
parser.add_argument('-l', '--local',
                    action='store_true',
                    help="Are you connected to CEP's server?",
                    dest='local',
                    default=False)
parser.add_argument('-t', '--testing',
                    action='store_true',
                    help="Do you want to apply testing methods?",
                    dest='testing')
arguments = parser.parse_args()
