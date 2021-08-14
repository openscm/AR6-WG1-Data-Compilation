from collections import defaultdict

import pandas as pd


def read_badc(path):
    """Read a badc-csv file and return as pandas.DataFrame

    Parameters
    ----------
    path : file-like object as str or :class:`pathlib.Path`
        The path to a file in badc-csv format.

    Returns
    -------
    :obj:`pd.DataFrame`, dict, dict
        :obj:`pd.DataFrame` containing the data, a dict containing a mapping
        between the columns and their units and a ``dict`` containing the
        metadata
    """
    columns = {}
    units = {}
    metadata = defaultdict(dict)

    with open(path, "r") as file:
        for i, line in enumerate(file.readlines()):

            # get mapping for column names
            if line.startswith(("long_name", "comments")):
                row = line.strip("\n").split(",")
                if row[1] == "G":
                    # some global comment, ignore
                    continue

                id_int = row[1]
                if row[0] == "long_name":
                    name = row[2]
                    columns[id_int] = name
                    units[name] = row[3]
                else:
                    metadata[id_int][row[0]] = ",".join(row[2:])

            # get line number where data starts, then stop iteration
            if line.startswith("data"):
                first_data_row = i + 1
                break

    out_df = pd.read_csv(
        path, skiprows=first_data_row, skipfooter=1, engine="python"
    ).rename(columns=columns)

    metadata_out = {
        columns[k]: v
        for k, v in metadata.items()
    }

    return out_df, units, metadata_out
