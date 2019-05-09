# Generated by Django 2.2.1 on 2019-05-09 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointments_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(default='', max_length=50)),
                ('lastName', models.CharField(default='', max_length=50)),
                ('username', models.CharField(default='', max_length=30)),
                ('workplace', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='appointments_app.Hospital')),
            ],
        ),
    ]
