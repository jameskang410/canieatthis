# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('food', models.CharField(max_length=50, blank=True, null=True)),
                ('can_eat', models.CharField(max_length=10, blank=True, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'user_table',
            },
        ),
    ]
