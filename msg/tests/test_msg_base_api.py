import pytest
import json

from django.urls import reverse
from mixer.backend.django import mixer

from dbcore.models import Expense


def test_get_user_expense_category(db, api_login):
    """Test retrieving expense category for current user"""

    mixer.cycle(5).blend('dbcore.ExpenseCategory')

    api, user = api_login
    category = mixer.blend('dbcore.ExpenseCategory', user=user)

    request_data = {
        "id": user.id
    }
    response = api.generic(method='GET',
                           path=reverse('msg:get_user_expense_categories'),
                           data=json.dumps(request_data), 
                           content_type='application/json')
    
    assert response.data[0]['name'] == category.name
    assert response.data[0]['description'] == category.description


def test_creation_a_new_category_by_user(db, api_login):

    api, user = api_login
    request_data = {
        "user_id": user.id,
        "name": "test_category",
        "description": "-"
    }
    response = api.post(reverse('msg:create_new_user_category'), data=request_data)

    assert response.data['name'] == request_data['name']
    assert response.data['description'] == request_data['description']


def test_creation_new_user_expense(db, api_login):

    api, user = api_login

    category = mixer.blend('dbcore.ExpenseCategory', name='category_name', user=user)
    request_data = {
        "user_id": user.id,
        "category_name": category.name,
    }

    resonse = api.post(reverse('msg:new_expense_creation'), data=request_data)
    created_category = Expense.objects.get(user=user, category=category)

    assert resonse.status_code == 201
    assert created_category.user == user
    assert created_category.category == category
