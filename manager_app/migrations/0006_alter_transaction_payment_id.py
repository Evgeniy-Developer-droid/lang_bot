# Generated by Django 4.2.1 on 2023-05-21 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_app', '0005_alter_subscription_max_words_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='payment_id',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
