# Generated by Django 2.2.2 on 2021-03-05 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_mpesatransaction_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='user_id',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
