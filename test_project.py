import pytest
from unittest.mock import patch
from PIL import Image
from datetime import datetime
from countryinfo import CountryInfo
from project import Person, get_apod, country_info, get_name, get_location, get_birthday, get_today, elapsed

@patch('builtins.input', side_effect=["david scott"])
def test_get_name_case(mock_input):
    assert get_name() == "David Scott"

@patch('builtins.input', side_effect=[""])
def test_get_name_empty(mock_input):
    assert get_name() == "Michael Scott"

@patch('builtins.input', side_effect=["12345", "David Scott"])
def test_get_name_numeric(mock_input, capsys):
    assert get_name() == "David Scott"

    captured = capsys.readouterr()
    assert "Format: Alphabetic characters only" in captured.out

@patch('builtins.input', side_effect=["scranton, united states"])
def test_get_location_case(mock_input):
    assert get_location() == "Scranton, United States"

@patch('builtins.input', side_effect=[""])
def test_get_location_empty(mock_input):
    assert get_location() == "Scranton, United States"

@patch('builtins.input', side_effect=["scranton", "Scranton, United States"])
def test_get_name_city(mock_input, capsys):
    assert get_location() == "Scranton, United States"

    captured = capsys.readouterr()
    assert "Format: City, Country" in captured.out

@patch('builtins.input', side_effect=[""])
def test_get_birthday_empty(mock_input):

    mock_today = datetime(2024, 4, 14)

    with patch('project.get_today', return_value=mock_today):

        assert get_birthday() == "2024-04-13"

def test_apod():

    name = "Michael Scott"
    birthday = "1996-12-20"
    location = "Scranton, United States"

    with patch("project.get_name", return_value=name), \
        patch("project.get_birthday", return_value=birthday), \
        patch("project.get_location", return_value=location):

        person = Person()

        apod, title, explanation = get_apod(person)

        assert isinstance(apod, Image.Image)
        assert isinstance(title, str)
        assert isinstance(explanation, str)

def test_elapsed():

    mock_today = datetime(2024, 4, 14)

    name = "Michael Scott"
    birthday = "1996-12-20"
    location = "Scranton, United States"

    with patch('project.get_today', return_value=mock_today), \
        patch("project.get_name", return_value=name), \
        patch("project.get_birthday", return_value=birthday), \
        patch("project.get_location", return_value=location):

        person = Person()

        assert elapsed(person) == 239448

def test_country_info():

    name = "Michael Scott"
    birthday = "1996-12-20"
    location = "Scranton, United States"

    with patch("project.get_name", return_value=name), \
        patch("project.get_birthday", return_value=birthday), \
        patch("project.get_location", return_value=location):

        person = Person()

        cnt, pop, reg = country_info(person)

        assert cnt == "United States"
        assert pop == 319259000
        assert reg == "Northern America"
