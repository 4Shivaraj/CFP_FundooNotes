import pytest
from rest_framework.reverse import reverse


@pytest.fixture
def headers():
    return {"content_type": 'application/json'}


@pytest.fixture
def registration_data():
    return {'username': 'shivaraj', 'password': 'password', 'email': '4shivaraj.gowda@gmail.com',
            'phone_number': 98645678, 'location': 'bangalore'}


@pytest.fixture
def user_id(client, registration_data):
    header = {"content_type": 'application/json'}
    user_data = registration_data
    url = reverse('register')
    response = client.post(url, user_data, **header)
    return response.data.get('data').get('id')
