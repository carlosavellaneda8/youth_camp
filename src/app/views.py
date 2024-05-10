import streamlit as st
import pandas as pd
from data.etl import DataMapper
from data.transform_data import create_person_summary


def attendants(data: DataMapper):
    st.markdown("## Inscritos")

    if data.mapped is False:
        data.map()

    summary_data = create_person_summary(data=data)
    st.write(summary_data)

    st.markdown(f"""
    ### Resumen:

    **Cantidad de inscritos:** {summary_data.shape[0]}

    **Valor recaudado:** ${summary_data["Valor Abono"].sum():,.0f}
    """)


def weekly_summary(data: DataMapper):
    st.markdown("## Reporte semanal")

    registries_data = data.data
    registries_data["Created"] = pd.to_datetime(registries_data["Created"])
    registries_data["week"] = registries_data["Created"] - pd.to_timedelta(
        registries_data["Created"].dt.dayofweek, unit="d"
    )
    registries_data["week"] = registries_data["week"].dt.strftime("%Y-%m-%d")
    week_data = registries_data.groupby("week")["Valor Abono"].sum()
    st.bar_chart(week_data)
    st.table(week_data.reset_index())


def registries(data: DataMapper):
    st.markdown("## Registros de todas las consignaciones")

    registries_data = data.data
    st.write(registries_data.drop(
        columns=["Comprobante de pago", "Last Modified By", "Last Modified"]
    ))

def payments(data: DataMapper):
    st.markdown("## Desembolsos")


def pendings(data: DataMapper):
    st.markdown("## Pendientes")
