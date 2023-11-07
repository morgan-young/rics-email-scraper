"""
This file contains all the functions around
processing the output csv file.

"""

import pandas as pd


def convert_list_to_csv(url_list: list, csv_file_name: str):
    """
    This functiont takes a list and
    turns it into a csv file.

    :param list url_list: the list you want to turn into a csv
    :param str csv_file_name: what you want to name the output csv file

    """
    # changing the list into a set and back again to get rid of duplicates
    url_set = set(url_list)
    url_list = list(url_set)

    # putting the list into a dataframe so we can stick it in a csv file
    df = pd.DataFrame(url_list)
    df.to_csv(f"{csv_file_name}.csv", index=False)
