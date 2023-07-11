from django.urls import path

from msg.views import (
    GetUserExpenseCategories, CreateNewUserExpenseCategory, 
    CreateNewExpense, CreateNewExpenseProps, CreateFullExpense
)


urlpatterns = [
    path('categories/', GetUserExpenseCategories.as_view(), name='get_user_expense_categories'),
    path('create_category/', CreateNewUserExpenseCategory.as_view(), name='create_new_user_category'),
    path('create_expense/', CreateNewExpense.as_view(), name='new_expense_creation'),
    path('create_expense_props/', CreateNewExpenseProps.as_view(), name='new_expense_category_property_cration'),
    path('create_full_expense/', CreateFullExpense.as_view(), name='create_full_expense'),
]


app_name = 'msg'


