import requests
import streamlit as st
import pandas as pd
from google.cloud import storage
from google.oauth2 import service_account
from data.etl import DataMapper
from data.get_data import get_data


def build_client() -> storage.Client:
    """Build the GCS client needed to interact with storage"""
    cred_info = st.secrets.connections.gcs.to_dict()
    creds = service_account.Credentials.from_service_account_info(cred_info)
    client = storage.Client(credentials=creds)
    return client


def _create_doc_abbreviation(doc_type: str) -> str:
    """Create a document type abbreviation"""
    match doc_type:
        case "Cédula":
            return "cc"
        case "Tarjeta de Identidad":
            return "ti"
        case "Pasaporte":
            return "pass"
        case "Cédula de Extranjería":
            return "ce"
        case _:
            raise ValueError(f"Verificar el tipo de documento {doc_type}")


def get_records() -> DataMapper:
    """Get all records stored in Airtable"""
    data = get_data(
        base_id=st.secrets.airtable.base_id,
        table_name=st.secrets.airtable.inscriptions_table,
    )
    return data


def store_record(record: dict, client: storage.Client, bucket: str, path: str) -> list[str]:
    """
    Store in GCS a record's payment voucher

    Parameters
    ----------
    record: dict
        The Airtable record, which must contain the info of the file to download
    client: storage.Client
        The GCS client
    bucket: str
        The name of the bucket to store the data
    path: str
        The path where the data should live

    Returns
    -------
    None
        The data is stored and the function doesn't return any object
    """
    def _build_file_prefix(record: dict) -> str:
        """Build the file prefix of the file to store"""
        doc_type = _create_doc_abbreviation(record["Tipo de Documento"])
        doc_number = record["Número de Documento"]
        return f"{doc_type}_{doc_number}"

    def _build_file_name(path: str, file_prefix: str, voucher_record: dict) -> str:
        """Build the file name of the file to store"""
        file_extension = voucher_record["filename"].split(".")[-1]
        voucher_id = voucher_record["id"]
        return f"{path}/{file_prefix}_{voucher_id}.{file_extension}"

    def _download_file(voucher_record: dict, file_path: str) -> None:
        """Download the file content"""
        url = voucher_record["url"]
        response = requests.get(url)
        with open(file_path, "wb") as file:
            file.write(response.content)

    def _store_file(client: storage.Client, bucket: str, file_name: str) -> None:
        """Store the content of the URL into GCS"""
        gcs_bucket = client.get_bucket(bucket)
        blob = gcs_bucket.blob(file_name)
        blob.upload_from_filename(file_name)
        return

    gcs_files = []
    for voucher_record in record["Comprobante de pago"]:
        file_name = _build_file_name(
            path=path,
            file_prefix=_build_file_prefix(record=record),
            voucher_record=voucher_record,
        )

        _download_file(voucher_record=voucher_record, file_path=file_name)
        print(f"File {file_name} was downloaded successfully")

        _store_file(
            client=client,
            bucket=bucket,
            file_name=file_name,
        )
        print(f"File {file_name} was uploaded successfully")
        gcs_files.append(file_name)

    return gcs_files


def main():
    client = build_client()
    data = get_records().data

    final_data = []
    for idx in range(len(data)):
        record = data.iloc[idx].to_dict()
        file_names = store_record(
            record=record,
            client=client,
            bucket="youth_camp_registries",
            path="payment_vouchers",
        )
        final_data.append({
            "document_type": record["Tipo de Documento"],
            "document_number": record["Número de Documento"],
            "record_timestamp": record["Created"],
            "gcs_files": file_names,
        })

    final_data = pd.DataFrame(final_data)
    data_file = "gcs_records_map.parquet"
    final_data.to_parquet(data_file)
    blob = client.get_bucket("youth_camp_registries").blob(data_file)
    blob.upload_from_filename(data_file)

    raw_data_file = "raw_data_snapshot.parquet"
    data.to_parquet(raw_data_file)
    blob = client.get_bucket("youth_camp_registries").blob(raw_data_file)
    blob.upload_from_filename(raw_data_file)


if __name__ == "__main__":
    main()
