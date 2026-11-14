
import json
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from tennis_career import data


# Sample records provided in the homework instructions.
FEMALE_MATCHES = [
    [
        "19951030", "Canadian Open", "Carpet", "W", "L", "", "",
        "WC", "Q1", "6-1 6-1", "3", "Anne Miller", "149", "7",
        "", "R", "19770119", "", "USA", "0", "", "", "", "",
        "", "", "1995-W-WT-CAN-02A-1995-013"
    ],
    [
        "19970307", "Indian Wells", "Hard", "W", "L", "", "",
        "WC", "Q1", "6-4 6-0", "3", "Alexia Dechaume Balleret",
        "87", "", "", "R", "19700503", "", "FRA", "0", "",
        "", "", "", "", "", "1997-W-WT-USA-02A-1997-006"
    ],
    [
        "19970804", "Manhattan Beach", "Hard", "W", "L", "", "",
        "WC", "Q3", "7-6 4-6 6-3", "3", "Magui Serna", "54",
        "6", "", "L", "19790301", "167", "ESP", "0", "", "",
        "", "", "", "", "1997-W-WT-USA-07A-1997-026"
    ]
]


MALE_MATCHES = [
    [
        "20010910", "Spain F10", "Hard", "S", "L", "", "",
        "WC", "R32", "2-6 7-5 6-2", "3", "Guillermo Platel",
        "731", "", "", "R", "22.264202601", "", "ESP",
        "0", "", "", "", "", "", "", "", "", "", "",
        "", "", "", "", "", "", "", "", "", "",
        "2001-M-FU-ESP-10A-2001-002", "", "1", "1"
    ],
    [
        "20010917", "Seville CH", "Clay", "C", "L", "", "",
        "WC", "R16", "3-6 6-1 6-3", "3", "Stefano Galvani",
        "161", "2", "", "R", "24.2902121834", "178",
        "ITA", "0", "", "", "", "", "", "", "", "",
        "", "", "", "", "", "", "", "", "", "",
        "2", "", "", "", "2001-784-024", "", "2", "2"
    ],
    [
        "20010917", "Seville CH", "Clay", "C", "W", "", "",
        "WC", "R32", "6-4 6-4", "3", "Israel Matos Gil",
        "751", "", "Q", "U", "18.7597535934", "",
        "ESP", "0", "", "", "", "", "", "", "",
        "", "", "", "", "", "", "", "", "", "",
        "", "", "2001-784-015", "", "1", "1"
    ]
]


def mock_javascript(matches):
    """Create a mock Tennis Abstract JavaScript response."""
    response = Mock()
    response.status_code = 200
    response.text = f"var morematchmx = {json.dumps(matches)};"
    return response


@pytest.mark.parametrize(
    "matches,player_name",
    [
        (FEMALE_MATCHES, "Serena Williams"),
        (MALE_MATCHES, "Rafael Nadal")
    ]
)
def test_fetch_career_matches(matches, player_name):
    """Check that both JavaScript formats are parsed correctly."""
    response = mock_javascript(matches)

    with patch.object(data.requests, "get", return_value=response):
        result = data._fetch_career_matches(player_name)

    assert result == matches
    assert len(result) == 3


@pytest.mark.parametrize(
    "matches,expected_opponent",
    [
        (FEMALE_MATCHES, "Anne Miller"),
        (MALE_MATCHES, "Guillermo Platel")
    ]
)
def test_create_match_dataframe(matches, expected_opponent):
    """Check that match fields are extracted correctly."""
    df = data._create_match_dataframe(matches)

    assert len(df) == 3
    assert list(df.columns) == [
        "match_date", "result", "opponent", "opponent_info"
    ]
    assert df["opponent"].iloc[0] == expected_opponent
    assert df["result"].tolist() == ["L", "L", "W"] if (
        matches is MALE_MATCHES
    ) else df["result"].tolist() == ["L", "L", "L"]


def test_calculate_player_age():
    """Check player age calculation using the sample dates."""
    df = data._create_match_dataframe(MALE_MATCHES)
    result = data._calculate_player_age(df, "1986-06-03")

    assert result["player_age"].iloc[0] == pytest.approx(
        15.27, abs=0.02
    )
    assert pd.api.types.is_datetime64_any_dtype(
        result["match_date"]
    )


def test_female_opponent_ages():
    """Check female opponent ages calculated from birthdates."""
    df = data._create_match_dataframe(FEMALE_MATCHES)
    df = data._calculate_player_age(df, "1981-09-26")
    result = data._calculate_opponent_age(df, "female")

    expected = (
        pd.Timestamp("1995-10-30") - pd.Timestamp("1977-01-19")
    ).days / 365.25

    assert result["opponent_age"].iloc[0] == pytest.approx(expected)
    assert result["opponent_age"].iloc[1] > 26
    assert result["opponent_age"].iloc[2] > 18


def test_male_opponent_ages():
    """Check male opponent ages supplied directly in the data."""
    df = data._create_match_dataframe(MALE_MATCHES)
    df = data._calculate_player_age(df, "1986-06-03")
    result = data._calculate_opponent_age(df, "male")

    assert result["opponent_age"].iloc[0] == pytest.approx(
        22.264202601
    )
    assert result["opponent_age"].iloc[1] == pytest.approx(
        24.2902121834
    )
    assert result["opponent_age"].iloc[2] == pytest.approx(
        18.7597535934
    )


def test_calculate_age_difference():
    """Check that age difference equals player minus opponent."""
    df = pd.DataFrame({
        "player_age": [20.0, 30.0],
        "opponent_age": [25.0, 22.0]
    })

    result = data._calculate_age_difference(df)

    assert result["age_difference"].tolist() == [-5.0, 8.0]


def test_invalid_gender():
    """Check that invalid gender inputs raise an error."""
    df = pd.DataFrame({
        "match_date": pd.to_datetime(["2020-01-15"]),
        "opponent_info": ["30"]
    })

    with pytest.raises(ValueError):
        data._calculate_opponent_age(df, "invalid")


@pytest.mark.parametrize(
    "gender,page",
    [("female", "wplayer.cgi"), ("male", "player.cgi")]
)
def test_fetch_player_birthdate(gender, page):
    """Check birthdate parsing and gender-specific URLs."""
    response = Mock()
    response.text = "var dob = 19860603;"

    with patch.object(
        data.requests, "get", return_value=response
    ) as mock_get:
        result = data._fetch_player_birthdate(
            "Test Player", gender
        )

    assert result == pd.Timestamp("1986-06-03")
    assert page in mock_get.call_args.args[0]


@pytest.mark.parametrize(
    "matches,gender,birthdate",
    [
        (FEMALE_MATCHES, "female", "1981-09-26"),
        (MALE_MATCHES, "male", "1986-06-03")
    ]
)
def test_get_player_matches(matches, gender, birthdate):
    """Check the full pipeline using mocked source records."""
    with patch.object(
        data, "_fetch_player_birthdate",
        return_value=pd.Timestamp(birthdate)
    ), patch.object(
        data, "_fetch_career_matches",
        return_value=matches
    ):
        df = data.get_player_matches("Test Player", gender)

    assert len(df) == 3
    assert df["match_date"].notna().all()
    assert df["player_age"].notna().all()
    assert df["opponent_age"].notna().all()
    assert df["age_difference"].notna().all()
    assert (
        df["age_difference"]
        == df["player_age"] - df["opponent_age"]
    ).all()
