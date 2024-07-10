import pandas as pd

COLUMNS_TO_OVERRIDE = [
    "Número de Documento",
    "Tipo de Documento",
    "Nombres",
    "Apellidos",
    "Celular",
    "Correo",
    "Fecha de Nacimiento",
    "Ministerio/Obra",
    "Detalle Obra",
    "Invitado por",
]
IDS_TO_OVERRIDE = {
    1022997110: 1032482046,
    1095308711: 1146335157,
    1098723115: 1146335157,
}


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


def get_person_info(data: pd.DataFrame, id: int) -> pd.DataFrame:
    """
    Get the info of a person based on the id number

    Parameters
    ----------
    data: pd.DataFrame
        The registries dataframe
    id: int
        The id number of the person

    Returns
    -------
    pd.DataFrame
        The filtered dataframe with the person's information
    """
    subset_data = data.loc[data["Número de Documento"] == id, COLUMNS_TO_OVERRIDE]
    assert subset_data.shape[0] > 0, "The id number is not found on the dataframe"
    return subset_data.head(1).reset_index(drop=True)


def get_registry_info(data: pd.DataFrame, id: int) -> pd.DataFrame:
    """
    Get the registries of a person based on the id number

    Parameters
    ----------
    data: pd.DataFrame
        The registries dataframe
    id: int
        The id number of the person

    Returns
    -------
    pd.DataFrame
        The filtered dataframe with the person's registries information
    """
    registry_cols = [col for col in data.columns if col not in COLUMNS_TO_OVERRIDE]
    registry_cols = ["Número de Documento"] + registry_cols
    registry_info = data.loc[data["Número de Documento"] == id, registry_cols]
    return registry_info


def move_registry_to_other(data: pd.DataFrame, old_id: int, new_id: int) -> pd.DataFrame:
    """
    Move the registry to another person

    Parameters
    data: pd.DataFrame
        The registries data
    old_id: int
        The person that initially did the registry
    new_id: int
        The person that will be the new receiver of the registry

    Returns
    -------
    pd.DataFrame
        The data with the updated registry
    """
    person_info = get_person_info(data=data, id=new_id)
    registry_info = get_registry_info(data=data, id=old_id)
    registry_info["Número de Documento"] = new_id
    new_data = person_info.merge(registry_info, on=["Número de Documento"])
    return pd.concat([
        data.loc[data["Número de Documento"] != old_id],
        new_data,
    ]).reset_index(drop=True)


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
    ids_to_delete = get_ids_to_delete(data=updates_data)
    final_data = delete_records(data=registries_data, ids=ids_to_delete)

    # Move registries to other persons
    for old_id, new_id in IDS_TO_OVERRIDE.items():
        final_data = move_registry_to_other(data=final_data, old_id=old_id, new_id=new_id)

    return final_data
