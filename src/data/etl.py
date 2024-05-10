import re
import pandas as pd
from unidecode import unidecode
from pyairtable import Api


def _records_to_dataframe(records: list[dict]) -> pd.DataFrame:
    """
    Transform records into a pandas dataframe

    Parameters
    ----------
    records : list[dict]
        The records retrieved from Airtable

    Returns
    -------
    data : pd.DataFrame
        The data transformed into a pandas dataframe
    """
    fields_data = [record["fields"] for record in records]
    data = pd.DataFrame(fields_data)
    return data


def _normalize_columns_map(data: pd.DataFrame) -> dict:
    """
    Create a mapping dictionary to have a normalized column names

    Parameters
    ----------
    data : pd.DataFrame
        The raw input data

    Returns
    -------
    column_map : dict
        The mapping between original column names and the normalized column names
    """
    def _normalize_str(column_name: str) -> str:
        """Normalize a column name"""
        column_name = unidecode(column_name)
        column_name = column_name.strip()
        column_name = re.sub(" +|/", "_", column_name)
        column_name = re.sub(r"\(|\)", "", column_name)
        column_name = column_name.lower()
        return column_name

    column_map = {column_name: _normalize_str(column_name=column_name) for column_name in data.columns}
    return column_map


def _reverse_columns_map(columns_map: dict) -> dict:
    """Reverse a column map dictionary"""
    reversed_dict = {value: key for key, value in columns_map.items()}
    return reversed_dict


class AirtableDataExtractor:

    def __init__(self, api_token: str) -> None:
        self.api = Api(api_token)

    def get_records(self, base_id: str, table_name: str, view: str | None = None) -> list[dict]:
        """
        Get records of the specified table

        Parameters
        ----------
        base_id : str
            The Airtable's base id
        table_name : str
            The Airtable's table name id

        Returns
        -------
        records : list[dict]
            The list of records registered in the table
        """
        table = self.api.table(base_id=base_id, table_name=table_name)
        if view:
            return table.all(view=view)

        return table.all()


class DataMapper:

    def __init__(self, data: list[dict] | pd.DataFrame) -> None:
        if isinstance(data, list):
            self.data = _records_to_dataframe(records=data)
        else:
            self.data = data
        self.columns_map = _normalize_columns_map(data=self.data)
        self.reversed_map = _reverse_columns_map(columns_map=self.columns_map)
        self.mapped = False

    def map(self) -> None:
        """
        Map the data's columns with normalized strings
        """
        assert self.mapped is False
        self.data = self.data.rename(columns=self.columns_map)
        self.mapped = True

    def unmap(self) -> None:
        """
        Unmap the data's columns to the original column names
        """
        assert self.mapped is True
        self.data = self.data.rename(columns=self.reversed_map)
        self.mapped = False
