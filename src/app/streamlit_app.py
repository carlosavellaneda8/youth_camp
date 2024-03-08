import streamlit as st
from utils import check_password
from app.views import (
    attendants,
    payments,
    pendings,
)


def registries():
    st.markdown("## Consignaciones")


st.set_page_config(
    page_title="Retiro Internacional TBUCF-2024",
    page_icon="🌎",
    layout="wide",
)

page_names_to_funcs = {
    "Consignaciones": registries,
    "Inscritos": attendants,
    "Desembolsos": payments,
    "Pendientes": pendings,
}
page_names = page_names_to_funcs.keys()

if check_password():
    st.title(":earth_americas: Retiro Internacional TBUCF-2024")
    selected_page: str = st.sidebar.selectbox("Selecciona una página", page_names)
    page_names_to_funcs[selected_page]()
