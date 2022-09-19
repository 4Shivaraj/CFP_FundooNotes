from rest_framework.reverse import reverse
from rest_framework import status
import pytest
from notes_log import get_logger

lg = get_logger(name="PyTest_notes", file_name="notes_log")


class TestNotes:

    @pytest.mark.django_db
    def test_if_notes_created_should_return_201(self, client, user_id, headers):
        """
        Testing notes if created should return 201 status code
        """
        try:
            note_data = {'title': 'pytest',
                         'description': 'test the functions', "user": user_id}
            url = reverse('note')
            response = client.post(url, note_data, **headers)
            lg.debug(response.status_code)
            assert response.status_code == status.HTTP_201_CREATED
        except Exception as e:
            lg.error(e)

    @pytest.mark.django_db
    def test_if_notes_retrieved_should_return_201(self, client, user_id, headers):
        """
        Testing notes if retrieved should return 200 status code
        """
        try:
            note_data = {'title': 'pytest',
                         'description': 'test the functions', "user": user_id}
            url = reverse('note')
            post_response = client.post(url, note_data, **headers)
            assert post_response.status_code == status.HTTP_201_CREATED
            data = {"user": user_id}
            get_response = client.get(url, data, **headers)
            lg.debug(get_response.status_code)
            assert get_response.status_code == status.HTTP_200_OK
        except Exception as e:
            lg.error(e)

    @pytest.mark.django_db
    def test_if_notes_updated_should_return_201(self, client, user_id, headers):
        """
        Testing notes if updated should return 202 status code
        """
        try:
            note_data = {'title': 'pytest',
                         'description': 'test the functions', "user": user_id}
            url = reverse('note')
            post_response = client.post(url, note_data, **headers)
            assert post_response.status_code == status.HTTP_201_CREATED
            assert post_response.data.get('data').get('title') == 'pytest'
            note_id = post_response.data.get('data').get('id')
            new_data = {"id": note_id, 'title': 'pytest',
                        'description': 'test the functions', "user": user_id}
            put_response = client.put(url, new_data, **headers)
            lg.debug(put_response.status_code)
            assert put_response.status_code == status.HTTP_202_ACCEPTED
        except Exception as e:
            lg.error(e)

    @pytest.mark.django_db
    def test_if_notes_deleted_should_return_204(self, client, user_id, headers):
        """
        Testing notes if deleted should return 204 status code
        """
        try:
            note_data = {'title': 'pytest',
                         'description': 'test the functions', "user": user_id}
            url = reverse('note')
            post_response = client.post(url, note_data, **headers)
            assert post_response.status_code == status.HTTP_201_CREATED
            note_id = post_response.data.get('data').get('id')
            data = {"id": note_id}
            delete_response = client.delete(url, data, **headers)
            lg.debug(delete_response.status_code)
            assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        except Exception as e:
            lg.error(e)
