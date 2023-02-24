"""Echelon-to-COPERT Interface
"""

from sys import argv
from os import getenv
from os.path import isdir, isfile, join
from csv import reader
from json import dump, dumps
from time import time
from argparse import (ArgumentParser, RawTextHelpFormatter,
                      ArgumentDefaultsHelpFormatter, ArgumentTypeError)

from dotenv import load_dotenv

from logsvc import set_logging

EPILOG="""
environment variables:
  CATEGORY              The category of the vehicle (default: Passenger Car)
  FUEL                  The fuel used by the vehicle (default: Petrol)
  SEGMENT               The segment the vehicle belongs in (default: Mini),
  EURO_STANDARD         The EURO standard of the vehicle (default: Euro 4),
  URBAN_OFF_PEAK_SPEED  The off-urban peak speed in kmph(default: 30.0),
  URBAN_PEAK_SPEED      The urban peak speed in kmph (default: 15),
  URBAN_OFF_PEAK_SHARE  The off-urban time share (default: 0.6),
  URBAN_PEAK_SHARE      The urban time share (default: 0.4)
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
    parser.add_argument('--env', action='store_true', default=False,
                        help='Use .env file (dev)')

    # FIXME - change this to json_in
    parser.add_argument('CSV_IN', type=strfile, default=None,
                        help='The CSV output file from Echelon as input to the connector')
    # FIXME - add here vehicle json - same as copert v2 but without stock, mean_activity
    # FIXME - add climate json - same as copert v2
    parser.add_argument('OUTDIR', type=strdir, help='The output directory')

    args = parser.parse_args(argv[1:])

    logger = set_logging('e2c', msg_fmt=MSG_FMT, vcount=args.verbosity)
    cmdargs = "".join(["\t" + item + "\n" for item in argv])[:-1]
    logger.debug('CMD : %s', cmdargs)
    logger.debug('AGRS: %s', args)

    if args.env:
        logger.debug('Using .env file')
        load_dotenv()

    tick = time()
    logger.info("Execution started")

    # input setup from echelon file
    # FIXME - this should be from the JSON output of Echelon v2
    # total_distance_km, number_of_vehicles
    # TODO examine case of more than one elements in the list
    act, stock = [], []
    with open(args.CSV_IN, encoding='utf-8') as fpin:
        rdr = reader(fpin, delimiter=';')
        next(rdr)
        for row in rdr:
            act.append(row[11])
            stock.append(row[13])
    logger.debug("mean activity: %s", act)
    logger.debug("stock        : %s", stock)

    # input setup from environment
    # FIXME - change this to JSON -> conform with vehicles JSON of copert v2
    # but without the stock, mean activity
    cat = getenv("CATEGORY", "Passenger Cars").split(';')
    fuel = getenv("FUEL", "Petrol").split(';')
    seg = getenv("SEGMENT", "Mini").split(';')
    estd = getenv("EURO_STANDARD", "Euro 4").split(';')
    uosp = getenv("URBAN_OFF_PEAK_SPEED", "30").split(';')
    usp = getenv("URBAN_PEAK_SPEED", "15").split(';')
    uosh = getenv("URBAN_OFF_PEAK_SHARE", "0.6").split(';')
    ush = getenv("URBAN_PEAK_SHARE", "0.4").split(';')

    params = [cat, fuel, seg, estd, stock, act,
              uosp, usp, uosh, ush]

    # check length of input parameters matches
    try:
        assert all(map(lambda item: len(item)==len(act), params)),\
            'not all input parameters have the same length'
    except AssertionError as exc:
        logger.error('lens: %s', str([len(el) for el in params]))
        raise AssertionError from exc

    # create the output
    # FIXME get code from ctrl of copert v2 for the creation of the xlsx file
    # call init_xlsx
    data = []
    for veh_tuple in zip(*params):
        icat, ifuel, iseg, iestd, istock, iact, \
            iuosp, iusp, iuosh, iush = veh_tuple
        vehicle = {
            "CATEGORY": icat,
            "FUEL": ifuel,
            "SEGMENT": iseg,
            "EURO_STANDARD": iestd,
            "STOCK": int(istock),
            "MEAN_ACTIVITY": float(iact),
            "URBAN_OFF_PEAK_SPEED": float(iuosp),
            "URBAN_PEAK_SPEED": float(iusp),
            "URBAN_OFF_PEAK_SHARE": float(iuosh),
            "URBAN_PEAK_SHARE": float(iush)
        }
        data.append(vehicle)

    fout = join(args.OUTDIR, "vehicles.json")
    with open(fout, 'w', encoding='utf8') as fpout:
        dump(data, fpout, indent=2)
        logger.debug("data dumped\n%s", dumps(data, indent=2))
    logger.info('Output created [%s]', fout)

    logger.info('Execution completed [%.3fs]', time()-tick)

if __name__ == '__main__':
    main()
