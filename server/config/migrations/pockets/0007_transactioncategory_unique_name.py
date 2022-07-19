# Generated by Django 3.2.2 on 2022-07-13 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pockets', '0006_alter_transactioncategory_name'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='transactioncategory',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_name'),
        ),
    ]