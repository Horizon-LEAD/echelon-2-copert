"""COPERT Interface
"""

from sys import argv
from os.path import exists
from csv import reader
from json import load, dump
from argparse import (ArgumentParser, RawTextHelpFormatter,
                      ArgumentDefaultsHelpFormatter, ArgumentTypeError)

from dotenv import load_dotenv

from logsvc import set_logging


MSG_FMT = "[%(asctime)s][%(levelname)-8s]\
[%(filename)12s#L%(lineno)-4d][%(name)10s]  %(message)s"


def strdir(path):
    """Argparse type checking method
    string path for file should exist"""
    if exists(path):
        return path
    raise ArgumentTypeError("IO directory does not exist")


class RawDefaultsHelpFormatter(ArgumentDefaultsHelpFormatter, RawTextHelpFormatter):
    """Argparse formatter class"""


def main():
    """ echelon2copert interface main
    """

    parser = ArgumentParser(description=__doc__,
                            formatter_class=RawDefaultsHelpFormatter)

    parser.add_argument('-v', '--verbosity', action='count',
                        default=0, help='Increase output verbosity')
    parser.add_argument('--env', action='store_true', default=False,
                        help='Use .env file (dev)')

    parser.add_argument('simkey', type=lambda x: strdir(x), default=None,
                        help='Input directories')

    args = parser.parse_args(argv[1:])

    logger = set_logging('e2c', msg_fmt=MSG_FMT, vcount=args.verbosity)
    logger.debug('CMD: %s', ' '.join(argv))
    logger.debug('AGRS: %s', args)

    if args.env:
        logger.debug('Using .env file')
        load_dotenv()

    mean_activity, stock = 0, 0
    with open(f"data/{args.simKey}/outputs/output.csv") as fpin:
        rdr = reader(fpin, delimiter=';')
        next(rdr)
        data = next(rdr)
        mean_activity = data[11]
        stock = data[13]

    logger.debug("mean activity: %s, stock: %s", mean_activity, stock)

    data = {}

    with open(f"data/{args.simKey}/inputs/vehicles.json") as fpout:
        data = load(fpout)

    with open(f"data/{args.simKey}/inputs/vehicles.json", 'wb') as fpout:
        data[0]["MEAN_ACTIVITY"] = mean_activity
        data[0]["STOCK"] = stock
        dump(data, fpout)

    logger.debug("data dumped: %s", data)


if __name__ == '__main__':
    main()
