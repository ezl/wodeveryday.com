# Generated by Django 2.2.6 on 2020-06-27 20:53

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gym',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website', models.TextField(blank=True, null=True)),
                ('photo', models.TextField(blank=True, null=True)),
                ('ready_to_link', models.TextField(blank=True, null=True)),
                ('ordernum', models.TextField(blank=True, null=True)),
                ('lat', models.TextField(blank=True, null=True)),
                ('lon', models.TextField(blank=True, null=True)),
                ('city', models.TextField(blank=True, null=True)),
                ('name_search', models.TextField(blank=True, null=True)),
                ('photo_version', models.TextField(blank=True, null=True)),
                ('zip', models.TextField(blank=True, null=True)),
                ('country_short_code', models.TextField(blank=True, null=True)),
                ('bad_standing', models.TextField(blank=True, null=True)),
                ('effective_date', models.TextField(blank=True, null=True)),
                ('status', models.TextField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('active', models.TextField(blank=True, null=True)),
                ('state_code', models.TextField(blank=True, null=True)),
                ('show_on_map', models.TextField(blank=True, null=True)),
                ('kids', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('country', models.TextField(blank=True, null=True)),
                ('org_type', models.TextField(blank=True, null=True)),
                ('aid', models.TextField(blank=True, null=True)),
                ('full_state', models.TextField(blank=True, null=True)),
                ('continent', models.TextField(blank=True, null=True)),
                ('name_slug', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GymLeaderboard',
            fields=[
                ('leaderboard_api_id', models.IntegerField(blank=True, null=True)),
                ('gym', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='core.Gym')),
                ('data', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(), size=None)),
            ],
        ),
    ]
