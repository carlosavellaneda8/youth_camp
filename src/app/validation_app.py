import pandas as pd
import streamlit as st
from data.get_data import get_registries

ID_TYPES = [
    "Cédula",
    "Tarjeta de Identidad",
    "Pasaporte",
    "Cédula de Extranjería",
]
REGISTER_URL = "https://airtable.com/appfWLdJbvKBGUtOi/pagtpbNW7quXqROkI/form"
WAITING_LIST_URL = "https://airtable.com/app9s8t2zfpa5oCqn/shrWIR9vIBfeWDveW"
REGISTERED = f"""### ¡Estás inscrito!
Hemos confirmado que ya estás inscrito a nuestro retiro. Te animamos a llenar [el formulario]({REGISTER_URL}) para registrar un nuevo abono."""
UNREGISTERED = f"""### ¡Lo sentimos!
No apareces dentro del listado de inscritos al retiro. 
Te animamos a orar e inscribirte a nuestra [lista de espera]({WAITING_LIST_URL}).

**Nota:** Si encuentras una inconsistencia con esto, puedes contactarte con José Mejía ([3022485108](https://wa.me/573022485108)), Carlos Avellaneda ([3203471465](https://wa.me/573203471465)) o Juan Sebastián Piña ([3204668582](https://wa.me/573204668582)).
"""


def is_id_in_data(data: pd.DataFrame, id: int, id_type: str) -> bool:
    """Search if the id and id type is in the data"""
    query = f"numero_de_documento == {id} and tipo_de_documento == '{id_type.upper()}'"
    data_subset = data.query(query)
    if len(data_subset) > 0:
        return True
    return False


# Set the app's config
st.set_page_config(
    page_title="Retiro Internacional TBUCF-2024",
    page_icon="🌎",
    layout="wide",
)

registries_data, _ = get_registries()
registries_data.map()
suscribers = registries_data.data[["tipo_de_documento", "numero_de_documento"]].drop_duplicates()
suscribers["tipo_de_documento"] = suscribers["tipo_de_documento"].str.upper()

st.title(":earth_americas: Retiro Internacional TBUCF-2024")
id_type = st.selectbox(
    label="Ingresa el tipo de documento", options=ID_TYPES, index=None, placeholder="Escoge una opción"
)
if id_type:
    id = st.number_input(
        label="Ingresa el número de documento", step=1, format="%i", value=None
    )


if id:
    id_found = is_id_in_data(data=suscribers, id=id, id_type=id_type)
    if id_found:
        st.markdown(REGISTERED)
    else:
        st.markdown(UNREGISTERED)
