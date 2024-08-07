import os
from astropy.table import Table
from astropy.io import registry

from casa_formats_io.casa_low_level_io.table import CASATable


def identify_casa_table(origin, *args, **kwargs):
    if (isinstance(args[2], str) and
            os.path.isdir(args[2]) and
            os.path.exists(os.path.join(args[2], 'table.dat'))):
        with open(os.path.join(args[2], 'table.dat'), 'rb') as f:
            return f.read(4) == b'\xbe\xbe\xbe\xbe'


def read_casa_table(filename, data_desc_id=None):
    import time
    start = time.time()
    table = CASATable.read(filename)
    print(f"Time to read table info: {time.time() - start}")

    start = time.time()
    astable = table.as_astropy_table(data_desc_id=data_desc_id)
    print(f"Time to produce data table: {time.time() - start}")

    #return table.as_astropy_table(data_desc_id=data_desc_id)
    return astable


def read(filename, name):
    table = CASATable.read(filename)

    return table.get_column(name=name)


registry.register_identifier('casa-table', Table, identify_casa_table)
registry.register_reader('casa-table', Table, read_casa_table)
