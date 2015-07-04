# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrashReport',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('stack_trace', models.TextField(default='')),
                ('logcat', models.TextField(default='')),
                ('shared_preferences', models.TextField(default='')),
                ('environment', models.TextField(default='')),
                ('total_mem_size', models.BigIntegerField(default=0, verbose_name='Total Memory Size')),
                ('initial_configuration', models.TextField(default='')),
                ('display', models.TextField(default='')),
                ('available_mem_size', models.BigIntegerField(default=0, verbose_name='Available Memory Size')),
                ('phone_model', models.CharField(max_length=50, default='')),
                ('user_comment', models.TextField(default='')),
                ('crash_configuration', models.TextField(default='')),
                ('device_features', models.TextField(default='')),
                ('settings_system', models.TextField(default='', verbose_name='System Settings')),
                ('file_path', models.CharField(max_length=100, default='')),
                ('installation_id', models.CharField(max_length=100, default='')),
                ('user_crash_date', models.CharField(max_length=50, default='', verbose_name='Crash Date')),
                ('app_version_name', models.CharField(max_length=50, default='', verbose_name='Version Name')),
                ('user_app_start_date', models.CharField(max_length=50, default='', verbose_name='Application Start Date')),
                ('settings_global', models.TextField(default='', verbose_name='Global Settings')),
                ('build', models.TextField(default='')),
                ('settings_secure', models.TextField(default='', verbose_name='Secure Settings')),
                ('dumpsys_meminfo', models.TextField(default='')),
                ('user_email', models.CharField(max_length=50, default='')),
                ('report_id', models.CharField(max_length=100, default='')),
                ('product', models.CharField(max_length=50, default='')),
                ('package_name', models.CharField(max_length=100, default='', verbose_name='Package Name')),
                ('brand', models.CharField(max_length=50, default='')),
                ('android_version', models.CharField(max_length=50, default='')),
                ('app_version_code', models.CharField(max_length=50, default='', verbose_name='Version Code')),
                ('is_silent', models.CharField(max_length=50, default='')),
                ('custom_data', models.TextField(default='')),
                ('description', models.TextField(default='')),
                ('solved', models.CharField(max_length=10, choices=[('solved', 'Solved'), ('unsolved', 'Unsolved')], default='unsolved', verbose_name='Status')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
