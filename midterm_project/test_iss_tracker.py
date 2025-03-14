import pytest
import math
from iss_tracker import range_data, data_set_closest, average_speed

mock_data = [
    {
        "EPOCH": "2025-052T12:42:35.002Z",
        "X": {"#text": "6789450.123"},
        "Y": {"#text": "-123456.789"},
        "Z": {"#text": "3456789.456"},
        "X_DOT": {"#text": "-2.34567"},
        "Y_DOT": {"#text": "5.67890"},
        "Z_DOT": {"#text": "-0.98765"}
    },
    {
        "EPOCH": "2025-053T13:00:10.123Z",
        "X": {"#text": "6789123.567"},
        "Y": {"#text": "-120000.345"},
        "Z": {"#text": "3457000.891"},
        "X_DOT": {"#text": "-2.34678"},
        "Y_DOT": {"#text": "5.67999"},
        "Z_DOT": {"#text": "-0.98876"}
    },
    {
        "EPOCH": "2025-054T14:15:45.567Z",
        "X": {"#text": "6788800.890"},
        "Y": {"#text": "-118000.567"},
        "Z": {"#text": "3457500.123"},
        "X_DOT": {"#text": "-2.34789"},
        "Y_DOT": {"#text": "5.68088"},
        "Z_DOT": {"#text": "-0.98987"}
    },
    {
        "EPOCH": "2025-055T15:30:20.789Z",
        "X": {"#text": "6788500.234"},
        "Y": {"#text": "-115000.678"},
        "Z": {"#text": "3458000.456"},
        "X_DOT": {"#text": "-2.34890"},
        "Y_DOT": {"#text": "5.68177"},
        "Z_DOT": {"#text": "-0.99098"}
    }
]

def test_range_data():
    earliest, latest = range_data(mock_data)
    assert earliest == mock_data[0]['EPOCH']
    assert latest == mock_data[3]['EPOCH']

    # Testing invalid data
    with pytest.raises(ValueError, match="Invalid Time entered"):
        range_data([{"EPOCH": "None", "X": {"#text": "None"}, "Y": {"#text": "None"}, "Z": {"#text": "None"},
            "X_DOT": {"#text": "None"}, "Y_DOT": {"#text": "None"}, "Z_DOT": {"#text": "None"},}])

def test_data_set_closest():
    ans = data_set_closest(mock_data)
    comparison = []
    for key in list_data[index_of].keys():
        if(key == 'EPOCH'):
            comparison.append(list_data[index_of][key])
        else:
            comparison.append(list_data[index_of][key]['#text'])
    assert ans == comparison

    # Edge Case: Empty list
    with pytest.raises(IndexError):
        data_set_closest([], "EPOCH")

    # AI helped create this edge case
    # Edge Case: Missing Key
    invalid_data = [{"TIME": "2025-052T12:42:35.002Z"}]  # Wrong key name
    with pytest.raises(KeyError):
        data_set_closest(invalid_data, "EPOCH")

    # Edge Case: Single Data Point
    single_data = [mock_data[0]]
    single_expected = [mock_data[0]["EPOCH"]] + [mock_data[0][key]["#text"] for key in ["X", "Y", "Z", "X_DOT", "Y_DOT", "Z_DOT"]]
    
    assert data_set_closest(single_data, "EPOCH") == single_expected, "Test failed: Single data point should return itself"

def test_average_speed():
    closest = data_set_closest(mock_data)
    test_av_sp, test_ins_sp = average_speed(mock_data, closest)
    actual_ins_sp = math.sqrt((2.34567 ** 2) + (5.67890 ** 2) + (0.98765 ** 2))
    actual_av_sp = 6.22535
    tolerance = .1
    assert abs(test_av_sp - actual_av_sp) <= tolerance
    assert abs(test_ins_sp - actual_ins_sp) <= tolerance

    # AI helped create this case
    with pytest.raises(ZeroDivisionError):
        average_speed([], closest_data)
    
    # AI helped create this case
    single_data = [mock_data[0]]
    expected_single_avg_speed = calculate_speed(single_data[0]["X_DOT"]["#text"], single_data[0]["Y_DOT"]["#text"], single_data[0]["Z_DOT"]["#text"])
    assert average_speed(single_data, closest_data) == (expected_single_avg_speed, expected_inst_speed), "Test failed: Single data point case"




