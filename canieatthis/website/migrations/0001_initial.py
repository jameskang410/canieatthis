# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodTable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('food', models.CharField(blank=True, max_length=50, null=True)),
                ('can_eat', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'food_table',
            },
        ),
    ]
