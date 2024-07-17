import streamlit as st
from data.etl import AirtableDataExtractor

GREETING = """
¡Hola, {name}! Bienvenido a nuestro retiro IronRunner: No dejes de correr.

Durante el retiro, harás parte del equipo {team}, y tendrás a tu disposición las siguientes personas que estarán dispuestos a ayudarte en lo que sea que necesites:

- {male_captain}
- {female_captain}

Cuando llegues a TierraAlta, busca el logo de tu equipo en el hangar. ¡Que Dios use grandemente este retiro en tu vida!
"""


class Person:
    def __init__(
        self, id: int, name: str, team: str, male_captain: str, female_captain: str, alias: str
    ) -> None:
        self.id = id
        self.name = name
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


@st.cache_data
def get_teams_data() -> list[dict]:
    """Retrieve the teams data"""
    etl = AirtableDataExtractor(api_token=st.secrets.airtable.token)
    records = etl.get_records(
        base_id=st.secrets.airtable.teams_base,
        table_name=st.secrets.airtable.teams_table,
    )
    records = [record["fields"] for record in records]
    return records


@st.cache_data
def get_team_info(team: str, team_metadata: list[dict]) -> tuple[str, str, str]:
    """Get the captains of a team"""
    team = [team_info for team_info in team_metadata if team_info["Equipo"] == team][0]
    male_captain = team["Confidente Hombre"]
    female_captain = team["Confidente Mujer"]
    alias = team["Alias"]
    return male_captain, female_captain, alias


@st.cache_data
def create_teams_dict(team_data: list[dict], team_metadata: list[dict]) -> dict:
    """Turn the teams data into a dict"""
    teams_dict = {}
    for record in team_data:
        if record.get("Número Documento", None):
            id = int(record["Número Documento"])
            name = record["Nombres"]
            team = record["Equipo"]
            male_captain, female_captain, alias = get_team_info(team=team, team_metadata=team_metadata)
            teams_dict[id] = {
                "id": id,
                "name": name,
                "team": team,
                "male_captain": male_captain,
                "female_captain": female_captain,
                "alias": alias,
            }

    return teams_dict


@st.cache_data
def get_all_ids(data: list[dict]) -> set[int]:
    ids = []
    for record in data:
        id = record.get("Número Documento", None)
        if id:
            ids.append(int(id))
        else:
            print(f"ID not found for record {record}")
    return ids


@st.cache_data
def get_teams_metadata() -> list[dict]:
    """Retrieve the teams metadata"""
    etl = AirtableDataExtractor(api_token=st.secrets.airtable.token)
    records = etl.get_records(
        base_id=st.secrets.airtable.teams_base,
        table_name=st.secrets.airtable.teams_metadata_table,
    )
    records = [record["fields"] for record in records]
    return records


team_records = get_teams_data()
team_metadata = get_teams_metadata()
registered_ids = get_all_ids(data=team_records)
teams_dict = create_teams_dict(team_data=team_records, team_metadata=team_metadata)

st.image("src/app/imgs/logo.png")

id = st.number_input(label="Ingresa tu número de documento", value=None, format="%i", step=1)
if id:
    if is_registered(id=id, registered_ids=registered_ids):
        user = Person(**teams_dict[id])
        st.markdown(user)
        st.image(f"src/app/imgs/{user.alias}.png")
    else:
        st.markdown("Pailas papi")
