import streamlit as st

GREETING = """
¡Hola, {name}! Bienvenido a nuestro retiro IronRunner: No dejes de correr. Estamos muy felices de contar con tu participación y esperamos que pases un tiempo increíble.

A continuación, te presentamos la información del equipo al que pertenences:

- **Equipo:** {team}
- **Confidente de los hombres:** {male_captain}
- **Confidente de las mujeres:** {female_captain}

Cuando llegues a TierraAlta, busca el logo de tu equipo en el auditorio principal, en donde te estará esperando el resto del equipo. ¡Que Dios use grandemente este retiro en tu vida!
"""


class Person:
    def __init__(
        self, id: int, name: str, team: str, male_captain: str, female_captain: str, alias: str
    ) -> None:
        self.id = id
        self.name = name.strip().title()
        self.team = team
        self.male_captain = male_captain
        self.female_captain = female_captain
        self.alias = alias

    def __str__(self):
        return GREETING.format(
            name=self.name,
            team=self.team,
            male_captain=self.male_captain,
            female_captain=self.female_captain,
        )


def is_registered(id: int, registered_ids: set[int]) -> bool:
    """Check if the id entered by the user is registered or not"""
    return id in registered_ids
