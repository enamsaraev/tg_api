# Generated by Django 4.2.3 on 2023-07-11 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbcore', '0004_remove_expense_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensecategoryproperty',
            name='expense_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
