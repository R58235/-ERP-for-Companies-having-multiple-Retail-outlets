# Generated by Django 4.1 on 2022-09-07 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_shop_address_alter_shop_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='cancelled',
            field=models.CharField(default='NO', max_length=3),
        ),
    ]