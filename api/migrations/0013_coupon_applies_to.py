# Generated by Django 2.2.2 on 2021-04-04 18:35

from django.db import migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20210404_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='applies_to',
            field=picklefield.fields.PickledObjectField(blank=True, editable=False, null=True),
        ),
    ]
