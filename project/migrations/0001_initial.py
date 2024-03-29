# Generated by Django 2.1.5 on 2019-06-03 20:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='CandidateChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(blank=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Candidate')),
            ],
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=1000)),
                ('begin_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ElectionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secrecy', models.BooleanField()),
                ('candidate_selection_number', models.IntegerField()),
                ('voter_equality', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='OversightBody',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='OversightBodyPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OversightMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('units', models.ManyToManyField(to='project.OversightBody')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Election')),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voting_power', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='VotingUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('parent_unit', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='project.VotingUnit')),
            ],
        ),
        migrations.AddField(
            model_name='voter',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.VotingUnit'),
        ),
        migrations.AddField(
            model_name='voter',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vote',
            name='voter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Voter'),
        ),
        migrations.AddField(
            model_name='oversightbody',
            name='permissions',
            field=models.ManyToManyField(to='project.OversightBodyPermission'),
        ),
        migrations.AddField(
            model_name='oversightbody',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.VotingUnit'),
        ),
        migrations.AddField(
            model_name='election',
            name='base_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.VotingUnit'),
        ),
        migrations.AddField(
            model_name='election',
            name='election_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.ElectionType'),
        ),
        migrations.AddField(
            model_name='candidatechoice',
            name='vote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Vote'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='election',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='project.Election'),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('election', 'voter')},
        ),
        migrations.AlterUniqueTogether(
            name='candidatechoice',
            unique_together={('vote', 'candidate')},
        ),
    ]
