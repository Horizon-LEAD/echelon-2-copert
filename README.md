# Echelon-to-COPERT Connector

A model connecting data from the Echelon model (v1, v2) to COPERT model.

---

## Introduction

Echelon caclulated the total distance traveled by a fleet of cars to satisfy a certain services demand. Then this output could be transferred to COPERT so that an evaluation of the GHG emissions can be performed. This connector model takes as input the output from the Echelon model, extracts all the necessary values and passes it to the definition of the vehicles from COPERT together with more necessary vehicle parameters.


## Installation

The model is packaged as a python application. The `requirements.txt` and `Pipenv` files are provided for the setup of an environment where the module can be installed. The package includes a `setup.py` file and it can be therefore installed with a `pip install .` when we are at the same working directory as the `setup.py` file. For testing purposes, one can also install the package in editable mode `pip install -e .`.

After the install is completed, an executable `e2c` will be available to the user.

Furthermore, a `Dockerfile` is provided so that the user can package the parcel generation model. To build the image the following command must be issued from the project's root directory:

```
docker build -t e2c:latest .
```

## Usage

The executable's help message provides information on the parameters that are needed.

```
$ e2c --help
usage: e2c [-h] [-v] [--env] CSV_IN OUTDIR

Echelon-to-COPERT Interface

positional arguments:
  CSV_IN           The CSV output file from Echelon as input to the connector
  OUTDIR           The output directory

optional arguments:
  -h, --help       show this help message and exit
  -v, --verbosity  Increase output verbosity (default: 0)
  --env            Use .env file (dev) (default: False)

environment variables:
  CATEGORY              The category of the vehicle (default: Passenger Car)
  FUEL                  The fuel used by the vehicle (default: Petrol)
  SEGMENT               The segment the vehicle belongs in (default: Mini),
  EURO_STANDARD         The EURO standard of the vehicle (default: Euro 4),
  URBAN_OFF_PEAK_SPEED  The off-urban peak speed in kmph(default: 30.0),
  URBAN_PEAK_SPEED      The urban peak speed in kmph (default: 15),
  URBAN_OFF_PEAK_SHARE  The off-urban time share (default: 0.6),
  URBAN_PEAK_SHARE      The urban time share (default: 0.4)
```

### Examples

In the following examples, it is assumed that the user has placed all necessary input files in the `sample-data/inputs` directory while making sure that the `sample-data/outputs` directory exists.

```
# running the executable
e2c -vvv sample-data/input/echelon-output.csv sample-data/output/ --env

# running as module
python -m src.e2c sample-data/input/echelon-output.csv sample-data/output/ --env

# docker run
docker run
```
