# Generated by Django 2.2.17 on 2021-02-14 17:07

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hasker', '0005_auto_20210209_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='content',
            field=ckeditor.fields.RichTextField(db_index=True),
        ),
    ]