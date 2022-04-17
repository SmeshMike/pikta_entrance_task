import os
import sys
from unittest.mock import patch

import pytest
from requests.exceptions import RequestException, Timeout

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(SCRIPT_DIR, ".."))

import http_requests as hr


@patch("requests.post")
def test_get_payment_details_valid_data(mock_run):
    mock_run.return_value.status_code = 200
    mock_run.return_value.text = '{"payeeDetails": {"ha": {"Haha": "he"}}}'
    assert hr.get_payment_details(1, 2) == {"ha": {"Haha": "he"}}


@patch("requests.post")
def test_get_payment_details_request_excetpion(mock_run):
    mock_run.side_effect = RequestException()
    with pytest.raises(RequestException):
        hr.get_payment_details(1, 2)


@patch("requests.post")
def test_get_payment_details_timout_excetpion(mock_run):
    mock_run.side_effect = Timeout()
    with pytest.raises(Timeout):
        hr.get_payment_details(1, 2)
