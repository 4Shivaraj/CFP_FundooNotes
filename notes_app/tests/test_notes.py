from rest_framework.reverse import reverse
from rest_framework import status
import pytest
from notes_log import get_logger

lg = get_logger(name="PyTest_notes", file_name="notes_log")


class TestNotes:

    @pytest.mark.django_db
    def test_if_notes_created_should_return_201(self, client, registration_data, headers):
        """
        Testing notes if created should return 201 status code
        """
        try:
            # Register
            data = registration_data
            url = reverse('register')
            client.post(url, data)

            # Login
            url = reverse('login')
            login_data = {'username': 'shivaraj',
                          'password': 'password', 'is_verified': True}
            login_response = client.post(
                url, login_data, **headers)
            token = login_response.content["token"]
            token_header = {"content_type": 'application/json', "token": token}

            # Note Creation
            note_data = {'title': 'pytest',
                         'description': 'test the functions'}
            url = reverse('note')
            response = client.post(url, note_data, **token_header)
            lg.debug(response.status_code)
            assert response.status_code == status.HTTP_201_CREATED

        except Exception as e:
            lg.error(e)

    @pytest.mark.django_db
    def test_if_notes_retrieved_should_return_201(self, client, registration_data, headers):
        """
        Testing notes if retrieved should return 200 status code
        """
        try:
            # Register
            data = registration_data
            url = reverse('register')
            client.post(url, data)

            # Login
            url = reverse('login')
            login_data = {'username': 'shivaraj',
                          'password': 'password', 'is_verified': True}
            login_response = client.post(
                url, login_data, **headers)
            token = login_response.content["token"]
            token_header = {"content_type": 'application/json', "token": token}

            # Posting Note
            note_data = {'title': 'pytest',
                         'description': 'test the functions'}
            url = reverse('note')
            client.post(url, note_data, **token_header)

            # Retrieving Note
            get_response = client.get(url, **token_header)
            lg.debug(get_response.status_code)
            assert get_response.status_code == status.HTTP_200_OK
        except Exception as e:
            lg.error(e)

    @pytest.mark.django_db
    def test_if_notes_updated_should_return_201(self, client, registration_data, headers):
        """
        Testing notes if updated should return 202 status code
        """
        try:
            # Register
            data = registration_data
            url = reverse('register')
            client.post(url, data)

            # Login
            url = reverse('login')
            login_data = {'username': 'shivaraj',
                          'password': 'password', 'is_verified': True}
            login_response = client.post(
                url, login_data, **headers)
            token = login_response.content["token"]
            token_header = {"content_type": 'application/json', "token": token}

            # Posting Note
            note_data = {'title': 'pytest',
                         'description': 'test the functions'}
            url = reverse('note')
            post_response = client.post(url, note_data, **token_header)
            note_id = post_response.data.get('data').get('id')

            # Updating Note
            new_data = {"id": note_id, 'title': 'pytest',
                        'description': 'test the functions'}
            put_response = client.put(url, new_data, **token_header)
            lg.debug(put_response.status_code)
            assert put_response.status_code == status.HTTP_202_ACCEPTED
        except Exception as e:
            lg.error(e)

    @pytest.mark.django_db
    def test_if_notes_deleted_should_return_204(self, client, registration_data, headers):
        """
        Testing notes if deleted should return 204 status code
        """
        try:
            # Register
            data = registration_data
            url = reverse('register')
            client.post(url, data)

            # Login
            url = reverse('login')
            login_data = {'username': 'shivaraj',
                          'password': 'password', 'is_verified': True}
            login_response = client.post(
                url, login_data, **headers)
            token = login_response.content["token"]
            token_header = {"content_type": 'application/json', "token": token}

            # Posting Note
            note_data = {'title': 'pytest',
                         'description': 'test the functions'}
            url = reverse('note')
            post_response = client.post(url, note_data, **token_header)
            note_id = post_response.data.get('data').get('id')

            # Deleting Note
            data = {"id": note_id}
            delete_response = client.delete(url, data, **token_header)
            lg.debug(delete_response.status_code)
            assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        except Exception as e:
            lg.error(e)
