# Generated by Django 2.2.2 on 2021-04-05 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20210405_0707'),
    ]

    operations = [
        migrations.AddField(
            model_name='mpesatransaction',
            name='coupon_code',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='mpesatransaction',
            name='discount_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wallettransaction',
            name='coupon_code',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='wallettransaction',
            name='discount_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
