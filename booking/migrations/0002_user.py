# Generated by Django 4.2.7 on 2024-01-08 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('user_information', models.JSONField()),
                ('datetime', models.DateTimeField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment', models.CharField(max_length=255)),
            ],
        ),
    ]