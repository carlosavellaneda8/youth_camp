import pandas as pd
from data.etl import DataMapper


def create_person_summary(data: DataMapper) -> pd.DataFrame:
    """Group data by person's id number and type, and retrieve the total transfered money"""
    person_cols = [
        "tipo_de_documento",
        "numero_de_documento",
        "nombres",
        "apellidos",
    ]
    person_data = (
        data
        .data[person_cols]
        .drop_duplicates(subset=["tipo_de_documento", "numero_de_documento"])
    )
    payment_summary = (
        data
        .data
        .groupby(["tipo_de_documento", "numero_de_documento"])["valor_abono"]
        .sum()
        .reset_index()
    )
    person_summary = (
        person_data.merge(payment_summary)
        .sort_values(by="valor_abono", ascending=False)
        .reset_index(drop=True)
    )
    rename_columns = {key: value for key, value in data.reversed_map.items() if key in person_summary.columns}
    return person_summary.rename(columns=rename_columns)
