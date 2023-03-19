from pytest_voluptuous import S
from schemas.resources import single_resource_schema, list_resource_schema
import logging
from utils.base_session import BaseSession

reqres = BaseSession('https://reqres.in/')


def test_create_user():
    data = {'name': 'Anna', 'job': 'star'}
    response = reqres.post('api/users', data=data)
    print(response.text)

    assert response.status_code == 201


def test_update_user():
    data = {'job': 'super star'}
    response = reqres.put('api/users/2', data=data)
    print(response.text)

    assert response.status_code == 200
    assert response.json()['job'] == 'super star'


def test_delete_user():
    response = reqres.delete('api/users/2')

    assert response.status_code == 204


def test_successful_user_registration():
    data = {'email': 'eve.holt@reqres.in', 'password': 'pistol'}
    response = reqres.post('api/register', data=data)
    token = response.json().get('token')

    assert response.status_code == 200
    assert len(token) != 0


def test_unsuccessful_login():
    data = {'email': 'vishny@user'}
    response = reqres.post('api/login', data=data)
    error = response.json()['error']
    print(error)

    assert response.status_code == 400
    assert error == 'Missing password'


def test_get_resource_schema():
    response = reqres.get('api/unknown/2')

    assert response.status_code == 200
    assert S(single_resource_schema) == response.json()


def test_get_list_of_recources_schema():
    response = reqres.get('api/unknown')

    assert response.status_code == 200
    assert S(list_resource_schema) == response.json()


def test_resources_per_page():
    response = reqres.get('api/unknown', params={'page': 1})
    per_page = response.json()['per_page']
    data = response.json()['data']
    logging.info(response.json())

    assert per_page == 6 and len(data) == 6