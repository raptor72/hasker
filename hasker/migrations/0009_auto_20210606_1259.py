# Generated by Django 2.2.17 on 2021-06-06 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hasker', '0008_auto_20210219_1816'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['-date_create']},
        ),
    ]