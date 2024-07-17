import streamlit as st
from data.etl import AirtableDataExtractor
from app.team_utils import Person


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


def check_id_number() -> bool:
    def id_entered():
        if st.session_state["id_number"] in registered_ids:
            st.session_state["id_correct"] = True
        else:
            st.session_state["id_correct"] = False

    def home_view():
        st.image("src/app/imgs/logo.png")
        st.number_input(
            "Ingresa tu número de documento",
            on_change=id_entered,
            format="%i",
            value=None,
            step=1,
            key="id_number",
        )

    if "id_correct" not in st.session_state:
        home_view()
        return False
    elif not st.session_state["id_correct"]:
        home_view()
        st.error("Documento incorrecto, intenta nuevamente. Si tienes dudas, contáctate con Sebastián Rubiano ([313 4382109](https://wa.me/573134382109))")
        return False
    else:
        return True


team_records = get_teams_data()
team_metadata = get_teams_metadata()
registered_ids = get_all_ids(data=team_records)
teams_dict = create_teams_dict(team_data=team_records, team_metadata=team_metadata)


if (check_id_number()) & ("id_number" in st.session_state):
    id = st.session_state["id_number"]
    user = Person(**teams_dict[id])
    st.image("src/app/imgs/logo.png")
    st.markdown(user)
    if user.alias != "apoyo":
        st.image(f"src/app/imgs/{user.alias}.png")
