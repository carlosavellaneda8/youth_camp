import streamlit as st
import pandas as pd
from app.utils import create_ministries_filter, create_churches_filter
from data.etl import DataMapper
from data.transform_data import create_person_summary, filter_data


def home():
    md_text = """## Inicio

Bienvenido al dashboard de seguimiento de nuestro retiro internacional de jóvenes.

Selecciona en el menú de la izquierda la opción que desees.
    """
    st.markdown(md_text)


def attendants(data: DataMapper):
    st.markdown("## Inscritos")

    dataset, main_filter = create_ministries_filter(data=data)
    if main_filter == "Obra/Iglesia Hija":
        dataset = create_churches_filter(data=dataset)
    summary_data = create_person_summary(data=dataset)
    st.write(summary_data)

    st.markdown(f"""
    ### Resumen:

    **Cantidad de inscritos:** {summary_data.shape[0]}

    **Valor recaudado:** ${summary_data["Valor Abono"].sum():,.0f}
    """)


def weekly_summary(data: DataMapper):
    st.markdown("## Reporte semanal")

    dataset, main_filter = create_ministries_filter(data=data)
    if main_filter == "Obra/Iglesia Hija":
        dataset = create_churches_filter(data=dataset)
    dataset.unmap()
    registries_data = dataset.data
    registries_data["week"] = registries_data["Created"] - pd.to_timedelta(
        registries_data["Created"].dt.dayofweek, unit="d"
    )
    registries_data["week"] = registries_data["week"].dt.strftime("%Y-%m-%d")
    week_data = registries_data.groupby("week")["Valor Abono"].sum()
    st.bar_chart(week_data)
    st.table(week_data.reset_index())


def registries(data: DataMapper):
    st.markdown("## Registros de todas las consignaciones")

    dataset, main_filter = create_ministries_filter(data=data)
    if main_filter == "Obra/Iglesia Hija":
        dataset = create_churches_filter(data=dataset)
    dataset.unmap()
    registries_data = dataset.data
    st.write(
        registries_data.drop(
            columns=["Comprobante de pago", "Last Modified By", "Last Modified"]
        ).reset_index(drop=True)
    )


def payments(data: DataMapper):
    st.markdown("## Desembolsos")


def pendings(data: DataMapper):
    st.markdown("## Pendientes")
