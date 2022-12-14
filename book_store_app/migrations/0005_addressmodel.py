# Generated by Django 4.1 on 2022-09-12 17:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('book_store_app', '0004_alter_bookmodel_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressModel',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('country', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=250)),
                ('zip_or_posta_code', models.IntegerField()),
                ('phone', models.IntegerField()),
            ],
        ),
    ]
