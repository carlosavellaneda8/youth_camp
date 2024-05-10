import streamlit as st
from data.etl import AirtableDataExtractor, DataMapper


def get_data(base_id: str, table_name: str) -> DataMapper:
    """General function to get the data"""
    etl = AirtableDataExtractor(api_token=st.secrets.airtable.token)
    records = etl.get_records(base_id=base_id, table_name=table_name)
    data = DataMapper(data=records)
    return data


@st.cache_data(ttl=15 * 60)
def get_registries() -> DataMapper:
    data = get_data(
        base_id=st.secrets.airtable.base_id,
        table_name=st.secrets.airtable.inscriptions_table,
    )
    return data


@st.cache_data(ttl=15 * 60)
def get_payments() -> DataMapper:
    data = get_data(
        base_id=st.secrets.airtable.base_id,
        table_name=st.secrets.airtable.money_transfers_table,
    )
    return data
