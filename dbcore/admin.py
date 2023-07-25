from django.contrib import admin

from dbcore.models import (
   User, Expense, ExpenseCategory, ExpenseProperty
)


admin.site.register(User)
admin.site.register(Expense)
admin.site.register(ExpenseCategory)
admin.site.register(ExpenseProperty)
