# Generated by Django 2.1 on 2018-08-29 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('type', models.IntegerField(choices=[(1, 'ABSA'), (2, 'NER'), (3, 'BC'), (4, 'MCC')], default=1)),
                ('dbtype', models.IntegerField(choices=[(1, 'MONGO'), (2, 'MYSQL')], default=1)),
                ('dburi', models.CharField(max_length=512)),
                ('content_field', models.CharField(max_length=128)),
                ('sort_field', models.CharField(max_length=128)),
                ('sort_type', models.IntegerField(choices=[(1, 'DESC'), (2, 'ASC')], default=1)),
                ('limit', models.IntegerField(default=-1)),
                ('lastid', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'project',
            },
        ),
    ]
