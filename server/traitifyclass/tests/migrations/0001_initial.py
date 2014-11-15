# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first', models.CharField(max_length=100)),
                ('last', models.CharField(max_length=100)),
                ('test_id', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
