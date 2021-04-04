# Generated by Django 2.2.2 on 2021-04-04 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20210331_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_id', models.CharField(max_length=6, unique=True)),
                ('amount_off', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('currency', models.CharField(blank=True, max_length=3, null=True)),
                ('created', models.PositiveIntegerField()),
                ('duration', models.CharField(choices=[('once', 'once'), ('repeating', 'repeating'), ('forever', 'forever')], default='once', max_length=32)),
                ('duration_in_months', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=32)),
                ('percent_off', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('livemode', models.BooleanField(default=False)),
                ('max_redemptions', models.PositiveSmallIntegerField(default=1)),
                ('times_redeemed', models.PositiveSmallIntegerField(default=0)),
                ('redeem_by', models.PositiveSmallIntegerField()),
                ('valid', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(max_length=128)),
                ('applied', models.BooleanField(default=False)),
                ('date_applied', models.DateTimeField(blank=True, null=True)),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Coupon')),
            ],
        ),
    ]