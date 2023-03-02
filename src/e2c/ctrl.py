""" Controller Module

Contains functionality regarding...
"""

from os.path import join
from logging import getLogger

from xlsxwriter import Workbook


WORKSHEETS = ["SHEETS", "STOCK", "MEAN_ACTIVITY",
              "URBAN_OFF_PEAK_SPEED", "URBAN_PEAK_SPEED",
              "URBAN_OFF_PEAK_SHARE", "URBAN_PEAK_SHARE",
              "MIN_TEMPERATURE", "MAX_TEMPERATURE", "HUMIDITY"]
UNITS = ["[n]", "[km]", "[km/h]", "[km/h]",
         "[%]", "[%]", "[℃]", "[℃]", "[%]"]
VEHICLE_HEADER = ["Category", "Fuel", "Segment", "Euro Standard"]
CLIMATE_HEADER = ["Month"]
MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
INPUT_FILENAME = "copert_input.xlsx"

logger = getLogger("copert.ctrl")


def init_xlsx(params, path='/tmp'):
    """_summary_

    :param path: _description_
    :type path: _type_
    :param params: _description_
    :type params: _type_
    :return: _description_
    :rtype: _type_
    """

    filepath = join(path, INPUT_FILENAME)
    wbk = Workbook(filepath)

    fmt_header = wbk.add_format({
        'bold': True,
        'font_color': 'white',
        'bg_color': '#0099DC',
        'align': 'center'
    })
    fmt_percent = wbk.add_format({'num_format': '0.0%'})
    fmt_num = wbk.add_format({'num_format': '#,##0.0'})

    for worksheet_name in WORKSHEETS:
        _ = wbk.add_worksheet(worksheet_name)

    ws_sheets = wbk.get_worksheet_by_name('SHEETS')
    ws_sheets.write(0, 0, 'SHEET_NAME', fmt_header)
    ws_sheets.write(0, 1, 'Unit', fmt_header)
    for i, (sheet, unit) in enumerate(zip(WORKSHEETS[1:], UNITS)):
        ws_sheets.write_url(i+1, 0, f"internal:'{sheet}'!$A$1", string=sheet)
        ws_sheets.write(i+1, 1, unit)

    VEHICLE_HEADER.append(params['year'])
    for ws_name in WORKSHEETS[1:-3]:
        wsh = wbk.get_worksheet_by_name(ws_name)
        for j, col_name in enumerate(VEHICLE_HEADER):
            wsh.write(0, j, col_name, fmt_header)

        fmt = fmt_num
        if ws_name.endswith('_SHARE'):
            fmt = fmt_percent
        # TODO examine case of more than one elements in the list of vehicles
        wsh.write(1, 0, params['vehicles']['CATEGORY'])
        wsh.write(1, 1, params['vehicles']['FUEL'])
        wsh.write(1, 2, params['vehicles']['SEGMENT'])
        wsh.write(1, 3, params['vehicles']['EURO_STANDARD'])
        wsh.write(1, 4, params['vehicles'][ws_name], fmt)

    CLIMATE_HEADER.append(params['year'])
    for ws_name in WORKSHEETS[-3:]:
        wsh = wbk.get_worksheet_by_name(ws_name)
        for j, col_name in enumerate(CLIMATE_HEADER):
            wsh.write(0, j, col_name, fmt_header)

        fmt = fmt_num
        if ws_name == 'HUMIDITY':
            fmt = fmt_percent
        for i, (month, value) in enumerate(zip(MONTHS, params['climate'][ws_name])):
            wsh.write(i+1, 0, month)
            wsh.write(i+1, 1, value, fmt)

    wbk.close()

    logger.info("input file created successfully: %s", filepath)

    return filepath
