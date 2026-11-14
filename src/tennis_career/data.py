import json
import re
import pandas as pd
import requests


def _fetch_career_matches(player_name):
    """Retrieve a player's raw career match records from Tennis Abstract."""
    player_id = re.sub(r"\s+", "", player_name.strip())
    url = f"https://www.tennisabstract.com/jsmatches/{player_id}Career.js"

    response = requests.get(url, timeout=20)

    if response.status_code == 404:
        raise ValueError(f"Player '{player_name}' was not found.")

    response.raise_for_status()

    match = re.search(
        r"var\s+morematchmx\s*=\s*(\[[\s\S]*?\]);",
        response.text
    )

    if match is None:
        raise ValueError(f"No career match data found for '{player_name}'.")

    return json.loads(match.group(1))


def _create_match_dataframe(matches):
    """Convert raw match records into a DataFrame."""
    columns = {
        0: "match_date",
        4: "result",
        11: "opponent",
        16: "opponent_info",
    }

    df = pd.DataFrame([row[:17] for row in matches])
    df = df.rename(columns=columns)

    return df[list(columns.values())]


def _calculate_player_age(df, birthdate):
    """Calculate the player's age at each match."""
    df = df.copy()

    df["match_date"] = pd.to_datetime(
        df["match_date"], format="%Y%m%d", errors="coerce"
    )

    birthdate = pd.Timestamp(birthdate)

    df["player_age"] = (
        (df["match_date"] - birthdate).dt.days / 365.25
    )

    return df


def _calculate_opponent_age(df, gender):
    """Calculate opponent ages based on player gender."""
    df = df.copy()

    if gender == "female":
        opponent_birthdates = pd.to_datetime(
            df["opponent_info"], format="%Y%m%d", errors="coerce"
        )
        df["opponent_age"] = (
            (df["match_date"] - opponent_birthdates).dt.days / 365.25
        )

    elif gender == "male":
        df["opponent_age"] = pd.to_numeric(
            df["opponent_info"], errors="coerce"
        )

    else:
        raise ValueError("Gender must be 'female' or 'male'.")

    return df


def _calculate_age_difference(df):
    """Calculate the age difference between player and opponent."""
    df = df.copy()

    df["age_difference"] = (
        df["player_age"] - df["opponent_age"]
    )

    return df


def _fetch_player_birthdate(player_name, gender):
    """Fetch a tennis player's birth date from Tennis Abstract."""
    player_id = player_name.replace(" ", "")

    if gender.lower() == "female":
        page = "wplayer.cgi"
    elif gender.lower() == "male":
        page = "player.cgi"
    else:
        raise ValueError("Gender must be 'male' or 'female'")

    url = f"https://www.tennisabstract.com/cgi-bin/{page}?p={player_id}"

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    match = re.search(
        r"var\s+dob\s*=\s*['\"]?(\d{8})",
        response.text
    )

    if match is None:
        raise ValueError(f"Could not find birth date for {player_name}")

    return pd.to_datetime(match.group(1), format="%Y%m%d")


def get_player_matches(player_name, gender):
    """Retrieve a player's matches and calculate age differences."""

    birthdate = _fetch_player_birthdate(player_name, gender)

    matches = _fetch_career_matches(player_name)

    df = _create_match_dataframe(matches)

    df = _calculate_player_age(df, birthdate)

    df = _calculate_opponent_age(df, gender)

    df = _calculate_age_difference(df)

    return df