# Generated by Django 5.1.3 on 2025-02-14 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swishcoin', '0003_blockchain'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='mined',
            field=models.BooleanField(default=False),
        ),
    ]
