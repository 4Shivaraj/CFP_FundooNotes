from multiprocessing.connection import Client
from rest_framework.reverse import reverse
from rest_framework import status
import pytest
from notes_log import get_logger

lg = get_logger(name="PyTest_User", file_name="notes_log")

"""
* By default python prevents database access, To enable the access from the database,
    that is why we are using @pytest.mark.django_db decorator
* we are specifying duplicates in every function, to remove duplication 
    (voilating dry concept) we are creating a fixtures in conftest.py, this fixtures 
    are automatically loads without explicitly import this module
* each time pytest is running in every function, it will treat database as blank
"""


class TestUser:
    @pytest.mark.django_db
    def test_if_user_registered_return_201(self, client, headers, registration_data):
        """
        Testing user if registered should return 201 status code
        """
        try:
            # Arrange
            data = registration_data
            # Act
            url = reverse('register')
            response = client.post(url, data, **headers)
            # Assert
            lg.debug(response.status_code)
            assert response.status_code == status.HTTP_201_CREATED
        except Exception as e:
            lg.error(e)

    @pytest.mark.django_db
    def test_if_user_logged_in_return_202(self, client, headers, registration_data):
        """
        Testing user if logged in should return 202 status code
        """
        try:
            # Register
            # Arrange
            data = registration_data
            # Act
            url = reverse('register')
            response = client.post(url, data, **headers)
            # Assert
            assert response.status_code == status.HTTP_201_CREATED

            # Login
            # Arrange
            url = reverse('login')
            login_data = {'username': 'shivaraj', 'password': 'password'}
            # Act
            login_response = client.post(
                url, login_data, **headers)
            # Assert
            lg.debug(login_response.status_code)
            assert login_response.status_code == status.HTTP_202_ACCEPTED
        except Exception as e:
            lg.error(e)

    @pytest.mark.django_db
    def test_if_user_login_is_invalid_return_400(self, client, headers, registration_data):
        """
        Testing user if logged in is invalid should return 400 status code
        """
        try:
            # Register
            # Arrange
            data = registration_data
            # Act
            url = reverse('register')
            response = client.post(url, data, **headers)
            # Assert
            assert response.status_code == status.HTTP_201_CREATED

            # Login
            # Arrange
            url = reverse('login')
            login_data = {'username': 'shivaraj', 'password': '12344'}
            # Act
            login_response = client.post(
                url, login_data, **headers)
            # Assert
            lg.debug(login_response.status_code)
            assert login_response.status_code == status.HTTP_400_BAD_REQUEST
        except Exception as e:
            lg.error(e)
