import streamlit as st
from data.etl import AirtableDataExtractor
from app.team_utils import Person


@st.cache_data
def get_persons_data() -> list[dict]:
    """Retrieve the teams data"""
    etl = AirtableDataExtractor(api_token=st.secrets.airtable.token)
    records = etl.get_records(
        base_id=st.secrets.airtable.checkin_base,
        table_name=st.secrets.airtable.checkin_table,
    )
    records = [record["fields"] for record in records]
    return records


def preprocess_data(records: list[dict]) -> dict[int, dict]:
    output = {}
    for record in records:
        id = record.pop("Documento")
        output[id] = record

    return output


def is_ok_status(person_info: dict[str, dict]) -> bool:
    """Check the payment status of an attendant"""
    missing_money = person_info.get("Faltante")
    return missing_money <= 0


def format_person(person_info: dict[str, dict]) -> str:
    """Format the person's info"""
    name = person_info.get("Nombres", "").title()
    last_name = person_info.get("Apellidos", "").title()
    total_payment = person_info.get("Valor Total")
    missing = person_info.get("Faltante")
    text = f"""Esta es la información de la persona:

* **Nombre:** {name}
* **Apellido:** {last_name}
* **Total abonado:** {total_payment}
* **Faltante:** {missing}
    """
    return text


records = get_persons_data()
records = preprocess_data(records=records)
st.image("src/app/imgs/logo.png")
id = st.number_input(
    "Número de documento:",
    format="%i",
    value=None,
    step=1,
)

if id:
    person = records.get(id)
    if person:
        if is_ok_status(person_info=person):
            st.markdown("## La persona puede abordar el bus")
        else:
            st.markdown("## La persona tiene saldo pendiente")
            st.markdown("Es necesario revisar su caso")
        text = format_person(person_info=person)
        st.markdown(text)
    else:
        st.error("La persona no está inscrita o se registró con un número incorrecto. Revisar su caso")
