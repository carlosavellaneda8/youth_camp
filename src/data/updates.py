import pandas as pd


def get_ids_to_delete(data: pd.DataFrame) -> list[int]:
    """
    Get the list of ids to delete

    Parameters
    ----------
    data: pd.DataFrame
        The data both from GCS and Airtable

    Returns
    -------
    list[int]
        The list of ids to delete
    """
    mask = data["Tipo de devolución"].isin(["Consignación", "Retiro de niños"])
    ids_to_delete = data.loc[mask, "Número de Documento"].drop_duplicates()
    return ids_to_delete.tolist()


def delete_records(data: pd.DataFrame, ids: list[int]) -> pd.DataFrame:
    """
    Delete the records of people that cannot go to the camp

    Parameters
    ----------
    data: pd.DataFrame
        The final dataset
    ids: list[int]
        The list of ids to delete

    Returns
    -------
    pd.DataFrame
        The final dataset without the records to delete
    """
    mask = data["Número de Documento"].isin(ids)
    return data[~mask]


def update_data(registries_data: pd.DataFrame, updates_data: pd.DataFrame) -> pd.DataFrame:
    """
    Execute the different updates in the registries data

    Parameters
    ----------
    registries_data: pd.DataFrame
        The data from GCS and Airtable that contains the registries information
    updates_data: pd.DataFrame
        The data that contains the required updates to perform

    Returns
    -------
    pd.DataFrame
        The updated data
    """
    # Delete the ids from the dataset
    # TODO: add the logic of money transfer to other people
    ids_to_delete = get_ids_to_delete(data=updates_data)
    final_data = delete_records(data=registries_data, ids=ids_to_delete)

    return final_data
