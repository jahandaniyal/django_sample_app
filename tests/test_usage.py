import json
import pytest

from django.urls import reverse
from rest_framework import status

from tests.helpers import (
    create_usage,
    create_usage_types,
    create_user,
    get_time_now,
    get_user,
    reverse_querystring
)


@pytest.mark.django_db
class TestUsageTypes:

    def test_create_usage_admin(self, api_client_admin):
        api_client, user_id = create_user('Penny')
        usage_type = create_usage_types('Heating', 'kwh', 3.89)

        url = reverse('usages', args=[user_id.id.hex])
        data = json.dumps({"user_id": user_id.id.hex, "usage_type_id": usage_type.id,
                           "usage_at": get_time_now(), "amount": 25})
        response = api_client_admin.post(url, data=data, content_type="application/json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_usage(self):
        api_client, user_id = create_user('Penny')
        usage_type = create_usage_types('Heating', 'kwh', 3.89)

        url = reverse('usages', args=[user_id.id.hex])
        data = json.dumps({"usage_type_id": usage_type.id, "usage_at": get_time_now(), "amount": 25})
        response = api_client.post(url, data=data, content_type="application/json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_usage_wrong_user_fails(self):
        api_client1, user_id1 = create_user('Penny')
        api_client2, user_id2 = create_user('Sheldon')

        usage_type = create_usage_types('Heating', 'kwh', 3.89)

        url = reverse('usages', args=[user_id1.id.hex])
        data = json.dumps({"user_id": user_id1.id.hex, "usage_type_id": usage_type.id,
                           "usage_at": get_time_now(), "amount": 25})
        response = api_client2.post(url, data=data, content_type="application/json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_all_usages_admin(self, api_client_admin):
        usage_type_1 = create_usage_types('Heating', 'kwh', 3.89)
        usage_type_2 = create_usage_types('Electricity', 'kwh', 1.5)
        usage_type_3 = create_usage_types('Water', 'kg', 26.93)

        api_client, user_id = create_user('Penny')

        create_usage(usage_type_id= usage_type_1, user_id=user_id, usage_at=get_time_now(), amount= 50)
        create_usage(usage_type_id= usage_type_2, user_id=user_id, usage_at=get_time_now(), amount= 10)
        create_usage(usage_type_id= usage_type_3, user_id=user_id, usage_at=get_time_now(), amount= 30)

        url = reverse_querystring('usages', args=[user_id.id.hex],  query_kwargs={'limit': 100, 'offset': 0})
        response = api_client_admin.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3

    def test_get_usage_admin(self, api_client_admin):
        usage_type_1 = create_usage_types('Heating', 'kwh', 3.89)
        usage_type_2 = create_usage_types('Electricity', 'kwh', 1.5)

        api_client, user_id = create_user('Penny')

        create_usage(usage_type_id= usage_type_1, user_id=user_id, usage_at=get_time_now(), amount= 50)
        usage = create_usage(usage_type_id= usage_type_2, user_id=user_id,
                             usage_at=get_time_now(), amount= 10)

        url = reverse_querystring('usages', args=[user_id.id.hex], postfix=usage.id,
                                  query_kwargs={'limit': 100, 'offset': 0})
        response = api_client_admin.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['user']['name'] == 'Penny'
        assert response.data['user']['id'] == user_id.id
        assert response.data['usage']['id'] == usage.id
        assert response.data['usage']['name'] == 'Electricity'
        assert response.data['usage']['unit'] == 'kwh'
        assert response.data['usage']['factor'] == 1.5

    def test_get_usage(self):
        usage_type = create_usage_types('Electricity', 'kwh', 1.5)

        api_client, user_id = create_user('Penny')

        usage = create_usage(usage_type_id= usage_type, user_id=user_id,
                             usage_at=get_time_now(), amount= 10)

        url = reverse_querystring('usages', args=[user_id.id.hex], postfix=usage.id,
                                  query_kwargs={'limit': 100, 'offset': 0})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['user']['name'] == 'Penny'
        assert response.data['user']['id'] == user_id.id
        assert response.data['usage']['id'] == usage.id
        assert response.data['usage']['name'] == 'Electricity'
        assert response.data['usage']['unit'] == 'kwh'
        assert response.data['usage']['factor'] == 1.5


    def test_get_usage_wrong_user_fails(self):
        usage_type_1 = create_usage_types('Heating', 'kwh', 3.89)
        usage_type_2 = create_usage_types('Electricity', 'kwh', 1.5)

        api_client_1, user_id_1 = create_user('Penny')
        api_client_2, user_id_2 = create_user('Howard')

        create_usage(usage_type_id= usage_type_1, user_id=user_id_1, usage_at=get_time_now(), amount= 50)
        usage = create_usage(usage_type_id= usage_type_2, user_id=user_id_1,
                             usage_at=get_time_now(), amount= 10)

        url = reverse_querystring('usages', args=[user_id_1.id.hex], postfix=usage.id,
                                  query_kwargs={'limit': 100, 'offset': 0})
        response = api_client_2.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_usage_admin(self, api_client_admin):
        usage_type = create_usage_types('Heating', 'kwh', 3.89)

        api_client, user_id = create_user('Penny')

        usage = create_usage(usage_type_id=usage_type, user_id=user_id, usage_at=get_time_now(), amount=50)

        url = reverse_querystring('usages', args=[user_id.id.hex], postfix=usage.id,
                                  query_kwargs={'limit': 100, 'offset': 0})

        data = json.dumps({"amount": 5.16, "usage_at": get_time_now()})
        response = api_client_admin.put(url, data=data, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert float(response.data['usage']['amount']) == 5.16

    def test_update_usage(self):
        usage_type = create_usage_types('Heating', 'kwh', 3.89)

        api_client, user_id = create_user('Penny')

        usage = create_usage(usage_type_id=usage_type, user_id=user_id, usage_at=get_time_now(), amount=50)

        url = reverse_querystring('usages', args=[user_id.id.hex], postfix=usage.id,
                                  query_kwargs={'limit': 100, 'offset': 0})

        data = json.dumps({"amount": 5.16, "usage_at": get_time_now()})
        response = api_client.put(url, data=data, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert float(response.data['usage']['amount']) == 5.16

    def test_update_usage_wrong_user_fails(self):
        usage_type = create_usage_types('Heating', 'kwh', 3.89)

        api_client_1, user_id_1 = create_user('Penny')
        api_client_2, user_id_2 = create_user('Howard')

        usage = create_usage(usage_type_id=usage_type, user_id=user_id_1, usage_at=get_time_now(), amount=50)

        url = reverse_querystring('usages', args=[user_id_1.id.hex], postfix=usage.id,
                                  query_kwargs={'limit': 100, 'offset': 0})

        data = json.dumps({"amount": 5.16, "usage_at": get_time_now()})
        response = api_client_2.put(url, data=data, content_type='application/json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_all_usages_admin(self, api_client_admin):
        usage_type_1 = create_usage_types('Heating', 'kwh', 3.89)
        usage_type_2 = create_usage_types('Electricity', 'kwh', 1.5)
        usage_type_3 = create_usage_types('Water', 'kg', 26.93)

        api_client, user_id = create_user('Penny')

        create_usage(usage_type_id=usage_type_1, user_id=user_id, usage_at=get_time_now(), amount=50)
        create_usage(usage_type_id=usage_type_2, user_id=user_id, usage_at=get_time_now(), amount=10)
        create_usage(usage_type_id=usage_type_3, user_id=user_id, usage_at=get_time_now(), amount=30)

        url = reverse_querystring('usages', args=[user_id.id.hex], query_kwargs={'limit': 100, 'offset': 0})
        response = api_client_admin.delete(url)
        assert response.status_code == status.HTTP_200_OK

    def test_delete_usage_admin(self, api_client_admin):
        usage_type_1 = create_usage_types('Heating', 'kwh', 3.89)
        usage_type_2 = create_usage_types('Electricity', 'kwh', 1.5)
        usage_type_3 = create_usage_types('Water', 'kg', 26.93)

        api_client, user_id = create_user('Penny')

        create_usage(usage_type_id=usage_type_1, user_id=user_id, usage_at=get_time_now(), amount=50)
        create_usage(usage_type_id=usage_type_2, user_id=user_id, usage_at=get_time_now(), amount=10)
        usage = create_usage(usage_type_id=usage_type_3, user_id=user_id, usage_at=get_time_now(), amount=30)

        url = reverse_querystring('usages', args=[user_id.id.hex], postfix=usage.id,
                                  query_kwargs={'limit': 100, 'offset': 0})
        response = api_client_admin.delete(url)
        assert response.status_code == status.HTTP_200_OK
        url = reverse_querystring('usages', args=[user_id.id.hex], query_kwargs={'limit': 100, 'offset': 0})
        response = api_client_admin.get(url)
        assert len(response.data['results']) == 2

    def test_delete_all_usages(self):
        usage_type_1 = create_usage_types('Heating', 'kwh', 3.89)
        usage_type_2 = create_usage_types('Electricity', 'kwh', 1.5)
        usage_type_3 = create_usage_types('Water', 'kg', 26.93)

        api_client, user_id = create_user('Penny')

        create_usage(usage_type_id=usage_type_1, user_id=user_id, usage_at=get_time_now(), amount=50)
        create_usage(usage_type_id=usage_type_2, user_id=user_id, usage_at=get_time_now(), amount=10)
        create_usage(usage_type_id=usage_type_3, user_id=user_id, usage_at=get_time_now(), amount=30)

        url = reverse_querystring('usages', args=[user_id.id.hex], query_kwargs={'limit': 100, 'offset': 0})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_200_OK

    def test_delete_usage(self):
        usage_type_1 = create_usage_types('Heating', 'kwh', 3.89)
        usage_type_2 = create_usage_types('Electricity', 'kwh', 1.5)
        usage_type_3 = create_usage_types('Water', 'kg', 26.93)

        api_client, user_id = create_user('Penny')

        create_usage(usage_type_id=usage_type_1, user_id=user_id, usage_at=get_time_now(), amount=50)
        create_usage(usage_type_id=usage_type_2, user_id=user_id, usage_at=get_time_now(), amount=10)
        usage = create_usage(usage_type_id=usage_type_3, user_id=user_id, usage_at=get_time_now(), amount=30)

        url = reverse_querystring('usages', args=[user_id.id.hex], postfix=usage.id,
                                  query_kwargs={'limit': 100, 'offset': 0})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        url = reverse_querystring('usages', args=[user_id.id.hex], query_kwargs={'limit': 100, 'offset': 0})
        response = api_client.get(url)
        assert len(response.data['results']) == 2

    def test_delete_usage_wrong_user_fails(self):
        usage_type_1 = create_usage_types('Heating', 'kwh', 3.89)
        usage_type_2 = create_usage_types('Electricity', 'kwh', 1.5)
        usage_type_3 = create_usage_types('Water', 'kg', 26.93)

        api_client_1, user_id_1 = create_user('Penny')
        api_client_2, user_id_2 = create_user('Howard')

        create_usage(usage_type_id=usage_type_1, user_id=user_id_1, usage_at=get_time_now(), amount=50)
        create_usage(usage_type_id=usage_type_2, user_id=user_id_1, usage_at=get_time_now(), amount=10)
        usage = create_usage(usage_type_id=usage_type_3, user_id=user_id_1, usage_at=get_time_now(), amount=30)

        url = reverse_querystring('usages', args=[user_id_1.id.hex], postfix=usage.id,
                                  query_kwargs={'limit': 100, 'offset': 0})
        response = api_client_2.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        url = reverse_querystring('usages', args=[user_id_1.id.hex], query_kwargs={'limit': 100, 'offset': 0})
        response = api_client_1.get(url)
        assert len(response.data['results']) == 3
