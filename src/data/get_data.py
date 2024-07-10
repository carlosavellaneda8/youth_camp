import streamlit as st
import pandas as pd
from st_files_connection import FilesConnection
from data.etl import AirtableDataExtractor, DataMapper
from data.updates import update_data

THRESHOLD_DATE = "2024-06-03"


def get_data(base_id: str, table_name: str) -> DataMapper:
    """General function to get the data"""
    etl = AirtableDataExtractor(api_token=st.secrets.airtable.token)
    records = etl.get_records(base_id=base_id, table_name=table_name)
    data = DataMapper(data=records)
    return data


def get_gcs_data(file_path: str) -> DataMapper:
    """Retrieve data stored in GCS"""
    conn = st.connection("gcs", type=FilesConnection)
    data = conn.read(file_path, input_format="parquet")
    data = data[data["Created"] < THRESHOLD_DATE]
    return DataMapper(data=data)


def get_updates_data() -> pd.DataFrame:
    """Get the data of updates"""
    updates_data = get_data(
        base_id=st.secrets.airtable.base_id,
        table_name=st.secrets.airtable.updates_table,
    ).data
    return updates_data


@st.cache_data(ttl=15 * 60)
def get_registries() -> DataMapper:
    airtable_data = get_data(
        base_id=st.secrets.airtable.base_id,
        table_name=st.secrets.airtable.inscriptions_table,
    )
    gcs_data = get_gcs_data(file_path="youth_camp_registries/new_backup_raw_data_snapshot.parquet")
    data = pd.concat([airtable_data.data, gcs_data.data])
    data = data.drop_duplicates(subset=["Tipo de Documento", "Número de Documento", "Created"])
    data_to_change = get_updates_data()
    data = update_data(registries_data=data, updates_data=data_to_change)
    return DataMapper(data=data)


@st.cache_data(ttl=15 * 60)
def get_payments() -> DataMapper:
    data = get_data(
        base_id=st.secrets.airtable.base_id,
        table_name=st.secrets.airtable.money_transfers_table,
    )
    return data
