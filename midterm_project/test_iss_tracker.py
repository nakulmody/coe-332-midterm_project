import pytest
from unittest.mock import patch, MagicMock
import json
import math
import requests
import redis
from your_module import fetching_data, calc_speed, get_location, get_epochs


# Test fetching data
@pytest.fixture
def mock_redis():
    # Create a mock Redis client
    mock_rd = MagicMock()
    with patch('redis.Redis', return_value=mock_rd):
        yield mock_rd

@pytest.fixture
def mock_requests():
    # Mock requests.get
    with patch('requests.get') as mock_get:
        yield mock_get

def test_fetching_data(mock_redis, mock_requests):
    # Mock the Redis client
    mock_rd = mock_redis

    # Mock the GET request
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'<ndm><oem><body><segment><data><stateVector><X_DOT><#text>0.123</#text></X_DOT></stateVector></data></segment></body></oem></ndm>'
    mock_requests.return_value = mock_response

    fetching_data()

    # Ensure the Redis set method was called with the correct data
    mock_rd.set.assert_called_with("iss_data", json.dumps([{'X_DOT': {"#text": "0.123"}}]))


# Test calc_speed
def test_calc_speed():
    # Test sample data for calculating speed
    list_data = [{'X_DOT': {"#text": "1.0"}, 'Y_DOT': {"#text": "2.0"}, 'Z_DOT': {"#text": "3.0"}}]
    index = 0
    result = calc_speed(list_data, index)
    expected = math.sqrt(1.0**2 + 2.0**2 + 3.0**2)
    assert result == pytest.approx(expected, rel=1e-2)


# Test get_location
@pytest.fixture
def mock_geopy():
    # Mock geopy.geocoders.Nominatim
    with patch('geopy.geocoders.Nominatim') as mock_geopy_class:
        yield mock_geopy_class

@pytest.fixture
def mock_redis_get():
    # Mock Redis get method
    with patch('redis.Redis.get') as mock_get:
        yield mock_get

def test_get_location(mock_redis_get, mock_geopy):
    # Mock Redis data
    mock_redis_get.return_value = json.dumps([{'EPOCH': '2025-001T12:00:00.000Z', 'X': {'#text': '1000'}, 'Y': {'#text': '2000'}, 'Z': {'#text': '3000'}}])

    # Mock geolocator
    mock_geoloc = MagicMock()
    mock_geoloc.reverse.return_value = ["Somewhere, Earth"]
    mock_geopy.return_value = mock_geoloc

    result = get_location('2025-001T12:00:00.000Z')

    expected = "The latitude of the ISS is 0.0. The longitude is 0.0. The altiude is 0.0. The geoposition is Somewhere, Earth\n"
    assert result == expected


# Test get_epochs
@pytest.fixture
def mock_request_args():
    with patch('flask.request.args.get') as mock_get:
        yield mock_get

def test_get_epochs(mock_redis_get, mock_request_args):
    # Mock Redis data
    mock_redis_get.return_value = json.dumps([{'EPOCH': '2025-001T12:00:00.000Z', 'X': {'#text': '1000'}, 'Y': {'#text': '2000'}, 'Z': {'#text': '3000'}}])

    # Mock request args for limit and offset
    mock_request_args.return_value = '1'  # Set the limit to 1 for testing

    result = get_epochs()

    assert len(result) == 1
    assert result[0]['EPOCH'] == '2025-001T12:00:00.000Z'