"""Echelon-to-COPERT Interface
"""

from sys import argv
from os.path import isdir, isfile
import json
from time import time
from json import load
from e2c.ctrl import init_xlsx
from argparse import (ArgumentParser, RawTextHelpFormatter,
                      ArgumentDefaultsHelpFormatter, ArgumentTypeError)

from logsvc import set_logging

# TODO: add an example
EPILOG="""
"""
MSG_FMT = "[%(asctime)s][%(levelname)-8s]\
[%(filename)12s#L%(lineno)-3d][%(name)3s]  %(message)s"
COPERT_VEH_PARAMS = ["CATEGORY", "FUEL", "SEGMENT", "EURO_STANDARD",
                     "STOCK", "MEAN_ACTIVITY",
                     "URBAN_OFF_PEAK_SPEED", "URBAN_PEAK_SPEED",
                     "URBAN_OFF_PEAK_SHARE", "URBAN_PEAK_SHARE"]


def strfile(path):
    """Argparse type checking method
    string path for file should exist"""
    if isfile(path):
        return path
    raise ArgumentTypeError("Input file does not exist")


def strdir(path):
    """Argparse type checking method
    string path for file should exist"""
    if isdir(path):
        return path
    raise ArgumentTypeError("Input directory does not exist")


class RawDefaultsHelpFormatter(ArgumentDefaultsHelpFormatter, RawTextHelpFormatter):
    """Argparse formatter class"""


def main():
    """ echelon2copert interface main
    """
    parser = ArgumentParser(description=__doc__,
                            epilog=EPILOG,
                            formatter_class=RawDefaultsHelpFormatter)

    parser.add_argument('-v', '--verbosity', action='count',
                        default=0, help='Increase output verbosity')
    parser.add_argument('Echelon_Output_IN', type=strfile, default=None,
                        help='The Json output file from Echelon as input to the connector')
    parser.add_argument('Vehicle_Json_IN', type=strfile, default=None,
                        help='Vehicle json same as Copert v2 - exclude stock, mean_activity')
    parser.add_argument('Climate_Json_IN', type=strfile, default=None,
                        help='Climate json same as Copert v2')
    parser.add_argument('year', type=int, default=None,
                        help='Set the year')

    parser.add_argument('OUTDIR', type=strdir, help='The output directory')

    args = parser.parse_args(argv[1:])

    logger = set_logging('e2c', msg_fmt=MSG_FMT, vcount=args.verbosity)
    cmdargs = "".join(["\t" + item + "\n" for item in argv])[:-1]
    logger.debug('CMD : %s', cmdargs)
    logger.debug('AGRS: %s', args)

    tick = time()
    logger.info("Execution started")
    params_cli = {}

    # input setup from echelon file
    # TODO examine case of more than one elements in the list
    act, stock = 0, 0
    with open(args.Echelon_Output_IN, encoding='utf-8') as f:
        data = json.load(f)
        for rec in data:
            act += rec['total_distance_km']
            stock += rec['number_vehicles']
    logger.debug("mean activity: %s", act)
    logger.debug("stock        : %s", stock)

    # input setup from vehicles
    vehicles = {}
    with open(args.Vehicle_Json_IN, encoding='utf-8') as f:
        vehicles = json.load(f)

    # check length of input parameters matches
    try:
        assert (len(vehicles) == 1), 'Only one vehicle is currently supported.'
        vehicles = vehicles[0]
    except AssertionError as exc:
        logger.error('lens: %s', len(vehicles))
        raise AssertionError from exc
    
    # enrich vehicles with stock and mean activity
    vehicles['STOCK'] = stock
    vehicles['MEAN_ACTIVITY'] = act
    params_cli['vehicles'] = vehicles

    # input setup from vehicles
    with open(args.Climate_Json_IN) as fpv:
        params_cli['climate'] = load(fpv)
    logger.debug('CLI: %s', params_cli)

    params_cli['year'] = args.year

    # create the output
    filepath = init_xlsx(params_cli, path=args.OUTDIR)
    logger.debug('FILEPATH: %s', filepath)

    logger.info('Execution completed [%.3fs]', time()-tick)

if __name__ == '__main__':
    main()
