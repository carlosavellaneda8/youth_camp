import streamlit as st
import numpy as np
from data.etl import DataMapper
from data.transform_data import filter_data


def check_password():
    """Returns `True` when the user enters the correct password"""

    def _password_entered() -> bool:
        """Check if the password is correct"""
        if st.session_state["password"] == st.secrets.app["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Password", type="password", on_change=_password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password", type="password", on_change=_password_entered, key="password"
        )
        st.error("Incorrect password!")
        return False

    return True


def create_ministries_filter(data: DataMapper) -> tuple[DataMapper, str]:
    """Filter the data by ministries"""
    ministries = ["Todos"] + data.data["Ministerio/Obra"].drop_duplicates().dropna().tolist()

    with st.sidebar:
        main_filter = st.selectbox("Filtrar por:", ministries)

    data_subset = filter_data(data=data, column_name="Ministerio/Obra", value=main_filter)
    data_subset.map()
    return data_subset, main_filter


def create_churches_filter(data: DataMapper) -> DataMapper:
    """Filter the data by churches"""
    data.unmap()
    churches = data.data["Detalle Obra"].drop_duplicates().dropna().tolist()
    churches.sort()
    churches = ["Todos"] + churches
    with st.sidebar:
        secondary_filter = st.selectbox("Selecciona la obra/iglesia hija:", churches)

    data_subset = filter_data(data=data, column_name="Detalle Obra", value=secondary_filter)
    data_subset.map()
    return data_subset
