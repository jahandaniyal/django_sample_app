import json
import pytest

from django.urls import reverse
from rest_framework import status

from tests.helpers import create_user, create_usage_types, get_user


@pytest.mark.django_db
class TestUsageTypes:

    def test_create_usage_type_admin(self, api_client_admin):
        url = reverse('usage_types')
        data = json.dumps({"name": "Heating", "unit": "kwh", "factor": 3.89})
        response = api_client_admin.post(url, data=data, content_type="application/json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_all_usage_types_admin(self, api_client_admin):
        create_usage_types('Heating', 'kwh', 3.89)
        create_usage_types('Water', 'kg', 26.93)
        create_usage_types('Electricity', 'kwh', 1.5)

        url_get = reverse('usage_types')

        response = api_client_admin.get(url_get)
        assert len(response.data['Usage Types']) == 3

    def test_get_usage_type_admin(self, api_client_admin):
        usage_type = create_usage_types('Heating', 'kwh', 3.89)
        url = reverse('usage_type', args=[usage_type.id])
        response = api_client_admin.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Heating'
        assert response.data['unit'] == 'kwh'
        assert response.data['factor'] == 3.89

    def test_update_usage_type_admin(self, api_client_admin):
        usage_type = create_usage_types('Heating', 'kwh', 3.89)
        url = reverse('usage_type', args=[usage_type.id])

        data = json.dumps({"name": "Heating", "unit": "m3", "factor": 5.16})
        response = api_client_admin.put(url, data=data, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Heating'
        assert response.data['unit'] == 'm3'
        assert float(response.data['factor']) == 5.16

    def test_delete_usage_type_admin(self, api_client_admin):
        usage_type = create_usage_types('Heating', 'kwh', 3.89)
        url = reverse('usage_type', args=[usage_type.id])

        response = api_client_admin.delete(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_usage_type(self):
        usage_type = create_usage_types('Heating', 'kwh', 3.89)
        api_client, user_id = create_user('Penny')

        url = reverse('usage_type', args=[usage_type.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Heating'
        assert response.data['unit'] == 'kwh'
        assert response.data['factor'] == 3.89