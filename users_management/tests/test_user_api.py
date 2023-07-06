import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model



def test_user_registration_success(db, api):
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