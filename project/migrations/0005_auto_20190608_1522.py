# Generated by Django 2.1.5 on 2019-06-08 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20190606_2123'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='candidate',
            unique_together={('election', 'name')},
        ),
    ]
