import pytest
import json

from mixer.backend.django import mixer

from django.urls import reverse
from django.contrib.auth import login


def test_user_registration_successfull(db, api):
    """Test UserRegistration view - success"""

    request_data = {
        "email": "test@mail.com",
        "chat_id": 1234567890,
        "password": "test_pass123"
    }
    response = api.post(reverse('user_management:user_registration'), data=request_data)

    assert response.data['id'] == 1
    assert response.data['email'] == request_data['email']
    assert response.data['chat_id'] == request_data['chat_id']
    assert 'password' not in response.data.keys()


def test_user_registration_unsuccessfull(db, api):
    """Test UserRegistration view - failure"""

    request_data = {
        "test": "Invalid data!"
    }
    response = api.post(reverse('user_management:user_registration'), data=request_data)
    
    assert response.status_code == 400


def test_user_login_successfull(db, api):
    """Test UserLogin view - success"""
    
    user = mixer.blend('dbcore.User')
    user.set_password('secretpass')
    user.save()

    request_data = {
        "email": user.email,
        "password": 'secretpass'
    }
    response = api.post(reverse('user_management:user_login'), data=request_data)

    assert response.data['login'] == True


def test_user_login_unsuccessfull(db, api):
    """Test UserLogin view - failure"""
    
    user = mixer.blend('dbcore.User', email='test@mail.ru')
    user.set_password('secretpass')
    user.save()

    request_data = {
        "email": 'ttttt@mail.mail',
        "password": '123456'
    }
    response = api.post(reverse('user_management:user_login'), data=request_data)

    assert response.status_code == 500


def test_get_user_info_successful(api_login):
    """Test GetUserInfo view - success"""

    api, user = api_login

    request_data = {
        "id": 1
    }
    response = api.generic(method='GET', 
                           path=reverse('user_management:get_user_info'), 
                           data=json.dumps(request_data), 
                           content_type='application/json')

    assert response.data['email'] == user.email


def test_user_logout(api_login):

    api, _ = api_login
    response = api.generic(method='GET', 
                           path=reverse('user_management:user_logout'), 
                           content_type='application/json')

    assert response.data['logout'] == True