import streamlit as st
from utils import check_password
from data.get_data import get_registries
from app.views import (
    home,
    attendants,
    weekly_summary,
    registries,
    payments,
    pendings,
)

# Set the app's config
st.set_page_config(
    page_title="Retiro Internacional TBUCF-2024",
    page_icon="🌎",
    layout="wide",
)

# Download the data
registries_data, no_refund_amount = get_registries()

# Define the names, functions and arguments
page_names_to_funcs = {
    "Inicio": home,
    "Inscritos": attendants,
    "Reporte semanal": weekly_summary,
    "Consignaciones": registries,
    "Desembolsos": payments,
    "Pendientes": pendings,
}
page_names_to_args = {
    "Inicio": None,
    "Inscritos": {"data": registries_data, "no_refund_amount": no_refund_amount},
    "Reporte semanal": {"data": registries_data},
    "Consignaciones": {"data": registries_data},
    "Desembolsos": {"data": registries_data},
    "Pendientes": {"data": registries_data},
}
page_names = page_names_to_funcs.keys()

# Start the app if the password is correct
if check_password():
    st.title(":earth_americas: Retiro Internacional TBUCF-2024")
    selected_page: str = st.sidebar.selectbox("Selecciona una página", page_names)
    args = page_names_to_args[selected_page]
    if args:
        page_names_to_funcs[selected_page](**args)
    else:
        page_names_to_funcs[selected_page]()
