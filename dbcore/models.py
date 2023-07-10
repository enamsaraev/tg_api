from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fileds):
        """Creates and saves a new user"""

        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fileds)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custon user model that supportsusing email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    chat_id = models.BigIntegerField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    first_name = None
    last_name = None
    username = None

    USERNAME_FIELD = 'email'

    objects = UserManager()


class Expense(models.Model):
    user = models.ForeignKey('User',
                             related_name='expenses',
                             on_delete=models.SET_NULL,
                             null=True)
    category = models.ForeignKey('ExpenseCategory',
                                      related_name='expenses',
                                      on_delete=models.SET_NULL,
                                      null=True)
    date = models.DateField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.date}: {self.user.email}'
    

class ExpenseCategory(models.Model):
    user = models.ForeignKey('User',
                             related_name='expense_categories',
                             on_delete=models.SET_NULL,
                             null=True)
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    description = models.CharField(max_length=255, null=False, blank=False)
    deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    

class ExpenseCategoryProperty(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    expense = models.FloatField()
    description = models.CharField(max_length=255, null=False, blank=False)
    raw_string= models.TextField()
    category = models.ForeignKey('ExpenseCategory',
                                      related_name='expense_category_props',
                                      on_delete=models.SET_NULL,
                                      null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name 
    