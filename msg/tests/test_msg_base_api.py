import pytest
import json

from django.urls import reverse
from mixer.backend.django import mixer

from dbcore.models import Expense, ExpenseCategory, ExpenseProperty


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
    """Test ategory creation"""

    api, user = api_login
    request_data = {
        "user_id": user.id,
        "name": "test_category",
        "description": "-"
    }
    response = api.post(reverse('msg:create_new_user_category'), data=request_data)

    assert response.data['name'] == request_data['name']
    assert response.data['description'] == request_data['description']


@pytest.mark.parametrize(
        'name, description, status_code', [
            ('', 123, 400),
            (45, '', 400),
            ('', '', 400),
        ]
)
def test_creation_a_new_category_by_user_400(db, api_login, name, description, status_code):
    api, user = api_login
    category = mixer.blend('dbcore.ExpenseCategory')

    request_data = {
        "user_id": user.id,
        "name": name,
        "description": description
    }
    response = api.post(reverse('msg:create_new_user_category'), data=request_data)

    last_category = ExpenseCategory.objects.last()

    assert response.status_code == status_code
    assert last_category.id == category.id


def test_creation_new_user_expense(db, api_login):
    """Test new expense object creation by user"""

    api, user = api_login

    category = mixer.blend('dbcore.ExpenseCategory', name='category_name', user=user)
    request_data = {
        "user_id": user.id,
        "expense_category_name": category.name,
    }

    resonse = api.post(reverse('msg:new_expense_creation'), data=request_data)
    created_category = Expense.objects.get(user=user, category=category)

    assert resonse.status_code == 201
    assert created_category.user == user
    assert created_category.category == category


def test_new_expense_category_property_creation(db, api_login):
    """Test expense data creation"""
    
    api, user = api_login

    category = mixer.blend('dbcore.ExpenseCategory', name='category_name', user=user)
    expense = mixer.blend('dbcore.Expense', user=user, category=category)
    request_data = {
        "name": "тест трата",
        "expense": 273.5,
        "description": "-",
        "raw_string": "тест трата 273.5",
        "expense_id": expense.id
    }

    response = api.post(reverse('msg:new_expense_category_property_cration'), data=request_data)
    created_expense = Expense.objects.filter(category__id=category.id, user__id=user.id).last()
    created_expense_category_property = ExpenseProperty.objects.get(expense_obj__category__name=category.name, expense_obj__user__id=user.id)

    assert response.status_code == 201
    assert created_expense_category_property.name == request_data['name']
    assert created_expense_category_property.expense == request_data['expense']
    assert created_expense_category_property.description == request_data['description']
    assert created_expense_category_property.raw_string == request_data['raw_string']
    assert created_expense_category_property.expense_obj.id == created_expense.id


def test_creating_a_full_user_expense(db, api_login):
    """Test full expense data creation"""

    api, user = api_login

    category = mixer.blend('dbcore.ExpenseCategory', name='some_name', user=user)
    request_data = {
        "user_id": user.id,
        "expense_category_name": category.name,
        "name": "тест трата полная",
        "expense": 456.9,
        "description": "-",
        "raw_string": "тест трата полная 456.9"
    }

    response = api.generic(method='POST', path=reverse('msg:create_full_expense'), data=json.dumps(request_data), content_type='application/json')
    created_expense = Expense.objects.filter(user__id=user.id, category__name=category.name).last()
    created_expense_property = ExpenseProperty.objects.filter(expense_obj__category__name=category.name, expense_obj__id=created_expense.id).last()

    assert response.status_code == 201 

    assert created_expense.user.id == user.id
    assert created_expense.category.id == category.id

    assert created_expense_property.expense_obj.id == created_expense.id
    assert created_expense_property.name == request_data['name']
    assert created_expense_property.expense == request_data['expense']
    assert created_expense_property.description == request_data['description']
    assert created_expense_property.raw_string == request_data['raw_string']