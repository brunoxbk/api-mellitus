# Generated by Django 5.0.7 on 2024-10-03 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='diabete',
        ),
        migrations.AddField(
            model_name='user',
            name='diabetes',
            field=models.CharField(blank=True, choices=[('1', 'Tipo 1'), ('2', 'Tipo 2')], max_length=3, null=True, verbose_name='tipo diabetes'),
        ),
        migrations.AlterField(
            model_name='user',
            name='diagnostico',
            field=models.IntegerField(blank=True, null=True, verbose_name='tempo de diagnostico'),
        ),
    ]