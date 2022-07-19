# Generated by Django 3.2.2 on 2022-07-15 07:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pockets', '0007_transactioncategory_unique_name'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='transactioncategory',
            name='unique_name',
        ),
        migrations.AlterUniqueTogether(
            name='transactioncategory',
            unique_together={('user', 'name')},
        ),
    ]
