# Generated by Django 4.2 on 2023-05-17 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ordered_Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateOfOrdeing', models.DateTimeField(auto_now=True)),
                ('nameOfTable', models.CharField(max_length=150)),
                ('productName', models.CharField(max_length=150)),
                ('productCount', models.IntegerField()),
            ],
        ),
    ]