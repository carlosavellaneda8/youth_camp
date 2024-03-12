import streamlit as st
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


def payments():
    st.markdown("## Desembolsos")


def pendings():
    st.markdown("## Pendientes")
