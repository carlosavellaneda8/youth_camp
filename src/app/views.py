import streamlit as st
import pandas as pd
from data.get_data import get_registries
from data.transform_data import create_person_summary


def attendants():
    st.markdown("## Inscritos")

    registries_data = get_registries()
    if registries_data.mapped is False:
        registries_data.map()

    summary_data = create_person_summary(data=registries_data)
    st.write(summary_data)

    st.markdown(f"""
    ### Resumen:

    **Cantidad de inscritos:** {summary_data.shape[0]}

    **Valor recaudado:** ${summary_data["Valor Abono"].sum():,.0f}
    """)


def weekly_summary():
    st.markdown("## Reporte semanal")

    registries_data = get_registries().data
    registries_data["Created"] = pd.to_datetime(registries_data["Created"])
    registries_data["week"] = registries_data["Created"] - pd.to_timedelta(registries_data["Created"].dt.dayofweek, unit="d")
    registries_data["week"] = registries_data["week"].dt.strftime("%Y-%m-%d")
    week_data = registries_data.groupby("week")["Valor Abono"].sum()
    st.bar_chart(week_data)
    st.table(week_data.reset_index())


def registries():
    st.markdown("## Registros")

    registries_data = get_registries().data
    st.write(registries_data.drop(
        columns=["Comprobante de pago", "Last Modified By", "Last Modified"]
    ))

def payments():
    st.markdown("## Desembolsos")


def pendings():
    st.markdown("## Pendientes")
