import streamlit as st
from etl import AirtableDataExtractor, DataMapper


etl = AirtableDataExtractor(api_token=st.secrets.airtable.token)
records = etl.get_records(
    base_id=st.secrets.airtable.base_id,
    table_name=st.secrets.airtable.inscriptions_table,
)
data = DataMapper(records=records)
breakpoint()
