# Generated by Django 2.2.2 on 2021-04-04 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_remove_coupon_applies_to'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='discount',
            unique_together={('customer_id', 'coupon')},
        ),
    ]
