# Generated by Django 4.2.1 on 2023-05-19 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubNow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('end', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('sub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_history', to='manager_app.subscription')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subsriptions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
